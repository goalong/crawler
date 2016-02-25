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
# import pdb

Mongo_Conn = MongoClient('localhost', 27017)
url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city='    
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) \
	Version/8.0 Mobile/12A4345d Safari/600.1.4'}

class Lagou():
	def __init__(self):
		self.job_list = []

	def start(self):
		self.keyWords = raw_input('请输入搜索关键字：')      #有待改进，根据不同的输入情况，观察是否需要做改动
		self.city = raw_input('请输入城市名：')
		self.job_list = self.getJobs() 
		self.save_to_db()


	def getJobs(self):
		for pageNum in range(1, 2):
			postdata = urllib.urlencode(
								{'pn':pageNum, 'kd':self.keyWords})
			request = urllib2.Request(url=url+self.city, data = postdata, headers = headers)
			
			response = urllib2.urlopen(request).read()
			json_obj = json.loads(response)
			self.job_list.extend(json_obj['content']['result'])
		return self.job_list

	def save_to_db(self):
		collection_name = raw_input('请输入集合名：')
		for index, data in enumerate(self.job_list):
			save(data, collection_name)
			print '存储第{0}条数据'.format(index)
		print '存储完成'


def save(data, collection_name):
		data['_id'] = data['positionId']
		data['updateTime'] = datetime.now()
		
		Mongo_Conn['jobinfo'][collection_name].update_one(
			filter={'_id': data['_id']},
			update={'$set': data}, 
			upsert=True
			)

if __name__ == '__main__':
	lagou = Lagou()
	lagou.start()

	


