from pydantic import BaseModel


class ExtrasBreakdownResponse(BaseModel):
    extra_id: int
    match_id: int
    innings_number: int
    over_number: int
    ball_number: int
    extra_type: str
    extra_runs: int

    class Config:
        from_attributes = True