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

        self.qwd = QWD()

    def login(self):

        self.qwd.login()

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

        def get_image(image_storage, url):
            r = requests.get(url, stream=True)
            for block in r.iter_content(1024):
                image_storage.write(block)
            image_storage.seek(0)

        # print('FromUserName')
        # print(msg['FromUserName'])
        # print(msg['Content'])
        print(self.set_skuid)
        now_time = datetime.datetime.now()
        reg_time = r'20\w\w-\w\w-\w\w 03:0[0-1]:00\S+'
        result_time = re.findall(reg_time, str(now_time))
        if len(result_time) > 0:
            self.set_skuid.clear()
        text = ''
        if len(self.jk_id) != len(self.jk_name):
            self.jk_id = self.get_jkid()
        # print('jk_id')
        # print(jk_id)
        # print('ng_id')
        # print(ng_id)
        if len(self.ng_id) != len(self.ng_name):
            self.ng_id = self.get_ng_id()
        # print('ng_id')
        # print(ng_id)

        print msg['Content']

        for i in range(len(self.jk_id)):
            print i, self.jk_id[i], msg['FromUserName']
            if msg['FromUserName'] == self.jk_id[i]:
                # print('------测试-----' + msg['Content'])
                reg_url_cn = r'(http://url\.cn/\S\S\S\S\S\S\S)'
                result = re.findall(reg_url_cn, msg['Content'])
                # print(result)
                if len(result)>0:
                    text = QWD.get_new_msg(msg['Content'], result)
                else:
                    text = msg['Content']
                # print(text)
                https_result =  re.findall(r'(https://union-click\.jd\.com/jdc\?d=\S\S\S\S\S\S)', text)
                print text, https_result
                if len(https_result)>0:
                    for i in range(len(https_result)):
                        skuid = QWD.get_skuid(str(https_result[i]))
                        skuurl = self.qwd.getShareUrl(skuid)
                        money_msg = text.replace(https_result[i], skuurl)
                        text = money_msg
                        url_img = self.qwd.get_img(skuid)

                        # XXX: Directly send image buffer
                        '''
                        image_storage = io.BytesIO()
                        get_image(image_storage, url_img)
                        '''
                        img = 'img/{0}.jpg'.format(skuid)
                        if not os.path.exists('img'):
                            os.mkdir('img')

                        with codecs.open(img, 'wb') as f:
                            f.write(urllib2.urlopen(url_img).read())

                        print skuid, skuurl, text, url_img, img

                    if skuid not in list(self.set_skuid):

                        self.set_skuid.add(skuid)

                        for group in self.toGroups:

                            interval = int(random.random() * 5)
                            print interval

                            time.sleep(interval)
                            #itchat.send(text, toUserName=ng_id[j])
                            ret = group.send(text)
                            print ret, text

                            time.sleep(interval)

                            # XXX: Directly send image buffer
                            #ret = group.send_image(image_storage)
                            ret = group.send_image(img)
                            print ret
                            # if len(aaaa['BaseResponse']['ErrMsg']) == 0:
                            #      itchat.send("@img@%s".format(img))

                    # XXX: Directly send image buffer
                    #image_storage.close()

                        # print(int(random.random() * 500))
                        # time.sleep(int(random.random() * 500))

