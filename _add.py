# -*- coding: utf-8 -*-
import docformat
from utils import *
from gui.editor import editor as e

def handler(gpass,dpath):
    clearScreen()

    title, content = ''
    while True:
        s = e(title,content,[])
        s.showDialog()
        result = s.result
        if result != None:
            # Do a confirm
            print result
            if raw_input('直接按回车重新修改 输入任意内容回车即保存').strip() != '':
                break
        else:
            return

    # Save
    raw_input('Saved')
