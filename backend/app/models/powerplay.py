from sqlalchemy import Column, Integer, Numeric, ForeignKey, SmallInteger, Text

from app.db.database import Base


class Powerplay(Base):
    __tablename__ = "powerplays"

    powerplay_id = Column(Integer, primary_key=True, index=True)

    match_id = Column(
        Integer,
        ForeignKey("matches.match_id"),
        nullable=False
    )

    innings_number = Column(SmallInteger, nullable=False)

    from_over = Column(Numeric(3, 1), nullable=False)

    to_over = Column(Numeric(3, 1), nullable=False)

    powerplay_type = Column(Text, nullable=False)