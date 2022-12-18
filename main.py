from flask import Flask , render_template, request,redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup.html')
def signup():
    return render_template("signup.html")

@app.route('/signup', methods=["POST"])
def signupP():
    for key, value in request.form.items():
        print(key,value)
    return redirect('/')

@app.route('/base.html')
def base():
    return render_template("base.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    return render_template("error.html",error=f"{path} does not exist")

if __name__ == "__main__":
    app.run(debug=True)