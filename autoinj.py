#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import json
import urllib
import urllib2
import redis
import requests
import param

class Autoinj(object):
	"""
		sqlmapapi 接口建立和管理sqlmap任务
		by zhangh (zhanghang.org#gmail.com)

		php install requests
	"""

	def __init__(self, server='', target='', method='', data='', cookie='', referer=''):
		super(Autoinj, self).__init__()
		self.server = server
		if self.server[-1] != '/':
			self.server = self.server + '/'
		if method == "GET":
			self.target = target + '?' + data
		else:
			self.target = target
		self.taskid = ''
		self.engineid = ''
		self.status = ''
		self.method = method
		self.data = data
		self.referer = referer
		self.cookie = cookie
		self.start_time = time.time()
		#print "server: %s \ttarget:%s \tmethod:%s \tdata:%s \tcookie:%s" % (self.server, self.target, self.method, self.data, self.cookie)

	def task_new(self):
		code = urllib.urlopen(self.server + param.task_new).read()
		self.taskid = json.loads(code)['taskid']
		return True

	def task_delete(self):
		url = self.server + param.task_del
		url = url.replace(param.taskid, self.taskid)
		requests.get(url).json()

	def scan_start(self):
		headers = {'Content-Type':'application/json'}
		url = self.server + param.scan_task_start
		url = url.replace(param.taskid, self.taskid)
		data = {'url':self.target}
		t = requests.post(url, data=json.dumps(data), headers=headers).text
		t = json.loads(t)
		self.engineid = t['engineid']
		return True

	def scan_status(self):
		url = self.server + param.scan_task_status
		url = url.replace(param.taskid, self.taskid)
		self.status = requests.get(url).json()['status']

	def scan_data(self):
		url = self.server + param.scan_task_data
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def option_set(self):
		headers = {'Content-Type':'application/json'}
		url = self.server + param.option_task_set
		url = url.replace(param.taskid, self.taskid)
		data = {}
		if self.method == "POST":
			data["data"] = self.data
		if len(self.cookie)>1:
			data["cookie"] = self.cookie
		#print data

		t = requests.post(url, data=json.dumps(data), headers=headers).text
		t = json.loads(t)

	def option_get(self):
		url = self.server + param.option_task_get
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def scan_stop(self):
		url = self.server + param.scan_task_stop
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def scan_kill(self):
		url = self.server + param.scan_task_kill
		url = url.replace(param.taskid, self.taskid)
		return requests.get(url).json()

	def run(self):
		# 开始任务
		if not self.task_new():
			print "Error: task created failed."
			return False
		# 设置扫描参数
		self.option_set()
		# 启动扫描任务
		if not self.scan_start():
			print "Error: scan start failed."
			return False
		# 等待扫描任务
		while True:
			self.scan_status()
			if self.status == 'running':
				time.sleep(3)
			elif self.status== 'terminated':
				break
			else:
				print "unkown status"
				break
			if time.time() - self.start_time > 30000:
				error = True
				self.scan_stop()
				self.scan_kill()
				break

		# 取结果
		res = self.scan_data()
		# 删任务
		self.task_delete()
		print "耗时:" + str(time.time() - self.start_time)
		return res



# if __name__ == '__main__':
# 	server = 'http://127.0.0.1:8775/'
# 	target = 'http://192.168.48.124:8080/index/news'
# 	#target = 'http://127.0.0.1:8080/index/login'
# 	data = "id=1"
# 	cookies = ""
# 	inj = Autoinj(server, target, 'GET', data, cookies)
# 	rs = inj.run()
# 	print rs

# 	if len(rs['data'])>0:
# 		print "SQL注入"






