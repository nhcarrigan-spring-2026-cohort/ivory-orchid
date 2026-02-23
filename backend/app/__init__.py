from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder="../../frontend/templates")
db = SQLAlchemy()

#Sets various config from env vars or defaults
if os.getenv("SQLALCHEMY_DATABASE_URI") and os.getenv("SQLALCHEMY_DATABASE_URI").strip() != "":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) + "/database.db"

#Import database models
from . import types, utils

db.init_app(app)

def setup_db():
    first = types.Shelter.query.get(1)

#Create the tables if they are missing
with app.app_context():
    utils.setup_db(db)

#Import here all the files that contain at least an endpoint
from . import dataEndpoints, static

app.register_blueprint(dataEndpoints.data_bp)
