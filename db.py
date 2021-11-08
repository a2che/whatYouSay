import sqlite3



class EasySql:
	"""docstring for EasySql"""
	def __init__(self):
		self.db = "what.db"
		conn = sqlite3.connect(self.db)
		cursor = conn.cursor()

		cursor.execute("CREATE TABLE IF NOT EXISTS User(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,login char(30) NOT NULL, mail char(30) NOT NULL, password char(50) NOT NULL)")
		cursor.execute("CREATE TABLE IF NOT EXISTS TimeUser(secretKey char(8) PRIMARY KEY NOT NULL,login char(30) NOT NULL, mail char(30) NOT NULL, password char(50) NOT NULL)")
		cursor.execute("CREATE TABLE IF NOT EXISTS Theme(themeId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, userId INTEGER NOT NULL, name char(50))")
		cursor.execute("CREATE TABLE IF NOT EXISTS Words(themeId INTEGER NOT NULL, word char(150))")
		cursor.execute("CREATE TABLE IF NOT EXISTS Statistic(themeId INTEGER NOT NULL, source char(30) NOT NULL,num INTEGER, date INTEGER NOT NULL, UNIQUE(themeId,source,date))")
		cursor.execute("CREATE TABLE IF NOT EXISTS PasswordsKeys(key INTEGER,id INTEGER)")

		conn.commit()

	def getComand(self,sql):
		with sqlite3.connect(self.db) as conn:
			cursor = conn.cursor()
			cursor.execute(sql)
			return cursor.fetchall()
	def insertComand(self,sql):
		with sqlite3.connect(self.db) as conn:
			cursor = conn.cursor()
			cursor.execute(sql)
			conn.commit()
