import requests
import concurrent.futures
import datetime
from datetime import timezone

class RedditSearch:
	def __init__(self):
		print()
		print("       .   ")
		print("      /    ")
		print("  ( '_' )   ")
		print()


	def AsyncSearchOn(self,query,start_date):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(self.SearchOn,query,start_date) 
			return future.result()

	def SearchOn(self,query,start_date):
		result = []
		params = {"q" : query, "after": self.getEpochFrom(start_date)}
		resp = requests.get("https://api.pushshift.io/reddit/search/comment/", params = params)
		print()
		print()
		print(resp)
		print()
		print()

		result = self.getUserFormat(resp.json()["data"])
		return result

	def getUserFormat(self,items):
		result = []
		for i in items:
			user = {"from_id" : i["author"], "content" : i["body"], "name" : i["author"], "date" : i["created_utc"], "type" : "Reddit"}
			result.append(user)
		return result

	def getEpochFrom(self,start_date):
		d = (int(datetime.datetime.now().replace(tzinfo=timezone.utc).timestamp()) - start_date) // 86400
		return str(int(d)) + "d"



