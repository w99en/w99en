#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <string>
#include <queue>
#include <chrono>
#include <algorithm>
#include <cctype>
using namespace std;

// 去除字符串首尾的空白字符
string trim(const string &str) {
	size_t start = str.find_first_not_of(" \t\n\r");
	if (start == string::npos)
		return "";
	size_t end = str.find_last_not_of(" \t\n\r");
	return str.substr(start, end - start + 1);
}

// 读取图的函数（增强健壮性）
vector<vector<int>> readGraph(const string &filename, int &V, int &E) {
	ifstream file(filename);
	if (!file.is_open()) {
		cerr << "Error: Cannot open file " << filename << endl;
		exit(1);
	}

	string line;
	// 读取顶点数 V
	while (getline(file, line)) {
		line = trim(line);
		if (line.empty() || line[0] == '#')
			continue;
		try {
			V = stoi(line);
			break;
		} catch (const std::invalid_argument &) {
			cerr << "Error: First line must be vertex count (integer), but got: '" << line << "'" << endl;
			exit(1);
		}
	}

	// 读取边数 E
	while (getline(file, line)) {
		line = trim(line);
		if (line.empty() || line[0] == '#')
			continue;
		try {
			E = stoi(line);
			break;
		} catch (const std::invalid_argument &) {
			cerr << "Error: Second line must be edge count (integer), but got: '" << line << "'" << endl;
			exit(1);
		}
	}

	vector<vector<int>> adj(V);
	int line_num = 2;
	while (getline(file, line)) {
		line_num++;
		line = trim(line);
		if (line.empty() || line[0] == '#')
			continue;

		istringstream iss(line);
		int u, v;
		if (!(iss >> u >> v)) {
			cerr << "Warning: Invalid edge format at line " << line_num << ": '" << line << "'" << endl;
			continue;
		}
		if (u < 0 || u >= V || v < 0 || v >= V) {
			cerr << "Warning: Vertex index out of range [0," << V - 1 << "] at line "
			     << line_num << ": " << u << " " << v << endl;
			continue;
		}
		adj[u].push_back(v);
		adj[v].push_back(u);
	}

	return adj;
}

// 使用BFS计算连通分量数
int countConnectedComponents(const vector<vector<int>> &adj) {
	int V = adj.size();
	vector<bool> visited(V, false);
	int components = 0;

	for (int u = 0; u < V; ++u) {
		if (!visited[u]) {
			components++;
			queue<int> q;
			q.push(u);
			visited[u] = true;

			while (!q.empty()) {
				int current = q.front();
				q.pop();

				for (int v : adj[current]) {
					if (!visited[v]) {
						visited[v] = true;
						q.push(v);
					}
				}
			}
		}
	}
	return components;
}

// 并查集类
class UnionFind {
	private:
		vector<int> parent;
		vector<int> rank;
	public:
		UnionFind(int size) {
			parent.resize(size);
			rank.resize(size, 0);
			for (int i = 0; i < size; ++i)
				parent[i] = i;
		}

		int find(int x) {
			if (parent[x] != x)
				parent[x] = find(parent[x]);
			return parent[x];
		}

		void unite(int x, int y) {
			int rootX = find(x);
			int rootY = find(y);
			if (rootX == rootY)
				return;

			if (rank[rootX] < rank[rootY])
				parent[rootX] = rootY;
			else {
				parent[rootY] = rootX;
				if (rank[rootX] == rank[rootY])
					rank[rootX]++;
			}
		}

		bool connected(int x, int y) {
			return find(x) == find(y);
		}
};

// 优化的桥检测算法
vector<pair<int, int>> findBridgesOptimized(const vector<vector<int>> &adj) {
	int V = adj.size();
	vector<pair<int, int>> bridges;

	// 构建DFS树
	vector<int> parent(V, -1);
	vector<int> depth(V, 0);
	vector<bool> visited(V, false);
	vector<vector<int>> tree(V);

	// BFS构建树（避免递归栈溢出）
	for (int i = 0; i < V; ++i) {
		if (!visited[i]) {
			queue<int> q;
			q.push(i);
			visited[i] = true;

			while (!q.empty()) {
				int u = q.front();
				q.pop();

				for (int v : adj[u]) {
					if (!visited[v]) {
						parent[v] = u;
						depth[v] = depth[u] + 1;
						tree[u].push_back(v);
						visited[v] = true;
						q.push(v);
					}
				}
			}
		}
	}

	// 初始化并查集
	UnionFind uf(V);

	// 处理非树边
	for (int u = 0; u < V; ++u) {
		for (int v : adj[u]) {
			if (parent[u] == v || parent[v] == u)
				continue; // 跳过树边
			if (depth[u] < depth[v])
				continue; // 只处理从深到浅的边

			// 找到u和v的LCA
			int a = u, b = v;
			while (a != b) {
				if (depth[a] > depth[b])
					a = parent[a];
				else
					b = parent[b];
			}
			int lca = a;

			// 合并路径上的节点到LCA
			a = u;
			while (a != lca) {
				uf.unite(a, lca);
				a = parent[a];
			}

			b = v;
			while (b != lca) {
				uf.unite(b, lca);
				b = parent[b];
			}
		}
	}

	// 检测桥
	for (int u = 0; u < V; ++u) {
		for (int v : tree[u]) {
			if (!uf.connected(u, v)) {
				bridges.emplace_back(min(u, v), max(u, v));
			}
		}
	}

	// 去重（因为是无向图）
	sort(bridges.begin(), bridges.end());
	bridges.erase(unique(bridges.begin(), bridges.end()), bridges.end());

	return bridges;
}

int main() {
	vector<string> filenames = {"testG.txt", "mediumG.txt", "largeG.txt"};

	for (const string &filename : filenames) {
		cout << "\n==== Processing " << filename << " ====" << endl;

		int V = 0, E = 0;
		auto start_read = chrono::high_resolution_clock::now();
		vector<vector<int>> adj = readGraph(filename, V, E);
		auto end_read = chrono::high_resolution_clock::now();

		cout << "Vertices: " << V << ", Edges: " << E << endl;
		cout << "Connected components: " << countConnectedComponents(adj) << endl;

		auto start_bridge = chrono::high_resolution_clock::now();
		auto bridges = findBridgesOptimized(adj);
		auto end_bridge = chrono::high_resolution_clock::now();

		auto read_time = chrono::duration_cast<chrono::milliseconds>(end_read - start_read).count();
		auto bridge_time = chrono::duration_cast<chrono::milliseconds>(end_bridge - start_bridge).count();

		cout << "Found " << bridges.size() << " bridges in " << bridge_time << " ms" << endl;
		cout << "Total time (read+compute): " << (read_time + bridge_time) << " ms" << endl;

		// 打印前10个桥（如果存在）
		int print_count = min(10, (int)bridges.size());
		if (print_count > 0) {
			cout << "First " << print_count << " bridges:" << endl;
			for (int i = 0; i < print_count; ++i) {
				cout << "  " << bridges[i].first << " - " << bridges[i].second << endl;
			}
		}
	}

	return 0;
}