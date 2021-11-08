import xlwt
from tempfile import TemporaryFile


from flask import Flask, session, redirect, jsonify, request, render_template, url_for, send_from_directory
from db import EasySql
from flask_mail import Mail, Message
from threading import Thread
import random
from itertools import groupby

from datetime import timedelta, datetime, timezone

import sys
sys.path.append("modules")
# coding: utf8

# Устанавливаем стандартную внешнюю кодировку = utf8


from VkSearcher import VKsearch
from YoutubeSearch import YouTubeSearch
from RedditSearher	import RedditSearch
from ALLMAZAFAKASearcher import AllSearcher

app = Flask(__name__)
app.config.from_object('config')

DB = EasySql()
mail = Mail(app)


def send_async_email(msg):
	with app.app_context():
		mail.send(msg)

def send_email(type,recipient, args = {}):
    msg = Message(app.config["MAIL_TYPES"][type]["SUBJECT"], sender = app.config["SENDERS"][0], recipients = [recipient])
    msg.html = render_template("mails/" + app.config["MAIL_TYPES"][type]["HTML"], args = args)
    thr = Thread(target = send_async_email, args = [msg])
    thr.start()

def keyGenerate():
	res = ''
	for i in range(app.config["KEY_SIZE"]):
		res += chr(random.randint(65,90))
	return res




def timeTo(time):
	normalTIme = datetime.fromtimestamp(time)
	return f'{normalTIme.day}:{normalTIme.month}'
def timeForAuthors(time):
	normalTIme = datetime.fromtimestamp(time)
	return f'{normalTIme.day}-{normalTIme.month}-{normalTIme.day} \n {normalTIme.hour}:{normalTIme.minute}'

def saveExel(data,themeId):
	book = xlwt.Workbook()
	sheet1 = book.add_sheet('VkUsers')
	sheet1.write(0,0,"Имя")
	sheet1.write(0,1,"Платформа")
	sheet1.write(0,2,"Дата")
	sheet1.write(0,3,"Ссылка")
	for c,u in enumerate(data):
		sheet1.write(c+1,0,u["name"])
		sheet1.write(c+1,1,u["type"])
		sheet1.write(c+1,2,timeForAuthors(int(u["date"])))
		sheet1.write(c+1,3,"https://vk.com/" + u["screen_name"])

	book.save(f"{app.config['AUTHORS_DIRECTORY']}/{themeId}.xls")
	book.save(TemporaryFile())

def returnStat(data):
	stat = {}
	dates = [x[0] for x in data]
	
	dates.sort()
	dates = [timeTo(y) for y in dates]
	dates = [el for el, _ in groupby(dates)]
	print(dates)
	for s in data:
		try:
			stat[s[1]]["Nums"][dates.index(timeTo(s[0]))] = s[2]
		except Exception:
			try:
				stat[s[1]] = {}
				stat[s[1]]["Nums"] = [0] * len(dates)
				stat[s[1]]["Nums"][dates.index(timeTo(s[0]))] = s[2]
			except Exception as e:
				print(e)
				continue
	for k in stat.keys():
		stat[k]["Title"] = app.config["GRAF_TYPEES"][k.lower()]["Title"]
		stat[k]["Color"] = app.config["GRAF_TYPEES"][k.lower()]["Color"]

	return {"dates":dates,"stat":stat}

def getOptimal(three,type, themeId):
	last = DB.getComand("SELECT date FROM Statistic WHERE source = '{}' AND themeId = {} ORDER BY date DESC LIMIT 1".format(type,themeId))[0][0]
	if three > last:
		return last
	else:
		return three

#print(returnStat(DB.getComand("SELECT date,source,num FROM Statistic WHERE themeId = {}".format(59))))
		

@app.route('/')
def index():
	if session.get("user") == None or session.get("user") == {}:
		return redirect("/face")
	else:
		data = DB.getComand("SELECT * FROM User WHERE login = '{}' AND password = '{}'".format(session["user"]["login"],session["user"]["password"]))
		if data == None or data == []:
			return redirect("/face")
	themes = DB.getComand("SELECT name, themeId FROM Theme WHERE userId = {}".format(session["user"]["id"]))
	print(themes)
	LS = returnStat(DB.getComand("SELECT date,source,num FROM Statistic WHERE themeId = {}".format(session["user"]["id"])))
	return render_template("what.html",themes = themes,stat = LS["stat"], lables = LS["dates"], login = session["user"]["login"])



