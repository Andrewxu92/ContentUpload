#!/usr/bin/python
# - * - coding: utf-8 - * - 
#Written by Wang, Weipeng on 2017/07/19 
#Be advised, you should modify ftplib.py as PASV will return a new IP but python don't know.
#Add a fix_host in ftplib.py and deliver it to makepasv method

from ftplib import FTP_TLS
import logging
import os
from ssl import SSLContext,Purpose
import ssl
import time
from SNS import snsInform
from logModule import logModule

class FTPupload:
	
	def __init__(self,host,user,password):
		self.host = host #
		self.user = user #
		self.password = password #
		self.sns = snsInform()
		self.logger = logModule()

	def FTPconnect(self):
		#initial FTP object and login the HCA FTP server 
		try:
			ftp = FTP_TLS()
			ftp.set_pasv(True,self.host)
			ftp.ssl_version = ssl.PROTOCOL_TLSv1
			ftp.connect(host=self.host,port=21)
			ftp.set_debuglevel(2)
			ftp.auth()
			ftp.login(self.user,self.password)
			ftp.prot_p()
			self.logger.info('FTP login successfull')
			#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' FTP login successful')
			return ftp
		except Exception as e:
			self.sns.informError()
			self.logger.error('FTP connection Error')
			#print (e)

	def fileUpload(self):
		#Upload file to FTP server 
		#if failed then retry
		#Retry 3 times. If still failure, terminate the code
		ftp = self.FTPconnect()
		trytime = 0
		response = 0
		loop = 1
		while(loop):
			if (trytime==0):
				try:
					#print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Start to uploaded china.tar.gz to FTP server')
					self.logger.info('Start to uploaded china.tar.gz to FTP server (%s)'%self.host)
					ftp.nlst() 
					file_name=''
					if self.host == '':
						file_name = ''
					f = open(file_name,'rb')
					#filepath = '/home/ubuntu/AWSHCA/china.tar.gz'	
					ftp.storbinary('STOR %s'%os.path.basename(file_name),f)#,buffersize)
					f.close()
					ftp.close()
					#if os.path.exist(file_name):
					#	os.remove(file_name) 
					#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' china.tar.gz uploaded succssful')
					self.logger.info('china.tar.gz uploaded successfully to %s'%self.host)
					response = 1
					loop = 0
					#print (loop)
					break
				except Exception as e:
					self.sns.informError()
					self.logger.error('uploaded to %s termiated due to %s'%(self.host,e))
					break

			elif (trytime<4):
				#print ('Upload failure, retrying....'
				self.logger.debug('Upload failure,retrying....')
				time.sleep(30) 
				trytime = trytime + 1
			else:
				#print ('FTP upload failed.Ending.')
				self.logger.error('FTP upload to %s failed. Closing'%self.host)
				loop = 0
				break
		ftp.close()
		if (os.path.exists(file_name)) and (self.host != ''):
			os.remove(file_name)
			self.logger.info('File deleted')
		elif (self.host == '') and os.path.exists(file_name):
			os.renames(file_name,'')
			self.logger.info('File renameed')
		return response
#FTP = FTPupload()
#FTP.fileUpload()
