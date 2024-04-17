import pprint
import sys
import json
import urllib.parse

from mitmproxy import http
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException

error_dict = {"fail":0}
count_dict = {"suc":0, "fail":0}

control_commands = [{1:[1,2,3]},{2:[1,5]}]

data_type_index_pre = [
    [[0 for _ in range(4)] for _ in range(len(command[next(iter(command))]))]
    for command in control_commands
]

data_type_index_after = [
    [[0 for _ in range(6)] for _ in range(len(command[next(iter(command))]))]
    for command in control_commands
]

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
                                for i in data_type_index_pre:
                                        for j in data_type_index_pre[i]:
                                            for k in data_type_index_pre[i][j]:
                                                if data_type_index_pre[i][j][k] == 10:
                                                    continue
                                                else:
                                                    index_pre_list = []
                                                    index_pre_list.append(i)
                                                    index_pre_list.append(j)
                                                    index_pre_list.append(k)
                                                    data_type_index_pre[i][j][k] = data_type_index_pre[i][j][k]+1
                                count = count + 1
                                if (data_dict["result"][0]["code"] in error_dict):
                                    error_dict[data_dict["result"][0]["code"]] += 1
                                elif (data_dict["result"][0]["code"] not in error_dict):
                                    error_dict[data_dict["result"][0]["code"]] = 1
                                if (response_time > 0.3)):
                                    data_type_index_after[index_pre_list[0]][index_pre_list[1]][index_pre_list[2]] = data_type_index_after[index_pre_list[0]][index_pre_list[1]][index_pre_list[2]] + 1          
                            else:
                                count = count - 1
    except FlowReadException as e:
        print(f"Flow file corrupted: {e}")
delete_list = []
for i in data_type_index_after:
    for j in data_type_index_after[i]:
        for k in data_type_index_after[i][j]:
            if data_type_index_after[i][j][k] < 10:
                tmp_del_list = []
                tmp_del_list.append(i)
                tmp_del_list.append(j)
                tmp_del_list.append(k)
                delete_list.append(tmp_del_list)
print(delete_list)