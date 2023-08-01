from flask import Blueprint

app = Blueprint("basics",__name__)
log=None
from . import sesson,image

def init(app,log_=print):
    global log
    log=log_
    sesson.init_app(app)