from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, Text

from app.db.database import Base


class Wicket(Base):
    __tablename__ = "wickets"

    wicket_id = Column(Integer, primary_key=True, index=True)

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id"),
        nullable=False
    )

    innings_number = Column(SmallInteger, nullable=False)

    batting_team = Column(Text, nullable=False)

    over_number = Column(SmallInteger, nullable=False)

    ball_number = Column(SmallInteger, nullable=False)

    batter_out = Column(Text, nullable=False)

    bowler = Column(Text, nullable=False)

    fielder = Column(Text)

    kind_of_wicket = Column(Text, nullable=False)