import os
import re
import sys
import time

def parse_parameters(method_signature):
    params = re.search(r'\((.*?)\)', method_signature)
    if not params:
        return []

    params_str = params.group(1)
    param_types = []
    param_type = ''
    for char in params_str:
        param_type += char
        if char in 'ZBCSIFDJ' or char == ';':
            param_types.append(param_type)
            param_type = ''
        elif char == '[':
            continue

    return param_types

def find_react_method_annotations(directory):
    react_methods = []
    for root, dirs, files in os.walk(directory):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for file in files:
            if file.endswith(".smali"):
                file_path = os.path.join(root, file)
                class_name = file_path.replace(directory, '').replace('/', '.').replace('.smali', '')
                if class_name.startswith('.'):
                    class_name = class_name[1:]
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                    methods = re.findall(r'\.method.*?\.annotation runtime Landroid/webkit/JavascriptInterface;.*?\.end method', contents, re.DOTALL)
                    if methods:
                        while ".method" in contents:
                            function_start = contents.find(".method")
                            function_end = contents.find(".end method")
                            function_tmp = contents[function_start:function_end]
                            contents = contents[function_end + 5 : ]
                            if function_tmp.find(".annotation runtime Landroid/webkit/JavascriptInterface;")>=0:
                                method_name = function_tmp[:function_tmp.find("(")]
                                method_name = method_name[method_name.rfind(" ")+1:]
                                params = function_tmp[function_tmp.find("(") + 1 : function_tmp.find(")")]
                                param_types = []
                                print(current_time, root, file, "method_name",method_name)
                                while(len(params)>0):
                                    if params[0] == "L":
                                        param_value = params[1:params.find(";")]
                                        param_types.append("\'" + param_value + "\'")
                                        if ((len(params) - 1) == (params.find(";"))):
                                            params = ""
                                        else:
                                            params = params[params.find(";") + 1:]
                                    elif params[0] in "ZBCSIFDJ":
                                        if params[0] == "Z":
                                            param_types.append("\'boolean\'")
                                        elif params[0] == "B":
                                            param_types.append("\'byte\'")
                                        elif params[0] == "C":
                                            param_types.append("\'char\'")
                                        elif params[0] == "S":
                                            param_types.append("\'short\'")
                                        elif params[0] == "I":
                                            param_types.append("\'int\'")
                                        elif params[0] == "F":
                                            param_types.append("\'float\'")
                                        elif params[0] == "D":
                                            param_types.append("\'double\'")
                                        elif params[0] == "J":
                                            param_types.append("\'long\'")
                                        if len(params) == 1:
                                            params = ""
                                        else:
                                            params = params[1:]
                                    elif params[0] == "[":
                                        if params[1] != "L":
                                            param_types.append("\'" + params[:2] + "\'")
                                            if len(params) == 2:
                                                params = ""
                                            else:
                                                params = params[2:]
                                        elif params[1] == "L":
                                            param_value = params[0:params.find(";")]
                                            param_types.append("\'" + param_value + "\'")
                                            if ((len(params) - 1) == (params.find(";"))):
                                                params = ""
                                            else:
                                                params = params[params.find(";") + 1:]
                                method_info = {
                                    'class': class_name,
                                    'method': method_name,
                                    'param_count': len(param_types),
                                    'param_types': param_types
                                }
                                react_methods.append(method_info)
    return react_methods

def generate_array(n):
    return [f"a{i}" for i in range(1, n + 1)]


def generate_frida_script(methods, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('Java.perform(function () {\n')
        for method in methods:
            params_list = method['param_types']
            params_str = ",".join(params_list)
            params_str = params_str.replace("/",".")
            method_name = method["method"]
            class_name = method["class"]
            params_input_list = generate_array(len(params_list))
            params_input_str = ",".join(params_input_list)
            sanitized_class_name = class_name.replace(".", "_")
            file.write(f'    var {sanitized_class_name} = Java.use("{class_name}");\n')
            file.write(f'    {sanitized_class_name}.{method_name}.overload({params_str}).implementation = function({params_input_str})' +  '{\n')
            file.write(f'        var data = this.{method_name}({params_input_str});\n')
            file.write(f'        console.log(\'{method_name}\',{params_input_str});\n')
            file.write('        return data;\n')
            file.write('    };\n\n')
        file.write('});\n')


directory_path = ''
react_methods = find_react_method_annotations(directory_path)
# react_methods = [{'class': 'com.facebook.react.animated.NativeAnimatedModule', 'method': 'addAnimatedEventToView', 'param_count': 2, 'param_types': ["'java/lang/String'", "'com/facebook/react/bridge/ReadableMap'"]}]
#generate_frida_script(react_methods, 'hook_script.js')
with open("js_method.txt", 'w', encoding='utf-8') as file:
    for method in react_methods:
        print(method["method"])
        file.write(method["method"])
        file.write("\n")