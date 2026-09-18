from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import time

class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to
        self.rev = rev
        self.capacity = capacity

class MaxFlow:
    def __init__(self, N):
        self.size = N
        self.graph = [[] for _ in range(N)]
    
    def add_edge(self, fr, to, cap):
        forward = Edge(to, len(self.graph[to]), cap)
        backward = Edge(fr, len(self.graph[fr]), 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)
    
    def bfs_level(self, s, t, level):
        q = deque()
        level[:] = [-1]*self.size
        level[s] = 0
        q.append(s)
        while q:
            v = q.popleft()
            for edge in self.graph[v]:
                if edge.capacity > 0 and level[edge.to] < 0:
                    level[edge.to] = level[v] + 1
                    q.append(edge.to)
    
    def dfs_flow(self, v, t, upTo, iter_, level):
        if v == t:
            return upTo
        for i in range(iter_[v], len(self.graph[v])):
            edge = self.graph[v][i]
            if edge.capacity > 0 and level[v] < level[edge.to]:
                d = self.dfs_flow(edge.to, t, min(upTo, edge.capacity), iter_, level)
                if d > 0:
                    edge.capacity -= d
                    self.graph[edge.to][edge.rev].capacity += d
                    return d
            iter_[v] += 1
        return 0
    
    def max_flow(self, s, t):
        flow = 0
        level = [-1]*self.size
        while True:
            self.bfs_level(s, t, level)
            if level[t] < 0:
                return flow
            iter_ = [0]*self.size
            while True:
                f = self.dfs_flow(s, t, float('inf'), iter_, level)
                if f == 0:
                    break
                flow += f
            level = [-1]*self.size
    
    def max_flow_better(self, s, t):
        flow = 0
        level = [-1]*self.size
        while True:
        # 优化1：直接在BFS中填充level，无需重置
            if not self.bfs_level(s, t, level):
                return flow
        
            iter_ = [0]*self.size
            while True:
            # 优化2：使用更高效的DFS实现
                f = self.dfs_flow(s, t, float('inf'), iter_, level)
                if f == 0:
                    break
                flow += f

def visualize_flow_network(teams, games, team_indices, x, max_possible):
    num_teams = len(teams)
    num_games = len(games)
    size = 1 + num_games + num_teams + 1
    
    G = nx.DiGraph()
    pos = {}
    labels = {}
    
    # 添加节点
    G.add_node(0)
    pos[0] = (0, 0)
    labels[0] = "Source"
    
    for i in range(num_games):
        node = 1 + i
        G.add_node(node)
        pos[node] = (1, i - num_games/2)
        labels[node] = f"{games[i][0]}\nvs\n{games[i][1]}"
    
    for i in range(num_teams):
        node = 1 + num_games + i
        G.add_node(node)
        pos[node] = (2, i - num_teams/2)
        labels[node] = teams[i][0]
    
    sink = 1 + num_games + num_teams
    G.add_node(sink)
    pos[sink] = (3, 0)
    labels[sink] = "Sink"
    
    # 添加边
    for i in range(num_games):
        game_node = 1 + i
        G.add_edge(0, game_node, capacity=games[i][2])
    
    for i in range(num_games):
        team1, team2, _ = games[i]
        game_node = 1 + i
        team1_node = 1 + num_games + team_indices[team1]
        team2_node = 1 + num_games + team_indices[team2]
        G.add_edge(game_node, team1_node, capacity=float('inf'))
        G.add_edge(game_node, team2_node, capacity=float('inf'))
    
    for i in range(num_teams):
        if i == x:
            cap = float('inf')
        else:
            cap = max_possible - teams[i][1]
        team_node = 1 + num_games + i
        if cap < 0:
            cap = 0
        G.add_edge(team_node, sink, capacity=cap)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color='skyblue', font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title(f"Flow Network for {teams[x][0]} (Max Possible: {max_possible})")
    plt.show()

def print_elimination_analysis(teams, games, team_indices, x, max_possible, visualize=False):
    print(f"\n=== 分析 {teams[x][0]} 队 ===")
    
    # 检查简单淘汰
    for i in range(len(teams)):
        if i == x:
            continue
        if max_possible < teams[i][1]:
            return "Trivially eliminated"
    if visualize:
        visualize_flow_network(teams, games, team_indices, x, max_possible)
    # 构建流网络
    total_games = sum(g for _, _, g in games)
    num_teams = len(teams)
    num_games = len(games)
    
    size = 1 + num_games + num_teams + 1
    mf = MaxFlow(size)
    S = 0
    T = size - 1
    
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
            cap=float('inf')
        else:
            cap = max_possible - teams[i][1]
        team_node = 1 + num_games + i
        
        if cap < 0:
            cap = 0
        mf.add_edge(team_node, T, cap)
      

    starttime = time.perf_counter()
    flow = mf.max_flow(S, T)
    endtime = time.perf_counter()

    
    print(f"Dinic用时 {endtime - starttime} 秒")

    starttime = time.perf_counter()
    flow = mf.max_flow_better(S, T)
    endtime = time.perf_counter()

    
    print(f"Dinic优化用时 {endtime - starttime} 秒")
    
    
    if flow == total_games:
        return "Not eliminated"
    else:
        return "Eliminated"

def solve_baseball_with_details(teams, games, visualize=False):
  
    team_indices = {name: i for i, (name, _, _) in enumerate(teams)}
    results = {}
    
    for x in range(len(teams)):
        x_name, w_x, r_x = teams[x]
        max_possible = w_x + r_x
        status = print_elimination_analysis(teams, games, team_indices, x, max_possible, visualize)
        results[x_name] = status
    
    print("\n=== 最终结果 ===")
    for team, status in results.items():
        print(f"{team}: {status}")

# 更新后的数据
teams = [
    ("Atlanta", 83, 8),
    ("Philadelphia", 80, 3),
    ("New York", 78, 6),
    ("Montreal", 77, 3)
]

games = [
    ("Atlanta", "Philadelphia", 1),
    ("Atlanta", "New York", 6),
    ("Atlanta", "Montreal", 1),
    ("Philadelphia", "Montreal", 2)
]

# 运行分析并可视化
solve_baseball_with_details(teams, games, visualize=False)