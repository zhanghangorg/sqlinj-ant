#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
	通过一个url搜集同域下全部非静态资源并上报到redis
'''
import re
import sys
import urllib
import urlparse
import requests

#判断url是否同域
def samedomain(domain, urls):
	rs = set()
	for url in urls:
		req = urlparse.urlparse(url)
		if ("http" == req[0] or "https" == req[0]) and req[1] == domain: 
			rs.add(url)
		elif len(req[0]) == 0:
			path = req[2]
			if path[0] != '/':
				path = '/' + path
			if len(req[4])>0:
				path = path + "?" + req[4]
				print path
			rs.add("http://" + domain + path)
	return rs

#通过页面代码提取
def queryUrl(domain, code):
	#return re.findall('<a.*?href="?((\w|\.|:|\/|\?|=|&)*)"?.*</a>', code, re.I)
	return re.findall("<a.*?href=\"([\w\.\:\/\?\=\&%]+)\"", code, re.I)


def crossfire(url):
	req = urlparse.urlparse(url)
	domain = req[1]
	code = requests.get(url).text
	allurl = queryUrl(domain, code)
	return samedomain(domain, allurl)

def main():
	if len(sys.argv) < 2:
		print "缺少参数： python %s http://hostname" % sys.argv[0]
		exit()
	url = sys.argv[1]
	level = 3

	urls = crossfire(url)
	for url in urls:
		print url
		urls = urls | crossfire(url)
	print urls

if __name__ == '__main__':
	main()