@app.route('/face',methods = ["GET","POST"])
def face():
	if request.method == "POST":
		data = DB.getComand("SELECT id,login,password FROM User WHERE mail = '{0}' AND password = '{1}'".format(request.form["mail"],request.form["password"]))
		if data != None and data != []:
			session["user"] = {}
			session["user"]["id"] = data[0][0]
			session["user"]["login"] = data[0][1]
			session["user"]["password"] = data[0][2]
			return redirect("/")

	if session.get("user") == None or session.get("user") == {}:
		return render_template("face.html")
	else:
		data = DB.getComand("SELECT * FROM User WHERE login = '{}' AND password = '{}'".format(session["user"]["login"],session["user"]["password"]))
		if data != None:
			return redirect("/")
	return render_template("face.html")

@app.route("/logOut", methods = ["GET"])
def logOut():
	session["user"] = {}
	return redirect("/face")


@app.route('/addTheme', methods = ["POST"])
def addTheme():
	data = request.json

	DB.insertComand("INSERT INTO Theme(userId,name) VALUES({},'{}')".format(session["user"]["id"], data["ThemeName"]))
	themeId = DB.getComand("SELECT themeId FROM Theme WHERE userId = {} ORDER BY themeId DESC LIMIT 1".format(session["user"]["id"]))[0][0]
	for w in data["Words"]:
		DB.insertComand("INSERT INTO Words(themeId, word) VALUES({},'{}')".format(themeId,w))

	timeStart = int((datetime.now() - timedelta(7)).replace(tzinfo=timezone.utc).timestamp()) - (datetime.now().hour * 3600) - (datetime.now().minute * 60) - datetime.now().second  
	for p in app.config["PLATFORMS"]:
		DB.insertComand("INSERT INTO Statistic(themeId,date,source,num) VALUES({},{},'{}',0)".format(themeId,timeStart,p))	
	

	print(DB.getComand("SELECT name FROM Theme WHERE userId = {}".format(session["user"]["id"])))
	return jsonify({"themes": DB.getComand("SELECT name, themeId FROM Theme WHERE userId = {}".format(session["user"]["id"]))})


@app.route('/getTheme', methods = ["POST"])
def getTheme():
	words = DB.getComand("SELECT word FROM Words WHERE themeId = {}".format(request.form["id"]))

	print("|||||||||||||||||||||||||||||")
	print("|||||||||||||||||||||||||||||")
	print("search by "+ str(request.form["id"]))
	print("|||||||||||||||||||||||||||||")
	print("|||||||||||||||||||||||||||||")

	#AIzaSyDhxz2Q6xqtoY8f-WNzf6UnCwkm-oP837Y
	dates = {}
	result = []
	errors = ""
	timeStart = int((datetime.now() - timedelta(3)).replace(tzinfo=timezone.utc).timestamp()) - (datetime.now().hour * 3600) - (datetime.now().minute * 60) - datetime.now().second  
	for w in words:
		result.extend(VKsearch(app,DB,request.form["id"]).AsyncSearchOn(w[0], getOptimal(timeStart,"Vk",request.form["id"])))
		saveExel(result,str(request.form["id"]))
		try:
			result.extend(YouTubeSearch(app).AsyncSearchOn(w[0],getOptimal(timeStart,"Youtube",request.form["id"])))
		except Exception:
			errors = "Возможно некоторые платформы будут не доступны по техническим причинам"
		result.extend(RedditSearch().AsyncSearchOn(w[0], getOptimal(timeStart,"Reddit",request.form["id"])))
		result.extend(AllSearcher(app).AsyncSearchOn(w[0], getOptimal(timeStart,"All",request.form["id"])))
	print("!!! EXELENT !!!")
	print("!!! EXELENT !!!")
	print("!!! EXELENT !!!")

	return jsonify({'results' : result,"errors":errors})

@app.route("/checkMail", methods = ["POST"])
def checkMail():
	if DB.getComand("SELECT * FROM User WHERE mail = '{}'".format(request.form["mail"])) == []:
		return "yes"
	return "no"

