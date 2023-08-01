from flask import render_template, session, request, redirect,jsonify
from . import app,log

@app.route('/')
def index():
    # if 'username' not in session:
    #     return redirect('/login')
    return render_template('index.html',theme="light",textTheme="dark")
