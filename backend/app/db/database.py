# app/db/database.py
# CricketIQ AI - Database connection setup using SQLAlchemy 2.0 style.
# This file is responsible for ONE thing only: creating the database
# engine/session machinery that the rest of the app will use to talk
# to PostgreSQL. Models, schemas, and routes do NOT belong here.

import os                              # built-in module to read environment variables
from dotenv import load_dotenv         # loads variables from a .env file into the environment

from sqlalchemy import create_engine   # builds the low-level connection to PostgreSQL
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # SQLAlchemy 2.0 ORM tools

# ---------------------------------------------------------------------
# STEP 1: Load environment variables from the .env file
# ---------------------------------------------------------------------
# load_dotenv() looks for a file named ".env" (by default, in the
# project's root folder) and loads any KEY=VALUE lines inside it into
# the environment, so we can read them with os.getenv() below.
# This keeps secrets like passwords OUT of our source code.
load_dotenv()

# ---------------------------------------------------------------------
# STEP 2: Read the database connection string from the environment
# ---------------------------------------------------------------------
# We expect a variable named DATABASE_URL to exist inside the .env file,
# formatted like this for PostgreSQL:
#
#   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/cricketiq
#
# os.getenv() reads that value. If it's missing, we raise a clear error
# immediately instead of letting the app fail later with a confusing
# connection error.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError(
        "DATABASE_URL is not set. Please add it to your .env file, e.g.\n"
        "DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cricketiq"
    )

# ---------------------------------------------------------------------
# STEP 3: Create the SQLAlchemy engine
# ---------------------------------------------------------------------
# The "engine" is the core object that manages the actual connection(s)
# to PostgreSQL. It doesn't connect immediately - connections are opened
# only when they're actually needed (lazy connection).
#
# echo=False keeps SQL query logging off by default. Set it to True
# temporarily while debugging if you want to see every SQL statement
# SQLAlchemy sends to PostgreSQL in your terminal.
engine = create_engine(DATABASE_URL, echo=False)

from sqlalchemy import text

try:
    with engine.connect() as conn:
        print("===================================")
        print("DATABASE:", conn.execute(text("SELECT current_database()")).scalar())
        print("SCHEMA:", conn.execute(text("SELECT current_schema()")).scalar())
        print("TABLES:", conn.execute(text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname='public'
        """)).fetchall())
        print("===================================")
except Exception as e:
    print("DATABASE ERROR:", e)

# ---------------------------------------------------------------------
# STEP 4: Create a session factory
# ---------------------------------------------------------------------
# A "session" is what we use to actually run queries and commit changes
# to the database. Instead of creating sessions by hand everywhere,
# SessionLocal is a factory - calling SessionLocal() gives us a brand
# new session connected through our engine.
#
# autocommit=False: changes are only saved to the DB when we explicitly
#                   call session.commit() - this gives us control over
#                   when data is actually written.
# autoflush=False:  SQLAlchemy won't automatically push pending changes
#                   to the DB before every query - we control that too.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------------------------------------------------
# STEP 5: Create the Base class for our ORM models
# ---------------------------------------------------------------------
# Every table model we create later (in app/models/) will inherit from
# this Base class. SQLAlchemy uses it to keep track of all our models
# and their table definitions in one place.
#
# This is the SQLAlchemy 2.0 style of defining Base - using a class
# that inherits from DeclarativeBase, instead of the older
# declarative_base() function style used in SQLAlchemy 1.x.
class Base(DeclarativeBase):
    pass

# ---------------------------------------------------------------------
# STEP 6: Dependency function to get a database session
# ---------------------------------------------------------------------
# FastAPI route functions will use this via Depends(get_db) to receive
# a working database session for the duration of a single request.
#
# This is a generator function (it uses "yield" instead of "return").
# - Everything BEFORE "yield" runs when the request starts (open a session).
# - The session is handed to the route function to use.
# - Everything AFTER "yield" runs when the request finishes (close the
#   session), even if an error happened - because it's wrapped in a
#   try/finally block. This guarantees we never leave connections open.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()