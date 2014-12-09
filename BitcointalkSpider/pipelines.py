# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from BitcointalkSpider.items import User, Post, Thread
import time
from BitcointalkSpider.settings import SPIDER_WORK_DIR
import os


class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
	def __init__(self):
		pass
	def process_item(self, item, spider):
		if  item.__class__ == User:
		#time format 
		#time.strptime(str, "%B %d, %Y, %H:%M:%S %p")
			rtimelen = len(item["registerDate"])
			localtime = time.localtime()
			try:
				if rtimelen == 1:
					usertime = time.strptime(item["registerDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
				elif rtimelen == 2:
					usertime = localtime
				else:
					usertime = time.struct_time([0 for i in range(9)])
			except:
				usertime = time.struct_time([0 for i in range(9)])
			userpath = os.path.join(SPIDER_WORK_DIR, "User", str(usertime.tm_year) + str(usertime.tm_mon))
			if os.path.exists(userpath):
				pass
			else:
				os.makedirs(userpath)
			try:
				eachuserfile = os.path.join(userpath, item["name"][0].__str__())
			except:
				eachuserfile = os.path.join(userpath, "NONENAME")
			userfile = codecs.open(eachuserfile, "ab", encoding = "utf-8")
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			userfile.write(line)
			userfile.close()

		if item.__class__ == Thread:
			'''	sort by time
			try:
				time = item["time"][0].__str__()
			else:

			localtime = time.localtime()
			if time.find("at") == -1:
				usertime = time.strptime(time, "%B %d, %Y, %I:%M:%S %p")
			else:
				usertime  = localtime	#aboutly equal, but lastest they date is equal, this is enough
			'''
			Thread_work_dir = os.path.join(SPIDER_WORK_DIR, "Thread")
			if item["ofBoard"] != []:
				#print item["ofBoard"]
				Threadpath = reduce(os.path.join, map(lambda x: unicode.encode(x, "utf-8"), item["ofBoard"]), Thread_work_dir)
				#print Threadpath
			else:
				Threadpath = os.path.join(Thread_work_dir, "NONEBOARD")
			if os.path.exists(Threadpath):
				pass
			else:
				os.makedirs(Threadpath)
			eachThreadfile = os.path.join(Threadpath, item["url"].split("=")[1].__str__())
			Threadfile = codecs.open(eachThreadfile, "ab", encoding = "utf-8")
			#There we can add some \n to make it comfortable for people to read
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			Threadfile.write(line)
			Threadfile.close()

		return item

	def spider_closed(self, spider):
		pass


'''
some standard datas

{"name": ["Uri"], 
"gender": [], 
"age": ["N/A"], 
"posts": ["1"], 
"lastData": ["August 10, 2014, 03:50:08 PM"], 
"activity": ["1"], 
"bitcoinAddress": [], 
"position": ["Newbie"], 
"Email": ["hidden"]},
{"content": [{"topic": ["\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"content": ["\u05e9\u05dc\u05d5\u05dd \u05dc\u05db\u05d5\u05dc\u05dd,", "\u05de\u05d9\u05e9\u05d4\u05d5 \u05de\u05db\u05d9\u05e8 \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05d8\u05d5\u05d1\u05d9\u05dd \u05d1\u05e8\u05e9\u05ea \u05e9\u05d0\u05e4\u05e9\u05e8 \u05dc\u05d4\u05e8\u05d5\u05d5\u05d9\u05d7 \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df?"], 
"user": ["johnatan32"], 
"time": ["May 11, 2014, 04:32:14 PM"]}, {"topic": ["Re: \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"content": ["\u05d4\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05d4\u05dd \u05e2\u05e4\"\u05e8 (\u05db\u05de\u05d5) \u05d4\u05d9\u05de\u05d5\u05e8\u05d9\u05dd - \u05dc\u05d0 \u05de\u05db\u05d9\u05e8 \u05d0\u05e3 \u05d0\u05d7\u05d3 \u05de\u05d4\u05dd... "], 
"user": ["r1973"], 
"time": ["May 11, 2014, 07:40:39 PM"]}], 
"ofBoard": ["Bitcoin Forum", "Local", "\u05e2\u05d1\u05e8\u05d9\u05ea (Hebrew)", "\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"url": "https://bitcointalk.org/index.php?topic=604954.0", "topic": " \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df \u00a0(Read 323 times)\n\t\t\t\t", "user": ["johnatan32"], 
"time": ["May 11, 2014, 04:32:14 PM"]},

'''
