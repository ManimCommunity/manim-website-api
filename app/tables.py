from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import TEXT

Base = declarative_base()
video_table = Table(
    "video",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime),
    Column("yt_videoid", String(64), nullable=False),
    Column("link", String(255), nullable=False),
    Column("author", String(255)),
    Column("yt_channelid", String(64)),
    Column("title", TEXT(1024, charset="utf8mb4")),
    Column("published", DateTime),
    Column("updated", DateTime),
    Column("thumbnail_url", String(255)),
    Column("summary", TEXT(4096, charset="utf8mb4")),
    Column("view_count", Integer),
    Column("like_count", Integer),
    Column("json", JSON),
    Column("is_manim_video", Boolean),
    UniqueConstraint("yt_videoid", name="uix_1"),
)
