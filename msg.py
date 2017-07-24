# -*- coding:utf-8 -*-

import codecs
import io
import os
import random
import re
import urllib2

import requests
import datetime
import itchat
import time

from itchat.content import TEXT
from qwd import QWD
from utils import getProperty

class Message:

    def __init__(self, qwd):
        self.qwd = qwd

    def translate(self, msg):

        # print('------测试-----' + msg['Content'])
        reg_url_cn = r'(http://url\.cn/\S\S\S\S\S\S\S)'
        result = re.findall(reg_url_cn, msg)
        # print(result)
        if len(result)>0:
            text = QWD.get_new_msg(msg, result)
        else:
            text = msg

        # print(text)
        https_result = re.findall(r'(https://union-click\.jd\.com/jdc\?d=\S\S\S\S\S\S)', text)
        print text, https_result

        if len(https_result) == 0:
            return None

        for i in range(len(https_result)):
            self.skuid = self.qwd.getSkuId(str(https_result[i]))
            skuurl = self.qwd.getShareUrl(self.skuid)
            money_msg = text.replace(https_result[i], skuurl)
            self.text = money_msg

            url_img = self.qwd.getImage(self.skuid)

            self.img = 'img/{0}.jpg'.format(self.skuid)
            if not os.path.exists('img'):
                os.mkdir('img')

            with codecs.open(self.img, 'wb') as f:
                f.write(urllib2.urlopen(url_img).read())

            print self.skuid, self.text, self.img

        return self

class MessageCenter:

    def __init__(self, configFile):

        self.configFile = configFile

        self.qwd = QWD(configFile)
        self.qwd.login()

    def translate(self, msg):

        message = Message(self.qwd)
        return message.translate(msg)

