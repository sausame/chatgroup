# -*- coding:utf-8 -*-

import codecs
import json
import random
import re
import requests
import urllib2

from utils import getMatchString, getProperty

class CPS:

    def __init__(self):
        pass

    def login(self):
        pass

    def getSkuId(self):
        pass

class QWD:

    def __init__(self, configFile):

        self.configFile = configFile

        self.jxjpin = ''   ##用户名
        self.pinType = ''   ##通过url获取
        self.apptoken = ''   ##网站的tocken

        self.appid = getProperty(self.configFile, 'cps-qwd-appid')
        self.ctype = getProperty(self.configFile, 'cps-qwd-ctype')
        self.ie = getProperty(self.configFile, 'cps-qwd-ie')
        self.p = getProperty(self.configFile, 'cps-qwd-p')
        self.uuid = getProperty(self.configFile, 'cps-qwd-uuid')

        self.pin = getProperty(self.configFile, 'cps-qwd-pin')
        self.tgt = getProperty(self.configFile, 'cps-qwd-tgt')

        self.shareUrl = getProperty(self.configFile, 'cps-qwd-share-url')
        self.imageUrl = getProperty(self.configFile, 'cps-qwd-share-image-url')

        self.shareCookie = getProperty(self.configFile, 'cps-qwd-share-cookie')

        self.userAgent = getProperty(self.configFile, 'cps-qwd-http-user-agent')

    def login(self):

        # Url
        url = getProperty(self.configFile, 'cps-qwd-login-url')

        # Data
        scheme = getProperty(self.configFile, 'cps-qwd-login-data')
        print scheme
        data = scheme.format(self)

        # Request
        req = urllib2.Request(url=url, data=data)
        res = urllib2.urlopen(req)

        response = res.read()
        print url, data

        with open('a.json', 'w+') as fp:
            fp.write(response)

        obj = json.loads(response.decode('utf-8', 'ignore'))

        # Login status
        errCode = int(obj.pop('errCode'))

        if errCode is not 0:
            print 'Failed to login to', url, ':\n', response
            return False

        print('Logined to qwd.jd.com')

        obj = obj.pop('loginInfo')

        self.apptoken = obj.pop('apptoken')
        self.pinType = obj.pop('pinType')
        self.jxjpin = obj.pop('jxjpin')

        return True

    @staticmethod
    def isValidShareUrl(url):
        pattern = r'(https://union-click\.jd\.com/jdc\?d=\w+)'
        return re.match(pattern, url) is not None

    def getShareUrl(self, skuid):

        url = self.shareUrl.format(skuid)

        cookie = self.shareCookie.format(self)

        req = urllib2.Request(url)

        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', self.userAgent)

        res = urllib2.urlopen(req)
        html = res.read()

        return getMatchString(html, r'"skuurl":"(.*?)"')

    def getSkuId(self, url):

        req = urllib2.Request(url)
        req.add_header('User-Agent', self.userAgent)

        res = urllib2.urlopen(req)
        html = res.read()

        with open('b.html', 'w+') as fp:
            fp.write(html)

        url = getMatchString(html, r"hrl='(.*?)'")
        print url

        req = urllib2.Request(url)
        req.add_header('User-Agent', self.userAgent)

        res = urllib2.urlopen(req)
        html = res.read()

        data = getMatchString(html, r'window._itemOnly = (.*?);')

        with open('c.html', 'w+') as fp:
            fp.write(html)

        print data

        obj = json.loads(data.decode('utf-8', 'ignore'))
        obj = obj.pop('item')

        skuId = obj.pop('areaSkuId')

        return skuId

    def getImage(self, skuid):

        url = self.imageUrl.format(random.randint(1000000000, 9999999999), skuid)
        req = urllib2.Request(url)

        cookie = self.shareCookie.format(self)

        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', self.userAgent)

        res = urllib2.urlopen(req)
        html = res.read()

        img = getMatchString(html, r'skuimgurl":"(https://img\S+)",')

        return img

    def saveImage(self, path, skuid):

        with codecs.open(path, 'wb') as fp:

            url = self.getImage(skuid)
            fp.write(urllib2.urlopen(url).read())

