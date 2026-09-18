from collections import deque
import time

# 定义边的类，每条边有目标节点、反向边的索引和容量
class Edge:
    def __init__(self, to, rev, capacity):
        self.to = to  # 目标节点
        self.rev = rev  # 反向边的索引
        self.capacity = capacity  # 边的容量

# 定义Edmonds-Karp算法的类
class EdmondsKarp:
    def __init__(self, N):
        self.size = N  # 网络中节点的数量
        self.graph = [[] for _ in range(N)]  # 用邻接表表示图，每个节点有一个边的列表
    
    # 添加一条边到图中
    def add_edge(self, fr, to, cap):
        forward = Edge(to, len(self.graph[to]), cap)  # 正向边
        backward = Edge(fr, len(self.graph[fr]), 0)  # 反向边，初始容量为0
        self.graph[fr].append(forward)  # 添加正向边到起始节点
        self.graph[to].append(backward)  # 添加反向边到目标节点
    
    # 计算最大流
    def max_flow(self, s, t):
        flow = 0  # 初始化流量为0
        while True:
            # BFS找增广路径
            parent = [-1] * self.size  # 用来记录路径的父节点
            parent[s] = s  # 源点的父节点是自己
            q = deque([s])  # 用队列实现BFS
            found = False  # 标记是否找到增广路径
            
            while q and not found:
                v = q.popleft()  # 从队列中取出一个节点
                for edge in self.graph[v]:
                    if edge.capacity > 0 and parent[edge.to] == -1:  # 如果这条边有容量且目标节点未被访问
                        parent[edge.to] = v  # 记录路径
                        if edge.to == t:  # 如果到达汇点
                            found = True
                            break
                        q.append(edge.to)  # 将目标节点加入队列
            
            if not found:  # 如果没有找到增广路径
                break
            
            # 计算路径上的最小剩余容量
            path_flow = float('inf')  # 初始化路径流量为无穷大
            v = t  # 从汇点开始
            while v != s:  # 一直找到源点
                u = parent[v]  # 当前节点的父节点
                for edge in self.graph[u]:
                    if edge.to == v:  # 找到从u到v的边
                        path_flow = min(path_flow, edge.capacity)  # 更新路径流量
                        break
                v = u  # 移动到父节点
            
            # 更新残留网络
            v = t  # 从汇点开始
            while v != s:  # 一直更新到源点
                u = parent[v]  # 当前节点的父节点
                for edge in self.graph[u]:
                    if edge.to == v:  # 找到从u到v的边
                        edge.capacity -= path_flow  # 更新正向边容量
                        self.graph[v][edge.rev].capacity += path_flow  # 更新反向边容量
                        break
                v = u  # 移动到父节点
            
            flow += path_flow  # 增加总流量
        
        return flow  # 返回最大流量

# 判断某个队伍是否被淘汰
def is_eliminated(teams, games, team_index):
    team_name, wins, remaining = teams[team_index]  # 当前队伍的信息
    max_possible = wins + remaining  # 当前队伍最多能赢的比赛数
    
    # 检查简单淘汰情况
    for i, (_, w, _) in enumerate(teams):
        if i != team_index and w > max_possible:  # 如果有其他队伍已经赢的比赛数大于当前队伍的最大可能胜场
            return True, f"{team_name} 已被简单淘汰，因为 {teams[i][0]} 已赢 {w} 场"
    
    # 创建流网络
    total_games = sum(g for _, _, g in games)  # 所有比赛的总次数
    team_indices = {name: i for i, (name, _, _) in enumerate(teams)}  # 每个队伍的索引
    
    # 节点编号：
    # 0: 源点
    # 1-n: 比赛节点
    # n+1-n+m: 球队节点
    # n+m+1: 汇点
    num_games = len(games)  # 比赛的数量
    num_teams = len(teams)  # 队伍的数量
    size = 1 + num_games + num_teams + 1  # 网络的总节点数
    ek = EdmondsKarp(size)  # 创建Edmonds-Karp算法的实例
    
    S = 0  # 源点
    T = size - 1  # 汇点
    
    # 添加源点到比赛节点的边
    for i in range(num_games):
        game_node = 1 + i  # 比赛节点的编号
        ek.add_edge(S, game_node, games[i][2])  # 添加边，容量为比赛的次数
    
    # 添加比赛节点到球队节点的边
    for i in range(num_games):
        team1, team2, _ = games[i]  # 比赛的两个队伍
        game_node = 1 + i  # 比赛节点的编号
        team1_node = 1 + num_games + team_indices[team1]  # 队伍1的节点编号
        team2_node = 1 + num_games + team_indices[team2]  # 队伍2的节点编号
        ek.add_edge(game_node, team1_node, float('inf'))  # 添加边，容量为无穷大
        ek.add_edge(game_node, team2_node, float('inf'))  # 添加边，容量为无穷大
    
    # 添加球队节点到汇点的边
    for i in range(num_teams):
        if i == team_index:
            cap = float('inf')  # 当前队伍到汇点的边容量为无穷大
        else:
            cap = max_possible - teams[i][1]  # 其他队伍到汇点的边容量
        team_node = 1 + num_games + i  # 队伍节点的编号
        if cap < 0:
            cap = 0  # 如果容量小于0，设置为0
        ek.add_edge(team_node, T, cap)  # 添加边
    
    # 计算最大流
    start_time = time.perf_counter()  # 开始时间
    flow = ek.max_flow(S, T)  # 计算最大流
    end_time = time.perf_counter()  # 结束时间
    print(f"流量最大值: {flow}, 用时 {end_time - start_time:.6f} 秒")
    
    if flow == total_games:  # 如果最大流等于所有比赛的总次数
        return False, f"{team_name} 可能夺冠，最大可达 {max_possible} 胜"
    else:
        return True, f"{team_name} 被淘汰，无法达到足够胜场"

# 分析所有队伍的情况
def analyze_teams(teams, games):
    print("=== 棒球赛淘汰分析 ===")
    
    for i in range(len(teams)):  # 遍历所有队伍
        eliminated, reason = is_eliminated(teams, games, i)  # 判断队伍是否被淘汰
        status = "淘汰" if eliminated else "存活"  # 状态
        print(f"{teams[i][0]}: {status} - {reason}")  # 输出结果

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

# 调用函数分析所有队伍
analyze_teams(teams, games)