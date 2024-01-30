package soot_call_graph.test;

import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.xmlpull.v1.XmlPullParserException;
import soot_call_graph.test.CGExporter;

import soot.MethodOrMethodContext;
import soot.PackManager;
import soot.Scene;
import soot.SootClass;
import soot.SootMethod;
import soot.jimple.infoflow.InfoflowConfiguration.CallgraphAlgorithm;
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration;
import soot.jimple.infoflow.android.SetupApplication;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Edge;
import soot.jimple.toolkits.callgraph.Targets;
import soot.options.Options;

public class CGGenerator {
    public final static String androidPlatformPath = "E:/flowdroid/android-platforms-master/android-platforms-master/";
    public final static String appPath = "E:/flowdroid/SmartHome-DB-Sdk-Dev-78006-9.0.605-4059-develop-20231130.apk";
    public final static String outputPath = "E:/flowdroid/sootOutput/";
    public final static String sourceSinkFile = "E:/flowdroid/CallGraph_source.txt";
    static Object ob = new Object();

    private static Map<String,Boolean> visited = new HashMap<String,Boolean>();
    private static CGExporter cge = new CGExporter();

    public static void main(String[] args) throws IOException, XmlPullParserException{
        
        // Provide the path to the APK file
        String apkPath = "E:/flowdroid/SmartHome-DB-Sdk-Dev-77400-8.7.501-2066-develop-20230706.apk";

        soot.G.reset();
        Options.v().set_output_format(Options.output_format_jimple);
        Options.v().set_allow_phantom_refs(true);
        Options.v().set_process_dir(Collections.singletonList(apkPath));
        Options.v().set_src_prec(Options.src_prec_apk);
        Options.v().set_android_jars("E:/flowdroid/android-platforms-master/android-platforms-master/");
        Options.v().set_whole_program(true);
        Options.v().set_process_multiple_dex(true);

        System.out.println("before Call Graph:");

        // Load the APK file
        Scene.v().loadNecessaryClasses();

        // Build the call graph
        PackManager.v().getPack("cg").apply();
        CallGraph callGraph = Scene.v().getCallGraph();

        // Print the call graph
        System.out.println("Call Graph:");

        // Print the call graph (you can customize the output format)
        System.out.println(callGraph);
        for (SootMethod method : Scene.v().getEntryPoints()) {
            if (method.isConcrete()) {
                Iterator<Edge> edges = cg.edgesOutOf(method);
                while (edges.hasNext()) {
                    Edge edge = edges.next();
                    System.out.println(method + " -> " + edge.getTgt());
                }
            }
        }
        
//      final InfoflowAndroidConfiguration config = new InfoflowAndroidConfiguration();
//      config.getAnalysisFileConfig().setTargetAPKFile(appPath);
//      config.getAnalysisFileConfig().setAndroidPlatformDir(androidPlatformPath);
//      config.setMergeDexFiles(true);
//      // config.setCodeEliminationMode(InfoflowConfiguration.CodeEliminationMode.NoCodeElimination);
//      config.setCallgraphAlgorithm(CallgraphAlgorithm.CHA); // CHA or SPARK
//      SetupApplication app = new SetupApplication(config);
//      System.out.print("before  runInfoflow \n");
//      Options.v().set_whole_program(true);
//        Options.v().set_allow_phantom_refs(true);
//      //app.runInfoflow(sourceSinkFile);
//      System.out.print("before call graph\n");
//        // Iterate over the methods and print their names
//      app.constructCallgraph();
//      CallGraph callGraph = Scene.v().getCallGraph();
//      //SootMethod 
//      SootMethod entryPoint = app.getDummyMainMethod();
        CallGraph cg = Scene.v().getCallGraph();
        //visit(cg,entryPoint);
        //cge.exportMIG("flowdroidCFG", outputPath);
        //String className_pre = "com.tuya.smart.rnplugin.tyrctcameramanager.TYRCTCameraManager";
        String className_pre = "com.xiaomi.router.miio.miioplugin$Stub";
        SootClass sootClass = Scene.v().loadClassAndSupport(className_pre);
        sootClass.setApplicationClass();

        for (SootMethod method : sootClass.getMethods()) {
            System.out.println(method.getSignature());
        }

        SootClass sootClass_new = Scene.v().forceResolve(className_pre, SootClass.BODIES);
        if (sootClass_new.isPhantom()) {
            System.out.println(className_pre + " does not exist in the APK.");
        } else {
            System.out.println(className_pre + " exists in the APK.");
        }
        SootClass sootClass1 = Scene.v().loadClassAndSupport(className_pre);
        sootClass1.setApplicationClass();
        // Get all methods in the class
        List<SootMethod> methods = sootClass1.getMethods();

        // Iterate over the methods and print their names
        for (SootMethod method : methods) {
            System.out.println("Method: " + method.getName());
        }
        
        className_pre = "com.xiaomi.router.miio.miioplugin";
        sootClass_new = Scene.v().forceResolve(className_pre, SootClass.BODIES);
        if (sootClass_new.isPhantom()) {
            System.out.println(className_pre + " does not exist in the APK.");
        } else {
            System.out.println(className_pre + " exists in the APK.");
        }
        SootClass sootClass11 = Scene.v().loadClassAndSupport(className_pre);
        sootClass11.setApplicationClass();
        // Get all methods in the class
        List<SootMethod> methods1 = sootClass11.getMethods();

        // Iterate over the methods and print their names
        for (SootMethod method : methods1) {
            System.out.println("Method: " + method.getName());
        }
        //tuya
        //String targetMethodName = "<com.tuya.smart.rnplugin.tyrctcameramanager.TYRCTCameraManager: void startPtzLeft()>"; 
        
//        //Xiaomi
        String targetMethodName = "<com.xiaomi.router.miio.miioplugin$Stub: boolean onTransact(int,android.os.Parcel,android.os.Parcel,int)>"; 
        //String targetMethodName = "<com.bsgamesdk.android.BSGameSdk: void login(com.bsgamesdk.android.callbacklistener.CallbackListener)>"; 
//        String targetMethodName = "<com.bsgamesdk.android.BSGameSdk: com.bsgamesdk.android.BSGameSdk initialize(boolean,android.app.Activity,java.lang.String,java.lang.String,java.lang.String,java.lang.String,android.os.Handler)>";

        SootMethod targetMethod = Scene.v().grabMethod(targetMethodName);

        if (targetMethod != null) {
             Iterator<MethodOrMethodContext> ctargets = new Targets(callGraph.edgesInto(targetMethod));
             if (ctargets != null) {
               while (ctargets.hasNext()) {
                  SootMethod child = (SootMethod) ctargets.next();
                  System.out.println(targetMethodName +" may call" + child);
                  if (!visited.containsKey(child.getSignature())) visit(callGraph, child);
               }
             }
        }
        if (targetMethod != null) {
            Iterator<MethodOrMethodContext> ctargets = new Targets(callGraph.edgesOutOf(targetMethod));
            if (ctargets != null) {
              while (ctargets.hasNext()) {
                 SootMethod child = (SootMethod) ctargets.next();
                 System.out.println(targetMethodName +" may call" + child);
                 if (!visited.containsKey(child.getSignature())) visit(callGraph, child);
              }
            }
//            for (Iterator<Edge> it = callGraph.edgesOutOf(targetMethod); it.hasNext();) {
//                Edge edge = it.next();
//                SootMethod srcMethod = edge.getSrc().method();
//                System.out.println(srcMethod.getSignature());
//            }
        }
        String className = "com.tuya.smart.rnplugin.tyrctcameramanager.TYRCTCameraManager";
        
        SootClass sootClass111 = Scene.v().loadClassAndSupport(className_pre);
        sootClass111.setApplicationClass();
        // Get all methods in the class
        List<SootMethod> methods11 = sootClass111.getMethods();

        // Iterate over the methods and print their names
        for (SootMethod method : methods11) {
            System.out.println("Method: " + method.getName());
        }
////        System.out.println("new");
//      className = "com.tuya.smart.camera.devicecontrol.MqttIPCCameraDeviceManager";
//      sootClass = Scene.v().loadClassAndSupport(className);
////        sootClass.setApplicationClass();
////        // Get all methods in the class
////        methods = sootClass.getMethods();
////        for (SootMethod method : methods) {
////            System.out.println("Method: " + method.getName());
////        }
//        String methodName = "startPtz";
//        String methodSubSignature = "void startPtz(com.tuya.smart.camera.devicecontrol.mode.PTZDirection)";
////        String methodName = "startPtzLeft";
////        String methodSubSignature = "void startPtzLeft()";
//        targetMethod = sootClass.getMethod(methodSubSignature);
//
//        if (targetMethod != null) {
//            System.out.println("调用 " + targetMethodName + " 的方法：");
//            for (Iterator<Edge> it = callGraph.edgesInto(targetMethod); it.hasNext();) {
//                Edge edge = it.next();
//                SootMethod srcMethod = edge.getSrc().method();
//                System.out.println(srcMethod.getSignature());
//            }
//        }
//        if (sootClass.declaresMethodByName(methodName)) {
//            SootMethod method = sootClass.getMethod(methodSubSignature);
//            System.out.println("Found method: " + method.getSignature());
//            Iterator<Edge> edgeIterator = callGraph.edgesInto(method);
//            while (edgeIterator.hasNext()) {
//                Edge edge = edgeIterator.next();
//                SootMethod tgt = edge.getTgt().method();
//                System.out.println("before tgt" + tgt.getSignature());
//                System.out.println("  " + tgt.getSignature());
//            }
//        }else {
//            System.out.println("Method not found in class.");
//        }
//        if (sootClass.declaresMethodByName(methodName)) {
//            SootMethod method = sootClass.getMethod(methodSubSignature);
//            System.out.println("Found method: " + method.getSignature());
//            visit(callGraph,method);
//            cge.exportMIG("flowdroidCFG", outputPath);
//        } else {
//            System.out.println("Method not found in class.");
//        }
//        SetupApplication app = new SetupApplication(androidPlatformPath, appPath);
//        soot.G.reset();
//        //传入AndroidCallbacks文件
//        app.setCallbackFile(CGGenerator.class.getResource("/AndroidCallbacks.txt").getFile());
//        app.constructCallgraph();
//
//        //SootMethod 
//        SootMethod entryPoint = app.getDummyMainMethod();
//        CallGraph cg = Scene.v().getCallGraph();
//        visit(cg,entryPoint);
//        cge.exportMIG("flowdroidCFG", outputPath);
//      System.out.println("Method not found in class.");

    }
//    public static void main(String[] args) throws IOException, XmlPullParserException{
//        // Configure Soot for APK analysis
//      Options.v().set_src_prec(Options.src_prec_apk);
//
//        Options.v().set_android_jars(androidPlatformPath);
//        Options.v().set_process_dir(Collections.singletonList(appPath)); // Replace with APK path
//        Options.v().set_whole_program(true);
//        Options.v().set_allow_phantom_refs(true);
//        Options.v().set_process_multiple_dex(true);
//        Options.v().set_output_format(Options.output_format_none);
//
//        // Enable call graph generation
//        Options.v().setPhaseOption("cg.spark", "on");
//
//        // Load classes and methods from APK
//        Scene.v().loadNecessaryClasses();
//        System.out.println("test");
//        // Execute Soot
//        PackManager.v().runPacks();
//        
//        // Retrieve and process the call graph
//        CallGraph callGraph = Scene.v().getCallGraph();
//        String targetFunctionSignature = "com.tuya.smart.camera.devicecontrol.MqttIPCCameraDeviceManager。startPtz(com.tuya.smart.camera.devicecontrol.mode.PTZDirection)";
//        for (Edge edge : callGraph) {
//            SootMethod srcMethod = edge.src();
//            SootMethod tgtMethod = edge.tgt();
//
//            if (tgtMethod.getSignature().equals(targetFunctionSignature)) {
//                // Found a caller of the target function
//                System.out.println("Caller Method: " + srcMethod.getSignature());
//                // You can analyze or store information about the caller method here
//            }
//        }
//        System.out.println("test");
//
//
////        SetupApplication app = new SetupApplication(androidPlatformPath, appPath);
////        soot.G.reset();
////        //传入AndroidCallbacks文件
////        app.setCallbackFile(CGGenerator.class.getResource("/AndroidCallbacks.txt").getFile());
////        app.constructCallgraph();
////
////        //SootMethod 
        SootMethod entryPoint = app.getDummyMainMethod();
        CallGraph cg = Scene.v().getCallGraph();
        visit(cg,entryPoint);
        cge.exportMIG("flowdroidCFG", outputPath);
//    }
    private static boolean isJavaLibraryMethod(SootMethod method) {
        String packageName = method.getDeclaringClass().getPackageName();
        System.out.println(packageName.startsWith("java.") || packageName.startsWith("javax.") || packageName.startsWith("sun."));
        return packageName.startsWith("java.") || packageName.startsWith("javax.") || packageName.startsWith("sun.");
    }
    private static void visit(CallGraph cg,SootMethod m){
        String identifier = m.getSignature();
        visited.put(identifier, true);
        cge.createNode(identifier);
        Iterator<MethodOrMethodContext> ptargets = new Targets(cg.edgesInto(m));
        if(ptargets != null){
            while(ptargets.hasNext())
            {
                SootMethod p = (SootMethod) ptargets.next();
                if(p == null){
                    System.out.println("p is null");
                }
                if(!visited.containsKey(p.getSignature())){
                    visit(cg,p);
                }
            }
        }
        Iterator<MethodOrMethodContext> ctargets = new Targets(cg.edgesOutOf(m));
        if(ctargets != null){
            while(ctargets.hasNext())
            {
                SootMethod c = (SootMethod) ctargets.next();
                if(c == null){
                    System.out.println("c is null");
                }
                cge.createNode(c.getSignature());
                cge.linkNodeByID(identifier, c.getSignature());
                if(!visited.containsKey(c.getSignature())){
                    visit(cg,c);
                }
            }
        }
    }
}
