from sqlalchemy import Column, Integer, Text

from app.db.database import Base


class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, index=True)
    venue_name = Column(Text, unique=True, nullable=False)
    city = Column(Text, nullable=True)