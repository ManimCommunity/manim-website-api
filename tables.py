from sqlalchemy import *

video_table = Table(
    "video",
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime, nullable=False),
    Column("yt_videoid", String(64), nullable=False),
    Column("link", String(255), nullable=False),
    Column("author", String(255)),
    Column("yt_channelid", String(64)),
    Column("title", String(1024)),
    Column("published", DateTime),
    Column("updated", DateTime),
    Column("thumbnail_url", String(255)),
    Column("summary", String(255)),
    Column("view_count", Integer),
    Column("like_count", Integer),
    Column("json", JSON),
    Column("is_manim_video", Boolean),
)
