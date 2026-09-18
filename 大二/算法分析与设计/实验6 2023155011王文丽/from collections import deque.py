from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import time

# 定义边的类，每条边有目标节点、反向边的索引和容量
class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to  # 目标节点
        self.rev = rev  # 反向边的索引
        self.capacity = capacity  # 边的容量

# 定义最大流算法的类
class MaxFlow:
    def __init__(self, N):
        self.size = N  # 网络中节点的数量
        self.graph = [[] for _ in range(N)]  # 用邻接表表示图，每个节点有一个边的列表
    
    # 添加一条边到图中
    def add_edge(self, fr, to, cap):
        forward = Edge(to, len(self.graph[to]), cap)  # 正向边
        backward = Edge(fr, len(self.graph[fr]), 0)  # 反向边，初始容量为0
        self.graph[fr].append(forward)  # 添加正向边到起始节点
        self.graph[to].append(backward)  # 添加反向边到目标节点
    
    # 使用BFS为每个节点分配层次
    def bfs_level(self, s, t, level):
        q = deque()  # 用队列实现BFS
        level[:] = [-1]*self.size  # 初始化层次数组
        level[s] = 0  # 源点的层次为0
        q.append(s)  # 将源点加入队列
        while q:
            v = q.popleft()  # 从队列中取出一个节点
            for edge in self.graph[v]:
                if edge.capacity > 0 and level[edge.to] < 0:  # 如果这条边有容量且目标节点未被访问
                    level[edge.to] = level[v] + 1  # 更新目标节点的层次
                    q.append(edge.to)  # 将目标节点加入队列
    
    # 使用DFS寻找增广路径并更新流量
    def dfs_flow(self, v, t, upTo, iter_, level):
        if v == t:  # 如果到达汇点
            return upTo  # 返回当前路径的流量
        for i in range(iter_[v], len(self.graph[v])):
            edge = self.graph[v][i]
            if edge.capacity > 0 and level[v] < level[edge.to]:  # 如果这条边有容量且目标节点的层次更高
                d = self.dfs_flow(edge.to, t, min(upTo, edge.capacity), iter_, level)  # 递归寻找增广路径
                if d > 0:  # 如果找到增广路径
                    edge.capacity -= d  # 更新正向边的容量
                    self.graph[edge.to][edge.rev].capacity += d  # 更新反向边的容量
                    return d  # 返回增广路径的流量
            iter_[v] += 1  # 更新迭代器
        return 0  # 如果没有找到增广路径，返回0
    
    # 计算最大流
    def max_flow(self, s, t):
        flow = 0  # 初始化流量为0
        level = [-1]*self.size  # 初始化层次数组
        while True:
            self.bfs_level(s, t, level)  # 使用BFS为每个节点分配层次
            if level[t] < 0:  # 如果汇点不可达
                return flow  # 返回当前流量
            iter_ = [0]*self.size  # 初始化迭代器数组
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)  # 使用DFS寻找增广路径并更新流量
                if f == 0:  # 如果没有找到增广路径
                    break
                flow += f  # 更新总流量
            level = [-1]*self.size  # 重置层次数组
    
    # 优化后的最大流算法
    def max_flow_better(self, s, t):
        flow = 0  # 初始化流量为0
        level = [-1]*self.size  # 初始化层次数组
        while True:
            if not self.bfs_level(s, t, level):  # 使用BFS为每个节点分配层次
                return flow  # 如果汇点不可达，返回当前流量
            iter_ = [0]*self.size  # 初始化迭代器数组
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)  # 使用DFS寻找增广路径并更新流量
                if f == 0:  # 如果没有找到增广路径
                    break
                flow += f  # 更新总流量

# 可视化流网络
def visualize_flow_network(teams, games, team_indices, x, max_possible):
    num_teams = len(teams)  # 队伍数量
    num_games = len(games)  # 比赛数量
    size = 1 + num_games + num_teams + 1  # 网络的总节点数
    
    G = nx.DiGraph()  # 创建有向图
    pos = {}  # 节点位置
    labels = {}  # 节点标签
    
    # 添加节点
    G.add_node(0)  # 源点
    pos[0] = (0, 0)
    labels[0] = "Source"
    
    for i in range(num_games):  # 添加比赛节点
        node = 1 + i
        G.add_node(node)
        pos[node] = (1, i - num_games/2)
        labels[node] = f"{games[i][0]}\nvs\n{games[i][1]}"
    
    for i in range(num_teams):  # 添加球队节点
        node = 1 + num_games + i
        G.add_node(node)
        pos[node] = (2, i - num_teams/2)
        labels[node] = teams[i][0]
    
    sink = 1 + num_games + num_teams  # 汇点
    G.add_node(sink)
    pos[sink] = (3, 0)
    labels[sink] = "Sink"
    
    # 添加边
    for i in range(num_games):  # 从源点到比赛节点
        game_node = 1 + i
        G.add_edge(0, game_node, capacity=games[i][2])
    
    for i in range(num_games):  # 从比赛节点到球队节点
        team1, team2, _ = games[i]
        game_node = 1 + i
        team1_node = 1 + num_games + team_indices[team1]
        team2_node = 1 + num_games + team_indices[team2]
        G.add_edge(game_node, team1_node, capacity=float('inf'))
        G.add_edge(game_node, team2_node, capacity=float('inf'))
    
    for i in range(num_teams):  # 从球队节点到汇点
        if i == x:
            cap = float('inf')
        else:
            cap = max_possible - teams[i][1]
        team_node = 1 + num_games + i
        if cap < 0:
            cap = 0
        G.add_edge(team_node, sink, capacity=cap)
    
    # 绘制网络图
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='skyblue', font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f"Flow Network for {teams[x][0]} (Max Possible: {max_possible})")
    plt.show()

