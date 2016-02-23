# encoding: utf-8

"""
Todo:
将数据存储到mongo中
"""

import urllib2
import urllib
import json
from datetime import datetime
from pymongo import MongoClient


job_list = []
Mongo_Conn = MongoClient('localhost', 27017)
url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC'
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) \
	Version/8.0 Mobile/12A4345d Safari/600.1.4'}



for pageNum in range(1, 36):
	postdata = urllib.urlencode(
						{'pn':pageNum, 'kd':'Python'})
	request = urllib2.Request(url=url, data = postdata, headers = headers)
	response = urllib2.urlopen(request).read()
	json_obj = json.loads(response)
	job_list.extend(json_obj['content']['result'])



def save(data):
	data['_id'] = data['positionId']
	data['updateTime'] = datetime.now()

	Mongo_Conn['jobinfo']['lagou'].update_one(
		filter={'_id': data['_id']},
		update={'$set': data}, 
		upsert=True
		)

for index, data in enumerate(job_list):
	save(data)
	print '存储第{0}条数据'.format(index)

print '存储完成'
	


