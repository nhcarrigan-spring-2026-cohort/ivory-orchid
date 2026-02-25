import sys
import os

os.environ["FLASK_TESTING"] = "true"
os.environ["TESTING"] = "true"

sys.path.append("..")
from app import app
app.config["TESTING"] = True
