import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, desc
from tables import video_table, Base

from config import *
from scrape import scrape_rss_feeds


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Base.query = db.session.query_property()
Base.metadata.create_all(bind=db.engine)


@app.route("/videos/<int:page_id>")
@cross_origin()
def videos(page_id: int):
    if page_id <= 0:
        return "[]"
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
    return jsonify(result)


@app.route("/update")
def update():
    if "X-Appengine-Cron" in request.headers:
        if request.headers["X-Appengine-Cron"] == "true":
            scrape_rss_feeds(db)
            return "Update complete", 200

    return "Forbidden", 403


if __name__ == "__main__":
    app.run(debug=True, port=3001)
