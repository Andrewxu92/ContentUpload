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

class FTPDownload:
    def __init__(self):
        self.host = ''
        self.user = ''
        self.password = ''
        self.sns = snsInform()
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
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+' FTP login successful')
            return ftp
        except Exception as e:
            self.sns.informError()
            print (e)
    def fileDownload(self):
        ftp = self.FTPconnect()
        trytime = 0
        response = 0 
        loop = 1
        while(loop):
            try:
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+'Start to download china.tar.gz from FTP server')
                ftp.nlst()
                file_name = ''
                fp = open(file_name, 'wb+')
                ftp.retrbinary('RETR %s'%file_name,fp.write)
                #ftp.close()
                fp.close()
                response = 1
                loop = 0
            except Exception as e:
                self.sns.informError()
                print (e)
                loop = 0
        ftp.close()
        return response
FTP = FTPDownload()
FTP.fileDownload()
