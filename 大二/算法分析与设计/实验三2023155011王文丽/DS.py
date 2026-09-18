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


def d_satur(graph, max_colors):
    """
    使用DSATUR算法对图进行着色，并控制颜色数量
    :param graph: 图的邻接表
    :param max_colors: 最大可用颜色数
    :return: 每个顶点的着色结果，如果无法着色则返回 None
    """
    num_vertices = len(graph)
    colors = [-1] * num_vertices
    saturation = [set() for _ in range(num_vertices)]

    # 初始选择一个度数最大的顶点着色
    start_vertex = max(range(num_vertices), key=lambda v: len(graph[v]))
    colors[start_vertex] = 0
    # 更新相邻顶点的饱和度
    for neighbor in graph[start_vertex]:
        saturation[neighbor].add(0)
            # 调试信息，可查看饱和度更新情况
        print(f"更新顶点 {neighbor + 1} 的饱和度，添加颜色 {0}")

    for _ in range(num_vertices - 1):
        # 计算未着色顶点的饱和度
        uncolored_vertices = [v for v in range(num_vertices) if colors[v] == -1]
        max_saturation = -1
        next_vertex = None
        for v in uncolored_vertices:
            sat = len(saturation[v])
            if sat > max_saturation:
                max_saturation = sat
                next_vertex = v
            elif sat == max_saturation and len(graph[v]) > len(graph[next_vertex]):
                next_vertex = v

        # 为选择的顶点分配最小可用颜色
        available_colors = set(range(max_colors)) - saturation[next_vertex]
        if len(available_colors) < 1:
            print("无法使用给定的颜色数量完成填色。")
            return None
        min_color = min(available_colors)
        colors[next_vertex] = min_color
        print(f"选择顶点 {next_vertex + 1} 着色为颜色 {min_color}")

        # 更新相邻顶点的饱和度
        for neighbor in graph[next_vertex]:
            if min_color not in saturation[neighbor]:
                saturation[neighbor].add(min_color)
                # 调试信息，可查看饱和度更新情况
                print(f"更新顶点 {neighbor + 1} 的饱和度，添加颜色 {min_color}")
                      
    return colors


# 从文件读取边信息并构建图的邻接表
file_path = 'le450_25a.txt'
graph = parse_edges_from_file(file_path)

if graph:
    # 最大可用颜色数
    max_colors = 25

    # 进行填色
    colors = d_satur(graph, max_colors)

    if colors:
        print("DSATUR算法填色成功，各顶点的颜色如下：")
        for vertex, color in enumerate(colors):
            print(f"顶点 {vertex + 1} 的颜色为: {color}")
        # 检查相邻顶点颜色是否相同
        # for vertex in range(len(graph)):
        #     for neighbor in graph[vertex]:
        #         if colors[vertex] == colors[neighbor]:
        #             print(f"错误：顶点 {vertex + 1} 和顶点 {neighbor + 1} 相邻但颜色相同，颜色为 {colors[vertex]}")
    else:
        print("涂色失败，未生成涂色方案。")
    