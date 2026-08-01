from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.match import Match
from app.schemas.match import MatchResponse

router = APIRouter()


@router.get("/matches", response_model=list[MatchResponse])
def get_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()


@router.get("/matches/{match_id}", response_model=MatchResponse)
def get_match(match_id: int, db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.match_id == match_id).first()