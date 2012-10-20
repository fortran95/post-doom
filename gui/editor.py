# -*- coding: utf-8 -*-
from Tkinter import *

class editor:
    def __init__(self,title='',content='',questions=[]):
        self.title = str(title)
        self.content = str(content)
        self.questions = str(questions)

        self._createWidgets()
        self.result = None

    def _okcommand(self):
        self.result = {
            'title': self.titleBox.get(),
            'content': self.contentBox.get(1.0,END),
        }
        self.root.destroy()
        self.root.quit()

    def _createWidgets(self):
        self.root = Tk()
        self.root.title('编辑文件')
        self.root.resizable(0,0)

        self.titleBox = Entry()
        if self.title:
            self.titleBox.insert(END,self.title)

        self.contentBox = Text()
        if self.content:
            self.contentBox.insert(END,self.content)

        self.btnOK = Button(text='确认')
        self.btnOK['command'] = self._okcommand

        self.titleBox.grid(row=0,column=0,sticky=N+E+W+S)
        self.contentBox.grid(row=1,column=0)
        self.btnOK.grid(row=2,column=0)

    def showDialog(self):
        self.root.mainloop()

if __name__ == '__main__':
    e = editor('default','default')
    e.showDialog()
    print e.result
