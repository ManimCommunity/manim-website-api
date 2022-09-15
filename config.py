import os
from dotenv import load_dotenv

load_dotenv()


CRAWL_DELAY = 5
SECONDS_IN_DAY = 24 * 60 * 60
README_URL = (
    "https://raw.githubusercontent.com/ManimCommunity/awesome-manim/main/README.md"
)
# LAST_UPDATED = 0
# CURRENTLY_CRAWLING = False
# ENTRIES = []
VIDEOS_PER_PAGE = 30
TMP_FILE = "/tmp/data.json"

# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
# SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"