import multiprocessing
import time
 
def func(msg):
    print("msg:", msg['a'])
    time.sleep(2)
    print("end")
 
if __name__ == "__main__":
    pool = multiprocessing.Pool(2)
    pool.map_async(func, [{'a':3},{'a':4}])
 
    print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
    pool.close()
    pool.join()
    print("Sub-process(es) done.")