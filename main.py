#!/usr/bin/env python
# -*- coding:utf-8 -*-

import itchat
import sys
import traceback

from datetime import datetime
from wx import WX
from utils import ThreadWritableObject

def run(configFile):

    wx = None

    @itchat.msg_register(itchat.content.TEXT, isGroupChat = True)
    def text(msg):
        wx.text(msg)

    thread = ThreadWritableObject(configFile)
    thread.start()

    sys.stdout = thread
    sys.errout = thread # XXX: Actually, it does NOT work

    try:
        wx = WX(configFile)
        wx.login()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print 'Error occurs at', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        traceback.print_exc(file=sys.stdout)

    thread.quit()
    thread.join()

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print 'Usage:\n\t', sys.argv[0], 'config-file\n'
        exit()

    configFile = sys.argv[1]

    run(configFile)


