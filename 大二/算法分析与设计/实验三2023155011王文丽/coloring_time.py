import time
import random
import sys
import matplotlib.pyplot as plt

# 设置递归深度限制
sys.setrecursionlimit(10000)


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


def graph_coloring_util(graph, num_colors, vertices_order, index, colors):
    """
    回溯算法的核心递归函数
    :param graph: 图的邻接表表示
    :param num_colors: 可用的颜色数量
    :param vertices_order: 顶点排序后的列表
    :param index: 当前要填色的顶点在排序列表中的索引
    :param colors: 顶点的颜色分配列表
    :return: 如果可以完成填色返回 True，否则返回 False
    """
    if index == len(vertices_order):
        return True

    vertex = vertices_order[index]
    available_colors = get_available_colors(vertex, graph, colors, num_colors)
    for color in available_colors:
        if is_safe(vertex, color, graph, colors):
            colors[vertex] = color
            if graph_coloring_util(graph, num_colors, vertices_order, index + 1, colors):
                return True
            colors[vertex] = 0

    return False


def graph_coloring(graph, num_colors):
    """
    主填色函数
    :param graph: 图的邻接表表示
    :param num_colors: 可用的颜色数量
    :return: 如果可以完成填色返回颜色分配列表，否则返回 None
    """
    num_vertices = len(graph)
    colors = [0] * num_vertices

    # 按度数对顶点进行排序
    vertices_order = sorted(range(num_vertices), key=lambda v: len(graph[v]), reverse=True)

    if graph_coloring_util(graph, num_colors, vertices_order, 0, colors):
        return colors
    else:
        return None


def generate_random_graph(num_vertices, edge_probability):
    """
    随机生成图的邻接表
    :param num_vertices: 顶点数量
    :param edge_probability: 边出现的概率
    :return: 图的邻接表
    """
    graph = {i: [] for i in range(num_vertices)}
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_probability:
                graph[i].append(j)
                graph[j].append(i)
    return graph


# 可用的颜色数量
num_colors = 4
# 不同的图规模
sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500]
# 边出现的概率
edge_probability = 0.2
# 存储每个规模图的运行时间
run_times = []

for size in sizes:
    # 随机生成图
    graph = generate_random_graph(size, edge_probability)

    # 记录开始时间
    start_time = time.time()

    # 进行填色
    colors = graph_coloring(graph, num_colors)

    # 记录结束时间
    end_time = time.time()

    # 计算运行时间
    run_time = end_time - start_time
    run_times.append(run_time)

    print(f"图规模: {size}, 运行时间: {run_time:.4f} 秒")

# 绘制图表
plt.plot(sizes, run_times, marker='o')
plt.xlabel('number of vertices')
plt.ylabel('running time (seconds)')
plt.title('Running time of graph coloring algorithm')
plt.grid(True)
plt.show()
    