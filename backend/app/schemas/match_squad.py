from pydantic import BaseModel


class MatchSquadResponse(BaseModel):
    match_id: int
    player_id: str
    team_name: str
    player_name: str

    class Config:
        from_attributes = True