# coding:utf-8
import itchat
from params import *
import time

global GlobalParams, to
# 保存微信小号的userName


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def reply(msg):
    try:
        if msg.fromUserName == to:
            GlobalParams.set('time_in_minute', int(msg.text))
            itchat.send('%s reveived' % msg.text, to)
    except AttributeError:
        return

def main_itchat():
    global to
    itchat.auto_login(hotReload=True)
    to = itchat.search_friends(nickName=u'小号')[0].userName
    itchat.run(blockThread=False)
    while 1:
        GlobalParams.get('signal').wait()
        itchat.send(GlobalParams.get('msg'), to)
        time.sleep(20)
