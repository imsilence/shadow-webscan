#encoding: utf-8

import hashlib

def md5(txt):
    if not isinstance(txt, bytes):
        txt = str(txt).encode()
    return hashlib.md5(txt).hexdigest()