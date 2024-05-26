import pprint
import sys
import json
import urllib.parse

from mitmproxy import http
from mitmproxy import io
from mitmproxy.exceptions import FlowReadException


data_type_list = ["float", "string", "int", "boolean"]

platform = "Jingdong"
control_commands = [{0:["Error","Mode","Power","Reserve","Timing"]}]

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


with open("JD_Bull_plug_mitm_11_30", "rb") as logfile:
    freader = io.FlowReader(logfile)
    error_list = []
    count = 0
    try:
        index = 0
        for f in freader.stream():
            index = index + 1
            if isinstance(f, http.HTTPFlow):
                if "controlDevice_v1" in f.request.path:
                    print(f.request.path)
                    print(f.response)
                    if f.response != None:
                        request_data = f.request.content.decode("utf-8")
                        data_str = f.response.content.decode("utf-8")
                        try:
                            data_dict = json.loads(data_str)
                        except Exception as e:
                            continue
                        print(request_data)
                        if platform == "Jingdong":
                            outer_json = json.loads(request_data)
                            inner_json = json.loads(outer_json["json"])
                            value = str(inner_json["command"][0]["current_value"])
                            command = inner_json["command"][0]["stream_id"]
                        value_type = determine_type(value)
                        print(command)
                        print(data_type_index_list)
                        response_time = f.response.timestamp_end -f.request.timestamp_start
                        if "result" in data_dict:
                            if data_dict["result"] != None:
                                for i in range(0, len(data_type_index_list)):
                                    print(data_type_index_list[i], range(0, len(data_type_index_list[i])))
                                    for j in range(0, len(data_type_index_list[i])):
                                        print(i,j,control_commands,command)
                                        if control_commands[i][j] == command:
                                            data_type_index = data_type_list.index(value_type)
                                            if data_type_index_list[i][j][data_type_index] == 10:
                                                break
                                            elif (response_time <= 0.3):
                                                data_type_index_list[i][j][data_type_index] = data_type_index_list[i][j][data_type_index]+1
                                            else:
                                                data_type_index_list[i][j][data_type_index] = -999
    except FlowReadException as e:
        print(f"Flow file corrupted: {e}")
    print(data_type_index_list)
    for i in range(0, len(data_type_index_list)):
        for j in range(0, len(data_type_index_list[i])):
            for k in range(0, len(data_type_index_list[i][j])):
                if data_type_index_list[i][j][k] == 10:
                    print(control_commands[i][j], data_type_list[k])
 
