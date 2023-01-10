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


@app.route('/myProfile', methods=["POST","GET"])
def myProfile():
    startTime = time()
    
    if 'email' not in session and 'name' not in session:
        return redirect('/login')
    
    if request.method == "GET":
        fields=["Name","Course","Skills","Interests","Email","Password","Points","Rank","Position","JoinDate"]
        rdata={}
        data = db.getMembers([("Email","=",session['email'])],fields)
        for i in range(0,len(fields)):
            rdata[fields[i].lower()]=data[0][i]
        print(rdata)
        cprint(f"myProfile Page Sent:{time()-startTime}",'cyan')
        return render_template('myProfile.html',rData=rdata,courses=db.getCourses(fields=["Name"]))
    
    # Recive all data
    rData = request.form.copy()
    
    #Print data Recived
    cprint(f"My Profile",'blue')
    for key, value in rData.items():
        if key.startswith('0'):
            value = "********"
        cprint((key,value),'blue')
        
    # Error on not enough data
    if not ('name' in rData and '0password' in rData and 'skills' in rData
            and 'course' in rData and 'interests' in rData):
        return render_template("error.html",error=f"Incomplete data")
    
    # Invalid data 
    if len(rData['name'])<3:
        return render_template("myProfile.html",rData=rData,name=True,courses=db.getCourses(fields=["Name"]))
    if len(rData['0password'])<10 and len(rData['0password'])>0:
        return render_template("myProfile.html",rData=rData,password=True,courses=db.getCourses(fields=["Name"]))
    
    # Add to database
    # try:
    commit = db.changeMember(session['email'],rData)
    commits.append(commit)
    # except BaseException as e:
    #     return render_template("error.html",error=f"Error: {e}")
    
    # Add the req data to session
    keys = ['name']
    for key in keys:
        print(session)
        session[key]=rData[key]
        
    cprint(f"myProfile Time:{time()-startTime}",'cyan')
    return redirect('/')


@app.route('/signup', methods=["POST","GET"])
def signup():
    startTime = time()
    
    if 'email' in session and 'name' in session:
        return redirect('/')
    
    if request.method == "GET":
        cprint(f"Signup Page Sent:{time()-startTime}",'cyan')
        return render_template('signup.html',rData={},courses=db.getCourses(fields=["Name"]))
    
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
            and 'course' in rData and 'interests' in rData):
        return render_template("error.html",error=f"Incomplete data")
    
    # Invalid data 
    if len(rData['name'])<3:
        return render_template("signup.html",rData=rData,name=True,courses=db.getCourses(fields=["Name"]))
    if rData['email'].find('@') == -1:
        return render_template("signup.html",rData=rData,email=True,courses=db.getCourses(fields=["Name"]))
    if len(rData['0password'])<10:
        return render_template("signup.html",rData=rData,password=True,courses=db.getCourses(fields=["Name"]))
    
    # Add to database
    try:
        commit = db.addMember(rData['name'],rData['email'],rData['0password'],rData['course'],rData['interests'],rData['skills'])
        commits.append(commit)
    except BaseException as e:
        return render_template("error.html",error=f"Error: {e}")
    
    # Add the req data to session
    keys = ['email','name']
    for key in keys:
        session[key]=rData[key]
        
    cprint(f"Signup Time:{time()-startTime}",'cyan')
    return redirect('/')

@app.route('/login', methods=["POST","GET"])
def login():
    startTime = time()
    
    if 'email' in session and 'name' in session:
        return redirect('/')
    
    if request.method == "GET":
        cprint(f"Login Page Sent:{time()-startTime}",'cyan')
        return render_template('login.html',rData={})
    
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
        return render_template("login.html",error=f"Incomplete request")
    
    # check in database
    results = db.getMember(['Name','Email','Password'],rData['email'])
    if not results:
        return render_template("login.html",email=True,rData=rData)
    
    if results[0][2] != rData['0password']:
        return render_template("login.html",password=True,rData=rData)
    
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


@app.route('/')
def index():
    if 'email' not in session or 'name' not in session:
        return redirect('/login')
    return render_template('index.html')

# @app.route('/', defaults={'path': ''})
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