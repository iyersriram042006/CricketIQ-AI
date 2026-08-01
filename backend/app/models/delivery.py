from sqlalchemy import BigInteger, Column, ForeignKey, Integer, SmallInteger, Text

from app.db.database import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    delivery_id = Column(BigInteger, primary_key=True, index=True)

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id"),
        nullable=False
    )

    innings_number = Column(SmallInteger, nullable=False)

    batting_team = Column(Text, nullable=False)

    over_number = Column(SmallInteger, nullable=False)

    ball_number = Column(SmallInteger, nullable=False)

    batter = Column(Text, nullable=False)

    non_striker = Column(Text, nullable=False)

    bowler = Column(Text, nullable=False)

    batter_runs = Column(SmallInteger, default=0)

    extras_runs = Column(SmallInteger, default=0)

    total_runs = Column(SmallInteger, default=0)

    wides = Column(SmallInteger, default=0)