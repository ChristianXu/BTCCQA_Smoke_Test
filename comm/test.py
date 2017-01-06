from multiprocessing.queues import Queue
from multiprocessing.context import Process, SpawnContext
import os, time

# 写数据进程执行的代码:
def write1(q):
    print('Process to write: %s' % os.getpid())
    value = ['A', 'B', 'C']

    q.put(value)
    time.sleep(1)

def write2(q):
    print('Process to write: %s' % os.getpid())
    value = ['a', 'b', 'c']
    q.put(value)
    time.sleep(1)


if __name__=='__main__':

    # 父进程创建Queue，并传给各个子进程：
    s = SpawnContext()
    q = s.Queue()
    pw = Process(target=write1, args=(q,))
    pw2 = Process(target=write2, args=(q,))
    # pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    pw2.start()
    # 启动子进程pr，读取:
    # pr.start()
    # 等待pw结束:
    pw.join()
    pw2.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    # pr.terminate()

    print(11111)
    # while True:
    #     value = q.get(True)
    #     print('Get %s from queue.' % value)

    while not q.empty():

        value = q.get(True)
        print('Get %s from queue.' % value)

    print(q.empty())

    print(2222222)

