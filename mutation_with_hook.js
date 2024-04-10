var functionsToHook = [["com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge", "_handleMessageFromJs", 5]]

var target_class = "string"

var label = "current_value"

var key = "Power"

var value = "0"

var new_key = "power"

var new_value = "123"

Java.perform(function() {
    functionsToHook.forEach(function(functionInfo) {
        var className = functionInfo[0];
        var methodName = functionInfo[1];
        var argCount = functionInfo[2]; // 注意：这里的参数个数仅用于确定重载方法，可能需要更详细的信息来正确匹配方法签名

        var clazz = Java.use(className);
        if (!clazz || !clazz[methodName]) {
            console.log("Class or method not found: " + className + "." + methodName);
            return;
        }

        // 对于有重载的方法，需要具体指定哪一个版本的方法
        clazz[methodName].overloads.forEach(function(overload) {
            if (overload.argumentTypes.length === argCount) { // 匹配参数个数
                overload.implementation = function() {
                    console.log("Entering " + className + "." + methodName);
                    // 打印所有参数
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
                    return retval; // 返回原方法的返回值
                };
            }
        });
    });
});