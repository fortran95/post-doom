# -*- coding: utf-8 -*-
import docformat
from utils import *
from gui.editor import editor as e

def handler(gpass,dpath):
    title, content, qas = '','',{}
    while True:
        s = e(title,content,qas)
        s.showDialog()
        result = s.result
        if result != None:
            # Do a confirm
            title = formatTitle(result['title'])
            content = str(result['content'])
            qas = dict(result['qas'])

            clearScreen()
            if (not title) or (not content):
                print '标题或内容有误'
                continue
            print '即将记录如下信息：'
            print '标题 %s' % title.encode('utf-8')
            print '问答'
            for q in qas:
                print " * [%s] %s" % (q,qas[q])
            print '内容\n%s' % content.encode('utf-8')
            print '--------'
            cmd = raw_input('<Enter>:重新修改 s+<Enter>:保存 其他:取消').strip().lower()
            if cmd == 's':
                break
            elif cmd == '':
                continue
            else:
                return
        else:
            return

    # Save
    raw_input('Saved')
