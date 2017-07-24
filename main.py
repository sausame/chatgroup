#!/usr/bin/python2.7

import itchat
import sys

from wx import WX

@itchat.msg_register(itchat.content.TEXT, isGroupChat = True)
def text(msg):
    global wx
    wx.text(msg)

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print 'Usage:\n\t', sys.argv[0], 'config-file\n'
        exit()

    configFile = sys.argv[1]

    global wx

    wx = WX(configFile)
    wx.login()

