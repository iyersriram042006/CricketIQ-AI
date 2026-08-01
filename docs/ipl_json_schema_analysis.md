# IPL Match JSON (Cricsheet Format v1.2.0) — Structural Analysis & Database Design

This file (`335982.json` — IPL 2008, Match #1, Kolkata Knight Riders vs Royal Challengers Bangalore) follows the **Cricsheet standard JSON schema**, used broadly across ball-by-ball cricket datasets. Every IPL file you ingest will follow this same shape, so this analysis generalizes to your whole platform, not just this one match.

---

## 1. Complete JSON Hierarchy

```
root
├── meta                              (schema metadata — not match data)
│   ├── data_version
│   ├── created
│   └── revision
│
├── info                              (match-level descriptive data — one record per match)
│   ├── balls_per_over
│   ├── city
│   ├── dates []
│   ├── event { name, match_number }
│   ├── gender
│   ├── match_type
│   ├── officials { match_referees[], reserve_umpires[], tv_umpires[], umpires[] }
│   ├── outcome { winner, by { runs | wickets } }
│   ├── overs
│   ├── player_of_match []
│   ├── players { team_name: [player_names] }
│   ├── registry { people { player_name: unique_id } }
│   ├── season
│   ├── team_type
│   ├── teams []
│   ├── toss { decision, winner }
│   └── venue
│
└── innings []                        (one object per innings, in order batted)
    ├── team
    ├── powerplays [] { from, to, type }
    ├── target { overs, runs }        (only present on chasing innings)
    └── overs []
        └── over (number)
        └── deliveries []
            ├── actual_delivery       (over.ball notation, accounts for extra balls)
            ├── batter
            ├── non_striker
            ├── bowler
            ├── runs { batter, extras, total }
            ├── extras { wides | byes | legbyes | noballs | penalty }
            └── wickets [] { kind, player_out, fielders [{ name }] }
```

This is a **nested document**, not a flat table — the whole point of your job is to flatten it into relational structures without losing information or introducing duplication.

---

## 2. Explanation of Every Top-Level Section

### `meta`
Describes the *file itself*, not the match. It tells you which version of the Cricsheet schema was used to generate the file, when the file was created/exported, and its revision number (Cricsheet occasionally reissues corrected files for the same match). This is **pipeline/ingestion metadata** — useful for tracking data lineage and knowing whether you need to re-import a match if a newer revision is released, but it has no cricketing meaning.

### `info`
This is the single most important section for match-level facts. It is a flat bag of attributes that describes the match as a whole: where and when it was played, which tournament/season, who played, who officiated, the toss outcome, and the final result. Nearly every field here maps to exactly one row in a `matches` table, with some fields (players, officials, teams) needing to be broken into separate linking tables because they are one-to-many.

### `innings`
This is the ball-by-ball heart of the dataset. It's an array because a T20 match has (typically) two innings, but this section is what allows you to reconstruct the entire game, over by over, ball by ball, including who bowled to whom, how many runs were scored, and whether a wicket fell. It's inherently hierarchical (innings → overs → deliveries → extras/wickets), which is exactly why it needs to be normalized into multiple related tables rather than kept as JSON blobs in your production database.

---

## 3. Field-by-Field Explanation

### `meta` block

| Field | Meaning |
|---|---|
| `data_version` | Version of the Cricsheet schema spec this file conforms to (e.g. "1.2.0"). Needed to handle schema drift across older/newer files. |
| `created` | Date this JSON file was generated/published. |
| `revision` | Incrementing integer; a higher revision number for the same match means a corrected re-release (e.g. a scoring error fixed after the match). |

### `info` block

| Field | Meaning |
|---|---|
| `balls_per_over` | Almost always 6; exists because some historical formats (old ODIs/Tests) used 8-ball overs. Needed for correctly parsing `actual_delivery` notation. |
| `city` | City the match was played in. |
| `dates` | Array of ISO dates the match was played on. An array because multi-day formats (Test matches) span several dates; for T20 it's a single-element array. |
| `event.name` | Name of the tournament/competition (e.g. "Indian Premier League"). |
| `event.match_number` | The sequential match number within that tournament season (e.g. Match 1 of IPL 2008). |
| `gender` | "male" or "female" — distinguishes IPL from WPL etc. |
| `match_type` | Format of the match: T20, ODI, Test, etc. |
| `officials.match_referees` | Names of match referee(s). |
| `officials.reserve_umpires` | Reserve/standby umpire(s). |
| `officials.tv_umpires` | Third umpire (TV official) who handles reviews. |
| `officials.umpires` | On-field umpires (typically 2). |
| `outcome.winner` | Team name that won the match. |
| `outcome.by.runs` / `outcome.by.wickets` | Margin of victory — expressed as runs (if the team batting first won) or wickets remaining (if the team chasing won). Only one of these two keys is present per match. |
| `outcome` may also contain `result` (e.g. "tie", "no result") or `method` (e.g. "D/L") in other files — not present in this particular match since it had a clear winner. |
| `overs` | Total overs allotted per innings for this match format (20 for T20). |
| `player_of_match` | Array (usually one name) of the player awarded Man of the Match. |
| `players` | Dictionary keyed by team name, each value an array of the players who featured in the match for that team (the matchday squad/XI, not the full roster). |
| `registry.people` | A dictionary mapping every player/official name string appearing anywhere in this file to a **stable unique identifier** (a hash). This is critical: player names alone are not reliable keys (typos, nicknames, renamed players, two players sharing initials) — the registry ID is the true foreign key you should use. |
| `season` | Season label (e.g. "2007/08"); note early IPL seasons used cross-year labels while later seasons use a single year. |
| `team_type` | "club" (franchise team) vs "international" — relevant since Cricsheet also hosts international matches in the same schema. |
| `teams` | The two team names participating (order here does not necessarily indicate batting order — use `toss` and `innings[].team` for that). |
| `toss.decision` | What the toss winner chose to do: "bat" or "field". |
| `toss.winner` | Team that won the toss. |
| `venue` | Stadium name. |

### `innings[]` block

| Field | Meaning |
|---|---|
| `team` | Which team is batting in this innings. |
| `powerplays[].from` / `.to` | Over.ball range (e.g. 0.1 to 5.6) during which fielding restrictions applied. |
| `powerplays[].type` | Type of powerplay — "mandatory" (only type in older matches; newer ones may also have "batting"/"bowling" discretionary powerplays). |
| `target.overs` / `target.runs` | Only present in the second (chasing) innings — the number of runs needed and overs available to win. This is *derived* from the first innings' total, not independent data. |
| `overs[].over` | Zero-indexed over number. |
| `overs[].deliveries[]` | Array of every ball bowled in that over, **including extra balls** (wides/no-balls), which is why an over can have more than 6 delivery entries. |

### `deliveries[]` (the finest-grained record in the dataset)

| Field | Meaning |
|---|---|
| `actual_delivery` | The over.ball label as it actually happened (e.g. "0.3" appearing twice means a wide was bowled and re-bowled as the "real" 3rd ball) — this is the true chronological sequence key, more reliable than array index for reconstructing exact over composition. |
| `batter` | Player facing the ball. |
| `non_striker` | Player at the other end. |
| `bowler` | Player bowling the delivery. |
| `runs.batter` | Runs credited to the batter's individual score. |
| `runs.extras` | Runs that are extras (not credited to any batter). |
| `runs.total` | Sum of `runs.batter` + `runs.extras` — the runs added to the team score for this ball. **This is a derived/redundant field** (see Section 6). |
| `extras.wides` / `.byes` / `.legbyes` / `.noballs` / `.penalty` | Breakdown of *what kind* of extra occurred and how many runs it contributed. Only present when an extra occurred; a "clean" ball has no `extras` key at all. |
| `wickets[]` | Array (almost always length 1, but schema supports multiple simultaneous events, e.g. run-out off a no-ball) describing any dismissal on this ball. |
| `wickets[].kind` | Method of dismissal: caught, bowled, run out, lbw, stumped, etc. |
| `wickets[].player_out` | Name of the batter dismissed (not always the facing `batter` — e.g. non-striker run out). |
| `wickets[].fielders[].name` | Fielder(s) involved in the dismissal (catcher, thrower, etc.). Some dismissals (bowled, lbw) have no fielders. |

---

## 4. Relationships Between Sections

- **`meta` → whole file**: purely administrative, has no foreign-key relationship to cricketing data.
- **`info` → `innings`**: `info.teams` and `info.players` define the universe of teams/players that `innings[].team` and `deliveries[].batter/bowler/non_striker` must reference. Every player name appearing in `innings` **must** also appear in `info.players` and **must** be resolvable via `info.registry.people`.
- **`info.registry.people` → everywhere**: this is the *master identity resolution table*. Every name string in `players`, `officials`, `player_of_match`, `toss.winner`/`outcome.winner` (team names, not in registry) and every `batter`/`bowler`/`non_striker`/`player_out`/`fielders.name` in `innings` should be joined through this registry to get a stable player ID.
- **`info.toss` → `innings` order**: the toss decision determines which team's name appears in `innings[0].team` vs `innings[1].team`, and `innings[1].target` is mathematically derived from `innings[0]`'s final total.
- **`innings[].overs[].deliveries[].wickets[].player_out`**: cross-references back into `info.players[team]` for that innings' batting side.
- **`outcome.winner`**: cross-references `info.teams`, and is logically derivable (with effort) from replaying the full `innings` ball-by-ball data — i.e., it's a stored summary of something you could recompute, which matters for your redundancy analysis below.

In short: `info` is your **dimension/reference layer** (who, where, when, result), and `innings` is your **fact/event layer** (what happened, ball by ball). This is exactly the star-schema intuition you should carry into the relational design.

---

## 5. Which Fields Belong in Separate Database Tables

Grouping by natural entity/cardinality:

| Proposed Table | Source Fields | Why it's separate |
|---|---|---|
| **matches** | balls_per_over, city, dates[0] (or a linked match_dates table if multi-date), event.name, event.match_number, gender, match_type, overs, season, team_type, venue, toss.winner, toss.decision, outcome.winner, outcome.by.runs, outcome.by.wickets, meta.data_version, meta.revision | One row per match — the natural grain of `info`. |
| **teams** | Distinct values from `info.teams` across all matches | Teams are reused across hundreds of matches; must not be duplicated per file. |
| **players** | Distinct values from `info.registry.people` (name + registry ID) | Players are reused across matches, teams over seasons, and even across formats — needs its own master table keyed by the registry ID, not name. |
| **match_squads** (junction) | match_id, team_id, player_id (from `info.players`) | Many-to-many: a match has many players per team, a player appears in many matches. |
| **match_officials** (junction) | match_id, official_id, role (umpire/reserve_umpire/tv_umpire/match_referee) | One match has several officials in different roles; one official appears across many matches. |
| **innings** | match_id, innings_number, batting_team_id, target_runs, target_overs | One row per innings per match (grain: match + innings number). |
| **powerplays** | innings_id, from_over, to_over, type | One-to-many with innings (an innings can have multiple powerplay windows in some formats). |
| **overs** (optional, or fold into deliveries) | innings_id, over_number | Only worth a separate table if you need over-level aggregates often; otherwise derivable from deliveries. |
| **deliveries** | innings_id, over_number, actual_delivery, batter_id, non_striker_id, bowler_id, runs_batter, runs_extras, runs_total | This is your central fact table — one row per ball bowled. Highest volume table in the schema. |
| **extras** | delivery_id, extra_type (wide/bye/legbye/noball/penalty), extra_runs | Separate table (or type+amount columns) since a ball can only have zero or one extras type in this schema, but modeling it as its own table future-proofs against multi-extra balls in edge cases. |
| **wickets** | delivery_id, player_out_id, kind | One-to-many potential (rare double dismissals), and cleanly separates "did a wicket fall" from the ball event itself. |
| **wicket_fielders** (junction) | wicket_id, fielder_player_id | Many-to-many: a dismissal can involve multiple fielders (e.g. relay throw), and a fielder appears in many dismissals. |
| **player_of_match** (junction, or column on matches if always single) | match_id, player_id | Modeled as junction table since some matches (rain-affected/tied) award joint Player of the Match. |

---

## 6. Redundant / Derivable Fields to Flag

Being explicit about these will save you storage and — more importantly — prevent data integrity bugs where the stored value disagrees with the computed value:

1. **`runs.total`** = `runs.batter + runs.extras`, always. Store it if you want, but validate it on ingestion rather than trusting it blindly — treat it as a computed/check column, not a primary source of truth.
2. **`outcome.winner`** is, in principle, derivable by summing `innings[0].total` vs `innings[1].total` (plus D/L adjustments where applicable). Still worth storing directly since recomputing it requires replaying the whole innings and handling edge cases (super overs, D/L method, ties) — but be aware it is a *summary*, not independent data, and your ingestion pipeline should cross-validate it against the ball-by-ball totals as a data-quality check.
3. **`innings[1].target`** is entirely derived from `innings[0]`'s total runs + 1, and the format's max overs. No need to treat it as independently authoritative — good candidate for a computed column or a validation check instead of blind storage.
4. **Player names appearing in `players`, `batter`, `bowler`, `non_striker`, `player_out`, `fielders.name`** are all redundant *string* representations of the same underlying entity that's already uniquely identified in `registry.people`. Store the registry ID as the foreign key everywhere; keep the name only in the `players` master table (and optionally a "name as it appeared in this file" historical alias table, since player name spellings occasionally change between seasons — e.g. "Mohammad Hafeez" vs alternate transliterations across other files).
5. **`teams` (info) vs `innings[].team`** — `info.teams` just lists the two participants; `innings[].team` tells you the *order* they batted. Don't store the team list twice; derive the innings order from the `innings` table alone and drop the standalone `teams` array once teams are normalized.
6. **`match_type` and `overs`** are correlated (T20 implies 20 overs, ODI implies 50, etc.) but not strictly redundant since Cricsheet does support rain-shortened/variable-over matches where they diverge — keep both, but don't assume one always implies the other.

---

## 7. Optimized Relational Database Design (Conceptual, No SQL)

### Reference / Dimension Tables
- **teams**(team_id PK, team_name, team_type)
- **players**(player_id PK — use the registry hash as the natural key or map it to a surrogate int, full_name, gender)
- **venues**(venue_id PK, venue_name, city) — normalizes city+venue instead of repeating both strings per match
- **tournaments**(tournament_id PK, tournament_name) — normalizes `event.name` since it repeats across every match in a season
- **seasons**(season_id PK, tournament_id FK, season_label) — since "season" is really a child of "tournament"

### Match-Level Tables
- **matches**(match_id PK, season_id FK, match_number, venue_id FK, match_type, gender, team_type, balls_per_over, overs_allowed, toss_winner_team_id FK, toss_decision, outcome_winner_team_id FK, outcome_margin_type [runs/wickets/tie/no_result], outcome_margin_value, data_version, revision)
- **match_dates**(match_id FK, match_date) — handles multi-day formats cleanly without an array column
- **match_teams**(match_id FK, team_id FK, batting_order_position) — resolves which two teams played and in what order they batted, without repeating team names as free text
- **match_squads**(match_id FK, team_id FK, player_id FK) — the announced playing squad per side
- **match_officials**(match_id FK, official_player_id FK, role_type [umpire/reserve_umpire/tv_umpire/match_referee])
- **player_of_match**(match_id FK, player_id FK)

### Innings-Level Tables
- **innings**(innings_id PK, match_id FK, innings_number, batting_team_id FK, target_runs nullable, target_overs nullable)
- **powerplays**(powerplay_id PK, innings_id FK, from_over, to_over, powerplay_type)

### Ball-by-Ball Fact Tables
- **deliveries**(delivery_id PK, innings_id FK, over_number, actual_delivery_label, batter_id FK, non_striker_id FK, bowler_id FK, runs_batter, runs_extras, runs_total)
- **extras**(extra_id PK, delivery_id FK, extra_type [wide/bye/legbye/noball/penalty], extra_runs)
- **wickets**(wicket_id PK, delivery_id FK, player_out_id FK, dismissal_kind)
- **wicket_fielders**(wicket_id FK, fielder_player_id FK)

### Design Rationale
- **Star-schema shape**: `matches` sits at the center like a fact table for match-level analytics (e.g. "how many matches has each venue hosted", "team win rates by toss decision"), while `deliveries` is the true high-volume fact table for ball-by-ball analytics (batting averages, economy rates, phase-wise scoring, etc.). This two-fact-table design is normal in sports analytics: match-level BI queries don't need to scan millions of delivery rows, and delivery-level queries don't need to join through squad/official tables.
- **Every player reference uses `player_id`, never a raw name string** — this is the single most important integrity rule, since it's what lets you correctly aggregate a player's career stats across thousands of files where their name might be typed slightly differently.
- **Junction tables** (`match_squads`, `match_officials`, `wicket_fielders`) cleanly handle every one-to-many/many-to-many relationship in the source JSON without needing array/JSON columns inside a relational table.
- **`extras` and `wickets` are separated from `deliveries`** rather than adding five nullable extras columns and a wicket-kind column onto every delivery row — most balls have neither, so this keeps the fact table narrow and avoids sparse nullable columns.

---

## 8. Complete Data Dictionary

| Field (source path) | Data Type | Nullable | Cardinality / Notes |
|---|---|---|---|
| meta.data_version | string (semver) | No | One per file |
| meta.created | date | No | One per file |
| meta.revision | integer | No | One per file |
| info.balls_per_over | integer | No | Typically 6 |
| info.city | string | Yes | Some venues/neutral sites omit city |
| info.dates | array\<date\> | No | 1 element for T20/ODI, multiple for Test |
| info.event.name | string | No | Repeats across all matches in a tournament |
| info.event.match_number | integer | Yes | Not all matches (e.g. some historical/exhibition) have a sequential number |
| info.gender | enum(male, female) | No | |
| info.match_type | enum(T20, ODI, Test, ...) | No | |
| info.officials.umpires | array\<string\> | Yes | Usually 2 |
| info.officials.reserve_umpires | array\<string\> | Yes | 0 or 1 typically |
| info.officials.tv_umpires | array\<string\> | Yes | Usually 1 |
| info.officials.match_referees | array\<string\> | Yes | Usually 1 |
| info.outcome.winner | string (team name) | Yes | Null for tie/no-result matches |
| info.outcome.by.runs | integer | Yes | Mutually exclusive with `by.wickets` |
| info.outcome.by.wickets | integer | Yes | Mutually exclusive with `by.runs` |
| info.overs | integer | No | Max overs per innings for the format |
| info.player_of_match | array\<string\> | Yes | Usually 1, can be more (joint award) |
| info.players | object\<team → array\<string\>\> | No | Squad list, 11+ per team typically |
| info.registry.people | object\<name → hash id\> | No | Master identity map, includes players AND officials |
| info.season | string | No | e.g. "2007/08" or "2023" |
| info.team_type | enum(club, international) | No | |
| info.teams | array\<string\>, length 2 | No | |
| info.toss.decision | enum(bat, field) | No | |
| info.toss.winner | string (team name) | No | |
| info.venue | string | No | |
| innings[].team | string (team name) | No | |
| innings[].powerplays[].from | decimal (over.ball) | No | |
| innings[].powerplays[].to | decimal (over.ball) | No | |
| innings[].powerplays[].type | enum(mandatory, batting, bowling) | No | |
| innings[].target.overs | integer | Yes | Only present on 2nd/chasing innings |
| innings[].target.runs | integer | Yes | Only present on 2nd/chasing innings |
| innings[].overs[].over | integer | No | Zero-indexed |
| deliveries[].actual_delivery | string (over.ball) | No | Can repeat within an over (extra balls) |
| deliveries[].batter | string (name) | No | Resolve via registry |
| deliveries[].non_striker | string (name) | No | Resolve via registry |
| deliveries[].bowler | string (name) | No | Resolve via registry |
| deliveries[].runs.batter | integer | No | 0–6 typically |
| deliveries[].runs.extras | integer | No | 0 if no extra |
| deliveries[].runs.total | integer | No | Derived: batter + extras |
| deliveries[].extras.wides | integer | Yes | Only present if a wide occurred |
| deliveries[].extras.byes | integer | Yes | Only present if byes occurred |
| deliveries[].extras.legbyes | integer | Yes | Only present if leg byes occurred |
| deliveries[].extras.noballs | integer | Yes | Only present if a no-ball occurred (not in this file, but valid per schema) |
| deliveries[].extras.penalty | integer | Yes | Rare, penalty runs |
| deliveries[].wickets[].kind | enum(bowled, caught, lbw, run out, stumped, hit wicket, ...) | Yes | Only present if a wicket fell on this ball |
| deliveries[].wickets[].player_out | string (name) | Yes | Resolve via registry; may differ from `batter` (e.g. non-striker run out) |
| deliveries[].wickets[].fielders[].name | string (name) | Yes | 0 for bowled/lbw, 1+ for caught/run out |

---

### Summary Takeaway

The Cricsheet JSON is designed as a **self-contained document per match**, optimized for portability and human readability — not for relational querying at scale. The core normalization work for your platform is:
1. Pull `registry.people` out as the master player table and use its IDs everywhere instead of name strings.
2. Split `info` into `matches` plus junction tables for the one-to-many relationships (squads, officials, player-of-match).
3. Treat `innings` → `overs` → `deliveries` as a single flattened fact table (`deliveries`), with `extras` and `wickets` broken out into their own narrow child tables.
4. Flag `runs.total`, `outcome.winner`, and `target` as derivable fields you should validate against the ball-by-ball data rather than trust blindly on ingestion — this will catch data-quality issues in bulk IPL ingestion (a known issue across historical Cricsheet files where revisions get released to fix scoring errors).
