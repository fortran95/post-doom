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
            # Read Document
            pass

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

        answers = question_answers.values()
        enckey = self._calculate_key(key,answers)
        timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        content = "%s\n\n%s" % (timestamp,content)
        
        ciphertext = x(enckey).encrypt(content)

        constructed = {
            'key': Hash('md5',enckey).hexdigest(),
            'q&a': question_answers.keys(),
            'content': ciphertext.encode('base64').replace('\n',''),
        }

        return json.dumps(constructed,indent=4)

    def _calculate_key(self,key,answers):
        answers.sort()
        joint_ans = ';'.join([str(each).strip().lower() for each in answers])
        return Hash('whirlpool',joint_ans).hmac(key,True) + Hash('sha512',joint_ans).hmac(key,True)

if __name__ == '__main__':
    print EncryptedFile().generate('This is my very secret key',{'Parent':'1','b':2},'content')
