# -*- coding: utf-8 -*-
import getpass
import os
import random

from hashes import Hash

def randkey(length=128):
    ret = ''
    for i in range(0,length):
        ret += chr(random.randint(0,255))
    return ret

def formatTitle(title):
    # Title is combined with letters, numbers, _, with no others.
    title = title.strip()
    if len(title) > 256:
        return False
    legal = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-0123456789'
    ret = ''
    for each in title:
        if each in legal:
            ret += each
        else:
            ret += '_'
    return ret

def getGlobalPass():
    r = getpass.getpass(u'请输入全局保护密码，以便解密文件解锁密码\nType in global protection passphrase to decrypt file decrypting passphrases.\n'.encode('utf-8'))
    r = r.strip()
    if r:
        return Hash('whirlpool',r).digest() + Hash('sha512',r).digest()
    else:
        return False

def clearScreen():
    os.system('clear')
