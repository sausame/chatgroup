# -*- coding:utf-8 -*-

import random
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

        self.me = itchat.search_friends()

        print self.me['NickName'], 'is working'

        self.fromGroups = list()
        names = getProperty(self.configFile, 'wechat-input-groups').split(';')
        for name in names:
            groups = itchat.search_chatrooms(name=name)
            self.fromGroups.extend(groups)

        self.toGroups = list()
        names = getProperty(self.configFile, 'wechat-output-groups').split(';')
        for name in names:
            groups = itchat.search_chatrooms(name=name)
            self.toGroups.extend(groups)

        itchat.run()

    def text(self, msg):

        fromGroupName = msg['User']['UserName']

        for group in self.fromGroups:

            if fromGroupName == group['UserName']:
                break
        else: # Not found
            return

        user = itchat.search_friends(userName=msg['ActualUserName'])

        print '\n================================================================\n'
        print 'In', group['NickName'], ',', user['NickName'], 'sends a message:\n'
        print '----------------------------------------------------------------\n'
        print msg['Content']
        print '\n================================================================\n'

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

