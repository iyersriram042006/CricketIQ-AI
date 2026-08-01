from pydantic import BaseModel


class PlayerResponse(BaseModel):
    player_id: str
    player_name: str

    model_config = {
        "from_attributes": True
    }