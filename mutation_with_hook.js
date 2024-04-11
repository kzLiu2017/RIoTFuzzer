var functionsToHook = [["com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge", "_handleMessageFromJs", 5]]

var target_class = "string"

var label = "current_value"

var key = "Power"

var value = "0"

var new_key = "power"

var new_value = "123"

var control_commands = [{1:[1,2,3]}]

var platform = "Xiaomi"

var data_type = [[["int", "long", "string", "double", "float", "bool"], ["int", "long", "string", "double", "float", "bool"], "int", "long", "string", "double", "float", "bool"]]

function generate_data_type(index, valueIndex){
    dataTypeArray = data_type[index][valueIndex]
    var randomIndex = Math.floor(Math.random() * dataTypeArray.length);
    var data_type = dataTypeArray[randomIndex]
    return data_type
}

function fuzzing_value_generation(index, valueIndex){
    var data_type = generate_data_type(index,valueIndex)
    
}

function command_select(){
    var randomIndex = Math.floor(Math.random() * control_commands.length);
    var selectedObject = control_commands[randomIndex];
    
    var keys = Object.keys(selectedObject);
    var randomKeyIndex = Math.floor(Math.random() * keys.length);
    var selectedKey = keys[randomKeyIndex];
    
    var values = selectedObject[selectedKey];
    var randomValueIndex = Math.floor(Math.random() * values.length);
    var selectedValue = values[randomValueIndex];

    return [selectedKey, selectedValue, randomIndex, randomValueIndex]
}

Java.perform(function() {
    functionsToHook.forEach(function(functionInfo) {
        var className = functionInfo[0];
        var methodName = functionInfo[1];
        var argCount = functionInfo[2]; 

        var clazz = Java.use(className);
        if (!clazz || !clazz[methodName]) {
            console.log("Class or method not found: " + className + "." + methodName);
            return;
        }

        clazz[methodName].overloads.forEach(function(overload) {
            if (overload.argumentTypes.length === argCount) { 
                overload.implementation = function() {
                    console.log("Entering " + className + "." + methodName);
                    for (var i = 0; i < arguments.length; i++) {
                        var arg = arguments[i];
                        var argType = (arg === null) ? "null" : typeof arg;
                        if (argType === "object") {
                          try {
                            argType = arg.getClass().getName(); // 尝试获取 Java 类名
                          } catch (e) {
                            // 处理异常（可能是非 Java 对象）
                          }
                        }
                        console.log("Arg[" + i + "]: " + arguments[i]);
                        if (argType == target_class){
                            if (arguments[i].indexOf(label)!=-1){
                                arguments[i] = arguments[i].replace(key, new_key)
                                arguments[i] = arguments[i].replace(value, new_value)
                            }
                        }
                    }

                    var retval = this[methodName].apply(this, arguments); // 调用原方法
                    console.log("Leaving " + className + "." + methodName);
                    console.log("Return value: " + retval);
                    return retval;
                };
            }
        });
    });
});