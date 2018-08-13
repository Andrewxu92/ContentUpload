import urllib.request
import base64
import sys
import time
import json
from SNS import snsInform
from logModule import logModule

class CDRinform:
	
	def __init__(self):
		self.url = ''
		self.LP = ''
		self.sns = snsInform()
		self.logger = logModule()

	def sendInform(self,backend):
		username = ''
		password = ''
		#authtoken = username + ':' + password
		authtoken = base64.encodestring(('%s:%s' %(username, password)).encode()).decode().replace('\n','')
		header = {"Content-Type":"application/json","Authorization": "Basic " + authtoken}
		timestamp = int(time.time())
		reportID = int(1000*time.time())
		if(backend == ''):
			self.LP = ''
		else:
			self.LP = ''
		bodyString = {"hca-environment":backend,"content-status":"custom message","launch-package":self.LP,"package-type":"china","status":"Package uploaded successfully","report-id":reportID,"timestamp":timestamp}
		bodyJson = json.dumps(bodyString).encode('utf8')
		try:
			req = urllib.request.Request(url=self.url,data=bodyJson,headers=header)
			response =urllib.request.urlopen(req)
		except Exception as e:
			self.logger.error('CDR Inform failed due to %s'%e)
			self.sns.informError()
			print (e)



