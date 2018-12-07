import sqlite3
conn = sqlite3.connect('celebrities.db')
cursor = conn.cursor()
sql = '''delete from celebs where id=3'''
cursor.execute(sql)
conn.commit()
conn.close()