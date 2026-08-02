from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(tags=["Player Profile"])


@router.get("/players/{player_id}/profile")
def get_player(player_id: str, db: Session = Depends(get_db)):
    query = text("""
    SELECT
        p.player_id,
        p.player_name,
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

    result = db.execute(query, {"player_id": player_id}).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return dict(result._mapping)

@router.get("/player-comparison")
def compare_players(
    player1: str,
    player2: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            p.player_id,
            p.player_name,
            ps.runs,
            ps.balls_faced,
            ps.fours,
            ps.sixes,
            ps.strike_rate
        FROM players p
        LEFT JOIN player_stats ps
            ON p.player_name = ps.batter
        WHERE p.player_id = :player1
        OR p.player_id = :player2
    """)

    result = db.execute(
        query,
        {
            "player1": player1,
            "player2": player2,
        },
    )

    return [dict(row._mapping) for row in result]

@router.get("/player/{player_id}")
def get_player_by_id(player_id: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            player_id,
            player_name
        FROM players
        WHERE player_id = :player_id
    """)

    result = db.execute(query, {"player_id": player_id}).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return dict(result._mapping)