@app.route('/registration', methods = ["POST"])
def registration():
	key = keyGenerate()
	DB.insertComand("INSERT INTO TimeUser(secretKey, login, mail,password) VALUES('{}','{}','{}','{}')".format(key,request.form["login"],request.form["mail"],request.form["password"]))
	
	send_email("SECRET_CODE",request.form["mail"], {"name": request.form["login"], "key":key})

	return "<html>ПИСЬМООООо</html>"

@app.route('/secret/<key>', methods = ["GET"])
def keyCheck(key):
	data = DB.getComand("SELECT * FROM TimeUser WHERE secretKey = '{}'".format(key))
	if data != None:
		DB.insertComand("INSERT INTO User(login,password,mail) VALUES('{}','{}','{}')".format(data[0][1],data[0][3],data[0][2]))
		DB.insertComand("DELETE FROM TimeUser WHERE secretKey = '{}'".format(key))
		session["user"] = {}
		session["user"]["login"] = data[0][1]
		session["user"]["password"] = data[0][3]
		session["user"]["id"] = DB.getComand("SELECT id FROM User WHERE mail = '{}' AND password = '{}'".format(data[0][2],data[0][3]))[0][0]
		return render_template("confirm.html")

@app.route("/setStaticstic", methods = ["POST"])
def setStat():
	data = request.json["nums"]
	print(data)
	themeId = request.json["id"]
	print(themeId)
	for d in data.keys():
		if d == "Vk":
			continue
		for t in data[d]:
			DB.insertComand("INSERT INTO Statistic(themeId,date,source,num) VALUES({0},{1},'{2}',{3}) ON CONFLICT(themeId,source,date) DO UPDATE SET num = {3}".format(themeId,d,t,data[d][t])) 
	LS = returnStat(DB.getComand("SELECT date,source,num FROM Statistic WHERE themeId = {}".format(themeId)))
	diagrammNums = []
	diagrammLabels = []
	diagrammColors = []
	dd = DB.getComand("SELECT SUM(num), source FROM Statistic WHERE themeId = {} GROUP BY source".format(themeId))
	for dia in dd:
		diagrammLabels.append(app.config["GRAF_TYPEES"][dia[1].lower()]["Title"])
		diagrammColors.append(app.config["GRAF_TYPEES"][dia[1].lower()]["Color"])
		diagrammNums.append(dia[0]) 

	return jsonify({"stat" : LS["stat"], "lables" : LS["dates"],"diaL":diagrammLabels,"diaN":diagrammNums,"diaC":diagrammColors})

@app.route("/download/<themeId>",methods = ["GET"])
def download(themeId):
	print("LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOL")
	return send_from_directory(directory = app.config["AUTHORS_DIRECTORY"],filename = themeId + ".xls")

@app.route("/getStaticstic", methods = ["POST"])
def getStat():
	stat = DB.getComand("SELECT date,source,num FROM Statistic WHERE themeId = {}".format(request.form["id"]))

	return "FF" 

@app.route("/recoveryPassword", methods = ["POST"])
def recoveryPassword():
	id = DB.getComand("SELECT id FROM User WHERE mail = '{}'".format(request.form["mail"]))
	if id != []:
		while True:
			key = keyGenerate()
			if DB.getComand("SELECT * FROM PasswordsKeys WHERE key = '{}'".format(key)) != []:
				continue
			DB.insertComand("INSERT INTO PasswordsKeys(key,id) VALUES('{}',{})".format(key,id[0][0]))
			break
		send_email("HILL_PASSWORD",request.form["mail"],{"key": key})
		return "ok"
	return "BAD"

@app.route("/changePassword/<key>", methods=["GET","POST"])
def changePassword(key):
	id = DB.getComand("SELECT id FROM PasswordsKeys WHERE key = '{}'".format(key))
	if request.method == "POST":
		DB.insertComand("UPDATE User SET password = '{}' WHERE id = {}".format(request.form["password"],id[0][0]))
		DB.insertComand("DELETE FROM PasswordsKeys WHERE key = '{}'".format(key))
		return redirect("/")
	if id != []:
		return render_template("changePassword.html", key = key)


if __name__ == '__main__':
	app.run()



