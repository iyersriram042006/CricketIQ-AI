from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(tags=["Scorecard"])


@router.get("/matches/{match_id}/scorecard")
def scorecard(match_id: int, db: Session = Depends(get_db)):

    match = db.execute(
        text("""
            SELECT *
            FROM matches
            WHERE match_id = :id
        """),
        {"id": match_id},
    ).mappings().first()

    batting = db.execute(
        text("""
            SELECT
                batter,
                SUM(batter_runs) AS runs,
                COUNT(*) FILTER (WHERE wides = 0) AS balls
            FROM deliveries
            WHERE match_id = :id
            GROUP BY batter
            ORDER BY runs DESC
        """),
        {"id": match_id},
    ).mappings().all()

    wickets = db.execute(
        text("""
            SELECT
                batter_out,
                bowler,
                kind_of_wicket
            FROM wickets
            WHERE match_id = :id
        """),
        {"id": match_id},
    ).mappings().all()

    return {
        "match": match,
        "batting": batting,
        "wickets": wickets,
    }