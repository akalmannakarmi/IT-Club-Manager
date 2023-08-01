from flask import Flask
from logger import colorConsoleLog
from basics import app as basicAPP,init as basicInit
from clubSite import app as storeAPP,init as storeInit

app = Flask(__name__)
basicInit(app,log_=colorConsoleLog)
storeInit(app,log_=colorConsoleLog)
app.register_blueprint(basicAPP)
app.register_blueprint(storeAPP)

if __name__ == "__main__":
    app.run(debug=True)