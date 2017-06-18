from concurrent import futures
from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20

def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

# Need to return the count of flags downloaded.
def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        # map() returns a generator that can be iterated over to retrieve the
        # value returned by each function.
        res = executor.map(download_one, sorted(cc_list))

    # the executor.__exit__ method will call executor.shutdown(wait=True),
    # which will block until all threads are done.

    # Return the number of results obtained. If any of the threaded calls raised
    # an exception, that exception would be raised here as the implicit next()
    # call tried to retrieve the corresponding return value from the iterator.
    return len(list(res))


if __name__ == '__main__':
    main(download_many)
