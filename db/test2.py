import sqlite3
conn = sqlite3.connect('members.db',check_same_thread=False)
cur = conn.cursor()
cur.execute("""SELECT Interest FROM interests WHERE ID IN (?)""",(1,3))
print(cur.fetchall())