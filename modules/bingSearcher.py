import requests
from XMLConvertor import ElementTree, XmlDictConfig,XmlListConfig
for i in range(1000):
	f = requests.get("https://news.google.com/rss/search?q=covid-19&hl=ru&gl=RU&ceid=RU:ru")

print(f.text)
root = ElementTree.XML(f.text)
xmldict = XmlListConfig(root)
print(xmldict)