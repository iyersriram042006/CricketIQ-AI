from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(tags=["Players"])


@router.get("/players/{player_id}")
def player_profile(player_id: str, db: Session = Depends(get_db)):

    query = text("""
        SELECT
            p.player_id,
            p.player_name,
            ps.matches,
            ps.runs,
            ps.balls_faced,
            ps.fours,
            ps.sixes,
            ps.strike_rate
        FROM players p
        LEFT JOIN player_stats ps
        ON p.player_name = ps.batter
        WHERE p.player_id = :player_id
    """)

    result = db.execute(query, {
        "player_id": player_id
    }).first()

    if result is None:
        return {"message": "Player not found"}

    return dict(result._mapping)