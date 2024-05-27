import logging

from mitmproxy import tcp
from mitmproxy.utils import strutils
import urllib.request
import random
from mitmproxy import flow
import json
import string
import numpy
import copy
import os
import base64
import time
import hashlib
import datetime
import hmac
import codecs

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

from Crypto.Util.Padding import pad
import zlib


total_message = 0
message_to_device = 0
type_index = 0


result = [[0 for _ in range(len(types))] for _ in range(len(key_list))]
request_time_response = 0
request_time_request = 0


def tcp_message(flow: tcp.TCPFlow):
    global characterstics_json, charaName, result, request_time_request, request_time_response
    message = flow.messages[-1]
    if b"smart/mb/out/" in message.content:
        if len(message.content) > 56:
            aes_payload = message.content[56:]
            key = b'vr)qif.Jit3T5;X_'
            cipher = AES.new(key, AES.MODE_ECB)
            try:
                decrypted_data = unpad(cipher.decrypt(aes_payload), AES.block_size)
                result = decrypted_data.decode()
                if request_time_request != 0:
                    print("time_response no response")
                request_time_request = time.time()
            except (ValueError, KeyError) as e:
                result = "解密失败: " + str(e)
                print(result)
                print(aes_payload)
    if b"smart/mb/in/" in message.content:
        if len(message.content) > 56:
            if request_time_request != 0:
                if request_time_response == 0:
                    request_time_response = time.time()
                    time_interval = request_time_response - request_time_request
                    print("time_response", time_interval, request_time_response, request_time_request)
                    request_time_response = 0
                    request_time_request = 0