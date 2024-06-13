# RIoTFuzzer: Companion App Assisted Remote Fuzzing for Detecting Vulnerabilities in IoT Devices

## Demo

1. First reverse engineer the companion app with apktool (take JD Home app as example)
```shell
  java -jar apktool.jar d om.jd.iots.apk
```
2. Finding the border fucntion
```shell
  python3 find_jsinterfacemethod.py
```

3. Identify the mutation point
    * Configure the target_function in the  `find_mutation_point_with_hook.js` to the border functions found in last step.
    * Run the frida server in Android phone
    * find mutation point with frida 
    ```
      frida -U om.jd.iots -l find_mutation_point_with_hook.js
    ```
    * If does not identify the control command,   perform further call graph analysis
    ```
      python3 analyze_cg.py
    ```
4. After discovering the mutation point, start remote fuzzing
```
  frida -U om.jd.iots -l mutation_with_hook.js
```
