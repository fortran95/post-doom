# -*- coding: utf-8 -*-
import getpass
import os
import sys
import time

from hashes import Hash
from xipher import xipher as x
from utils import *
import _add
import _viewer

def listkeys(dpath,gkey):
    l = os.listdir(dpath)
    ret = {}
    for each in l:
        fpath = os.path.join(dpath,each)
        try:
            fkey = x(gkey).decrypt(open(fpath,'r').read())
        except:
            continue
        ret[each] = fkey
    return ret
def _exit():
    clearScreen()
    print '结束 / Exit now'
    exit()

basepath = os.path.realpath(os.path.dirname(sys.argv[0]))
dpath = os.path.join(basepath,'..','secret')
dpath = os.path.realpath(dpath)
epath = os.path.join(basepath,'encrypted')

GLOBALPASS = getGlobalPass()
if not GLOBALPASS:
    _exit()

while True:
    clearScreen()

    print '当前存储的文件解锁密钥如下 / Below are stored file keys'
    # List out all saved passphrases.
    keys_index = []
    keys_list = listkeys(dpath,GLOBALPASS)
    for each in keys_list:
        keys_index.append(each)
        print '[%3d] %s' % (len(keys_index),each)

    print '\n--- 菜单 / MENU ---'
    print '[add] 添加新文件存储'
    print '[del] 删除一条文件'
    print '[cat] 查阅一条文件'
    print '[auz] 重新输入全局解锁密钥'
    command = raw_input('请输入命令，或者直接回车退出').strip().lower()
    if not command:
        _exit()
    if command == 'auz':
        GLOBALPASS = getGlobalPass()
        if not GLOBALPASS:
            _exit()
    if command in ('del','cat'):
        try:
            num = int(raw_input('请输入文件编号'))
            if num < 1 or num > len(keys_index):
                raise Exception
        except:
            num = False
        if num:
            num -= 1
            selected_key = keys_index[num]
            if command == 'cat':
                readpath = os.path.join(epath,selected_key)
                if os.path.isfile(readpath):
                    content = open(os.path.join(epath,selected_key),'r').read()
                    _viewer.handle(keys_list[selected_key],content)
                else:
                    raw_input('文件不存在 / Cannot find this file')
            if command == 'del':
                if raw_input('请确认删除：\n%s\n输入[YES]确认' % selected_key) == 'YES':
                    try:
                        os.remove(os.path.join(epath,selected_key))
                        os.remove(os.path.join(dpath,selected_key))
                    except:
                        pass
    if command == 'add':
        _add.handler(GLOBALPASS,dpath,epath)
