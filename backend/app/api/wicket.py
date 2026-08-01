from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.wicket import Wicket
from app.schemas.wicket import WicketResponse

router = APIRouter()


@router.get("/wickets", response_model=list[WicketResponse])
def get_wickets(db: Session = Depends(get_db)):
    return db.query(Wicket).all()


@router.get("/wickets/{wicket_id}", response_model=WicketResponse)
def get_wicket(wicket_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Wicket)
        .filter(Wicket.wicket_id == wicket_id)
        .first()
    )