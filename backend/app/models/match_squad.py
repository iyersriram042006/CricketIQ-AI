from sqlalchemy import Column, ForeignKey, Integer, Text

from app.db.database import Base


class MatchSquad(Base):
    __tablename__ = "match_squads"

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

    team_name = Column(Text, nullable=False)

    player_name = Column(Text, nullable=False)