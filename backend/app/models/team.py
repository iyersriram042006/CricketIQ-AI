from sqlalchemy import Column, Integer, Text

from app.db.database import Base


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(Text, unique=True, nullable=False)