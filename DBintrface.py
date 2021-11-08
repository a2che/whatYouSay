import sqlite3
conn = sqlite3.connect("what.db")

cur = conn.cursor()


def insert():
	com = input()
	cur.execute(com)
	conn.commit()

def insertS(com):
	cur.execute(com)
	conn.commit()
def select():
	com = input()
	cur.execute(com)
	for r in cur.fetchall():
		row = ""
		for c in r:
			row += str(c)+"|"
		print(row)

def selectS(com):
	cur.execute(com)
	for r in cur.fetchall():
		row = ""
		for c in r:
			row += str(c)+"|"
		print(row)

while True:
	print("CHOOSE METHOD insert - 1, select - 2")
	c = input()
	if c == "1":
		insert()
	elif c == "2":
		select()
	elif c == "3":
		insertS("DELETE FROM Statistic")
		insertS("INSERT INTO Statistic(themeId,source,num,date) VALUES(59,'Vk',0,1594598400)")
		insertS("INSERT INTO Statistic(themeId,source,num,date) VALUES(59,'undefined',0,1594598400)")
		insertS("INSERT INTO Statistic(themeId,source,num,date) VALUES(59,'Youtube',0,1594598400)")
		insertS("INSERT INTO Statistic(themeId,source,num,date) VALUES(59,'All',0,1594598400)")
		selectS("SELECT * FROM Statistic")