from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from queue import Queue

from .config import SQLALCHEMY_DATABASE_URI
from .tables import Base

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
Base.query = db.session.query_property()
Base.metadata.create_all(bind=db.engine)
update_requests = Queue()
last_update: int = 0

from .main import *
