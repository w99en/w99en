import random
import time
import numpy as np
import matplotlib.pyplot as plt

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
def quick_sort_down(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x > pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x < pivot]
        return quick_sort_down(left) + middle + quick_sort_down(right)

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        # 找到未排序部分的最小值索引
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # 将最小值与当前索引位置的值交换
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        # 提前退出冒泡循环的标志
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # 如果没有发生交换，说明数组已经有序
        if not swapped:
            break
    return arr

def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # 将当前元素插入到已排序部分的合适位置
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # 合并两个有序数组
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 测试数据
# data = [64, 34, 25, 12, 22, 11, 90]
# print("选择排序结果：", selection_sort(data.copy()))
# print("冒泡排序结果：", bubble_sort(data.copy()))
# print("插入排序结果：", insertion_sort(data.copy()))
# print("合并排序结果：", merge_sort(data.copy()))
# print("快速排序结果：", quick_sort(data.copy()))






# 测试排序算法的平均运行时间
def test_sorting_algorithms(n):
    sorting_algorithms = {
        # "selection_sort": selection_sort,
        # "bubble_sort": bubble_sort,
        # "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort
    }

    # 生成 20 组随机数组
    samples = [[random.randint(1, 1000) for _ in range(n)] for _ in range(10)]

    # 测试每种排序算法的运行时间
    results = {}
    for name, sort_func in sorting_algorithms.items():
        total_time = 0
        for sample in samples:
            arr = sample.copy()  # 复制数组以避免被修改
            start_time = time.time()
            sort_func(arr)
            end_time = time.time()
            total_time += (end_time - start_time)
        avg_time = total_time / len(samples)
        results[name] = avg_time

    return results

# 主函数
if __name__ == "__main__":
    #固定n测试几种排序算法
    # n = int(input("请输入数组大小 n: "))
    # results = test_sorting_algorithms(n)
    # print(f"数组大小为 {n} 时，不同排序算法的平均运行时间：")
    # for name, avg_time in results.items():
    #     print(f"{name}: {avg_time:.8f} 秒")


    #大数据上的测试
    # n_values = np.linspace(100000,500000,5,dtype=int)
    # results = {alg: [] for alg in ["merge_sort", "quick_sort"]}# "selection_sort", "bubble_sort", "insertion_sort",

    # # 测试每个输入规模
    # for n in n_values:
    #     print(f"正在测试 n = {n}...")
    #     current_results = test_sorting_algorithms(n)
    #     for alg, avg_time in current_results.items():
    #         results[alg].append(avg_time)
    #         print(f"{alg} 的平均运行时间: {avg_time:.6f} 秒")
    # # current_results = test_sorting_algorithms(n_values)
    # # print(f"正在测试 n = {n_values}...")
    # # for alg, avg_time in current_results.items():
        
    # #     results[alg].append(avg_time)
    # #     print(f"{alg} 的平均运行时间: {avg_time:.6f} 秒")


    # # 绘制结果
    # plt.figure(figsize=(10, 6))
    # for alg, times in results.items():
    #     plt.plot(n_values, times, label=alg, marker='o')

    # # 推出的时间
    # merge_sort_times = [0.157,0.478, 0.789, 1.100, 1.376]
    # quick_sort_times = [0.071,0.217, 0.357, 0.495, 0.623]

    # plt.plot(n_values, merge_sort_times, label="merge_sort_theory", marker='.', linestyle='--', color='blue')
    # plt.plot(n_values, quick_sort_times, label="quick_sort_theory", marker='.', linestyle='--', color='orange')

    # plt.xlabel("imput n")
    # plt.ylabel("average running time (seconds)")
    # plt.title("different sorting algorithms' running time")
    # plt.legend()
    # plt.grid(True)
    # plt.xticks(n_values)
    # plt.show()


    samples_part = [[] for _ in range(100)]
    n=1000000000
    samples = [random.randint(-500000000, 500000000) for _ in range(n)]
    samples_part = [samples[i*10000000:(i+1)*10000000] for i in range(100)]

    top_10_in_each_part = []
    
    all_start_time = time.time()
    i=1
    for part in samples_part:
        start_time = time.time()
        part_sorted = quick_sort_down(part)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"分组排序{i}所用时间：{elapsed_time:.2f} 秒")
        top_10_in_each_part.append(part_sorted[0:10])
        i+=1

    top_10_in_each_part = [item for sublist in [[500000000, 499999976, 499999742, 499999736, 499999655, 499999648, 499999375, 499999362, 499999330, 499999200], [499999999, 499999963, 499999825, 499999795, 499999779, 499999739, 499999736, 499999582, 499999424, 499999346], [499999997, 499999814, 499999792, 499999686, 499999454, 499999431, 499999109, 499999072, 499998843, 499998837], [499999995, 499999494, 499999440, 499999380, 499999335, 499999191, 499999154, 499999080, 499999022, 499999002], [499999994, 499999950, 499999894, 499999830, 499999732, 499999523, 499999496, 499999460, 499999289, 499999248], [499999992, 499999984, 499999754, 499999668, 499999636, 499999628, 499999613, 499999569, 499999541, 499999367], [499999992, 499999944, 499999860, 499999718, 499999608, 499999594, 499999513, 499999465, 499999375, 499999339], [499999991, 499999987, 499999937, 499999828, 499999705, 499999651, 499999468, 499999313, 499999276, 499999275], [499999991, 499999941, 499999920, 499999901, 499999809, 499999784, 499999627, 499999603, 499999419, 499999315], [499999990, 499999924, 499999733, 499999702, 499999682, 499999678, 499999611, 499999566, 499999544, 499999387]] for item in sublist]
    top_10_in_each_part_sorted = quick_sort_down(top_10_in_each_part)
    end_time = time.time()
    print(top_10_in_each_part_sorted[0:10])
    elapsed_time = end_time - all_start_time
    print(f"总排序所用时间：{elapsed_time:.2f} 秒")
    
  


