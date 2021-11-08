import requests
from datetime import datetime, timezone
import concurrent.futures


class AllSearcher:
	def __init__(self,app):
		print()
		print("  ||\\\\    ||      ")
		print("  || \\\\   ||      ")
		print("  ||  \\\\  ||      ")
		print("  ||   \\\\ ||  ")
		print("  ||    \\\\||   ")
		print()


		self.api_keys =['53b3c0494d554305b8d247c27b38efa7']#app.config["NEWS_KEYS"]
	
	def AsyncSearchOn(self,query,start_date):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(self.SearchOn,query,start_date) 
			return future.result()

	def SearchOn(self,query,start_date):
		result = []
		params = {"q":query, "from":start_date,"sortBy":"publishedAt","county":"ru","apiKey":self.api_keys[0]}
		data = requests.get("http://newsapi.org/v2/everything", params = params)
		result.extend(self.getUserFormat(data.json()["articles"]))


		return result
#53b3c0494d554305b8d247c27b38efa7
	def getUserFormat(self, items):
		result = []
		for t in items:
			user = {"name":t["author"],"avatar":t["urlToImage"],"title":t["title"],"date": int(self.timeStampFrom(t["publishedAt"])), "content": t["content"],"type" : "All","url":t["url"]}
			result.append(user)
		return result

	def timeStampFrom(self,date):
		return datetime.strptime(date,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()

