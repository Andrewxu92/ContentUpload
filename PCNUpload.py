#!usr/bin/python

import os
from getVision import awscontent
from StaticImport import HttpHand
from FTPupload import FTPupload
import time

print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Automatic Content Upload for PCN starts')
aws = awscontent('LastModifiedPCN')
downloadCheck = aws.lastmodifyCheck() #Check any new file version on AWS S3 China. Yes then return 1
if (downloadCheck == 1):
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' New content found') #Log new file found
        #Upload to FTP HCA VCN
        ftp = FTPupload('36.110.88.230','bshsc-cn5','R5gkz1x6')
        if (ftp.fileUpload()):
                #After upload successful, trigger HCA to import
                si = HttpHand('https://rt.homeconnecthca.cn/importer/cdr','RGC Production')
                si.PostHand()
else:
        print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+ ' No new file need to be downloaded')
print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' Automatic Content Upload for PCN has been finished')


