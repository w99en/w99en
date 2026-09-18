import sys
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            if self.rank[x_root] == self.rank[y_root]:
                self.rank[x_root] += 1


def read_graph(filename):
    """读取图文件并返回顶点数、边数、边列表和邻接表"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

            if len(lines) < 2:
                raise ValueError("文件格式错误：至少需要包含顶点数和边数")

            V = int(lines[0])
            E = int(lines[1])

            edges = []
            adj = defaultdict(list)
            max_vertex = 0

            for line in lines[2:]:
                try:
                    u, v = map(int, line.split())
                    edges.append((u, v))
                    adj[u].append(v)
                    adj[v].append(u)
                    max_vertex = max(max_vertex, u, v)
                except ValueError:
                    continue

            if max_vertex >= V:
                print(f"警告：文件声明的顶点数{V}小于实际最大顶点编号{max_vertex}")
                V = max_vertex + 1

            for i in range(V):
                if i not in adj:
                    adj[i] = []

            print(f"成功读取图: {V}个顶点, {len(edges)}条边")
            return V, len(edges), edges, adj

    except FileNotFoundError:
        print(f"错误：文件 {filename} 未找到")
        sys.exit(1)
    except Exception as e:
        print(f"读取文件时出错: {e}")
        sys.exit(1)


def is_connected(V, adj):
    """检查图是否连通"""
    if V == 0:
        return True

    visited = set()
    start_node = next(iter(adj))

    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == V


def baseline_find_bridges(V, adj, edges):
    """基准算法：逐个移除边检查连通性"""
    bridges = []
    original_adj = defaultdict(list)

    for u in adj:
        original_adj[u] = adj[u].copy()

    for u, v in edges:
        if v in adj[u]:
            adj[u].remove(v)
            adj[v].remove(u)

            if not is_connected(V, adj):
                bridges.append((u, v))

            adj[u].append(v)
            adj[v].append(u)

    for u in original_adj:
        adj[u] = original_adj[u].copy()

    return bridges


def efficient_find_bridges(V, adj):
    """高效算法：使用DFS和时间戳"""
    bridges = []
    disc = [-1] * V
    low = [-1] * V
    time = [0]
    parent = [-1] * V

    def dfs(u):
        disc[u] = low[u] = time[0]
        time[0] += 1
        for v in adj[u]:
            if disc[v] == -1:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(V):
        if disc[i] == -1:
            dfs(i)

    return bridges


def visualize_graph(edges, bridges, title="Graph with Bridges"):
    """可视化图形并高亮显示桥"""
    G = nx.Graph()
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)  # 布局算法

    # 绘制图形
    plt.figure(figsize=(10, 8))

    # 绘制普通边（灰色）
    nx.draw_networkx_edges(G, pos, edgelist=[e for e in G.edges() if e not in bridges and (e[1], e[0]) not in bridges],
                           edge_color='gray', width=1)

    # 绘制桥（红色加粗）
    nx.draw_networkx_edges(G, pos, edgelist=bridges, edge_color='red', width=3)

    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')

    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=12)

    plt.title(title)
    plt.axis('off')
    plt.show()


def main():
    # 使用原始字符串避免转义问题
    filename = r"D:\AAA学习\A大二下\算法设计与分析\mediumDG.txt"  # 替换为您的实际文件路径

    print(f"\n正在处理文件: {filename}")

    try:
        V, E, edges, adj = read_graph(filename)
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    # 高效算法找桥
    print("\n[高效算法] 使用DFS和时间戳...")
    import time
    start = time.time()
    bridges = efficient_find_bridges(V, adj)
    end = time.time()
    print(f"找到桥数量: {len(bridges)}")
    print(f"耗时: {end - start:.6f}秒")

    # 可视化结果
    if bridges:
        print("\n找到的桥:")
        for bridge in sorted(bridges):
            print(bridge)

        # 可视化图形
        print("\n正在生成可视化图形...")
        visualize_graph(edges, bridges, f"Found {len(bridges)} Bridges")
    else:
        print("\n该图中没有桥")

        # 可视化原始图形
        print("正在生成可视化图形...")
        G = nx.Graph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
        plt.title("Graph with No Bridges")
        plt.axis('off')
        plt.show()

    print("\n处理完成")


if __name__ == "__main__":
    main()