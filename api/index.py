from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

from ._config import *
from ._config import SQLALCHEMY_DATABASE_URI
from ._crud import query_video
from ._tables import Base

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app, engine_options=SQLALCHEMY_ENGINE_OPTIONS)

Base.query = db.session.query_property()
with app.app_context():
    Base.metadata.create_all(bind=db.engine)


@app.route("/videos/<int:page_id>")
@cross_origin()
def videos(page_id: int):
    if page_id <= 0:
        return "[]"
    result = query_video(page_id, db)
    res = jsonify(result)
    res.add_etag()
    # Cache the result for 1 day
    res.cache_control.max_age = SECONDS_IN_HOUR
    res.cache_control.public = True
    res.cache_control.s_maxage = SECONDS_IN_DAY
    res.cache_control.immutable = True
    res.cache_control["stale-while-revalidate"] = SECONDS_IN_HOUR
    return res


# @app.get("/update")
# def update():
#     if not p.is_alive():
#         return "unable to update", 500
#     # mostly useless, because the inner loop will trigger it anyway
#     queue_update()
#     return "Update request received", 200

if __name__ == "__main__":
    app.run(debug=True, port=3001)
