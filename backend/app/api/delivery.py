from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.delivery import Delivery
from app.schemas.delivery import DeliveryResponse

router = APIRouter()


@router.get("/deliveries", response_model=list[DeliveryResponse])
def get_deliveries(db: Session = Depends(get_db)):
    return db.query(Delivery).all()


@router.get("/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Delivery)
        .filter(Delivery.delivery_id == delivery_id)
        .first()
    )