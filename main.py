from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

# from supabase import create_client, Client
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from tables import video_table, Base

from config import *
from update_entries import update_entries


# supabase: Client = create_client(url, key)


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
    rows = (
        supabase.table("video")
        .select("*")
        .eq("is_manim_video", True)
        .order("published", desc=True)
        .range((page_id - 1) * VIDEOS_PER_PAGE, page_id * VIDEOS_PER_PAGE)
        .execute()
    )
    return rows.json()


@app.route("/update")
def update():
    if "X-Appengine-Cron" in request.headers:
        if request.headers["X-Appengine-Cron"] == "true":
            update_entries(db)
            return "Update complete", 200

    return "Forbidden", 403


if __name__ == "__main__":
    app.run(debug=True, port=3001)
