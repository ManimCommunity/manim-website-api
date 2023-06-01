import json
import os
import re
from datetime import datetime

from api._config import TMP_FILE
from .youtube_search import Service


def extract_channel_id_from_rss_link(str):
    return re.findall(
        r"(?<=https://www.youtube.com/feeds/videos.xml\?channel_id=)[0-9a-zA-Z_-]+", str
    )


def extract_channel_id_from_channel_url(str):
    return re.findall(r"(?<=https://www.youtube.com/channel/)[0-9a-zA-Z_-]+", str)


def get_youtube_channel_id_from_custom_name(name):
    service = Service(
        10,
        os.getenv('YOUTUBE_DATA_APP_KEY'))
    return service.find_channel_by_custom_url(name)


def now():
    return datetime.utcnow().timestamp()


def get_data():
    if os.path.exists(TMP_FILE):
        return json.loads(open(TMP_FILE, "r").read())
    else:
        return {"last_updated": 0, "currently_crawling": False, "entries": []}


def save_data(data):
    return open(TMP_FILE, "w").write(json.dumps(data))

def is_manim_video(entry):
    try:
        check_str = entry["title"] + " " + entry["summary"]
        return (
            "manim" in check_str.lower()
            or "#some" in check_str.lower()
            or "SoME" in check_str
        )
    except:
        return False

def sanitize(str):
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    filtered_string = re_pattern.sub(u'\uFFFD', str)
    return filtered_string
