#encoding: utf-8
import scrapy
import re
import sys, os
#sys.setdefaultencoding("utf-8")
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.http import Request
from third.items import ThirdItem
import json
#import js2py
import time
i=1
base="C:/lyr/Data/tech/"
class techSpider(Spider):
	name='tech'
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
	}
	allowed_domains=['tech.sina.com.cn']	
	start_urls=[]
	for page in range(1,2000):
		urls = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page="+str(page)+"&r=0.7643548077821145&callback=&_=1542094996079"
		start_urls.append(urls)
	def parse(self,response):
		items=[]
		item=ThirdItem()
		datas=json.loads(response.body)
		newsList=datas['result']['data']
		#print('Data:',datas['result']['data'])
		dataLen=len(datas['result']['data'])
		
		for idx in range(dataLen):
			print("Next:",newsList[idx]["url"])
			yield Request(url=newsList[idx]["url"], headers=self.headers,callback=self.second_parse)

	def second_parse(self,response):
		head = response.xpath(u'//h1[@id="main_title"]/text()').extract()
		content = ""
		content_list=response.xpath(u'//div[@id="artibody"]/p/text()').extract()
		for content_one in content_list:
			content_one=content_one.replace('\xa0','').replace('\u3000','')
			content+=content_one
		item=ThirdItem()
		item['news_body']=content
		item['news_title']=head
		global i
		dir=base + "tech_"+ str(i) + ".txt"
		print(dir)
		i = i + 1
		fp = open(dir , 'w')
		fp.write(item['news_body'])
		fp.close()
		yield item
