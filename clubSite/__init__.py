from flask import Blueprint

app = Blueprint("clubSite",__name__)
log=None
from . import sites

def init(app,log_=print):
    global log
    log=log_