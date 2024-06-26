import pprint
import sys
import json
import urllib.parse

from mitmproxy import http
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException


data_type_list = ["float", "string", "int", "boolean"]

platform = "Xiaomi"
# jingdong
# control_commands = [{0:["Error","Mode","Power","Reserve","Timing"]}]
# xiaomi
key_2_list = [2,3,5]
control_commands = [{2:[1,2,3,5,6,7,8,9], 3:[1], 5:[1,2,3,4,5]}]


def determine_type(value):
    if value.lower() == "true":
        return "boolean"
    elif value.lower() == "false":
        return "boolean"
    
    try:
        int_value = int(value)
        return "int"
    except ValueError:
        pass

    try:
        float_value = float(value)
        return "float"
    except ValueError:
        pass
    return "string"

first_dim = len(control_commands)

# Calculate second dimension lengths
second_dims = [len(command_dict.keys()) for command_dict in control_commands]

# Calculate third dimension lengths
third_dims = [[len(control_commands[i][key]) for key in control_commands[i].keys()] for i in range(first_dim)]

# Fourth dimension length is 4
fourth_dim = 4

# Create four-dimensional array and initialize with 0
data_type_index_list = []

for i in range(first_dim):
    second_dim_array = []
    for j in range(second_dims[i]):
        third_dim_array = []
        for k in range(third_dims[i][j]):
            fourth_dim_array = [0] * fourth_dim
            third_dim_array.append(fourth_dim_array)
        second_dim_array.append(third_dim_array)
    data_type_index_list.append(second_dim_array)
print(data_type_index_list)


with open("/mnt/hgfs/remote_fuzzing_firmware/xiaomi/react-mini-app/fuzzing/xiaomi_cam_yuntai_10_20", "rb") as logfile:
    freader = io.FlowReader(logfile)
    error_list = []
    count = 0
    try:
        index = 0
        for f in freader.stream():
            index = index + 1
            key_index_1 = 0
            key_index_2 = 0
            if isinstance(f, http.HTTPFlow):
                if ("controlDevice_v1" in f.request.path) or ("miotspec/prop/set" in f.request.path):
                    print(f.request.content.decode("utf-8"))
                    print(f.response)
                    if f.response != None:
                        request_data = f.request.content.decode("utf-8")
                        data_str = f.response.content.decode("utf-8")
                        try:
                            data_dict = json.loads(data_str)
                        except Exception as e:
                            continue
                        if platform == "Jingdong":
                            outer_json = json.loads(request_data)
                            inner_json = json.loads(outer_json["json"])
                            value = str(inner_json["command"][0]["current_value"])
                            command = inner_json["command"][0]["stream_id"]
                        elif platform == "Xiaomi":
                            parsed_data = urllib.parse.parse_qs(request_data)
                            # 获取并解码'data'字段
                            data_json = parsed_data['data'][0]
                            data_dict_request = json.loads(data_json)

                            # 提取'siid'、'piid'和'value'的值
                            params = data_dict_request['params'][0]
                            key_2 = params['siid']
                            key_index_2 = key_2_list.index(key_2)
                            command = params['piid']
                            value = str(params['value'])
                        value_type = determine_type(value)
                        response_time = f.response.timestamp_end -f.request.timestamp_start
                        if "result" in data_dict:
                            if data_dict["result"] != None:
                                for j in range(0, len(control_commands[key_index_1][key_2])):
                                    print(key_index_1,key_2,j, control_commands[key_index_1][key_2])
                                    if control_commands[key_index_1][key_2][j] == command:
                                        data_type_index = data_type_list.index(value_type)
                                        print(key_index_1,key_index_2, j,data_type_index)
                                        print(data_type_index_list[0])
                                        if data_type_index_list[key_index_1][key_index_2][j][data_type_index] == 10:
                                            break
                                        elif (response_time <= 0.3):
                                            data_type_index_list[key_index_1][key_index_2][j][data_type_index] = data_type_index_list[key_index_1][key_index_2][j][data_type_index] + 1
                                            break
                                        else:
                                            data_type_index_list[key_index_1][key_index_2][j][data_type_index] = -999
                                            break
    except FlowReadException as e:
        print(f"Flow file corrupted: {e}")
    print(data_type_index_list)
    for i in range(0, len(data_type_index_list)):
        for j in range(0, len(data_type_index_list[i])):
            for k in range(0, len(data_type_index_list[i][j])):
                if data_type_index_list[i][j][k] == 10:
                    print(control_commands[i][j], data_type_list[k])
