import sqlite3
conn = sqlite3.connect('hubapp.sqlite')
c = conn.cursor()
c.execute('''DROP TABLE smsreport''')
c.execute('''DROP TABLE webreport''')
conn.commit()
conn.close()