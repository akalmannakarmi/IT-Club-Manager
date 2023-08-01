from flask import send_from_directory
from . import app

@app.route("/static/img/<image>",methods=["GET"])
def image(image):
    return send_from_directory("static/img",image)