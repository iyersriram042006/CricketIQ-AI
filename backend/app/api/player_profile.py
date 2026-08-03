from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

router = APIRouter(tags=["Player Profile"])


@router.get("/players/{player_id}/profile")
def get_player(player_id: str, db: Session = Depends(get_db)):
    query = text("""
    SELECT
        p.player_id,
        p.player_name,
        ps.runs,
        ps.balls_faced,
        ps.fours,
        ps.sixes,
        ps.strike_rate
    FROM players p
    LEFT JOIN player_stats ps
        ON p.player_name = ps.batter
    WHERE p.player_id = :player_id
""")

    result = db.execute(query, {"player_id": player_id}).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return dict(result._mapping)

@router.get("/player-comparison")
def compare_players(
    player1: str,
    player2: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            p.player_id,
            p.player_name,
            ps.runs,
            ps.balls_faced,
            ps.fours,
            ps.sixes,
            ps.strike_rate
        FROM players p
        LEFT JOIN player_stats ps
            ON p.player_name = ps.batter
        WHERE p.player_id = :player1
        OR p.player_id = :player2
    """)

    result = db.execute(
        query,
        {
            "player1": player1,
            "player2": player2,
        },
    )

    return [dict(row._mapping) for row in result]

@router.get("/player/{player_id}")
def get_player_by_id(player_id: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT
            player_id,
            player_name
        FROM players
        WHERE player_id = :player_id
    """)

    result = db.execute(query, {"player_id": player_id}).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Player not found")

    return dict(result._mapping)

@router.get("/players/{player_id}/career")
def get_player_career(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            player_id,
            player_name,

            matches,
            innings,
            not_outs,

            runs,
            balls_faced,
            highest_score,

            average,
            strike_rate,

            hundreds,
            fifties,
            thirties,
            ducks,

            fours,
            sixes,

            dot_balls,
            singles,
            doubles,
            triples,

            boundary_percentage,
            balls_per_boundary

        FROM player_career_stats
        WHERE player_id = :player_id
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        }
    ).mappings().first()

    return result

@router.get("/players/{player_id}/recent-innings")
def get_recent_innings(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            season,
            opponent,
            runs,
            balls_faced,
            strike_rate,
            out
        FROM player_match_stats
        WHERE player_id = :player_id
        ORDER BY match_id DESC
        LIMIT 10
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        },
    ).mappings().all()

    return result

@router.get("/players/{player_id}/career-progression")
def get_career_progression(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            match_id,
            season,
            runs
        FROM player_match_stats
        WHERE player_id = :player_id
        ORDER BY match_id
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        }
    ).mappings().all()

    return result

@router.get("/players/{player_id}/opponents")
def get_opponent_stats(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT
            COALESCE(
                ta.canonical_name,
                pms.opponent
            ) AS opponent,
            COUNT(*) AS matches,
            SUM(pms.runs) AS runs,

            ROUND(
                AVG(pms.runs),
                2
            ) AS average,

            ROUND(
                (
                    100.0 * SUM(pms.runs)::numeric
                ) /
                NULLIF(
                    SUM(pms.balls_faced),
                    0
                ),
                2
            ) AS strike_rate

        FROM player_match_stats pms

        LEFT JOIN team_aliases ta
            ON pms.opponent = ta.original_name

        WHERE pms.player_id = :player_id

        GROUP BY
        COALESCE(
            ta.canonical_name,
            pms.opponent
        )

        ORDER BY runs DESC;
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        }
    ).mappings().all()

    return result

@router.get("/players/{player_id}/season-stats")
def get_season_stats(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT

            season,

            COUNT(*) AS matches,

            SUM(runs) AS runs,

            MAX(runs) AS highest_score,

            ROUND(
                AVG(runs),
                2
            ) AS average,

            ROUND(
                (
                    100.0 * SUM(runs)::numeric
                )
                /
                NULLIF(
                    SUM(balls_faced),
                    0
                ),
                2
            ) AS strike_rate,

            COUNT(*) FILTER (
                WHERE runs >= 100
            ) AS hundreds,

            COUNT(*) FILTER (
                WHERE runs BETWEEN 50 AND 99
            ) AS fifties

        FROM player_match_stats

        WHERE player_id = :player_id

        GROUP BY season

        ORDER BY season DESC;
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        }
    ).mappings().all()

    return result

@router.get("/players/{player_id}/venues")
def get_venue_stats(
    player_id: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT

            COALESCE(
                va.canonical_name,
                player_match_stats.venue
            ) AS venue,

            COUNT(*) AS matches,

            SUM(runs) AS runs,

            MAX(runs) AS highest_score,

            ROUND(
                AVG(runs),
                2
            ) AS average,

            ROUND(
                (
                    100.0 * SUM(runs)::numeric
                )
                /
                NULLIF(
                    SUM(balls_faced),
                    0
                ),
                2
            ) AS strike_rate

        FROM player_match_stats
            LEFT JOIN venue_aliases va
                ON player_match_stats.venue = va.original_name

        WHERE player_id = :player_id

        GROUP BY
        COALESCE(
            va.canonical_name,
            player_match_stats.venue
        )

        ORDER BY runs DESC;
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
        }
    ).mappings().all()

    return result

@router.get("/players/{player_id}/vs-bowler")
def get_vs_bowler(
    player_id: str,
    bowler: str,
    db: Session = Depends(get_db),
):
    query = text("""
        SELECT

            :bowler AS bowler,

            COUNT(*) FILTER (
                WHERE d.wides = 0
            ) AS balls,

            SUM(d.batter_runs) AS runs,

            COUNT(*) FILTER (
                WHERE d.batter_runs = 4
            ) AS fours,

            COUNT(*) FILTER (
                WHERE d.batter_runs = 6
            ) AS sixes,

            (
                SELECT COUNT(*)
                FROM wickets w
                JOIN match_squads ms
                    ON w.match_id = ms.match_id
                    AND w.batter_out = ms.player_name
                WHERE
                    ms.player_id = :player_id
                    AND w.bowler = :bowler
            ) AS dismissals,
            ROUND(
                SUM(d.batter_runs)::numeric /
                NULLIF(
                    (
                        SELECT COUNT(*)
                        FROM wickets w
                        JOIN match_squads ms
                            ON w.match_id = ms.match_id
                            AND w.batter_out = ms.player_name
                        WHERE
                            ms.player_id = :player_id
                            AND w.bowler = :bowler
                    ),
                    0
                ),
                2
            ) AS average,

            ROUND(
                (
                    100.0 * SUM(d.batter_runs)::numeric
                )
                /
                NULLIF(
                    COUNT(*) FILTER (WHERE d.wides = 0),
                    0
                ),
                2
            ) AS strike_rate

        FROM deliveries d

        JOIN match_squads ms
            ON d.match_id = ms.match_id
            AND d.batter = ms.player_name

        WHERE
            ms.player_id = :player_id
            AND d.bowler = :bowler;
    """)

    result = db.execute(
        query,
        {
            "player_id": player_id,
            "bowler": bowler,
        },
    ).mappings().first()

    return result