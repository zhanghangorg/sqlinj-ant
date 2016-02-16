#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
	从redis取http请求详情，调用autoinj.py进行注入测试,并将注入结果插入到redis中
	使用前请首先确保redis db1中proxy.set 有数据
	by zhangh (zhanghang.org#gmail.com)
'''
import sys
import json
import time
import redis
import autoinj
import param


def insertHash(key, filed, value):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbNew)
	r.hset(key, filed, value)

def randomOne(setKey):
	r = redis.StrictRedis(host=param.host, port=param.port, password=param.password, db=param.dbNew)
	return r.spop(setKey)

def main():
	if len(sys.argv) < 2:
		print "缺少参数： python %s http://10.0.0.1:8775" % sys.argv[0]
		exit()
	server = sys.argv[1]
	while True:
		try:
			req = randomOne(param.joblist)
			reqJson = json.loads(req)
			method = reqJson["method"]
			target = reqJson["host"] + reqJson["uri"]
			data = reqJson["args"]
			cookie = reqJson["cookie"]

			inj = autoinj.Autoinj(server, target, method, data, cookie)
			rs = inj.run()
			print rs

			if len(rs['data'])>0:
				print "### INJ ###"
				print rs['data'][0]
				insertHash(param.sqlinj, req, rs['data'][0])
		except Exception, e:
			print "本次扫描发生了一点意外"
			print e
			time.sleep(1)


if __name__ == '__main__':
	main()
