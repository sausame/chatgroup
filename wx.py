# -*- coding:utf-8 -*-

import random
import requests
import itchat
import time

from msg import MessageCenter
from utils import getProperty

class WX:

    def __init__(self, configFile):

        self.configFile = configFile
        self.messageCenter = MessageCenter(configFile)

    def login(self):

        statusFile = getProperty(self.configFile, 'wechat-status-file')

        itchat.auto_login(hotReload=True, statusStorageDir=statusFile)

        self.fromGroups = list()
        names = getProperty(self.configFile, 'wechat-input-groups').split(';')
        for name in names:
            group = itchat.search_chatrooms(name=name)
            self.fromGroups.extend(group)

        self.toGroups = list()
        names = getProperty(self.configFile, 'wechat-output-groups').split(';')
        for name in names:
            group = itchat.search_chatrooms(name=name)
            self.toGroups.extend(group)

        print self.fromGroups, '\n', self.toGroups

        itchat.run()

    def text(self, msg):

        print msg['Content']

        fromGroupName = msg['FromUserName']

        print fromGroupName

        if '@51a3bda21ad4580153aaf90423c862f9' != fromGroupName:

            for group in self.fromGroups:
                if fromGroupName == group['UserName']:
                    break
            else: # Not found
                return

        message = self.messageCenter.translate(msg['Content'])

        if message is None:
            return

        for group in self.toGroups:

            interval = random.random() * 10
            time.sleep(interval)

            ret = group.send(message.text)
            print 'Send', message.text, ':', ret

            interval = random.random() * 10
            time.sleep(interval)

            ret = group.send_image(message.img)
            print 'Send', message.img, ':', ret

