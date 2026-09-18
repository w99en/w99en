import time
import sys


def is_safe(vertex, color, graph, colors):
    """
    检查给顶点 vertex 分配颜色 color 是否安全
    :param vertex: 当前顶点
    :param color: 要分配的颜色
    :param graph: 图的邻接表表示
    :param colors: 顶点的颜色分配列表
    :return: 如果安全返回 True，否则返回 False
    """
    for neighbor in graph[vertex]:
        if colors[neighbor] == color:
            return False
    return True


def get_available_colors(vertex, graph, colors, num_colors):
    """
    获取顶点的可用颜色列表
    """
    available = [True] * (num_colors + 1)
    for neighbor in graph[vertex]:
        if colors[neighbor] != 0:
            available[colors[neighbor]] = False
    return [i for i in range(1, num_colors + 1) if available[i]]


def mrv_dh_heuristic(graph, colors, num_colors):
    """
    MRV 和 DH 启发式策略，选择下一个要着色的顶点
    """
    min_remaining = float('inf')
    max_degree = -1
    next_vertex = None
    for vertex in range(len(graph)):
        if colors[vertex] == 0:
            available_colors = get_available_colors(vertex, graph, colors, num_colors)
            remaining = len(available_colors)
            degree = len(graph[vertex])
            if remaining < min_remaining or (remaining == min_remaining and degree > max_degree):
                min_remaining = remaining
                max_degree = degree
                next_vertex = vertex
    return next_vertex


def graph_coloring_util(graph, num_colors, colors, start_vertex=None):
    """
    回溯算法的核心递归函数
    :param graph: 图的邻接表表示
    :param num_colors: 可用的颜色数量
    :param colors: 顶点的颜色分配列表
    :param start_vertex: 开始涂色的顶点
    :return: 如果可以完成填色返回 True，否则返回 False
    """
    all_colored = True
    for color in colors:
        if color == 0:
            all_colored = False
            break
    if all_colored:
        return True

    if start_vertex is not None and colors[start_vertex] == 0:
        vertex = start_vertex
    else:
        vertex = mrv_dh_heuristic(graph, colors, num_colors)

    available_colors = get_available_colors(vertex, graph, colors, num_colors)
    print(f"正在尝试为顶点 {vertex + 1} 分配颜色")
    for color in available_colors:
        if is_safe(vertex, color, graph, colors):
            colors[vertex] = color
            if graph_coloring_util(graph, num_colors, colors):
                return True
            colors[vertex] = 0
            print(f"为顶点 {vertex + 1} 分配颜色 {color} 失败，回溯")

    return False


def graph_coloring(graph, num_colors, start_vertex=None):
    """
    主填色函数
    :param graph: 图的邻接表表示
    :param num_colors: 可用的颜色数量
    :param start_vertex: 开始涂色的顶点
    :return: 如果可以完成填色返回颜色分配列表，否则返回 None
    """
    num_vertices = len(graph)
    colors = [0] * num_vertices

    if graph_coloring_util(graph, num_colors, colors, start_vertex):
        return colors
    else:
        return None


def parse_edges_from_file(file_path):
    """
    从文件中读取边信息并构建图的邻接表
    :param file_path: 文件路径
    :return: 图的邻接表
    """
    graph = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('e'):
                    _, vertex1, vertex2 = line.split()
                    vertex1 = int(vertex1) - 1
                    vertex2 = int(vertex2) - 1
                    if vertex1 not in graph:
                        graph[vertex1] = []
                    if vertex2 not in graph:
                        graph[vertex2] = []
                    graph[vertex1].append(vertex2)
                    graph[vertex2].append(vertex1)

        # 确保所有顶点都有对应的邻接表
        num_vertices = max(graph.keys()) + 1 if graph else 0
        for i in range(num_vertices):
            if i not in graph:
                graph[i] = []

        return graph
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
        return {}


start_time = time.time()
# 从文件读取边信息并构建图的邻接表
file_path = 'le450_15b.txt'
graph = parse_edges_from_file(file_path)

if graph:
    # 可用的颜色数量
    num_colors = 15
    start_vertex = 2 # 节点 338 的索引是 337

    # 进行填色
    colors = graph_coloring(graph, num_colors, start_vertex)

    if colors:
        print("填色成功，各顶点的颜色如下：")
        for vertex, color in enumerate(colors):
            print(f"顶点 {vertex + 1} 的颜色为: {color}")
    else:
        print("无法使用给定的颜色数量完成填色。")
# 记录结束时间
end_time = time.time()

# 计算运行时间
run_time = end_time - start_time
print(f"程序运行时间: {run_time:.4f} 秒")