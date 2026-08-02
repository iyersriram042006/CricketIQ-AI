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

    innings = db.execute(
        text("""
            SELECT
                d.batting_team,
                d.innings_number,
                SUM(d.total_runs) AS runs,
                COUNT(*) FILTER (WHERE d.wides = 0) / 6.0 AS overs,
                COUNT(w.kind_of_wicket) AS wickets
            FROM deliveries d
            LEFT JOIN wickets w
                ON d.match_id = w.match_id
            AND d.innings_number = w.innings_number
            AND d.over_number = w.over_number
            AND d.ball_number = w.ball_number
            WHERE d.match_id = :id
            GROUP BY
                d.batting_team,
                d.innings_number
            ORDER BY
                d.innings_number
        """),
        {"id": match_id},
    ).mappings().all()

    batting = db.execute(
        text("""
            SELECT
                innings_number,
                batter,
                SUM(batter_runs) AS runs,
                COUNT(*) FILTER (WHERE wides = 0) AS balls
            FROM deliveries
            WHERE match_id = :id
            GROUP BY innings_number, batter
            ORDER BY innings_number, runs DESC
        """),
        {"id": match_id},
    ).mappings().all()

    wickets = db.execute(
        text("""
            SELECT
                innings_number,
                batter_out,
                bowler,
                kind_of_wicket
            FROM wickets
            WHERE match_id = :id
            ORDER BY innings_number
        """),
        {"id": match_id},
    ).mappings().all()

    return {
        "match": match,
        "innings": innings,
        "batting": batting,
        "wickets": wickets,
    }