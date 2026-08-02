# app/db/database.py
# CricketIQ AI - Database connection setup using SQLAlchemy 2.0 style.

import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# ---------------------------------------------------------------------
# STEP 1: Load environment variables
# ---------------------------------------------------------------------
load_dotenv()

# ---------------------------------------------------------------------
# STEP 2: Read DATABASE_URL
# ---------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError(
        "DATABASE_URL is not set. Please add it to your .env file.\n"
        "Example:\n"
        "DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cricketiq"
    )

# ---------------------------------------------------------------------
# STEP 3: Create SQLAlchemy engine
# ---------------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=False
)

# ---------------------------------------------------------------------
# STEP 4: Create session factory
# ---------------------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------------------------------------------------------------
# STEP 5: Base class for ORM models
# ---------------------------------------------------------------------
class Base(DeclarativeBase):
    pass

# ---------------------------------------------------------------------
# STEP 6: Database dependency
# ---------------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()