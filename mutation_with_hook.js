var functionsToHook = [["com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge", "_handleMessageFromJs", 5]];

var target_class = "string";

var label = "\"current_value\"";

var key_1 = "Power";

var key_2;

var ori_value = ["\"current_value\":1", "\"current_value\":0"];

var ori_value_key = "\"current_value\":"

var control_commands = [{1:["CurrentPowerSum", "Electric", "Power", "Voltage"]}];

var platform = "Jingdong";

// var functionsToHook = [["cafebabe.ag2", "setDeviceInfo", 3]];

// var target_class = "string";

// var label = "\"on\"";

// var key_1 = "Power";

// var key_2 = "switch";

// var ori_value = ["\"on\":1", "\"on\":0"];

// var ori_value_key = "\"on\":"

// var control_commands = [{1:["CurrentPowerSum", "Electric", "Power", "Voltage"]}];

// var platform = "Huawei";

var all_data_type = ["float", "string", "int", "bool"];

var data_type;

var data_type_fuzzing = [];

var mode = "fuzzing";

var all_data_type_index = [0, 0, 0, 0];

var data_type_index;

const MAX_INT_32 = 2147483647;
const MIN_INT_32 = -2147483648;

function data_type_initial(){
    data_type = control_commands.map(command => {
        var key = Object.keys(command)[0];
        var values = command[key];
        return Array.from({length: values.length}, () => Array.from(all_data_type));
    });
    data_type_index = control_commands.map(command => {
        var key = Object.keys(command)[0];
        var values = command[key];
        return Array.from({length: values.length}, () => Array.from(all_data_type_index));
    });
}

class RandomValues {
    constructor() {
        this.proposed_vals = {
            'int': {
                'fun': [this.low_pos, this.low_neg, this.big_pos, this.big_neg],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'float': {
                'fun': [this.low_pos_float, this.low_neg_float, this.big_pos_float, this.big_neg_float],
                'dist': [0.25, 0.25, 0.25, 0.25]
            },
            'bool': {
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
        return Math.floor(Math.random() * 256);
    }

    low_neg() {
        return Math.floor(Math.random() * 255) - 255;
    }

    big_pos() {
        return Math.floor(Math.random() * (MAX_INT_32 / 2 + 1)) + MAX_INT_32 / 2;
    }

    big_neg() {
        return Math.floor(Math.random() * (0 - MIN_INT_32 / 2 + 1)) + MIN_INT_32;
    }
    low_pos_float() {
        return Math.random() * 255.0;
    }

    low_neg_float() {
        return Math.random() * 255.0 - 255.0;
    }

    big_pos_float() {
        return Math.random() * MAX_INT_32 / 2 + MAX_INT_32 / 2
    }

    big_neg_float() {
        return Math.random() * (0 - MIN_INT_32 / 2) + MIN_INT_32;
    }
    true_Low() {
        return true;
    }

    false_Low() {
        return false;
    }

    printable_chars() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const length = Math.floor(Math.random() * 3000) + 1
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

class RandomValuesCons {
    constructor() {
        this.proposed_vals = {
            'int': {
                'fun': [this.int_value],
                'dist': [1]
            },
            'float': {
                'fun': [this.float_value],
                'dist': [1]
            },
            'bool': {
                'fun': [this.true_Low, this.false_Low],
                'dist': [0.5, 0.5]
            },
            'string': {
                'fun': [this.printable_chars],
                'dist': [1]
            },
        };

        Object.getOwnPropertyNames(RandomValuesCons.prototype)
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

    int_value() {
        return Math.floor(Math.random() * 11);
    }

    float_value() {
        return Math.random() * 10.0;
    }

    true_Low() {
        return true;
    }

    false_Low() {
        return false;
    }

    printable_chars() {
        const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        const length = Math.floor(Math.random() * 4) + 1
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
    var dataTypeArray = data_type[index][valueIndex]
    var randomIndex = Math.floor(Math.random() * dataTypeArray.length);
    var data_type_tmp = dataTypeArray[randomIndex];
    return data_type_tmp;
}

function generate_value_for_specific_data_type(data_type_tmp){
    const randomValues = new RandomValues();
    var randomValue = randomValues.generateByTypeName(data_type_tmp);
    return randomValue;
}

function generate_infer_value_for_specific_data_type(data_type_tmp){
    const randomValues  = new RandomValuesCons();
    var randomValue = randomValues .generateByTypeName(data_type_tmp);
    return randomValue;
}

function fuzzing_value_generation(index, valueIndex){
    var mutate_data_type = generate_data_type(index,valueIndex);
    var value = generate_value_for_specific_data_type(mutate_data_type);
    return value;
}

function getNthKey(obj, n) {
    const keys = Object.keys(obj);
    try {
        return obj[keys][n];
    }
    catch (e) {
        return undefined;
    }
}

function infer_value_generation(){
    for (var i = 0; i < data_type_index.length; i++) {
        for (var j = 0; j < data_type_index[i].length; j++) {
            for (var k = 0; k < data_type_index[i][j].length; k++) {
                var value = data_type_index[i][j][k];
                if (value < 10) {
                    var mutate_data_type = data_type[i][j][k];
                    var mutation_value = generate_infer_value_for_specific_data_type(mutate_data_type);
                    var mutation_command = getNthKey(control_commands[i], j)
                    value = value + 1;
                    data_type_index[i][j][k] = value;
                    return [mutation_command, mutation_value];
                } else {
                    console.log(`Skipping value: ${value} at [${i}][${j}][${k}]`);
                    continue;
                }
            }
        }
    }
    return false;
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
    data_type_initial()
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
                        if (argType == target_class){
                            if (arguments[i].indexOf(label)!=-1){
                                var commandValueArray = command_select();
                                var commandKey_1 = commandValueArray[0];
                                var commandKey_2 = commandValueArray[1];
                                var key_1_index = commandValueArray[2];
                                var key_2_index = commandValueArray[3];
                                if (mode == "infer") {
                                    var mutated_value = infer_value_generation();
                                    if (mutated_value == false){
                                        mode = "fuzzing";
                                    }
                                    else{
                                        commandKey_2 = mutated_value[0];
                                        new_value = mutated_value[1];
                                    }
                                }
                                else if (mode == "fuzzing"){
                                    var new_value = fuzzing_value_generation(key_1_index, key_2_index);
                                }
                                if (platform == "Jingdong" || platform == "Tuya"){
                                    arguments[i] = arguments[i].replace(key_1, commandKey_2);
                                }
                                else if (platform == "xiaomi" || platform == "huawei"){
                                    arguments[i] = arguments[i].replace(key_1, commandKey_1);
                                    arguments[i] = arguments[i].replace(key_2, commandKey_2);
                                }
                                for (var index = 0; index < arguments.length; index++) {
                                    if (arguments[i].indexOf(ori_value[index]) != -1){
                                        arguments[i] = arguments[i].replace(ori_value[index], ori_value_key+new_value);
                                        console.log(arguments[i]);
                                        break;
                                    }
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
