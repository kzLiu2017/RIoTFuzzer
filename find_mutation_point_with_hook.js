// var target_function = [
//     [
//         "com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge",
//         "_handleMessageFromJs",
//         [
//             "java.lang.String",
//             "java.lang.String",
//             "java.lang.String",
//             "java.lang.String",
//             "java.lang.String",
//         ],
//         "void"
//     ]
// ]
var target_function = [
    [
        "com.jd.smart.dynamiclayout.view.html.WebViewJavascriptBridge",
        "_handleMessageFromJs",
        [
            "java.lang.String",
            "java.lang.String",
            "java.lang.String",
            "java.lang.String",
            "java.lang.String",
        ],
        "void"
    ]
]

var label = "Power"

function main() {
    target_function.forEach(function (hookTarget) {
        const className = hookTarget[0];
        const methodName = hookTarget[1];
        const argsTypes = hookTarget[2];
        const returnType = hookTarget[3];

        const methodSignature = argsTypes.join(", ");

        // console.log(`Hooking ${className}.${methodName} with args [${methodSignature}] and return type ${returnType}`);

        const clazz = Java.use(className);

        const method = clazz[methodName].overload(...argsTypes);

        method.implementation = function (...args) {
            if (JSON.stringify(args).indexOf(label) != -1){
                console.log(`Called ${methodName} with args: ${JSON.stringify(args)}`);
            }

            const result = this[methodName](...args);

            //console.log(`Method ${methodName} returned: ${JSON.stringify(result)}`);

            return result;
        };
    });
}

Java.perform(function () {
    main();
});