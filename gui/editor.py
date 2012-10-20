# -*- coding: utf-8 -*-
from Tkinter import *

class editor:
    def __init__(self,title='',content='',questions={}):
        self.title = str(title)
        self.content = str(content)
        self.qas = dict(questions)

        self._createWidgets()
        self.result = None

    def _okcommand(self):
        qas = {}
        for qbox,abox in self.qalist:
            q = qbox.get().strip().encode('utf-8')
            a = abox.get().strip().encode('utf-8')
            if q and a:
                qas[q] = a
        self.result = {
            'title': self.titleBox.get().strip().encode('utf-8'),
            'content': self.contentBox.get(1.0,END).strip().encode('utf-8'),
            'qas': qas
        }
        self.root.destroy()
        self.root.quit()

    def _createWidgets(self):
        self.root = Tk()
        self.root.title('编辑文件')
        self.root.resizable(0,0)

        self.titleBox = Entry(self.root)
        if self.title:
            self.titleBox.insert(END,self.title)

        self.contentBox = Text(self.root,height=15,width=60)
        if self.content:
            self.contentBox.insert(END,self.content)

        self.qabox = Frame(self.root)
        self.qabox_p1 = Label(self.qabox,text='问题')
        self.qabox_p2 = Label(self.qabox,text='答案')
        self.qabox_p1.grid(row=0,column=0)
        self.qabox_p2.grid(row=0,column=1)
        self.qalist = []

        qakeys = self.qas.keys()
        for i in range(0,4):
            self.qalist.append((
                                Entry(self.qabox,width=25),
                                Entry(self.qabox,width=25)
                              ))
            ind = len(self.qalist) - 1
            self.qalist[ind][0].grid(row=i+1,column=0)
            self.qalist[ind][1].grid(row=i+1,column=1)

            if i < len(qakeys):
                self.qalist[ind][0].insert(END,qakeys[i])
                self.qalist[ind][1].insert(END,self.qas[qakeys[i]])

        self.btnOK = Button(text='确认')
        self.btnOK['command'] = self._okcommand

        self.titleBox.grid(row=0,column=0,sticky=N+E+W+S)
        self.contentBox.grid(row=1,column=0)
        self.qabox.grid(row=2,column=0,sticky=N+E+W+S)
        self.btnOK.grid(row=3,column=0)

    def showDialog(self):
        self.root.mainloop()

if __name__ == '__main__':
    e = editor('default','default')
    e.showDialog()
    print e.result
