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

def tcp_message(flow: tcp.TCPFlow):
    global characterstics_json, charaName, result
    if len(characterstics_json) == 0:
        response = urllib.request.urlopen("XXX")
        # response = response.read().decode("utf-8")
        response=codecs.decode(response.read(), 'utf-8-sig')
        characterstics_json = json.loads(response)
        services = characterstics_json["services"]
        global name_list, serviceId_list
        for characteristics in services:
            characteristics_tmp = characteristics["characteristics"]
            name_list_tmp = []
            for characteristics_name in characteristics_tmp:
                obj_name_list = []
                name_dict_tmp = {}
                if "arrayObjs" in characteristics_name.keys():
                    for subchar_name in characteristics_name["arrayObjs"]:
                        if "W" in subchar_name["method"]:
                            obj_name_list.append(subchar_name["characteristicName"])
                elif "properties" in characteristics_name.keys():
                    for subchar_name in characteristics_name["properties"]:
                        if "W" in subchar_name["method"]:
                            obj_name_list.append(subchar_name["characteristicName"])
                if "method" not in characteristics_name.keys():
                    continue
                if "W" in characteristics_name["method"]:
                    name_dict_tmp[characteristics_name["characteristicName"]] = obj_name_list
                if len(name_dict_tmp.keys()) != 0:
                    name_list_tmp.append(name_dict_tmp)
            if len(name_list_tmp) != 0:
                name_list.append(name_list_tmp)
                serviceId_list.append(characteristics["serviceId"])
        charaName = [copy.deepcopy(types) for _ in range(len(serviceId_list))]
        result = [[0 for _ in range(len(types))] for _ in range(len(serviceId_list))]