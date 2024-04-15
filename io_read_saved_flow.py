import pprint
import sys
import json
import urllib.parse

from mitmproxy import http
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException

error_dict = {"fail":0}
count_dict = {"suc":0, "fail":0}

with open("yeelight_new_method_1_18", "rb") as logfile:
    freader = io.FlowReader(logfile)
    error_list = []
    count = 0
    try:
        index = 0
        for f in freader.stream():
            index = index + 1
            if isinstance(f, http.HTTPFlow):
                if f.request.path == "/app/miotspec/prop/set":
                    if f.response != None:
                        request_data = f.request.content.decode("utf-8")
                        data_str = f.response.content.decode("utf-8")
                        try:
                            data_dict = json.loads(data_str)
                        except Exception as e:
                            continue
                        response_time = f.response.timestamp_end -f.request.timestamp_start
                        if "result" in data_dict:
                            if data_dict["result"] != None:
                                count = count + 1
                                if (data_dict["result"][0]["code"] in error_dict):
                                    error_dict[data_dict["result"][0]["code"]] += 1
                                elif (data_dict["result"][0]["code"] not in error_dict):
                                    error_dict[data_dict["result"][0]["code"]] = 1
                                if (response_time > 0.11) or (data_dict["result"][0]["code"] == 0) or (data_dict["result"][0]["code"] == -704002000):
                                    count_dict["suc"] += 1
                                else:
                                    count_dict["fail"] += 1
                            else:
                                count = count - 1
                                # error_dict["fail"] += 1
                        #     #print(data_dict["result"][0]["code"], type(data_dict["result"][0]["code"]))
                        #     if data_dict["result"][0]["code"] == -704083036:
                        #         print(urllib.parse.unquote(f.request.content.decode("utf-8"))[urllib.parse.unquote(f.request.content.decode("utf-8")).index("data="):])
                        # #         print(data_dict)
                        #         print(index)

                        # else:
                        #     print(urllib.parse.unquote(f.request.content.decode("utf-8"))[urllib.parse.unquote(f.request.content.decode("utf-8")).index("data="):])
                        #     print(data_dict)
                        # if data_dict["result"] == None:
                        #     print(urllib.parse.unquote(f.request.content.decode("utf-8"))[urllib.parse.unquote(f.request.content.decode("utf-8")).index("data="):])
                        #     print(data_dict)
                        if count == 5000:
                            break
    except FlowReadException as e:
        print(f"Flow file corrupted: {e}")
print(error_dict)
print(count_dict)