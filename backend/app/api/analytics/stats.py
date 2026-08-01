from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/top-batters")
def top_batters(db: Session = Depends(get_db)):
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
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]

@router.get("/top-bowlers")
def top_bowlers(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            bowler,
            COUNT(*) AS wickets
        FROM wickets
        GROUP BY bowler
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
            (SELECT COUNT(*) FROM teams) AS teams,
            (SELECT COUNT(*) FROM venues) AS venues,
            (SELECT COUNT(*) FROM deliveries) AS deliveries,
            (SELECT COUNT(*) FROM wickets) AS wickets
    """)

    result = db.execute(query).first()

    return dict(result._mapping)