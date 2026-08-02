from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.models.team import Team
from app.schemas.team import TeamResponse

router = APIRouter()


@router.get("/teams", response_model=list[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()


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
                    WHEN match_winner = :team1 THEN 1
                    ELSE 0
                END
            ) AS team1_wins,

            SUM(
                CASE
                    WHEN match_winner = :team2 THEN 1
                    ELSE 0
                END
            ) AS team2_wins

        FROM matches

        WHERE
        (
            team_1 = :team1
            AND team_2 = :team2
        )
        OR
        (
            team_1 = :team2
            AND team_2 = :team1
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
            team_name,
            COUNT(*) AS matches,
            SUM(
                CASE
                    WHEN match_winner = team_name THEN 1
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
        WHERE team_name = :team_name
        GROUP BY team_name
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
            batter,
            SUM(batter_runs) AS runs
        FROM deliveries
        WHERE batting_team = :team_name
        GROUP BY batter
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
        WHERE
            (
                m.team_1 = :team_name
                OR
                m.team_2 = :team_name
            )
            AND
            w.batting_team <> :team_name
            AND
            w.kind_of_wicket NOT IN (
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