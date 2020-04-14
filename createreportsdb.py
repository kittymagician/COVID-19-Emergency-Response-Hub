import sqlite3
conn = sqlite3.connect('hubapp.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE smsreport
             (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, telephone number text, category text, message text, status text)''')
c.execute('''CREATE TABLE webreport
             (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, telephone number text, category text, message text, status text)''')
conn.commit()
conn.close()