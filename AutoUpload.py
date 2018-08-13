#!/usr/bin/python
#Written by Wang, Weipeng on 2017/07/19. 
#Entrance for HCA content synchronization for VCN

import os
from getVision import awscontent
from StaticImport import HttpHand
from FTPupload import FTPupload
import time
from logModule import logModule
#print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+' Automatic Content Upload for VCN starts')
logger = logModule()
logger.info('starts')
aws = awscontent('')
downloadCheck = aws.lastmodifyCheck() #Check any new file version on AWS S3 China. Yes then return 1
if (downloadCheck == 1):
	#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' New content found') #Log new file found
	logger.info('')
	#Upload to FTP HCA VCN
	ftp = FTPupload('','','')
	if (ftp.fileUpload()):
		#After upload successful, trigger HCA to import 								
		si = HttpHand('','')
		si.PostHand()
else:
	#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+ ' No new file need to be downloaded')
	logger.info('No new file need to be downloaded from S3')
#print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+ ' Automatic Content Upload for VCN has been finished')
logger.info('Automatic Content Upload for VCN has been finished')
