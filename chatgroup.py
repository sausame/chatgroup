#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2017/5/23 21:13
# @Author  : lingxiangxiang
# @File    : test.py
import codecs
import os
import random
import re
import threading
import urllib2

import datetime
import itchat
import sys
import time

import multiprocessing
from itchat.content import TEXT
reload(sys)
sys.setdefaultencoding('utf8')

jxjpin = ''   ##用户名
pinType = ''   ##通过url获取
apptoken = ''   ##网站的tocken
appid = '161'   ##app的id
ctype = 'apple' ##客户端类型
ie = 'utf-8'    ##字符集
p = '1'         ##默认为1
pin = '18910148469_p'   ##账户名
tgt = 'AAFZKaOcAEA3VM9HrqXNMOHF621Aa-dp-v2WqwOGp4vgIaHdQrTlpHnRIWIbu6wodpHNAUeQSHjutqZKM27_9h3KgDD1bbkR'    ###我的理解是加密密码，通过抓包取得
uuid = '69D9E50C-3D8C-4CFE-BC2F-D1D65BB3C14D'   ##uuid   ##uuid
# 监控群的名字， 这些群一定要保存到自己的通讯录
jk_name = ['仓储部社区推广3群2-2', '链接生成群(俊浩)']
jk_id = list()
# 自己促销群
ng_name = ['京东员工内购群(凌)', '京东员工特价分享群(尚)']
ng_id = list()
set_skuid = set([])
# appid=161&ctype=apple&ie=utf-8&p=1&pin=xiongruhao&tgt=AAFZO6BoAEDiYZogkABc17kbYW9Nb721f5u0njKAUTVrOhcHBV6kHCvJZpo5XCf4cm0e5ekOCfNRZ1XMRTunnJ3hGi_AqBx5&uuid=69D9E50C-3D8C-4CFE-BC2F-D1D65BB3C14D


def qwd_login():
    global apptoken, pinType, jxjpin
    data = 'appid={0}&ctype={1}&ie={2}&p={3}&pin={4}&tgt={5}&uuid={6}'.format(appid, ctype, id, p, pin, tgt, uuid)
    # print(data)
    url = 'https://qwd.jd.com/cgi-bin/qwd_app_login'
    req = urllib2.Request(url=url, data=data)
    res = urllib2.urlopen(req)
    html = res.read()
    if html.find(r'msg": "pin login success') > 10:
        # 获得apptoken
        reg_apptoken = r'apptoken": "(.*?)",'
        apptoken = str(re.findall(reg_apptoken, html)[0])
        # print(apptoken)
        # 获得pinType
        reg_pinType = r'pinType": "(.*?)",'
        pinType = str(re.findall(reg_pinType, html)[0])
        # 获得jxjpin
        reg_jxjpin = r'jxjpin": "(.*?)",'
        jxjpin = str(re.findall(reg_jxjpin, html)[0])
        print('#########Welecome to qwd.jd.com!######################')
    else:
        print('京享街登录失败，请联系管理员凌大神！')


def get_share_url(skuid):
    global apptoken, jxjpin, pinType
    url = 'https://qwd.jd.com/fcgi-bin/qwd_itemshare?skuid={0}&type=1'.format(skuid)
    req = urllib2.Request(url)
    cookie = 'app_id={0}; apptoken={1}; client_type={2}; jxjpin={3}; pinType={4}; tgt={5}; qwd_chn=99; qwd_schn=2; login_mode=1;'.format(appid, apptoken, ctype, jxjpin, pinType, tgt)
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




def get_skuid(url):
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


def check_msg(msg):
    reg = r'https://union-click\.jd\.com'
    result = re.findall(reg, msg)
    if len(result)>0:
        return True
    else:
        return False


def get_jkid(jk_name):
    jk_list = []
    jk_id = []
    for i in range(len(jk_name)):
        jk_list.append(itchat.search_chatrooms(name=jk_name[i]))
        # print(jk_list)
        jk_id.append(jk_list[i][0]['UserName'])
    return jk_id

def get_ng_id(ng_name):
    ng_list = []
    zj_id = []
    print(len(ng_name))
    for i in range(len(ng_name)):
        ng_list.append(itchat.search_chatrooms(name=ng_name[i]))
        zj_id.append(ng_list[i][0]['UserName'])
    print zj_id
    return zj_id


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


def get_img(skuid):
    global apptoken, jxjpin, pinType
    g_tk = str(random.randint(1000000000, 9999999999))
    url = 'https://qwd.jd.com/fcgi-bin/qwd_searchitem_ex?g_tk=&pageindex=1&pagesize=20&key={1}'.format(g_tk, skuid)
    req = urllib2.Request(url)
    cookie = 'app_id={0}; apptoken={1}; client_type={2}; jxjpin={3}; pinType={4}; tgt={5}; qwd_chn=99; qwd_schn=2; login_mode=1;'.format(appid, apptoken, ctype, jxjpin, pinType, tgt)
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


@itchat.msg_register(itchat.content.TEXT, isGroupChat = True)
def text(msg):
    # print('FromUserName')
    # print(msg['FromUserName'])
    # print(msg['Content'])
    global jk_id, ng_id, jk_name, ng_name, set_skuid
    print(set_skuid)
    now_time = datetime.datetime.now()
    reg_time = r'20\w\w-\w\w-\w\w 03:0[0-1]:00\S+'
    result_time = re.findall(reg_time, str(now_time))
    if len(result_time) > 0:
        set_skuid.clear()
    text = ''
    if len(jk_id) != len(jk_name):
        jk_id = get_jkid(jk_name)
    # print('jk_id')
    # print(jk_id)
    # print('ng_id')
    # print(ng_id)
    if len(ng_id) != len(ng_name):
        ng_id = get_ng_id(ng_name)
    # print('ng_id')
    # print(ng_id)

    for i in range(len(jk_id)):
        if msg['FromUserName'] == jk_id[i]:
            # print('------测试-----' + msg['Content'])
            reg_url_cn = r'(http://url\.cn/\S\S\S\S\S\S\S)'
            result = re.findall(reg_url_cn, msg['Content'])
            # print(result)
            if len(result)>0:
                text = get_new_msg(msg['Content'], result)
            else:
                text = msg['Content']
            # print(text)
            https_result =  re.findall(r'(https://union-click\.jd\.com/jdc\?d=\S\S\S\S\S\S)', text)
            if len(https_result)>0:
                for i in range(len(https_result)):
                    skuid = get_skuid(str(https_result[i]))
                    qwd_login()
                    skuurl = get_share_url(skuid)
                    money_msg = text.replace(https_result[i], skuurl)
                    text = money_msg
                    url_img = get_img(skuid)
                    print(url_img)
                    img = 'img/{0}.jpg'.format(skuid)
                    if not os.path.exists('img'):
                        os.mkdir('img')
                    with codecs.open(img, 'wb') as f:
                        f.write(urllib2.urlopen(url_img).read())
                if skuid not in list(set_skuid):

                    for j in range(len(ng_id)):
                        print(int(random.random() * 500))
                        time.sleep(int(random.random() * 500))
                        itchat.send(text, toUserName=ng_id[j])
                        aaaa = itchat.send_image(img, toUserName=ng_id[j], mediaId=skuid)
                        print(aaaa)
                        # if len(aaaa['BaseResponse']['ErrMsg']) == 0:
                        #      itchat.send("@img@%s".format(img))
                        print('send success')
                    set_skuid.add(skuid)
                    # print(int(random.random() * 500))
                    # time.sleep(int(random.random() * 500))


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, statusStorageDir='lingxiangxiang.pkl')
    # itchat.auto_login()
    itchat.run()
