var functionsToHook = [["com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge", "_handleMessageFromJs", 5]]

var target_class = "string"

var label = "current_value"

var key = "Power"

var value = "0"

var control_commands = [{1:[1,2,3]}]

var platform = "Xiaomi"

var data_type = [[["int", "long", "string", "double", "float", "bool"], ["int", "long", "string", "double", "float", "bool"], "int", "long", "string", "double", "float", "bool"]]

const MAX_INT_32 = 2147483647;
const MIN_INT_32 = -2147483648;


class RandomValues {
    constructor() {
        this.proposed_vals = {
            'int': {
                'fun': [this.low_pos, this.low_neg, this.big_pos, this.big_neg],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'long': {
                'fun': [this.low_pos, this.low_neg, this.big_pos, this.big_neg],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'float': {
                'fun': [this.low_pos_float, this.low_neg_float, this.big_pos_float, this.big_neg_float],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'double': {
                'fun': [this.low_pos, this.low_neg, this.big_pos, this.big_neg],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'boolean': {
                'fun': [this.true_Low, this.false_Low],
                'dist': [0.5, 0.5]
            },
            'string': {
                'fun': [this.printable_chars],
                'dist': [1]
            },
        };

        Object.getOwnPropertyNames(RandomValues.prototype)
              .filter(prop => typeof this[prop] === 'function')
              .forEach(method => this[method] = this[method].bind(this));
    }

    randomChoice(arr, dist) {
        let acc = 0;
        let sum = dist.reduce((acc, val) => acc + val, 0);
        let rand = Math.random() * sum;
        for (let i = 0; i < dist.length; i++) {
            acc += dist[i];
            if (rand < acc) {
                return arr[i]();
            }
        }
    }

    randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    randomFloat(min, max) {
        return Math.random() * (max - min) + min;
    }

    low_pos() {
        return this.randomInt(0, 255);
    }

    low_neg() {
        return this.randomInt(-255, 0);
    }

    big_pos() {
        return this.randomInt(MAX_INT_32 / 2, MAX_INT_32);
    }

    big_neg() {
        return this.randomInt(MIN_INT_32, MIN_INT_32 / 2);
    }

    low_pos_float() {
        return this.randomFloat(0.0, 255.0);
    }

    low_neg_float() {
        return this.randomFloat(-255.0, 0.0);
    }

    big_pos_float() {
        return this.randomFloat(MAX_INT_32 / 2, MAX_INT_32);
    }

    big_neg_float() {
        return this.randomFloat(MIN_INT_32, MIN_INT_32 / 2);
    }

    true_Low() {
        return true;
    }

    false_Low() {
        return false;
    }

    printable_chars() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const length = this.randomInt(1, 255);
        let result = '"';
        for (let i = 0; i < length; i++) {
            result += characters.charAt(Math.floor(Math.random() * characters.length));
        }
        return result + '"';
    }
    generateByTypeName(typeName) {
        if (this.proposed_vals[typeName]) {
            return this.randomChoice(this.proposed_vals[typeName].fun, this.proposed_vals[typeName].dist);
        } else {
            throw new Error(`No random value generator defined for type: ${typeName}`);
        }
    }
}

function generate_data_type(index, valueIndex){
    dataTypeArray = data_type[index][valueIndex]
    var randomIndex = Math.floor(Math.random() * dataTypeArray.length);
    var data_type = dataTypeArray[randomIndex];
    return data_type;
}

function generate_value_for_specific_data_type(data_type){
    const randomValues = new RandomValues();
    var randomValue = randomValues.generateByTypeName(data_type);
    return randomValue;
}

function fuzzing_value_generation(index, valueIndex){
    var data_type = generate_data_type(index,valueIndex);
    var value = generate_value_for_specific_data_type(data_type);
    return value;
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
                                commandValueArray = command_select();
                                commandKey_1 = commandValueArray[0];
                                commandKey_2 = commandValueArray[1];
                                key_1_index = commandValueArray[2];
                                key_2_index = commandValueArray[3];
                                var new_value = fuzzing_value_generation(key_1_index, key_2_index);
                                if (platform == "Jingdong"){
                                    arguments[i] = arguments[i].replace(key, commandKey_2);
                                    arguments[i] = arguments[i].replace(value, new_value);
                                }
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