# 打印淘汰分析
def print_elimination_analysis(teams, games, team_indices, x, max_possible, visualize=False):
    print(f"\n=== 分析 {teams[x][0]} 队 ===")
    
    # 检查简单淘汰
    for i in range(len(teams)):
        if i == x:
            continue
        if max_possible < teams[i][1]:  # 如果其他队伍已经赢的比赛数大于当前队伍的最大可能胜场
            return "Trivially eliminated"
    
    if visualize:  # 如果需要可视化
        visualize_flow_network(teams, games, team_indices, x, max_possible)
    
    # 构建流网络
    total_games = sum(g for _, _, g in games)  # 所有比赛的总次数
    num_teams = len(teams)  # 队伍数量
    num_games = len(games)  # 比赛数量
    
    size = 1 + num_games + num_teams + 1  # 网络的总节点数
    mf = MaxFlow(size)  # 创建最大流算法的实例
    S = 0  # 源点
    T = size - 1  # 汇点
    
    # 从源点到比赛节点
    for i in range(num_games):
        game_node = 1 + i
        mf.add_edge(S, game_node, games[i][2])
       
    # 从比赛节点到球队节点
    for i in range(num_games):
        team1, team2, _ = games[i]
        game_node = 1 + i
        team1_node = 1 + num_games + team_indices[team1]
        team2_node = 1 + num_games + team_indices[team2]
        mf.add_edge(game_node, team1_node, float('inf'))
        mf.add_edge(game_node, team2_node, float('inf'))
      
    # 从球队节点到汇点
    for i in range(len(teams)):
        if i == x:
            cap = float('inf')
        else:
            cap = max_possible - teams[i][1]
        team_node = 1 + num_games + i
        
        if cap < 0:
            cap = 0
        mf.add_edge(team_node, T, cap)
      
    # 计算最大流
    starttime = time.perf_counter()  # 开始时间
    flow = mf.max_flow(S, T)  # 使用Dinic算法计算最大流
    endtime = time.perf_counter()  # 结束时间
    print(f"Dinic用时 {endtime - starttime} 秒")

    starttime = time.perf_counter()  # 开始时间
    flow = mf.max_flow_better(S, T)  # 使用优化后的Dinic算法计算最大流
    endtime = time.perf_counter()  # 结束时间
    print(f"Dinic优化用时 {endtime - starttime} 秒")
    
    if flow == total_games:  # 如果最大流等于所有比赛的总次数
        return "Not eliminated"  # 当前队伍没有被淘汰
    else:
        return "Eliminated"  # 当前队伍被淘汰

# 解决棒球赛问题并打印详细分析
def solve_baseball_with_details(teams, games, visualize=False):
    team_indices = {name: i for i, (name, _, _) in enumerate(teams)}  # 每个队伍的索引
    results = {}  # 保存每个队伍的分析结果
    
    for x in range(len(teams)):  # 遍历所有队伍
        x_name, w_x, r_x = teams[x]  # 当前队伍的信息
        max_possible = w_x + r_x  # 当前队伍最多能赢的比赛数
        status = print_elimination_analysis(teams, games, team_indices, x, max_possible, visualize)  # 分析当前队伍是否被淘汰
        results[x_name] = status  # 保存分析结果
    
    print("\n=== 最终结果 ===")  # 打印最终结果
    for team, status in results.items():
        print(f"{team}: {status}")

# 队伍信息
teams = [
    ("Atlanta", 83, 8),       # (队名, 已赢场数, 剩余比赛数)
    ("Philadelphia", 80, 3),
    ("New York", 78, 6),
    ("Montreal", 77, 3)
]

# 比赛信息
games = [
    ("Atlanta", "Philadelphia", 1),  # (队1, 队2, 剩余对阵次数)
    ("Atlanta", "New York", 6),
    ("Atlanta", "Montreal", 1),
    ("Philadelphia", "Montreal", 2)
]

# 运行分析并可视化
solve_baseball_with_details(teams, games, visualize=False)