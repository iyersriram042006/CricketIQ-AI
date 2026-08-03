import psycopg2

conn = psycopg2.connect(
    dbname="cricketiq",
    user="sriram",
)

cur = conn.cursor()

cur.execute("""
TRUNCATE TABLE player_career_stats;
""")

cur.execute("""
INSERT INTO player_career_stats (

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

)

SELECT

    player_id,

    MAX(player_name) AS player_name,

    COUNT(*) AS matches,

    COUNT(*) AS innings,

    COUNT(*) FILTER (
        WHERE out = FALSE
    ) AS not_outs,

    SUM(runs),

    SUM(balls_faced),

    MAX(runs),

    COALESCE(
        ROUND(
            SUM(runs)::numeric /
            NULLIF(
                COUNT(*) FILTER (WHERE out = TRUE),
                0
            ),
            2
        ),
        0
    ),

    ROUND(
        (
            100.0 * SUM(runs)::numeric
        ) /
        NULLIF(
            SUM(balls_faced),
            0
        ),
        2
    ),

    COUNT(*) FILTER (
        WHERE runs >= 100
    ),

    COUNT(*) FILTER (
        WHERE runs BETWEEN 50 AND 99
    ),

    COUNT(*) FILTER (
        WHERE runs BETWEEN 30 AND 49
    ),

    COUNT(*) FILTER (
        WHERE runs = 0
    ),

    SUM(fours),

    SUM(sixes),

    SUM(dot_balls),

    SUM(singles),

    SUM(doubles),

    SUM(triples),

    ROUND(
        (
            (SUM(fours) + SUM(sixes)) * 100.0
        ) /
        NULLIF(
            SUM(balls_faced),
            0
        ),
        2
    ),

    ROUND(
        SUM(balls_faced)::numeric /
        NULLIF(
            SUM(fours) + SUM(sixes),
            0
        ),
        2
    )

FROM player_match_stats

GROUP BY
    player_id;
""")

conn.commit()

print("player_career_stats generated successfully.")

cur.close()
conn.close()