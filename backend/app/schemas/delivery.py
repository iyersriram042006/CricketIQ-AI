from pydantic import BaseModel


class DeliveryResponse(BaseModel):
    delivery_id: int
    match_id: int
    innings_number: int
    batting_team: str
    over_number: int
    ball_number: int
    batter: str
    non_striker: str
    bowler: str
    batter_runs: int
    extras_runs: int
    total_runs: int
    wides: int

    class Config:
        from_attributes = True