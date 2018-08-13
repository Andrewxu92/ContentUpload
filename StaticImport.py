#Written by Wang Weipeng on 2017/07/19
#This file is to trigger HCA content import using REST interface
import json
import os
import urllib.request
import time
from SNS import snsInform
from CDRinform import CDRinform
from logModule import logModule

class HttpHand:
	def __init__(self,host,backend):
		self.data={}
		self.respCode = 0
		self.respMsg = ""
		self.host = host 
		self.headers = {'Authorization':'Basic'}
		self.sns = snsInform()
		self.backend = backend
		self.cdrinform = CDRinform()
		self.logger = logModule()

	def PostHand(self):
		#Trigger start import
		packageStatus = [0,0] 
		packageStatus = self.GetHand()
		thisTime = 0
		while (1):
			if(packageStatus == [1,0]):
				if(thisTime == 0):
					#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+ ' Start Import')
					self.logger.info('Start Import')
					try:
						host = self.host+"/start"
						req=urllib.request.Request(host,headers=self.headers,method='POST')
						response = urllib.request.urlopen(req)
						a = response.read().decode()
						a = json.loads(a)
						packageStatus = [0,0]
						thisTime = 1
					except Exception as e:
						self.logger.error('Import Error due to %s'%e)
						self.sns.informError()
						print (e)
						break
				else:
					#print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Import success') 
					self.logger.info('Import Success')
					self.sns.informComplete(self.backend)
					self.cdrinform.sendInform(self.backend)
					break
			elif(packageStatus == [1,1]):
				#print (thisTime)
				#print (packageStatus)
				if(thisTime == 1):
				#	print (thisTime)
					self.logger.debug('Import finished but have errors')
					#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+ ' Import finished but have errors.')
					self.sns.informFail(self.backend)
					self.cdrinform.sendInform(self.backend)
					return 0
					break
				else:
					packageStatus = [1, 0]
			else:
				#If importing waiting and get the status after 30 seconds
				#Generally it will take about 7mins to import and in first 3 mins HCA couldn't reply importing status which will lead to error(Request start import but HCA is actually importing))
				self.logger.info('Importing')
				time.sleep(30)
				packageStatus = self.GetHand()	

	def GetHand(self):
		#Get current import progress
		completedMark = 0
		errorMark = 0
		packageStatus = [0,0]
		try: 
			host = self.host+"/report"
			req=urllib.request.Request(host,headers=self.headers,method='GET')
			response = urllib.request.urlopen(req)
			a = response.read().decode()
			a = json.loads(a)
			#print(a)
			for b in a.keys():
				if (b == 'duration'):
					completedMark = 1
					packageStatus = [1,0]
			if (completedMark==1):
				for b in a.keys():
		#			print (b)
					if(b=='errors'):
						errorMark = 1
						packageStatus = [1,1]
		except Exception as e:
			self.logger.error('Import failed due to %s'%e)
			self.sns.informError()
			print (e)
		
		return packageStatus

