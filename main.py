from flask import Flask , render_template, request,redirect,session
from os import path
import json
from termcolor import cprint
from time import time,sleep
from threading import Thread
from db import db

app = Flask(__name__)
app.secret_key ="secret"
commits = []



@app.route('/signup', methods=["POST"])
def signup():
    startTime = time()
    # Recive all data
    rData = request.form.deepcopy()
    
    #Print data Recived
    cprint(f"Sign up",'blue')
    for key, value in rData.items():
        if key.startswith('0'):
            value = "********"
        cprint((key,value),'blue')
        
    # Error on not enough data
    if not ('name' in rData and 'email' in rData and '0password' in rData and 'skills' in rData
            and 'course' in rData and 'semester' in rData and 'interests' in rData):
        return render_template("error.html",error=f"Incomplete data")
    
    # Invalid data 
    if len(rData['name'])<3:
        return render_template("error.html",error=f"Name cant be shorter that 3")
    if rData['email'].find('@') == -1:
        return render_template("error.html",error=f"Invalid Email")
    if len(rData['0password'])<10:
        return render_template("error.html",error=f"Password cant be shorter that 10")
    
    # Add to database
    try:
        commit = db.addMember(rData['name'],rData['email'],rData['0password'],rData['course']+rData['semester'],rData['interests'],rData['skills'])
        commits.append(commit)
    except BaseException as e:
        return render_template("error.html",error=f"Error: {e}")
    
    # Add the req data to session
    keys = ['email','name']
    for key in keys:
        session[key]=rData[key]
        
    cprint(f"Signup Time:{time()-startTime}",'cyan')
    return redirect('/')

@app.route('/login', methods=["POST"])
def login():
    startTime = time()
    # Set all data recived to session
    rData = request.form.deepcopy()
    
    #Print data Recived
    cprint(f"Login up",'blue')
    for key, value in rData.items():
        if key.startswith('0'):
            value = "********" 
        cprint((key,value),'blue')
        
    # Error on not enough data
    if not ('email' in rData and '0password'):
        return render_template("error.html",error=f"Incomplete data")
    
    if rData['email'].find('@') == -1:
        return render_template("error.html",error=f"Invalid Email")
    if len(rData['0password'])<10:
        return render_template("error.html",error=f"Password cant be shorter that 10")
    
    # check in database
    results = db.getMember(['Name','Email','Password'],rData['email'])
    if not results[0]:
        return render_template("error.html",error=f"The account doesn't exist")
    
    if results[0][2] != rData['0password']:
        return render_template("error.html",error="Incorrect Password")
    
    # Add the req data to session
    keys = ['email']
    for key in keys:
        session[key]=rData[key]
    session['name']=results[0][0]
    
    cprint(f"Login Time:{time()-startTime}",'cyan')
    return redirect('/')

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    if 'name' in session:
        session.pop('name')
    return redirect('/login')

@app.route('/users',methods=['POST'])
def users():
    startTime = time()
    # Set all data recived to session
    rData = json.loads(request.data) 
    
    #Print data Recived
    cprint(f"Users {rData}",'blue')
        
        
    users = db.getMembers(rData['conditions'],rData['fields'])
    cprint(f"Users Data Sent:{time()-startTime}",'cyan')
    return users

@app.route('/interests')
def interests():
    interests = db.getInterests()
    return render_template('0interests.html',interests=interests)

# @app.route('/', defaults={'path': ''})
@app.route('/')
@app.route('/<path:p>')
def default(p=""):
    cprint(f"Data Recived:{p}",'blue')
    for key, value in request.form.items():
        cprint((key,value),'blue')
    if p == "":
        return render_template("index.html",session=session)
    p = p.lower()+".html"
    if path.exists(f"templates/{p}") and not p.startswith('0'):
        return render_template(p)
    return render_template("error.html",error=f"{p} does not exist")

def doCommits():
    while running:
        while len(commits)>0:
            commits[0]()
            commits.pop(0)
            cprint("Commited",'green')
        sleep(.01)

if __name__ == "__main__":
    running = True
    doCommitsT = Thread(target=doCommits)
    doCommitsT.start()
    app.run(debug=False)
    running = False