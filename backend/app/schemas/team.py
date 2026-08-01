from pydantic import BaseModel


class TeamResponse(BaseModel):
    team_id: int
    team_name: str

    class Config:
        from_attributes = True