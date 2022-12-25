import sqlite3

class Db:
    def __init__(self):
        self.conn = sqlite3.connect('test.db',check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create()
        
    def create(self):
        try:
            self.cur.execute("CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,Name NVARCHAR(20) NOT NULL)")
        except:
            pass
        
    def insert(self):
        self.cur.execute("INSERT INTO users (Name) VALUES ('myName')")
        return self.conn.commit()
    
    def query(self):
        self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()