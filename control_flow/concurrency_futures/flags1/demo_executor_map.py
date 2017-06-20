from time import sleep, strftime
from concurrent import futures

def display(*args):
    print(strftime('[%H:%M:%s]'), end = ' ')
    print(*args)

def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t'*n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t'*n, n))
    return n * 10

def main():
    display('Script starting.')

    # Create a ThreadPoolExecutor with 3 threads
    executor = futures.ThreadPoolExecutor(max_workers=3)

    # Submit 5 tasks to the executor, only three of them will start immediately.

    # The executor.map function has feature:
    #   It returns the results exactly in the same order as the calls are started.
    #   If the first call takes 10s to produce a result, and the others take 1s
    #   each, we'll be blocked for 10s as it tries to retrieve the first result
    #   of the generator returned by map. After that, we can get the remaining
    #   results without blocking since they will be done.

    # Often, it is preferable to get the results as they are ready, regardless
    # of the order they are submitted. To achieve that, we need combine the
    # Executor.submit() method and the futures.as_completed function.
    results = executor.map(loiter, range(5))

    # 'results' is a generator 
    display('results:', results)

    # The enumerate call will implicitly invoke next(results), which in turn
    # will invoke _f.result() on the internal _f future representing the first
    # call, loiter(0). The 'result' method will block until the future is done.
    # Therefor, each iteration in this loop will have to wait for the next
    # result to be ready.
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
