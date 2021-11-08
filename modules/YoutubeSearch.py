import requests
import concurrent.futures
import datetime
from datetime import timezone

class YouTubeSearch:
	NUM_TOKEN = 0
	def __init__(self, app): #app
		self.app_token =  app.config["YOUTUBE_TOKEN"]
		print("|    ___   |")
		print("|   | > |  |")
		print("|    ¯¯¯   |")

	def AsyncSearchOn(self,query,start_date):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(self.SearchOn,query,start_date) 
			return future.result()

	def SearchOn(self, query, start_date):

		print(f"{start_date}")
		result = []
		params = {
                    'q': query,
                    'part': 'id,snippet',
                    'maxResults': 1000,
                    'regionCode': 'RU',
                    "order":"date",
                    'key': self.app_token[self.NUM_TOKEN]
                }
		while True:
			r = requests.get("https://www.googleapis.com/youtube/v3/search?", params = params)
			try:
				result.extend(self.getUserFormat(r.json()["items"],start_date))
			except Exception:
				try:
					self.NUM_TOKEN +=1
					params["key"] = self.app_token[self.NUM_TOKEN]
					print(self.NUM_TOKEN)
					continue
				except:
					return []
			try:
				params["pageToken"] = r.json()["nextPageToken"]
			except Exception:
				break
			if result[len(result) - 1]["date"] <= start_date:
				break
		return result

	def getUserFormat(self, items,start_date):
		result = []
		for t in items:
			try:
				user = {"from_id" : t["id"]["videoId"],
						"owner_id": t["snippet"]["channelId"], 
						"name" : t["snippet"]["channelTitle"], 
						"content": t["snippet"]["description"], 
						"title": t["snippet"]["title"], 
						"avatar": t["snippet"]["thumbnails"]["default"]["url"],
						"date": self.timeStampFrom(t["snippet"]["publishedAt"]),
						"type" : "Youtube"}
			except Exception:
				continue
			if user["date"] >= start_date:
				result.append(user)
		return result

	def timeStampFrom(self,date):
		return datetime.datetime.strptime(str(date),"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()





