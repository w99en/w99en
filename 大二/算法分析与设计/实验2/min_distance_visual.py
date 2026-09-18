import math
import random
import time
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np

Point = Tuple[float, float]

def generate_points(n: int) -> List[Point]:
    """生成随机二维点"""
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

def brute_force(points: List[Point]) -> Tuple[float, Point, Point]:
    """蛮力法 O(n^2)"""
    min_dist = float('inf')
    result = (None, None)
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.dist(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                result = (points[i], points[j])
    return min_dist, *result

def closest_pair(points: List[Point]) -> Tuple[float, Point, Point]:
    """分治法 O(n log n)"""
    points_sorted_x = sorted(points, key=lambda x: (x[0], x[1]))

    def recursive_helper(px, py):
        if len(px) <= 3:
            return brute_force(px)

        mid = len(px) // 2
        mid_point = px[mid]

        Q = [p for p in py if p[0] <= mid_point[0]]
        R = [p for p in py if p[0] > mid_point[0]]

        d_left, p1_left, p2_left = recursive_helper(px[:mid], Q)
        d_right, p1_right, p2_right = recursive_helper(px[mid:], R)

        d = min(d_left, d_right)
        min_pair = (p1_left, p2_left) if d_left < d_right else (p1_right, p2_right)

        strip = [p for p in py if abs(p[0] - mid_point[0]) < d]
        min_strip = d
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 7, len(strip))):
                dist = math.dist(strip[i], strip[j])
                if dist < min_strip:
                    min_strip = dist
                    min_pair = (strip[i], strip[j])

        return (min_strip, *min_pair) if min_strip < d else (d, *min_pair)

    points_sorted_y = sorted(points, key=lambda x: (x[1], x[0]))
    return recursive_helper(points_sorted_x, points_sorted_y)

def run_test(sizes: List[int], run_brute_force: bool):
    results = []
    for size in sizes:
        print(f"\n正在测试规模: {size}")
        points = generate_points(size)

        # 运行分治法
        start = time.time()
        dc_dist, dc_p1, dc_p2 = closest_pair(points)
        dc_time = time.time() - start

        # 运行蛮力法
        bf_time = None
        if run_brute_force:
            start = time.time()
            bf_dist, bf_p1, bf_p2 = brute_force(points)
            bf_time = time.time() - start
            assert abs(dc_dist - bf_dist) < 1e-6, "结果不一致"
            print(f"最小距离: {bf_dist:.2f}, 点对: {bf_p1} 和 {bf_p2}")

        print(f"最小距离: {dc_dist:.2f}, 点对: {dc_p1} 和 {dc_p2}")

        results.append((size, bf_time, dc_time, dc_dist, dc_p1, dc_p2))
        if bf_time is not None:
            print(f"规模 {size}: 蛮力法 {bf_time:.2f}s | 分治法 {dc_time:.2f}s")
        else:
            print(f"规模 {size}: 蛮力法 N/A | 分治法 {dc_time:.2f}s")

        # 绘制小样本结果
        if size <= 100:  # 小样本时画出结果图
            plot_points_and_min_dist(points, dc_p1, dc_p2, dc_dist)

    return results

def plot_points_and_min_dist(points: List[Point], p1: Point, p2: Point, dist: float):
    """绘制点和最小距离点对的连线"""
    x_vals, y_vals = zip(*points)  # 提取点的坐标
    plt.figure(figsize=(6, 6))

    # 绘制所有点
    plt.scatter(x_vals, y_vals, color='blue', label='Points')

    # 绘制最小距离的点对
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', lw=2, label=f'Min Dist: {dist:.2f}')
    
    # 标注最小距离的点对
    plt.text(p1[0], p1[1], f'({p1[0]:.2f}, {p1[1]:.2f})', fontsize=9, color='green')
    plt.text(p2[0], p2[1], f'({p2[0]:.2f}, {p2[1]:.2f})', fontsize=9, color='green')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Points and Minimum Distance Pair')
    plt.legend()
    plt.grid(True)
    plt.show()

# 你可以将上面的代码直接插入原本的程序中
if __name__ == "__main__":
    # 测试规模配置
    small_sizes = [10, 20, 50, 100]  # 仅绘制小样本的图
    large_sizes = [200, 500, 1000]  # 大样本不绘制图

    print("正在运行小规模测试(蛮力法+分治法)...")
    small_results = run_test(small_sizes, run_brute_force=True)

    print("\n正在运行大规模测试(仅分治法)...")
    large_results = run_test(large_sizes, run_brute_force=False)
