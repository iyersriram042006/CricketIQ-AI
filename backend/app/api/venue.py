from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.venue import Venue
from app.schemas.venue import VenueResponse

router = APIRouter()


@router.get("/venues", response_model=list[VenueResponse])
def get_venues(db: Session = Depends(get_db)):
    return db.query(Venue).all()


@router.get("/venues/{venue_id}", response_model=VenueResponse)
def get_venue(venue_id: int, db: Session = Depends(get_db)):
    return db.query(Venue).filter(Venue.venue_id == venue_id).first()