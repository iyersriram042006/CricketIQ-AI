from sqlalchemy import Column, Integer, Text

from app.db.database import Base


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)

    team_1 = Column(Text, nullable=False)
    team_2 = Column(Text, nullable=False)

    venue = Column(Text)
    city = Column(Text)

    season = Column(Text)

    toss_winner = Column(Text)
    toss_decision = Column(Text)

    match_winner = Column(Text)