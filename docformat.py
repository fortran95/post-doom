# -*- coding: utf-8 -*-
import time
import json

from xipher import xipher as x
from hashes import Hash

class EncryptedFile:
    def __init__(self):
        pass

    def read(self,src,key_callback,qa_callback):
        if type(src)==str:
            try:
                constructed = json.loads(src)
                checkkey = str(constructed['key'])
                questions = list(constructed['questions'])
                content = str(constructed['content']).decode('base64')
            except:
                return False
        else:
            return False
        key = str(key_callback(u'请输入解密密钥/Enter decrypting key:'))
        qa = dict(qa_callback(u'请回答这些问题/Answer these questions:',questions))
        enckey = self._calculate_key(key,qa)

        if Hash('md5',enckey).hexdigest() != checkkey:
            return False

        try:
            return x(enckey).decrypt(content)
        except:
            return False

    def generate(self,key,question_answers,content):
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
        
        ciphertext = x(enckey).encrypt(content)

        constructed = {
            'key': Hash('md5',enckey).hexdigest(),
            'questions': question_answers.keys(),
            'content': ciphertext.encode('base64').replace('\n',''),
        }

        return json.dumps(constructed,indent=4)

    def _calculate_key(self,key,qa):
        answers = ['%s:%s' % (str(k).strip(),str(qa[k]).strip()) for k in qa.keys()]
        answers.sort()
        joint_ans = ';'.join([each.lower() for each in answers])
        return Hash('whirlpool',joint_ans).hmac(key,True) + Hash('sha512',joint_ans).hmac(key,True)

if __name__ == '__main__':
    docf = EncryptedFile().generate('k',{'Parent':'1','b':'Li '},'content')
    def askkey(p):
        return raw_input(p.encode('utf-8'))
    def askqa(p,q):
        print p
        ret = {}
        for each in q:
            ret[each] = raw_input(each.encode('utf-8'))
        return ret

    print EncryptedFile().read(docf,askkey,askqa)
