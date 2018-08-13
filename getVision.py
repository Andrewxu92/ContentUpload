#Written by Wang, Weipeng on 2017/07/19
#This file is to check file on AWS S3 and download it if it's later than previous record
#Using boto3 to connect AWS
 
import boto3
import os
import json
import time
from SNS import snsInform
from logModule import logModule
class awscontent:

	def __init__(self,filename):
		self.aws_access_key_id=''
		self.aws_secret_key_id=''
		self.filename = filename
		self.sns = snsInform()
		self.logger = logModule()
	def jsonRead(self):
		#Read previous file last modified date from LastModify file
		j_line = ''
		try:
			j_file=open(""+self.filename,'r+')
			j_line = j_file.readline()
			j_line = j_line.rstrip('\n')
			#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Last synchronized version is '+j_line)
			self.logger.info('Last Synchronized version is (%s)'%(j_line))
			j_file.close()
		except Exception as e:
			self.logger.error('Check latest version process failed due to %s'%(e))
			self.sns.informError()
			print (e)
			
		return j_line


	def jsonWrite(self,data):
		#Write last modified date into LastModify file
		with open(''+self.filename,'w+') as j_file:
			j_file.write(data)

	def lastmodifyCheck(self):
		#Check and compare last modified between file on AWS and previous record
		last_modify = self.jsonRead()
		try:
			s3=boto3.resource('s3','cn-north-1',aws_access_key_id=self.aws_access_key_id,aws_secret_access_key=self.aws_secret_key_id)
			obj = s3.Object('','')
			last_modified = '{:%Y-%m-%d %H:%M:%S}'.format(obj.last_modified)	
			#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Current S3 file version is ' +last_modified)
			self.logger.info('Current file version is %s'%(last_modified))
		except Exception as e:
			self.sns.informError()
			print (e)

		if(last_modified==last_modify):
			#Same file, no actions. Terminate code	
			return 0
		else:
			#Different file, download
			response = obj.download_file('')
			self.jsonWrite(last_modified)
			return 1

#aws = awscontent('LastModified')
#aws.lastmodifyCheck()
