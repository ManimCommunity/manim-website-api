import os

import certifi
from dotenv import load_dotenv

load_dotenv()


CRAWL_DELAY = 0.5
SECONDS_IN_HOUR = 60 * 60
SECONDS_IN_DAY = 24 * 60 * 60
UPDATE_INTERVAL = 4 * 60 * 60  # Run every 4 hours
README_URL = (
    "https://raw.githubusercontent.com/ManimCommunity/awesome-manim/main/README.md"
)
# LAST_UPDATED = 0
# CURRENTLY_CRAWLING = False
# ENTRIES = []
VIDEOS_PER_PAGE = 30
TMP_FILE = "/tmp/data.json"

# SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ENGINE_OPTIONS = {}
