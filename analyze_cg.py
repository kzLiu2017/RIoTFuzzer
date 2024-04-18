from igraph import *

def get_vertex_info(graph, vertex_ids):
    for vid in vertex_ids:
        label = graph.vs[vid]['label'] if 'label' in graph.vs[vid].attributes() else '无标签'
        print(f"顶点ID: {vid}, 标签: {label}")

def get_successors(graph, target_func):
    target_func_index = 0

    # 打印每个顶点的索引和对应的标签
    for idx, label in enumerate(labels):
        if target_func in label:
            target_func_index = idx
            print(f"Vertex {idx}: Label = {label}")
            print(target_func_index)

    if g.is_directed():
        successors = g.successors(target_func_index)
        print(f"由顶点ID {target_func_index} 直接指向的节点和标签:")
        get_vertex_info(g, successors)

def match_interface_implement(graph, target_func):
    for idx, label in enumerate(labels):
        if target_func in label:
            print(f"Vertex {idx}: Label = {label}")

g = Graph.Read_GML("/Data/diane-docker/workdir/tuya/callgraph.gml")
skip = ["bluetooth"]
# 获取所有顶点的标签
labels = g.vs['label']
# target_func = "com/xiaomi/smarthome/core/server/ICoreApi$Stub;->onTransact"
# target_func = "sendSmartHomeRequest"
# target_func = "startPtzLeft"
target_func = "startPtz("
get_successors(g, target_func)
# match_interface_implement(g, target_func)

