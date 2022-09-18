
import threading

from flask import jsonify
from flask_cors import cross_origin

from .config import *
from .crud import query_video
from . import app
from .fetch import update_loop, queue_update

if not os.environ.get("NO_UPDATE_THREAD"):
    p = threading.Thread(target=update_loop, daemon=True)
    p.start()


@app.route("/videos/<int:page_id>")
@cross_origin()
def videos(page_id: int):
    if page_id <= 0:
        return "[]"
    result = query_video(page_id)
    return jsonify(result)

@app.get("/update")
def update():
    if not p.is_alive():
        return "unable to update", 500
    # mostly useless, because the inner loop will trigger it anyway
    queue_update()
    return "Update request received", 200

if __name__ == "__main__":
    app.run(debug=True, port=3001)
