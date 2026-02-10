from flask import Flask

app = Flask(__name__, template_folder="../frontend/templates")

from backend import static
#Import here all the files that contain at least an endpoint
from backend import dataEndpoints
app.register_blueprint(dataEndpoints.data_bp)
