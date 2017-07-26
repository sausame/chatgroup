# -*- coding:utf-8 -*-

import os
import re
import requests
import itchat
import time

from datetime import timedelta, datetime
from qwd import QWD
from utils import getProperty, UrlUtils

class Message:

    def __init__(self, qwd):
        self.qwd = qwd

    def translateUrl(self, url):

        skuid = self.qwd.getSkuId(url)

        skuurl = self.qwd.getShareUrl(skuid)

        if not os.path.exists('img'):
            os.mkdir('img')

        img = 'img/{0}.jpg'.format(skuid)

        self.qwd.saveImage(img, skuid)

        print skuid, skuurl, img

        return skuid, skuurl, img

    def translate(self, msg):

        lastEnd = 0
        self.text = ''

        for m in re.finditer(UrlUtils.HTTP_URL_PATTERN, msg):

            self.text += msg[lastEnd:m.start()]
            lastEnd = m.end() + 1

            url = m.group(0)

            if UrlUtils.isShortUrl(url) is not None:
                originalUrl = UrlUtils.toOriginalUrl(url)
            else:
                originalUrl = url

            print url, originalUrl

            if QWD.isValidShareUrl(url):
                self.skuid, url, self.img = self.translateUrl(originalUrl)

            self.text += url

        if 0 == len(self.text):
            return False

        self.text += msg[lastEnd:]

        return True

class MessageCenter:

    def __init__(self, configFile):

        self.configFile = configFile

        self.qwd = QWD(configFile)
        self.qwd.login()

        self.skuIds = list()

        self.resetTimestamp = None

    def reset(self):

        #XXX: Reset skuids every 3:00 am
        RESET_HOUR = 3

        now = datetime.now().replace(minute=0, second=0, microsecond=0)

        if self.resetTimestamp is not None:

            delta = now - self.resetTimestamp

            if delta.days > 0:

                self.skuIds.clear()
                self.resetTimestamp = now.replace(hour=RESET_HOUR)

        else:
            self.resetTimestamp = now.replace(hour=RESET_HOUR)

    def translate(self, msg):

        self.reset()

        message = Message(self.qwd)

        if not message.translate(msg):
            return None

        if message.skuid in self.skuIds:
            return None

        self.skuIds.append(message.skuid)
        self.skuIds.sort()

        return message

