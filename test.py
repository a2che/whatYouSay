import sqlite3

con = sqlite3.connect("testss.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS test(a int UNIQUE, b text, c text)")

con.commit()

cur.execute("INSERT INTO test(a,b,c) VALUES(1,'2','3')")

con.commit()


cur.execute("SELECT * FROM test")
print(cur.fetchall())

cur.execute("INSERT INTO test(a,b,c) VALUES(1,'3','4') ON CONFLICT(a) DO UPDATE SET b = '3', c = '4'")
con.commit()

cur.execute("SELECT * FROM test")
print(cur.fetchall())