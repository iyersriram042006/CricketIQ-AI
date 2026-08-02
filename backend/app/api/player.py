from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerResponse

router = APIRouter()


@router.get("/players", response_model=list[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


from fastapi import Query
from sqlalchemy import text

@router.get("/players/search")
def search_players(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            player_id,
            player_name
        FROM players
        WHERE player_name ILIKE :search
        ORDER BY player_name
        LIMIT 10
    """)

    result = db.execute(
        query,
        {"search": f"%{q}%"}
    ).mappings().all()

    return result


@router.get("/players/search/{name}", response_model=list[PlayerResponse])
def search_player(name: str, db: Session = Depends(get_db)):
    players = (
        db.query(Player)
        .filter(func.lower(Player.player_name).contains(name.lower()))
        .all()
    )

    return players


@router.get("/players/{player_id}", response_model=PlayerResponse)
def get_player(player_id: str, db: Session = Depends(get_db)):
    player = (
        db.query(Player)
        .filter(Player.player_id == player_id)
        .first()
    )

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return player