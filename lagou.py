# encoding: utf-8

import urllib2
import urllib
import json
# import pdb

url = 'http://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC'
headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) \
	Version/8.0 Mobile/12A4345d Safari/600.1.4'}
postdata = urllib.urlencode(
	{'pn':2, 'kd':'Python'})

request = urllib2.Request(url=url, data = postdata, headers = headers)
response = urllib2.urlopen(request).read()

json_obj = json.loads(response)


for data in json_obj['content']['result']:
	for k, v in data.items():
		print k, v
		
	print '*'*75

	




