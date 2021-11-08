import requests
import concurrent.futures
import datetime
from datetime import timezone

class FlickerSearch:
	def __init__(self):
		pass

	def AsyncSearchOn(self,query,start_date):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.submit(self.SearchOn,query,start_date) 
			return future.result()   

	def SearchOn(self,query,start_date):
		result = []
		params = {"method":"flickr.photos.search","text" : query, "min_upload_date": start_date,"api_key":"f9ae7acc8ef59be2f60304f0950c5eb5","format":"json","nojsoncallback":"1"}
		page = 1
		while True:
				resp = requests.get(" https://www.flickr.com/services/rest/?", params = params)

				result = self.getUserFormat(resp.json()["photos"]["photo"])

				if page >= int(resp.json()["photos"]["pages"]):
					break
				page+=1
		return result

	def getUserFormat(self,items):
		result = []
		for i in items:
			user = {"title" : i["title"], "content" : "https://farm{0}.staticflickr.com/{1}/{2}_{3}.jpg".format(i["farm"],i["server"],i["id"],i["secret"])}
			result.append(user)
		return user


print(FlickerSearch().AsyncSearchOn("Ким",1591279672))