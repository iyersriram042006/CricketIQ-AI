from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.player_of_match import PlayerOfMatch
from app.schemas.player_of_match import PlayerOfMatchResponse

router = APIRouter()


@router.get("/player-of-match", response_model=list[PlayerOfMatchResponse])
def get_player_of_match(db: Session = Depends(get_db)):
    return db.query(PlayerOfMatch).all()


@router.get("/player-of-match/{match_id}", response_model=list[PlayerOfMatchResponse])
def get_player_of_match_by_match(match_id: int, db: Session = Depends(get_db)):
    return (
        db.query(PlayerOfMatch)
        .filter(PlayerOfMatch.match_id == match_id)
        .all()
    )