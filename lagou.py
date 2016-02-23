# encoding: utf-8

"""
抓取拉勾网上的招聘信息
将数据存储到mongo中
Todo：
1. IP代理
2. 模拟登录
3 各种进阶的对付反爬虫的应对技能
"""

import urllib2
import urllib
import json
from datetime import datetime
from pymongo import MongoClient
import pdb


job_list = []
Mongo_Conn = MongoClient('localhost', 27017)
url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city='    
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) \
	Version/8.0 Mobile/12A4345d Safari/600.1.4'}


keyWords = raw_input('请输入搜索关键字：')      #有待改进，根据不同的输入情况，观察是否需要做改动
city = raw_input('请输入城市名：') 

for pageNum in range(1, 2):
	postdata = urllib.urlencode(
						{'pn':pageNum, 'kd':keyWords})
	request = urllib2.Request(url=url+city, data = postdata, headers = headers)
	
	response = urllib2.urlopen(request).read()
	json_obj = json.loads(response)
	job_list.extend(json_obj['content']['result'])
pdb.set_trace()
for k, v in job_list[0]:
	print k, v



def save(data):
	data['_id'] = data['positionId']
	data['updateTime'] = datetime.now()
	collection_name = raw_input('请输入集合名：')
	Mongo_Conn['jobinfo'][collection_name].update_one(
		filter={'_id': data['_id']},
		update={'$set': data}, 
		upsert=True
		)

def save_to_db():
	for index, data in enumerate(job_list):
		save(data)
		print '存储第{0}条数据'.format(index)
	print '存储完成'

# if __name__ == '__main__':
# 	save_to_db
	


