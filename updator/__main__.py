import logging
import re
import time
import traceback
from datetime import datetime

import feedparser
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from ..api import db, app
from api._config import *
from api._crud import query_video
from .helper import get_youtube_channel_id_from_custom_name, is_manim_video, sanitize
from api._tables import video_table

engine = create_engine(SQLALCHEMY_DATABASE_URI, **SQLALCHEMY_ENGINE_OPTIONS)
Session = sessionmaker(engine)


def scrape_rss_feeds():
    # Get the README content
    # readme_path = Path(__file__).parent.parent.joinpath(Path("README.md")).absolute()
    # content = open(readme_path, "r").read()

    response = requests.get(README_URL)
    content = response.text

    # Get channel URLs from the content
    channel_ids = []
    channel_custom_names = []
    # channel_ids.extend(re.findall(r"https://www.youtube.com/channel/[0-9a-zA-Z_-]+", content))
    channel_ids.extend(
        re.findall(r"(?<=https://www\.youtube\.com/channel/)[0-9a-zA-Z_-]+", content)
    )
    channel_custom_names.extend(
        re.findall(r"(?<=https://www\.youtube\.com/c/)[0-9a-zA-Z_-]+", content)
    )

    # Try to fetch channel IDs for URLs with custom channel names,
    # because the RSS API only accepts channel IDs
    for channel_custom_name in channel_custom_names:
        try:
            channel_id = get_youtube_channel_id_from_custom_name(channel_custom_name)
            if channel_id:
                channel_ids.append(channel_id)
                print("Channel ID for", channel_custom_name, "=", channel_id)
            else:
                print("Could not get the channel ID for", channel_custom_name)
        except:
            print("Could not get the channel ID for", channel_custom_name)

        time.sleep(CRAWL_DELAY)

    for id in channel_ids:
        new_entries = []
        feed_url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + id
        print("Crawling", feed_url)
        feed = feedparser.parse(feed_url)
        new_entries.extend(feed["entries"])
        time.sleep(CRAWL_DELAY)

        rows = []
        for entry in new_entries:
            rows.append(
                {
                    "yt_videoid": entry["yt_videoid"],
                    "link": entry["link"],
                    "author": entry["author"],
                    "yt_channelid": entry["yt_channelid"],
                    "title": sanitize(entry["title"]),
                    "published": entry["published"],
                    "updated": entry["updated"],
                    "thumbnail_url": entry["media_thumbnail"][0]["url"],
                    "summary": sanitize(entry["summary"]),
                    "view_count": entry["media_statistics"]["views"],
                    "like_count": entry["media_starrating"]["count"],
                    "json": entry,
                    "is_manim_video": is_manim_video(entry),
                }
            )

        for row in rows:
            print("Video ID: ",row["yt_videoid"])
            try:
                current_time = datetime.now()
                data = {"created_at": current_time, **row}
                with Session() as session:
                    existing_item = (
                        session.query(video_table)
                        .filter_by(yt_videoid=data["yt_videoid"])
                        .first()
                    )
                    if existing_item:
                        update_stmt = (
                            video_table.update()
                            .where(video_table.c.yt_videoid == data["yt_videoid"])
                            .values(
                                **{
                                    **data,
                                    "updated_at": current_time,
                                }
                            )
                        )
                        session.execute(update_stmt)
                    else:
                        ins_stmt = video_table.insert().values(**data)
                        session.execute(ins_stmt)

                    session.commit()
            except:
                logging.warning(f"Could not insert row: {row}")
                print(traceback.format_exc())
                return
    # Reset the cache
    query_video.cache_clear()
    return None


if __name__ == "__main__":
    scrape_rss_feeds()
