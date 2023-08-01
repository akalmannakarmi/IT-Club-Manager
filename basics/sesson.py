from flask import current_app,render_template, session, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from . import app,log
import bcrypt

# Create database object
db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template('signup.html',theme="light",textTheme="dark",rData={})
    
    data = request.get_json()
    print(data)
    if type(data)!= dict:
        return jsonify({"status":"error","detail":"Require a dictionary data"})
    rq=['username','email','password','confirmPassword']
    if any(i not in data for i in rq):
        return jsonify({"status":"error","detail":"Require:"+','.join(rq)})
    data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    if not bcrypt.checkpw(data['confirmPassword'].encode('utf-8'), data['password'].encode('utf-8')):
        return jsonify({"status": "error", "detail": "Passwords don't match"})

        
    new_user = User(username=data['username'],email=data['email'],password=data['password'])

    with current_app.app_context():
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            column = str(e.orig).split('.')[-1].replace('\'', '').replace('\"', '').split('.')[-1].strip()
            if column == 'email':
                return jsonify({"status":"error","detail":"Email already Exists"})
            elif column == 'username':
                return jsonify({"status":"error","detail":"Username already Exists"})
            else:
                return jsonify({"status":"error","detail":f"Unknown Error {e}"})
    return jsonify({"status":"success","detail":"Signup Successful","redirect":"/login"})

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html',theme="light",textTheme="dark",rdata={})
    
    data = request.get_json()
    print(data)
    if type(data)!= dict:
        return jsonify({"status":"error","detail":"Require a dictionary data"})
    
    rq=['email','password']
    if any(i not in data for i in rq):
        return jsonify({"status":"error","detail":"Required:"+','.join(rq)})
    
    with current_app.app_context():
        user = User.query.filter_by(email=data['email']).first()
    
    if user is None:
        return jsonify({"status":"error","detail":"Account doesnt Exist"})

    if not bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
        return jsonify({"status":"error","detail":"Invalid password"})
    session['username'] = user.username
    return jsonify({"status":"success","detail":"Login Successful","redirect":"/"})

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    return redirect('/login')


def init_app(app):
    app.secret_key = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
    db.init_app(app)

    with app.app_context():
        db.create_all()

        return app