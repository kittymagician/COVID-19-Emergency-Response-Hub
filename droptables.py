import sqlite3
conn = sqlite3.connect('hubapp.sqlite')
c = conn.cursor()
c.execute('''DROP TABLE smsreport''')
c.execute('''DROP TABLE webreport''')
c.execute('''DROP TABLE phonereport''')
conn.commit()
conn.close()
