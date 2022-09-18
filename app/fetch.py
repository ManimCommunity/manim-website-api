import logging
import re
import sys
import time
import traceback
import threading
from datetime import datetime

import feedparser
import requests
from sqlalchemy.dialects.mysql import insert

from . import db, update_requests
from .config import *
from .crud import query_video
from .helper import (get_youtube_channel_id_from_custom_name, is_manim_video,
                     sanitize)
from .tables import video_table

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
        re.findall(r"(?<=https://www.youtube.com/channel/)[0-9a-zA-Z_-]+", content)
    )
    channel_custom_names.extend(
        re.findall(r"(?<=https://www.youtube.com/c/)[0-9a-zA-Z_-]+", content)
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
            try:
                current_time = datetime.now()
                insert_stmt = insert(video_table).values(
                    {"created_at": current_time, **row}
                )
                on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                    updated_at=current_time, **row
                )
                response = db.session.execute(on_duplicate_key_stmt)
                db.session.commit()
            except:
                logging.warning(f"Could not insert row: {row}")
                print(traceback.format_exc())
    # Reset the cache
    query_video.cache_clear()
    return None

def queue_update() -> None:
    update_requests.put(True)


def trigger_loop() -> None:
    while True:
        print("Sleeping for %ds" % UPDATE_INTERVAL)
        time.sleep(UPDATE_INTERVAL)
        queue_update()

def update_loop():
    # trigger this loop to run every UPDATE_INTERVAL seconds
    threading.Thread(target=trigger_loop, daemon=True).start()
    last_updated = 0
    while True:
        item = update_requests.get()
        if item and (time.time() - last_updated > UPDATE_INTERVAL):
            print("updating rss feeds")
            try:
                scrape_rss_feeds()
                print("done")
            except Exception:
                traceback.print_exc(file=sys.stdout)
            print("Waiting for next update")
            last_updated = time.time()
        else:
            print("already updated recently")
