import boto3 
import os
from logModule import logModule

class snsInform:

	def __init__(self):
		self.aws_access_key_id=''
		self.aws_secret_key_id=''
		self.s3 = boto3.client('sns',aws_access_key_id=self.aws_access_key_id,aws_secret_access_key=self.aws_secret_key_id,region_name='cn-north-1')
		self.topicarn=''
		self.filename = ''
		self.logger = logModule()
	def getFileversion(self,backend):
		file_version = ''
		if (backend == ''):
			self.filename = ''
		elif (backend == ''):
			self.filename = ''
		else:
			self.filename = ''
		try:
			f = open(''+self.filename,'r')
			file_version = f.readline().rstrip('\n')
		#	print (file_version)
			f.close()
		except Exception as e:
			self.logger.error('Latest Version couldn''t be fetched due to %s'%e) 			
		return file_version
	
	def informComplete(self,backend):
		file_version = self.getFileversion(backend)
		success_message='The latest content '+backend+' is imported successfully. File version '
		self.s3.publish(TopicArn=self.topicarn,MessageStructure='string',Message=success_message+file_version)
		#print (success_message+file_version)

	def informError(self):
		error='Import process failure due to unexpected errors,please check the log for details'
		self.s3.publish(TopicArn=self.topicarn,MessageStructure='string',Message=error)

	def informFail(self,backend):
		file_version= self.getFileversion(backend)
		fail_message='The latest content '+backend+' is imported but have errors, please check HCA side or content files. File version '
		self.s3.publish(TopicArn=self.topicarn,MessageStructure='string',Message=fail_message+file_version)
		#print (fail_message+file_version)
#s = snsInform()
#s.informFail(
