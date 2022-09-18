from functools import lru_cache

from sqlalchemy import desc, select

from . import db
from .config import VIDEOS_PER_PAGE
from .tables import video_table


@lru_cache(maxsize=None)
def query_video(page_id):
    stmt = (
        select(
            [
                video_table.c.title,
                video_table.c.author,
                video_table.c.yt_videoid,
                video_table.c.link,
                video_table.c.summary,
                video_table.c.published,
                video_table.c.updated,
                video_table.c.thumbnail_url,
                video_table.c.view_count,
                video_table.c.like_count,
            ]
        )
        .where(video_table.c.is_manim_video == True)
        .order_by(desc(video_table.columns.published))
        .offset((page_id - 1) * VIDEOS_PER_PAGE)
        .limit(VIDEOS_PER_PAGE)
    )
    response = db.session.execute(stmt)
    rows = response.fetchall()
    result = {"data": [dict(row) for row in rows]}
    return result
