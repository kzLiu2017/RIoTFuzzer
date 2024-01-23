from mitmproxy import http
from mitmproxy import ctx

import time
import hashlib
import hmac
import urllib.parse
import json
import os
import base64
import random
import string
import numpy
import copy

def generate_nonce():
    nonce = os.urandom(8) + int(time.time() / 60).to_bytes(4, 'big')
    return base64.b64encode(nonce).decode()


def generate_signed_nonce(secret, nonce):
    m = hashlib.sha256()
    m.update(base64.b64decode(secret))
    m.update(base64.b64decode(nonce))
    return base64.b64encode(m.digest()).decode()


def generate_signature(url, signed_nonce, nonce, data):
    sign = '&'.join([url, signed_nonce, nonce, 'data=' + data])
    signature = hmac.new(key=base64.b64decode(signed_nonce),
                         msg=sign.encode(),
                         digestmod=hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


def sign_data(uri, data, secret):
    if not isinstance(data, str):
        data = json.dumps(data)
    nonce = generate_nonce()
    signed_nonce = generate_signed_nonce(secret, nonce)
    signature = generate_signature(uri, signed_nonce, nonce, data)
    return {"_nonce":nonce, "data":data, "signature":signature}

MIN_INT_32 = -2147483648
MAX_INT_32 = 2147483647

def value_generation(index):
    # negative
    if index == 0:
        num = random.randint(0,1)
        # integer
        if num == 0:
            return -random.randint(2147483648,10000000000)
        # decimals
        elif num == 1:
            return -random.random()
        elif num == 2:
            return -random.randint(0,100000000)
    elif index == 1:
        num = random.randint(0,1)
        if num == 0:
            return random.randint(2147483648,10000000000)
        elif num == 1:
            return random.random()
    elif index == 2:
        return "test"

class RandomValues:
    def __init__(self, *args, **kwargs):
        self.proposed_vals = {
            'int': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'long': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'java.lang.Integer': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'java.lang.Float':{
                'fun': [self.low_pos_float],
                'dist': [1]
            },
            'float': {
                'fun': [self.low_pos_float],
                'dist': [1]
            },
            'java.lang.Double': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'boolean': {
                'fun': [self.true_Low],
                'dist': [1]
            },
            'java.lang.String': {
                'fun': [self.printable_chars],
                'dist': [1]
            },
            'byte': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'java.nio.ByteBuffer': {
                'fun': [self.low_pos],
                'dist': [1]
            },
            'array': {
                'fun': [self.low_pos_array],
                'dist': [0.5]
                # FIME: fix and use null array
            }
        }

    def low_pos_array(self):
        return random.randint(1, 10)

    def low_pos(self):
        return random.randint(0, 10)

    def low_neg(self):
        return random.randint(-10, 0)

    def big_pos_moderate_array(self):
        return random.randint(500, 16384)

    def big_pos_moderate(self):
        return random.randint(500, 16384)

    def big_pos(self):
        return random.randint(int(MAX_INT_32 / 2), MAX_INT_32)

    def big_neg(self):
        return random.randint(MIN_INT_32, int(MIN_INT_32 / 2))

    def low_pos_float(self):
        return random.uniform(0.0, 10.0)

    def low_neg_float(self):
        return random.uniform(-255.0, 0.0)

    def big_pos_float(self):
        return random.uniform(MAX_INT_32 / 2.0, float(MAX_INT_32))

    def big_neg_float(self):
        return random.uniform(float(MIN_INT_32), MIN_INT_32 / 2.0)

    def true_Low(self):
        return "true"

    def false_Low(self):
        return "false"

    def printable_chars(self):
        len = 4
        return "\"" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(len)) + "\""

    def fuzz_type(self, type_obj, obj_creator, array, primitive, *kargs, **kwargs):
        if array:
            n = numpy.random.choice(self.proposed_vals['array']['fun'], p=self.proposed_vals['array']['dist'])()
            val = [numpy.random.choice(self.proposed_vals[type_obj]['fun'], p=self.proposed_vals[type_obj]['dist'])() for i in range(0, n)]
        else:
            n = 1
            val = numpy.random.choice(self.proposed_vals[type_obj]['fun'], p=self.proposed_vals[type_obj]['dist'])()

        if obj_creator is not None:
            obj_creator(type_obj, primitive, val, n, *kargs, **kwargs)
        return val

    def fuzz_int(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('int', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_long(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('long', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_float(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('float', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_double(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('float', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_boolean(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('boolean', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_byte(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('byte', obj_creator, False, True, *kargs, **kwargs)

    def fuzz_byte_array(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('byte', obj_creator, True, True, *kargs, **kwargs)

    def fuzz_int_array(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('int', obj_creator, True, True, *kargs, **kwargs)

    def fuzz_java_lang_String(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('java.lang.String', obj_creator, False, False, *kargs, **kwargs)

    def fuzz_java_lang_Integer(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('java.lang.Integer', obj_creator, False, False, *kargs, **kwargs)

    def fuzz_java_lang_Float(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('java.lang.Float', obj_creator, False, False, *kargs, **kwargs)

    def fuzz_java_lang_Doable(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('java.lang.Doable', obj_creator, False, False, *kargs, **kwargs)

    def fuzz_java_nio_ByteBuffer(self, obj_creator, *kargs, **kwargs):
        return self.fuzz_type('java.nio.ByteBuffer', obj_creator, True, True, *kargs, **kwargs)

sp_dict = {2:[1,2,3,5,6,7,8,9], 3:[1], 5:[1,2,3,4,5], 8:[1,2,3]}
key_list = [2,3,5,8]

types = ['int', 'byte', 'java.lang.Integer', 'java.lang.String', 'boolean', 'java.lang.Float']


max_length = max(len(v) for v in sp_dict.values())
result = [[[0 for _ in range(len(types))] for _ in range(max_length)] for _ in range(len(key_list))]

def modify_request(body):
    siid = key_list[random.randint(0, len(key_list)-1)]
    piid = sp_dict[siid][random.randint(0, len(sp_dict[siid])-1)]
    v = RandomValues()
    empty_method = lambda *kargs, **kwargs: None
    i = random.randint(0,len(types) - 1)
    t = types[i]
    method = 'fuzz_' + t.replace('.', '_')
    value = ""
    if hasattr(v, method):
        value = getattr(v, method)(empty_method)

    body_new = body.replace('\"siid\":2', '\"siid\":' + str(siid))
    body_new = body_new.replace('\"piid\":1', ('\"piid\":' + str(piid)))
    if isinstance(value, str) == False:
        value = str(value)
    if body_new.find("value\":false") >= 0:
        body_new = body_new.replace('\"value\":false', ('\"value\":' + value))
    elif body_new.find("value\":true") >= 0:
        body_new = body_new.replace('\"value\":true', ('\"value\":' + value))
    ssecurity = "4bZXuBdeAjfY7zj0G6aCtA=="
    uri = "/miotspec/prop/set"
    sig = sign_data(uri, body_new, ssecurity)
    return body_new, sig

def request(flow: http.HTTPFlow) -> None:
    if flow.request.path == "/app/miotspec/prop/set":
        body = flow.request.urlencoded_form['data']
        if (body.find("value\":true") >= 0) or (body.find("value\":false") >= 0):
            body_new, sig = modify_request(body)
            flow.request.urlencoded_form['data'] = body_new
            flow.request.urlencoded_form['signature'] = sig["signature"]
            flow.request.urlencoded_form['_nonce'] = sig["_nonce"]