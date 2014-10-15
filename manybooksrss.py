import requests
import xmltodict
import json
from pymongo import MongoClient
import time

res=requests.get('http://manybooks.net/index.xml')

#Always encode XML to skip most of unicode errors

db = MongoClient('localhost')['manybooks']

encoded_xml = res.text.encode('utf-8')

od = xmltodict.parse(encoded_xml)

myjson = json.loads(json.dumps(od))

today = time.strftime('%y-%m-%d',time.gmtime())

if today not in db.collection_names():
	for item in myjson['rss']['channel']['item']:
		db[today].insert(item)
else:
	print 'already up to date'
