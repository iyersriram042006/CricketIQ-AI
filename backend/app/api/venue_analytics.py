from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(prefix="/venue-analytics", tags=["Venue Analytics"])


@router.get("/top-venues")
def top_venues(db: Session = Depends(get_db)):
    query = text("""
        SELECT
            venue,
            COUNT(*) AS matches
        FROM matches
        GROUP BY venue
        ORDER BY matches DESC
        LIMIT 10
    """)

    result = db.execute(query)

    return [dict(row._mapping) for row in result]