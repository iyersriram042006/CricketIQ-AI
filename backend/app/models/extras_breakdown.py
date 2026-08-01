from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, Text

from app.db.database import Base


class ExtrasBreakdown(Base):
    __tablename__ = "extras_breakdown"

    extra_id = Column(Integer, primary_key=True, index=True)

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id"),
        nullable=False
    )

    innings_number = Column(SmallInteger, nullable=False)

    over_number = Column(SmallInteger, nullable=False)

    ball_number = Column(SmallInteger, nullable=False)

    extra_type = Column(Text, nullable=False)

    extra_runs = Column(SmallInteger, nullable=False)