# -*- coding: utf-8 -*-
import docformat
from utils import *

def handle(deckey, content):    
    def setkey(p,d=deckey): return d
    def askqa(p,q):
        print p
        ret = {}
        for each in q:
            ret[each] = raw_input(each.encode('utf-8'))
        return ret
    while True:
        decrypted = docformat.EncryptedFile(content).read(setkey,askqa)
        if decrypted != False:
            clearScreen()
            print '[解密成功 内容显示如下]'
            print decrypted
            print '-----------------------'
            raw_input('按任意键返回')
            return
        else:
            if raw_input('解密失败\n<Enter>:重试(如果您怀疑这是答错问题所致) | 任意输入+<Enter>:退出').strip():
                return
