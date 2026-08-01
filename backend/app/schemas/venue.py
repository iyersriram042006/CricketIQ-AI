from pydantic import BaseModel


class VenueResponse(BaseModel):
    venue_id: int
    venue_name: str
    city: str | None = None

    class Config:
        from_attributes = True