from pydantic import BaseModel


class PowerplayResponse(BaseModel):
    powerplay_id: int
    match_id: int
    innings_number: int
    from_over: float
    to_over: float
    powerplay_type: str

    class Config:
        from_attributes = True