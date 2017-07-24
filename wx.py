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

from msg import MessageCenter
from utils import getProperty

class WX:

    def __init__(self, configFile):

        self.configFile = configFile

        self.jk_name = getProperty(self.configFile, 'wechat-input-groups').split(';')
        self.jk_id = list()

        self.ng_name = getProperty(self.configFile, 'wechat-output-groups').split(';')
        self.ng_id = list()

        self.set_skuid = set([])

        self.toGroups = list()

        self.messageCenter = MessageCenter(configFile)

    def login(self):

        statusFile = getProperty(self.configFile, 'wechat-status-file')

        itchat.auto_login(hotReload=True, statusStorageDir=statusFile)

        for name in self.ng_name:
            group = itchat.search_chatrooms(name=name)
            self.toGroups.extend(group)

        print self.toGroups

        itchat.run()

    def get_jkid(self):
        jk_list = []
        jk_id = []
        for i in range(len(self.jk_name)):
            jk_list.append(itchat.search_chatrooms(name=self.jk_name[i]))
            # print(jk_list)
            jk_id.append(jk_list[i][0]['UserName'])

        return jk_id

    def text(self, msg):

        #XXX: Move to message center
        print(self.set_skuid)

        #XXX: Reset skuids every 3:00 am
        #TODO: Bad design makes human confused
        now_time = datetime.datetime.now()
        reg_time = r'20\w\w-\w\w-\w\w 03:0[0-1]:00\S+'
        result_time = re.findall(reg_time, str(now_time))
        if len(result_time) > 0:
            self.set_skuid.clear()
        text = ''
        if len(self.jk_id) != len(self.jk_name):
            self.jk_id = self.get_jkid()

        print msg['Content']

        for i in range(len(self.jk_id)):

            print i, self.jk_id[i], msg['FromUserName']
            if msg['FromUserName'] == self.jk_id[i]:

                message = self.messageCenter.translate(msg['Content'])

                if message is None:
                    continue

                # XXX: Move to message center
                if message.skuid in list(self.set_skuid):
                    continue

                self.set_skuid.add(message.skuid)

                for group in self.toGroups:

                    interval = random.random() * 10
                    time.sleep(interval)

                    ret = group.send(message.text)
                    print 'Send', message.text, ':', ret

                    interval = random.random() * 10
                    time.sleep(interval)

                    ret = group.send_image(message.img)
                    print 'Send', message.img, ':', ret

