from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.match_squad import MatchSquad
from app.schemas.match_squad import MatchSquadResponse

router = APIRouter()


@router.get("/match-squads", response_model=list[MatchSquadResponse])
def get_match_squads(db: Session = Depends(get_db)):
    return db.query(MatchSquad).all()


@router.get("/match-squads/{match_id}", response_model=list[MatchSquadResponse])
def get_match_squad(match_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MatchSquad)
        .filter(MatchSquad.match_id == match_id)
        .all()
    )