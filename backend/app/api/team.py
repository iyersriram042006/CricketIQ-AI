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
            ) AS wins
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