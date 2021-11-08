import requests as r
import concurrent.futures
from datetime import datetime
from datetime import timezone

class VKsearch:
 	def __init__(self,app,DB,themeId):
 		self.appKeys = ["69cd545569cd545569cd54552669bf11d5669cd69cd5455371d6e16e7a65c6ddb4406d3"]
 		#self.querySettings = app.config["QUERY_SETTINGS"]
 		print()
 		print("   \\    // || //")
 		print("    \\  //  |||  ")
 		print("     \\//   || \\")
 		print()
 		self.DB = DB
 		self.themeId = themeId


 	def AsyncSearchOn(self,query,start_date):
 		with concurrent.futures.ThreadPoolExecutor() as executor:
		    future = executor.submit(self.SearchOn,query,start_date) 
		    return future.result()

 	def SearchOn(self,query,start_date):
 		print("-------------------------")
 		print(start_date)
 		print("-------------------------")
 		result = []
 		dates = self.drobTime(start_date) 
 		for d in range(1,len(dates)):
 			params = {"access_token": self.appKeys[0], "q": query, "extended": 1, "start_time" : dates[d],"end_time":dates[d-1], "v": "5.107", "count": "200"}

 			num = 0
	 		while True:
	 			try:
		 			response = r.get("https://api.vk.com/method/newsfeed.search", params = params)
		 			uss = self.getUserFormat(response.json()["response"])

		 			num+= len(uss) 
		 			result.extend(uss)
		 			params["start_from"] = response.json()["response"]["next_from"]

		 		except Exception as e:
		 			print(e)
		 			self.setStatistic(dates[d],num)
		 			break
	 	return result
#53b3c0494d554305b8d247c27b38efa7
 	def getUserFormat(self, response):
 		items = response["items"]
 		groups = response["groups"]
 		profiles = response["profiles"]
 		result = []
 		for t in items:
 			user = {"id": t["id"],"owner_id": t["owner_id"], "from_id": t["from_id"],"date": t["date"], "content": t["text"],"type" : "Vk"}
 			try:
 				data = self.getInfo(t["from_id"],profiles)
 				user["name"] = data["first_name"] + " " + data["last_name"]
 				user["avatar"] =  data["photo_50"]
 				user["screen_name"] = data["screen_name"]
 			except Exception as e:
 				try:
	 				data = self.getInfo(t["from_id"],groups)
	 				user["name"] = data["name"]
	 				user["avatar"] =  data["photo_50"]
	 				user["screen_name"] = data["screen_name"]
	 			except Exception:
	 				continue
 			result.append(user)
 		print("END DAY BEACH")
 		print(datetime.utcfromtimestamp(result[0]["date"]).strftime('%Y-%m-%d %H:%M:%S'))
 		print("START DATE BEACH")
 		print(datetime.utcfromtimestamp(result[len(result) - 1]["date"]).strftime('%Y-%m-%d %H:%M:%S'))


 		return result

 	def getInfo(self, id, data):
 		for d in data:
 			if str(d["id"]) == str(id):
 				return d
 		raise Exception("This id non exists")

 	def drobTime(self,date):
 		now = datetime.now()
 		predNow = (int(now.replace(tzinfo=timezone.utc).timestamp()) + 86400) - ((now.hour * 3600) + (now.minute * 60) + now.second)
 		dates = [predNow]
 		while True:
 			predNow-=86400
 			if predNow > date:
 				dates.append(predNow)
 			else:
 				dates.append(date)
 				break
 		return dates

 	def setStatistic(self,date,num):
 		self.DB.insertComand("INSERT INTO Statistic(themeId,date,source,num) VALUES({0},{1},'Vk',{2}) ON CONFLICT(themeId,source,date) DO UPDATE SET num = {2}".format(self.themeId,date,num)) 



