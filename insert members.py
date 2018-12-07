import sqlite3

conn = sqlite3.connect("celebrities.db")
cursor = conn.cursor()

sql = "insert into members values(?,?,?,?,?,?)"
data = ((1, "Joe", "Siler", 22, "silerja@dukes.jmu.edu", "I currently go to James Madison University", "silerja", "silerja"), (2, "Alex", "Martin", 22, "marti6ar@dukes.jmu.edu", "I currently go to James Madison University", "marti6ar", "marti6ar"))

cursor.executemany(sql,data)
conn.commit()
conn.close()