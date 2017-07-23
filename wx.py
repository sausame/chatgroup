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
from msg import MessageCenter

class WX:

    def __init__(self, configFile=None):

        #self.jk_name = ['京东员工内购群(凌)','得得']
        self.jk_name = ['得得']
        self.jk_id = list()
        # 自己促销群
        self.ng_name = ['啊啊啊啊']
        self.ng_id = list()
        self.set_skuid = set([])

        self.toGroups = list()

        self.messageCenter = MessageCenter()

    def login(self):

        itchat.auto_login(hotReload=True, statusStorageDir='status.pkl')

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

    def get_ng_id(self):
        ng_list = []
        zj_id = []
        print(len(self.ng_name))
        for i in range(len(self.ng_name)):
            ng_list.append(itchat.search_chatrooms(name=self.ng_name[i]))
            zj_id.append(ng_list[i][0]['UserName'])
        print zj_id
        return zj_id

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

        if len(self.ng_id) != len(self.ng_name):
            self.ng_id = self.get_ng_id()

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


