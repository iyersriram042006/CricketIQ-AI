from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.powerplay import Powerplay
from app.schemas.powerplay import PowerplayResponse

router = APIRouter()


@router.get("/powerplays", response_model=list[PowerplayResponse])
def get_powerplays(db: Session = Depends(get_db)):
    return db.query(Powerplay).all()


@router.get("/powerplays/{match_id}", response_model=list[PowerplayResponse])
def get_match_powerplays(match_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Powerplay)
        .filter(Powerplay.match_id == match_id)
        .all()
    )