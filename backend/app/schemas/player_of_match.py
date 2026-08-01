from pydantic import BaseModel


class PlayerOfMatchResponse(BaseModel):
    match_id: int
    player_id: str
    player_name: str

    class Config:
        from_attributes = True