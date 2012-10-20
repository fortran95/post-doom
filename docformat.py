# -*- coding: utf-8 -*-
import time
import json

from xipher import xipher as x
from hashes import Hash
from utils import formatTitle

class EncryptedFile:
    def __init__(self,src=None):        
        if type(src)==str:
            try:
                constructed = json.loads(src)
                self.keyhash = str(constructed['key'])
                self.questions = list(constructed['questions'])
                self.title = str(constructed['title'])
                self.ciphertext = str(constructed['content']).decode('base64')
                self.integrity_check = str(constructed['integrity'])
            except:
                raise Exception("错误的格式 / Bad file format")

    def read(self,key_callback,qa_callback):
        key = str(key_callback(u'请输入解密密钥/Enter decrypting key:'))
        qa = dict(qa_callback(u'请回答这些问题/Answer these questions:',self.questions))
        enckey = self._calculate_key(key,qa)

        if Hash('md5',enckey).hexdigest() != self.keyhash:
            print '密码错误或问题回答错误 / Incorrect key or answers'
            return False
        if self.integrity_check != self._calculate_integrity(enckey,
                                                             self.ciphertext,
                                                             self.title):
            print '内容完整性校验失败 可能文件已经被篡改 / Integrity check failed This file may have been altered'
            return False

        try:
            return x(enckey).decrypt(self.ciphertext)
        except:
            return False

    def generate(self,key,question_answers,title,content):
        # The encrypt key is generated as follows:
        #   1. Sort all Q&A answers.
        #   2. Join all Q&A answers with ";".
        #   3. HMAC the result with given key.
        # Text being encrypted is combined with content and time,
        # in a way that is human-friendly.
        #   The question, the encrypt key's hash are stored together
        # with ciphertext, so that it's easy to verify user's input
        # without attempted decrytion.

        enckey = self._calculate_key(key,question_answers)
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        content = "%s\n\n%s" % (timestamp,content)
        title = formatTitle(title)
        ciphertext = x(enckey).encrypt(content)

        integrity_check = self._calculate_integrity(enckey,
                                                    ciphertext,
                                                    title)

        constructed = {
            'key': Hash('md5',enckey).hexdigest(),
            'questions': question_answers.keys(),
            'title': title,
            'content': ciphertext.encode('base64').replace('\n',''),
            'integrity': integrity_check
        }

        return json.dumps(constructed,indent=4)

    def _calculate_integrity(self,key,*argv):
        s = ';'.join(argv)
        return Hash('sha224',s).hmac(key,False)

    def _calculate_key(self,key,qa):
        answers = ['%s:%s' % (str(k).strip(),str(qa[k]).strip()) for k in qa.keys()]
        answers.sort()
        joint_ans = ';'.join([each.lower() for each in answers])
        return Hash('whirlpool',joint_ans).hmac(key,True) + Hash('sha512',joint_ans).hmac(key,True)

if __name__ == '__main__':
    docf = EncryptedFile().generate('k',{'Parent':'p','b':'b'},'Title Of','content')
    def askkey(p):
        return raw_input(p.encode('utf-8'))
    def askqa(p,q):
        print p
        ret = {}
        for each in q:
            ret[each] = raw_input(each.encode('utf-8'))
        return ret
    
    print EncryptedFile(docf).read(askkey,askqa)
