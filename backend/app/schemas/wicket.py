from pydantic import BaseModel


class WicketResponse(BaseModel):
    wicket_id: int
    match_id: int
    innings_number: int
    batting_team: str
    over_number: int
    ball_number: int
    batter_out: str
    bowler: str
    fielder: str | None = None
    kind_of_wicket: str

    class Config:
        from_attributes = True