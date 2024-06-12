import multiprocessing
import EdgeColor
import time
def worker(vertex_num,results):
    start = time.time()
    edge_color = EdgeColor.EdgeColor(vertex_num)
    actual_k4_num, expection_k4_num = edge_color.calculate()
    end = time.time()
    results[vertex_num] = (actual_k4_num, expection_k4_num, end-start)
    edge_color.plot_result()
if __name__ == '__main__':
    num_list = [5,8,10,15,20,25,50]
    manager = multiprocessing.Manager()
    results = manager.dict()
    processes = []
    for vertex_num in num_list:
        p = multiprocessing.Process(target=worker, args=(vertex_num,results))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()
    print(results)