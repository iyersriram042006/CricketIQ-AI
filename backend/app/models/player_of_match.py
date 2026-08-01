from sqlalchemy import Column, ForeignKey, Integer, Text

from app.db.database import Base


class PlayerOfMatch(Base):
    __tablename__ = "player_of_match"

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id"),
        primary_key=True
    )

    player_id = Column(
        Text,
        ForeignKey("players.player_id"),
        primary_key=True
    )

    player_name = Column(Text, nullable=False)