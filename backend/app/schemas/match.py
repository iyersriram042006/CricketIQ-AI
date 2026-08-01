from pydantic import BaseModel


class MatchResponse(BaseModel):
    match_id: int
    team_1: str
    team_2: str
    venue: str | None = None
    city: str | None = None
    season: str | None = None
    toss_winner: str | None = None
    toss_decision: str | None = None
    match_winner: str | None = None

    class Config:
        from_attributes = True