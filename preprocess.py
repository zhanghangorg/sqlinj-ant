#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
	原始http请求信息以Hash形式保存在redis，hash格式不利于随机取一个http请求
	用此脚本将db0中http请求转移至db1，并以set形式保存
'''

import json
import redis
import sys
import param

def queryKey(key):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbOld)
	return r.keys(key)

def queryHashFields(key):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbOld)
	return r.hkeys(key)

def queryHashValue(key, filed):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbOld)
	return r.hget(key, filed)

def setAdd(key, value):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbNew)
	r.sadd(key, value)

def main():
	if len(sys.argv) < 2:
		print "缺少参数： python %s hostname" % sys.argv[0]
		exit()
	hostname = sys.argv[1]
	print hostname
	keys = queryKey(hostname)
	for key in keys:
		print key
		fileds = queryHashFields(key)
		total = len(fileds)
		times = 0
		print "共计%d个请求记录" % total
		for filed in fileds:
			times = times + 1
			req = queryHashValue(key, filed)
			setAdd(param.joblist, req)
			if times*10%total == 0:
				print str(times*100.0/total) + "%"
	print "finish..."

if __name__ == '__main__':
	main()
