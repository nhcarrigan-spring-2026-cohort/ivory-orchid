from flask import Flask

app = Flask(__name__, template_folder="../../frontend/templates")

#Import here all the files that contain at least an endpoint
from . import dataEndpoints, static

app.register_blueprint(dataEndpoints.data_bp)
