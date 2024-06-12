import multiprocessing
import UniformGraph
import time
import matplotlib.pyplot as plt


def worker(vertex_num, results):
    start = time.time()
    graphPartition = UniformGraph.UniformGraphPartition(vertex_num)
    costs = graphPartition.partition()
    end = time.time()
    results[vertex_num] = (end-start)
    graphPartition.plotCost(costs)


if __name__ == '__main__':
    num_list = [4, 8, 10, 16, 20, 50, 100, 1000, 5000]
    manager = multiprocessing.Manager()
    results = manager.dict()
    processes = []
    for vertex_num in num_list:
        p = multiprocessing.Process(target=worker, args=(vertex_num, results))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
    print(results)
    times = [results[vertex_num] for vertex_num in num_list]
    plt.plot(num_list, times, marker="*")
    plt.title("Execution time")
    plt.xlabel('vertex num')
    plt.ylabel('time (s)')
    plt.grid(True)
    plt.savefig("res/unfirom_graph_time.png")
