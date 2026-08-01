from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.extras_breakdown import ExtrasBreakdown
from app.schemas.extras_breakdown import ExtrasBreakdownResponse

router = APIRouter()


@router.get("/extras-breakdown", response_model=list[ExtrasBreakdownResponse])
def get_extras(db: Session = Depends(get_db)):
    return db.query(ExtrasBreakdown).all()


@router.get("/extras-breakdown/{match_id}", response_model=list[ExtrasBreakdownResponse])
def get_match_extras(match_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ExtrasBreakdown)
        .filter(ExtrasBreakdown.match_id == match_id)
        .all()
    )