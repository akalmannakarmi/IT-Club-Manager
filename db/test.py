from flask import Flask
from threading import Thread
from time import sleep
from test2 import Db

app = Flask(__name__)
myDb = Db()
commits = []

@app.route('/logout')
def logout():
    commit = myDb.insert()
    commits.append(commit)
    return 'Hello World'

def run():
    while running:
        if not commits:
            sleep(1)
            continue
        for i in range(len(commits)-1,0):
            commits[i]()
            commits.pop()
            print("Commited")
        
if __name__ == "__main__":
    running = True
    doCommitsT = Thread(target=app.run)
    doCommitsT.start()
    run()