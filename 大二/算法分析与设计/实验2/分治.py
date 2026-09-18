import math
import random
import time
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np

Point = Tuple[float, float]

def generate_points(n: int) -> List[Point]:
    """生成随机二维点"""
    return [(random.uniform(0, 10000), random.uniform(0, 10000)) for _ in range(n)]

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
        dc_dist, _, _ = closest_pair(points)
        dc_time = time.time() - start

        # 运行蛮力法
        bf_time = None
        if run_brute_force:
            start = time.time()
            bf_dist, _, _ = brute_force(points)
            bf_time = time.time() - start
            assert abs(dc_dist - bf_dist) < 1e-6, "结果不一致"

        results.append((size, bf_time, dc_time))
        if bf_time is not None:
            print(f"规模 {size}: 蛮力法 {bf_time:.2f}s | 分治法 {dc_time:.2f}s")
        else:
            print(f"规模 {size}: 蛮力法 N/A | 分治法 {dc_time:.2f}s")

    return results

def plot_results(results):
    sizes = [r[0] for r in results]
    bf_times = [r[1] for r in results if r[1] is not None]
    bf_sizes = [r[0] for r in results if r[1] is not None]
    dc_times = [r[2] for r in results]

    # 计算理论曲线
    # 使用第一个非None的蛮力法时间作为基准
    if len(bf_times) > 0:
        base_bf_size = bf_sizes[0]
        base_bf_time = bf_times[0]
        theoretical_bf = [base_bf_time * (n**2)/(base_bf_size**2) for n in bf_sizes]
    
    # 使用第一个分治法时间作为基准
    if len(dc_times) > 0:
        base_dc_size = sizes[0]
        base_dc_time = dc_times[0]
        theoretical_dc = [base_dc_time * (n * np.log2(n))/(base_dc_size * np.log2(base_dc_size)) for n in sizes]

    plt.figure(figsize=(15, 6))
    
    # 线性比例图
    plt.subplot(1, 2, 1)
    if len(bf_times) > 0:
        plt.plot(bf_sizes, bf_times, 'ro-', label='Brute Force (tual)')
        plt.plot(bf_sizes, theoretical_bf, 'r--', label='Brute Force (theoryO(n²))')
    plt.plot(sizes, dc_times, 'bo-', label='Divide and Conquer (tual)')
    plt.plot(sizes, theoretical_dc, 'b--', label='Divide and Conquer (theoryO(n log n))')
    plt.xlabel('Problem Size')
    plt.ylabel('Time (s)')
    plt.title('compareToO(n²) and O(n log n)')
    plt.legend()
    plt.grid(True)

    # 对数比例图
    # plt.subplot(1, 2, 2)
    # if len(bf_times) > 0:
    #     plt.loglog(bf_sizes, bf_times, 'ro-', label='Brute Force (tual)')
    #     plt.loglog(bf_sizes, theoretical_bf, 'r--', label='Brute Force (theoryO(n²))')
    # plt.loglog(sizes, dc_times, 'bo-', label='Divide and Conquer (tual)')
    # plt.loglog(sizes, theoretical_dc, 'b--', label='Divide and Conquer (theoryO(n log n))')
    # plt.xlabel('Problem Size (log)')
    # plt.ylabel('Time (s) (log)')
    # plt.title('compareToO(n²) and O(n log n) (log-log scale)')
    # plt.legend()
    # plt.grid(True)

    # plt.tight_layout()
    plt.show()

# ... (之后的代码保持不变)
if __name__ == "__main__":
    # 测试规模配置
    small_sizes = [10, 100, 1000, 5000, 10000, 100000]  # 蛮力法+分治法
    large_sizes = [200000, 500000, 1000000]  # 仅分治法

    print("正在运行小规模测试(蛮力法+分治法)...")
    small_results = run_test(small_sizes, run_brute_force=True)

    print("\n正在运行大规模测试(仅分治法)...")
    large_results = run_test(large_sizes, run_brute_force=False)

    # 合并结果
    all_results = small_results + large_results

    # 显示结果表格
    print("\n测试结果汇总:")
    print("规模\t蛮力法时间\t分治法时间")
    for size, bf, dc in all_results:
        if bf is not None:
            print(f"{size}\t{bf:.2f}s\t\t{dc:.2f}s")
        else:
            print(f"{size}\tN/A\t\t{dc:.2f}s")

    # 绘制图表
    plot_results(all_results)
    