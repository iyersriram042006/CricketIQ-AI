from sqlalchemy import Column, Text

from app.db.database import Base


class Player(Base):
    __tablename__ = "players"

    player_id = Column(Text, primary_key=True, index=True)
    player_name = Column(Text, nullable=False)