from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.models.team import Team
from app.schemas.team import TeamResponse

router = APIRouter()


@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            MIN(team_id) AS team_id,
            canonical_name AS team_name
        FROM team_aliases
        JOIN teams
            ON team_aliases.original_name = teams.team_name
        GROUP BY canonical_name
        ORDER BY canonical_name
    """)

    result = db.execute(query).mappings().all()

    return result

from fastapi import Query


@router.get("/teams/search")
def search_teams(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT DISTINCT
            canonical_name AS team_name
        FROM team_aliases
        WHERE canonical_name ILIKE :search
        ORDER BY canonical_name
        LIMIT 10
    """)

    result = db.execute(
        query,
        {
            "search": f"%{q}%"
        },
    ).mappings().all()

    return result

# ===========================
# TEAM COMPARISON
# IMPORTANT: Keep this BEFORE /teams/{team_name}
# ===========================

@router.get("/teams/compare")
def compare_teams(
    team1: str,
    team2: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            COUNT(*) AS matches,

            SUM(
                CASE
                    WHEN ta3.canonical_name = :team1 THEN 1
                    ELSE 0
                END
            ) AS team1_wins,

            SUM(
                CASE
                    WHEN ta3.canonical_name = :team2 THEN 1
                    ELSE 0
                END
            ) AS team2_wins

        FROM matches m

        JOIN team_aliases ta1
            ON m.team_1 = ta1.original_name

        JOIN team_aliases ta2
            ON m.team_2 = ta2.original_name

        LEFT JOIN team_aliases ta3
            ON m.match_winner = ta3.original_name

        WHERE
        (
            ta1.canonical_name = :team1
            AND ta2.canonical_name = :team2
        )
        OR
        (
            ta1.canonical_name = :team2
            AND ta2.canonical_name = :team1
        )
    """)

    result = db.execute(
        query,
        {
            "team1": team1,
            "team2": team2,
        },
    ).mappings().first()

    return result


# ===========================
# TEAM PROFILE
# ===========================

@router.get("/teams/{team_name}")
def get_team(team_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
        ta.canonical_name AS team_name,

        COUNT(*) AS matches,

        SUM(
            CASE
                WHEN ta2.canonical_name = ta.canonical_name THEN 1
                ELSE 0
            END
        ) AS wins,

        ROUND(
            100.0 *
            SUM(
                CASE
                    WHEN ta2.canonical_name = ta.canonical_name THEN 1
                    ELSE 0
                END
            ) /
            COUNT(*),
            2
        ) AS win_percentage,
        (
            SELECT MAX(team_runs)
            FROM (
                SELECT
                    d.match_id,
                    d.innings_number,
                    SUM(d.total_runs) AS team_runs
                FROM deliveries d

                JOIN team_aliases ta4
                    ON d.batting_team = ta4.original_name

                WHERE ta4.canonical_name = :team_name
                AND d.innings_number <= 2

                GROUP BY
                    d.match_id,
                    d.innings_number
            ) scores
        ) AS highest_score,
        (
            SELECT MIN(team_runs)
            FROM (
                SELECT
                    d.match_id,
                    d.innings_number,
                    SUM(d.total_runs) AS team_runs
                FROM deliveries d

                JOIN team_aliases ta5
                    ON d.batting_team = ta5.original_name

                WHERE ta5.canonical_name = :team_name
                AND d.innings_number <= 2

                GROUP BY
                    d.match_id,
                    d.innings_number
            ) scores
        ) AS lowest_score
        FROM (
            SELECT team_1 AS team_name, match_winner
            FROM matches

            UNION ALL

            SELECT team_2 AS team_name, match_winner
            FROM matches
        ) t

        JOIN team_aliases ta
            ON t.team_name = ta.original_name

        LEFT JOIN team_aliases ta2
            ON t.match_winner = ta2.original_name

        WHERE ta.canonical_name = :team_name

        GROUP BY ta.canonical_name
    """)

    result = db.execute(
        query,
        {"team_name": team_name},
    ).mappings().first()

    if result is None:
        return {"message": "Team not found"}

    return result


# ===========================
# TEAM TOP BATTERS
# ===========================

@router.get("/teams/{team_name}/stats")
def get_team_stats(team_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            d.batter,
            SUM(d.batter_runs) AS runs
        FROM deliveries d
        JOIN team_aliases ta
            ON d.batting_team = ta.original_name
        WHERE ta.canonical_name = :team_name
        GROUP BY d.batter
        ORDER BY runs DESC
        LIMIT 5
    """)

    result = db.execute(
        query,
        {"team_name": team_name},
    ).mappings().all()

    return result


# ===========================
# TEAM TOP BOWLERS
# ===========================

@router.get("/teams/{team_name}/bowlers")
def get_team_bowlers(team_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            w.bowler,
            COUNT(*) AS wickets
        FROM wickets w

        JOIN matches m
            ON w.match_id = m.match_id

        JOIN team_aliases ta1
            ON m.team_1 = ta1.original_name

        JOIN team_aliases ta2
            ON m.team_2 = ta2.original_name

        JOIN team_aliases ta3
            ON w.batting_team = ta3.original_name

        WHERE
        (
            ta1.canonical_name = :team_name
            OR
            ta2.canonical_name = :team_name
        )

        AND ta3.canonical_name <> :team_name

        AND w.kind_of_wicket NOT IN (
            'run out',
            'retired hurt',
            'retired out',
            'obstructing the field'
        )

        GROUP BY w.bowler
        ORDER BY wickets DESC
        LIMIT 5
    """)

    result = db.execute(
        query,
        {"team_name": team_name},
    ).mappings().all()

    return result

# ===========================
# TEAM RECENT FORM
# ===========================

@router.get("/teams/{team_name}/recent-form")
def get_team_recent_form(
    team_name: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            m.season,

            CASE
                WHEN ta1.canonical_name = :team_name
                THEN ta2.canonical_name
                ELSE ta1.canonical_name
            END AS opponent,

            CASE
                WHEN taw.canonical_name = :team_name
                THEN 'W'
                ELSE 'L'
            END AS result

        FROM matches m

        JOIN team_aliases ta1
            ON m.team_1 = ta1.original_name

        JOIN team_aliases ta2
            ON m.team_2 = ta2.original_name

        LEFT JOIN team_aliases taw
            ON m.match_winner = taw.original_name

        WHERE
            ta1.canonical_name = :team_name
            OR
            ta2.canonical_name = :team_name

        ORDER BY
            m.match_id DESC

        LIMIT 5
    """)

    result = db.execute(
        query,
        {
            "team_name": team_name,
        },
    ).mappings().all()

    return result

# ===========================
# TEAM RECORDS
# ===========================

@router.get("/teams/{team_name}/records")
def get_team_records(
    team_name: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            MAX(chase_score) AS highest_successful_chase

        FROM (
            SELECT
                m.match_id,
                SUM(d.total_runs) AS chase_score

            FROM matches m

            JOIN deliveries d
                ON m.match_id = d.match_id

            JOIN team_aliases ta
                ON d.batting_team = ta.original_name

            JOIN team_aliases tw
                ON m.match_winner = tw.original_name

            WHERE
                ta.canonical_name = :team_name
                AND tw.canonical_name = :team_name
                AND d.innings_number = 2

            GROUP BY
                m.match_id
        ) chase_scores
    """)

    result = db.execute(
        query,
        {
            "team_name": team_name,
        },
    ).mappings().first()

    return result