# app/core/config.py
# CricketIQ AI - Central place to load and store app configuration.
# This file is responsible for ONE thing only: reading settings (like
# secrets and connection strings) from the .env file so the rest of
# the app can use them without ever hardcoding sensitive values.

import os                          # built-in module to read environment variables
from dotenv import load_dotenv     # loads variables from a .env file into the environment

# ---------------------------------------------------------------------
# STEP 1: Load environment variables from the .env file
# ---------------------------------------------------------------------
# load_dotenv() looks for a file named ".env" (by default, in the
# project's root folder) and loads any KEY=VALUE lines inside it into
# the environment, so we can read them with os.getenv() below.
#
# We call this here too (not just in database.py) because config.py
# should be able to work standalone - any file that imports config.py
# shouldn't have to remember to call load_dotenv() itself first.
load_dotenv()

# ---------------------------------------------------------------------
# STEP 2: Read the DATABASE_URL setting
# ---------------------------------------------------------------------
# os.getenv() looks up the value of an environment variable by name.
# We expect a variable named DATABASE_URL to exist inside the .env file,
# formatted like this for PostgreSQL:
#
#   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/cricketiq
#
# If it's missing, we raise a clear error immediately at startup,
# instead of letting the app crash later with a confusing error deep
# inside some unrelated part of the code.
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError(
        "DATABASE_URL is not set. Please add it to your .env file, e.g.\n"
        "DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/cricketiq"
    )

# ---------------------------------------------------------------------
# Usage elsewhere in the app:
# ---------------------------------------------------------------------
#   from app.core.config import DATABASE_URL
#
# Any file that needs the connection string imports it from here,
# instead of calling os.getenv() again itself. This keeps all our
# configuration reading logic in exactly one place.