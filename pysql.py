import sqlite3
from datetime import datetime, date

now = datetime.now()
today = date.today()
d2 = today.strftime(" %B %d, %Y")
current_time = now.strftime("%H:%M:%S")
current_time += d2
print("time:", current_time)

db_connection = sqlite3.connect("dss.db")
db_cursor = db_connection.cursor()

username='admin'
password='12345678'
print(username)
# db_cursor.execute("INSERT INTO users VALUES(?,?,?,?,?)",(username,password,current_time,current_time,1))
# db_connection.commit()
#
db_cursor.execute("SELECT password FROM users WHERE username=?",(username,))
passw = db_cursor.fetchone()
print(passw[0])
#
# db_cursor.execute("UPDATE users SET password=?, last_login=? WHERE username=?",('123',current_time,'admin'))

db_connection.close()
