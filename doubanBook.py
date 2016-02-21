# coding=utf-8
import string
import re
import urllib2


class DoubanSpider(object):
	def __init__(self):
		self.pageNum = 1
		self.cur_url = "http://book.douban.com/top250?start={pageNum}&filter=&type="
		self.datas = []
		self._top_num = 1
		print "豆瓣图书Top250爬虫准备爬取数据。。。"
	def get_page(self, cur_page):
		url = self.cur_url
		try:
			html = urllib2.urlopen(url.format(pageNum=(cur_page-1)*25)).read().decode('utf-8')
		except urllib2.URLError, e:
			if hasattr(e, "code"):
				print "Error code: %s" % e.code
			elif hasattr(e, 'reason'):
				print "Reason: %s" % e.reason
		return html

	def find_title(self, html):
		temp_data = []
		book_items = re.findall(r'<div class="pl2">.*?title=(.*?)>', html, re.S)


		for index, item in enumerate(book_items):
			if item.find("&nbsp") == -1:
				temp_data.append("Top" + str(self._top_num) + " " + item)
				self._top_num += 1
		self.datas.extend(temp_data)

	def start_spider(self):
		while self.pageNum <= 10:
			html = self.get_page(self.pageNum)
			
			self.find_title(html)
			self.pageNum += 1
def main():
	print "豆瓣图书爬虫"
	my_spider = DoubanSpider()
	my_spider.start_spider()
	for item in my_spider.datas:
		print item
	print "over"

if __name__ == '__main__':
	main()