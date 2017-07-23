# -*- coding:utf-8 -*-

import random
import re
import requests
import urllib2

class CPS:

    def __init__(self):
        pass

    def login(self):
        pass

    def getSkuId(self):
        pass

class QWD:

    def __init__(self, configFile=None):

        self.jxjpin = ''   ##用户名
        self.pinType = ''   ##通过url获取
        self.apptoken = ''   ##网站的tocken

        self.appid = '161'   ##app的id
        self.ctype = 'apple' ##客户端类型
        self.ie = 'utf-8'    ##字符集
        self.p = '1'         ##默认为1
        #pin = '18910148469_p'   ##账户名
        #tgt = 'AAFZKaOcAEA3VM9HrqXNMOHF621Aa-dp-v2WqwOGp4vgIaHdQrTlpHnRIWIbu6wodpHNAUeQSHjutqZKM27_9h3KgDD1bbkR'    ###我的理解是加密密码，通过抓包取得

        #pin = 'sausame'
        #tgt = 'AAFZbKu8AED13SyRWYSyxryS607Ko-pAfHLy6Q6M-nVbK0V56nplwdnZlFotxalv5s_uZ0jiKV2BGhQABmpcYJTmvOrvjYP3'

        #pin = 'sausame'
        #tgt = 'AAFZbKyoAEDWaJEBE7AbPws1L6W50OAGLB4EtgT1wnefwWmjQbBiE1E9WvgUq9R3HgqKH_6dVY1uETPj5xxOXyjfrvL-u7ET'

        self.pin = 'jd_7d7714f53cba9'
        self.tgt = 'AAFZbKwFAEAALdMmvd6rioPDM22up9AEREocUbmRk3LF4gkpDA0GGRuFboCPi_L9GJmoDZxPNpUE1tBzK7EnM2TEcyWkTcSx'

        self.uuid = '69D9E50C-3D8C-4CFE-BC2F-D1D65BB3C14D'   ##uuid   ##uuid

    def login(self):
        # appid=161&ctype=apple&ie=utf-8&p=1&pin=xiongruhao&tgt=AAFZO6BoAEDiYZogkABc17kbYW9Nb721f5u0njKAUTVrOhcHBV6kHCvJZpo5XCf4cm0e5ekOCfNRZ1XMRTunnJ3hGi_AqBx5&uuid=69D9E50C-3D8C-4CFE-BC2F-D1D65BB3C14D
        data = 'appid={0}&ctype={1}&ie={2}&p={3}&pin={4}&tgt={5}&uuid={6}'.format(self.appid,
                self.ctype, self.ie, self.p, self.pin, self.tgt, self.uuid)

        # print(data)
        url = 'https://qwd.jd.com/cgi-bin/qwd_app_login'
        req = urllib2.Request(url=url, data=data)
        res = urllib2.urlopen(req)
        html = res.read()

        if html.find(r'msg": "pin login success') > 10:
            # 获得apptoken
            reg_apptoken = r'apptoken": "(.*?)",'
            self.apptoken = str(re.findall(reg_apptoken, html)[0])
            # print(apptoken)
            # 获得pinType
            reg_pinType = r'pinType": "(.*?)",'
            self.pinType = str(re.findall(reg_pinType, html)[0])
            # 获得jxjpin
            reg_jxjpin = r'jxjpin": "(.*?)",'
            self.jxjpin = str(re.findall(reg_jxjpin, html)[0])
            print('#########Welecome to qwd.jd.com!######################')
        else:
            print 'Failed to login to qwd:\n', html

    def getShareUrl(self, skuid):

        url = 'https://qwd.jd.com/fcgi-bin/qwd_itemshare?skuid={0}&type=1'.format(skuid)
        req = urllib2.Request(url)
        cookie = 'app_id={0}; apptoken={1}; client_type={2}; jxjpin={3}; pinType={4}; tgt={5}; qwd_chn=99; qwd_schn=2; login_mode=1;'.format(self.appid, self.apptoken, self.ctype, self.jxjpin, self.pinType, self.tgt)
        # print(cookie)
        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 (5715086848) JXJ/1.3.5.70426')
        res = urllib2.urlopen(req)
        html = res.read()
        # print(html)
        reg_skuurl = r'"skuurl":"(.*?)"'
        skuurl = str(re.findall(reg_skuurl, html)[0])
        # print(skuurl)
        return skuurl

    @staticmethod
    def get_skuid(url, configFile=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176 MicroMessenger/4.3.2')
        res = urllib2.urlopen(req)
        html = res.read()
        reg1 = r"hrl='(.*?)'"
        url_skuid = re.findall(reg1, html)[0]
        request = urllib2.Request(url_skuid)
        request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176 MicroMessenger/4.3.2')
        result = urllib2.urlopen(request).read()
        reg_id = r'"areaSkuId":"(\d+)"'
        skuid = str(re.findall(reg_id, result)[0])
        # print(skuid)
        return skuid

    @staticmethod
    def check_msg(msg):
        reg = r'https://union-click\.jd\.com'
        result = re.findall(reg, msg)
        if len(result)>0:
            return True
        else:
            return False

    @staticmethod
    def get_new_msg(msg, result):
        text = ''
        for i in range(len(result)):
            req = urllib2.Request(str(result[i]))
            res = urllib2.urlopen(req)
            html = res.read()
            reg1 = r"hrl='https://union-click\.jd\.com\S+&d=(\S\S\S\S\S\S)'"
            result1 = re.findall(reg1, html)[0]
            # print(result1)
            url = 'https://union-click.jd.com/jdc?d=' + str(result1)
            # print(url)
            text = msg.replace(str(result[i]), url)
            msg = text
            # print(text)
            # print('aaaaaaaaaaaaaaaaaaa')
        return text

    def get_img(self, skuid):
        g_tk = str(random.randint(1000000000, 9999999999))
        url = 'https://qwd.jd.com/fcgi-bin/qwd_searchitem_ex?g_tk=&pageindex=1&pagesize=20&key={1}'.format(g_tk, skuid)
        req = urllib2.Request(url)
        cookie = 'app_id={0}; apptoken={1}; client_type={2}; jxjpin={3}; pinType={4}; tgt={5}; qwd_chn=99; qwd_schn=2; login_mode=1;'.format(self.appid, self.apptoken, self.ctype, self.jxjpin, self.pinType, self.tgt)
        # print(cookie)
        req.add_header('Cookie', cookie)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 (5715086848) JXJ/1.3.5.70426')
        res = urllib2.urlopen(req)
        html = res.read()
        # print(html)
        reg_img = r'skuimgurl":"(https://img\S+)",'
        img = str(re.findall(reg_img, html)[0])
        # print(skuurl)
        return img

