import sqlite3
import os

try: 
    os.remove("Resources\\Data\\ip.db")
except FileNotFoundError:
    pass

conn = sqlite3.connect("Resources\\Data\\ip.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS allowed_ips (ip TEXT PRIMARY KEY)''')
cur.execute('''CREATE TABLE IF NOT EXISTS blocked_ips (ip TEXT PRIMARY KEY)''')
conn.commit()

conn.close()