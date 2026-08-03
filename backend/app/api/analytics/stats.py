from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


from fastapi import Query

@router.get("/top-batters")
def top_batters(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = text("""
        SELECT
            batter,
            runs,
            balls_faced,
            fours,
            sixes,
            strike_rate
        FROM player_stats
        ORDER BY runs DESC
        LIMIT :limit
    """)

    result = db.execute(query, {"limit": limit})

    return [dict(row._mapping) for row in result]

@router.get("/top-bowlers")
def top_bowlers(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            w.bowler,
            COUNT(*) AS wickets,
            COUNT(DISTINCT d.match_id) AS matches
        FROM wickets w
        JOIN deliveries d
            ON w.match_id = d.match_id
           AND w.innings_number = d.innings_number
           AND w.over_number = d.over_number
           AND w.ball_number = d.ball_number
        WHERE w.kind_of_wicket NOT IN (
            'run out',
            'retired hurt',
            'retired out',
            'obstructing the field'
        )
        GROUP BY w.bowler
        ORDER BY wickets DESC
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            (SELECT COUNT(*) FROM matches) AS matches,

            (SELECT COUNT(*) FROM players) AS players,

            (
                SELECT COUNT(DISTINCT canonical_name)
                FROM team_aliases
            ) AS teams,

            (
                SELECT COUNT(
                    DISTINCT COALESCE(
                        va.canonical_name,
                        m.venue
                    )
                )
                FROM matches m
                LEFT JOIN venue_aliases va
                    ON m.venue = va.original_name
            ) AS venues,

            (SELECT COUNT(*) FROM deliveries) AS deliveries,

            (SELECT COUNT(*) FROM wickets) AS wickets
    """)

    result = db.execute(query).first()

    return dict(result._mapping)

@router.get("/top-teams")
def top_teams(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            ta.canonical_name AS team,
            COUNT(*) AS wins
        FROM matches m
        JOIN team_aliases ta
            ON m.match_winner = ta.original_name
        WHERE m.match_winner IS NOT NULL
        GROUP BY ta.canonical_name
        ORDER BY wins DESC
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]

@router.get("/orange-cap")
def orange_cap(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            batter,
            runs
        FROM player_stats
        ORDER BY runs DESC
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]


@router.get("/purple-cap")
def purple_cap(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            w.bowler,
            COUNT(*) AS wickets
        FROM wickets w
        WHERE w.kind_of_wicket NOT IN (
            'run out',
            'retired hurt',
            'retired out',
            'obstructing the field'
        )
        GROUP BY w.bowler
        ORDER BY wickets DESC
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]