import sys
from collections import defaultdict, deque
import time


def read_graph(filename):
    """优化版文件读取，处理大型文件"""
    adj = defaultdict(list)
    max_vertex = 0
    with open(filename, 'r') as f:
        V = int(f.readline())
        E = int(f.readline())
        for _ in range(E):
            line = f.readline()
            if not line:
                break
            u, v = map(int, line.strip().split())
            adj[u].append(v)
            adj[v].append(u)
            max_vertex = max(max_vertex, u, v)
    return max_vertex + 1, adj


def efficient_find_bridges(V, adj):
    """迭代式DFS实现，避免递归问题"""
    bridges = []
    disc = [-1] * V
    low = [-1] * V
    time = 0
    parent = [-1] * V
    stack = []

    for i in range(V):
        if disc[i] == -1:
            stack.append((i, False))

            while stack:
                u, processed = stack.pop()
                if not processed:
                    disc[u] = low[u] = time
                    time += 1
                    stack.append((u, True))
                    for v in adj[u]:
                        if disc[v] == -1:
                            parent[v] = u
                            stack.append((v, False))
                        elif v != parent[u]:
                            low[u] = min(low[u], disc[v])
                else:
                    for v in adj[u]:
                        if parent[v] == u:
                            low[u] = min(low[u], low[v])
                            if low[v] > disc[u]:
                                bridges.append((u, v))
    return bridges


def main():
    filename = r"D:\360MoveData\Users\王文丽\Documents\WeChat Files\wxid_fsq4gdwfpo4x22\FileStorage\File\2025-06\largeG.txt"
    print(f"处理文件中: {filename}")
    start_time = time.time()  # 记录开始时间
    try:
        V, adj = read_graph(filename)
        print(f"读取完成: {V}个顶点")

        print("开始查找桥...")
        bridges = efficient_find_bridges(V, adj)
        print(f"找到桥数量: {len(bridges)}")

        if len(bridges) <= 20:
            print("桥列表:", bridges)
        else:
            print(f"显示前20座桥: {bridges[:20]}")

    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
    end_time = time.time()  # 记录结束时间
    print(f"运行时间: {end_time - start_time:.6f}秒")  # 打印运行时间


if __name__ == "__main__":
    main()