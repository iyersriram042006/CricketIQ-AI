import psycopg2

conn = psycopg2.connect(
    dbname="cricketiq",
    user="sriram",
)

cur = conn.cursor()

cur.execute("""
TRUNCATE TABLE player_match_stats;

WITH dismissal AS (
    SELECT
        match_id,
        batter_out,
        TRUE AS out,
        kind_of_wicket
    FROM wickets
)

INSERT INTO player_match_stats (
    match_id,
    player_id,
    player_name,
    season,
    venue,
    opponent,
    runs,
    balls_faced,
    fours,
    sixes,
    out,
    dismissal_type,
    strike_rate,

    dot_balls,
    singles,
    doubles,
    triples
)

SELECT

    d.match_id,

    ms.player_id,

    d.batter,

    m.season,

    m.venue,

    CASE
        WHEN d.batting_team = m.team_1
            THEN m.team_2
        ELSE m.team_1
    END,

    SUM(d.batter_runs),

    COUNT(*) FILTER (
        WHERE d.wides = 0
    ),

    COUNT(*) FILTER (
        WHERE d.batter_runs = 4
    ),

    COUNT(*) FILTER (
        WHERE d.batter_runs = 6
    ),

    COALESCE(BOOL_OR(dis.out), FALSE),

    MAX(dis.kind_of_wicket),

    ROUND(
        (
            100.0 * SUM(d.batter_runs)::numeric
        ) /
        NULLIF(
            COUNT(*) FILTER (WHERE d.wides = 0),
            0
        )::numeric,
        2
    ),

    COUNT(*) FILTER (
        WHERE d.wides = 0
        AND d.batter_runs = 0
    ),

    COUNT(*) FILTER (
        WHERE d.batter_runs = 1
    ),

    COUNT(*) FILTER (
        WHERE d.batter_runs = 2
    ),

    COUNT(*) FILTER (
        WHERE d.batter_runs = 3
    )

FROM deliveries d

JOIN matches m
ON d.match_id = m.match_id

JOIN match_squads ms
ON d.match_id = ms.match_id
AND d.batter = ms.player_name

LEFT JOIN dismissal dis
ON d.match_id = dis.match_id
AND d.batter = dis.batter_out

GROUP BY

    d.match_id,
    ms.player_id,
    d.batter,
    m.season,
    m.venue,
    CASE
        WHEN d.batting_team = m.team_1
            THEN m.team_2
        ELSE m.team_1
    END;

""")

conn.commit()

print("player_match_stats generated successfully.")

cur.close()
conn.close()