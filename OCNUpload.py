#!usr/bin/python

import os
from getVision import awscontent
from StaticImport import HttpHand
from FTPupload import FTPupload
import time
from logModule import logModule

#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Automatic Content Upload for OCN starts')
logger = logModule()
logger.info('Automatic Content Upload for OCN starts')
aws = awscontent('LastModifiedOCN')
downloadCheck = aws.lastmodifyCheck() #Check any new file version on AWS S3 China. Yes then return 1
if (downloadCheck == 1):
        #print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' New content found') #Log new file found
        logger.info('New Content found')
        #Upload to FTP HCA VCN
        ftp = FTPupload('36.110.88.228','bshsc-cn52','y5qoz09PCKKv')
        if (ftp.fileUpload()):
                #After upload successful, trigger HCA to import
                si = HttpHand('https://rt-demo.homeconnecthca.cn/importer/cdr','RGC Operation')
                si.PostHand()
else:
        #print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+ ' No new file need to be downloaded')
        logger.info('No new file need to be downloaded')
#print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Automatic Content Upload for OCN has been finished')
logger.info('Automatic Content Upload for OCN has been finished')
