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

request_key = 0.0

def request_new(flow_tcp, message):
    # 检查是否为 MQTT PUBLISH 消息
    if (b"signaltrans/v2/categories/command" in message.content) and (b"\"method\":\"POST\"" in message.content):
        global request_key
        if request_key == 0.0:
            request_key = time.time()

def response_new(flow_tcp, message):
    global request_key, message_to_device, result, type_index
    if (b"smarthome.notify" in message.content) and (b"POST" in message.content) and (b"commandRsp" in message.content):
        if request_key != 0.0:
            response_time = time.time() - request_key
            print("response_time", response_time)
            if response_time < 0.200:
                for serviceId in serviceId_list:
                    if serviceId.encode() in message.content:
                        index = serviceId_list.index(serviceId)
                        if len(result[index]) != 0:
                            if result[index][type_index] < 10:
                                result[index][type_index] = result[index][type_index] + 1
                            else:
                                charaName[index][type_index] = 0
                            break
                message_to_device += 1
            request_key = 0.0


def tcp_message(flow: tcp.TCPFlow):
    request_new(flow, message)
    response_new(flow, message)
