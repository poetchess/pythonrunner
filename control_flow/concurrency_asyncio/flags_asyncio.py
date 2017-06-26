'''
Two facts about every usage of yield from:

    Every arrangement of coroutines chained with yield from must be ultimately
    driven by a caller that is not a coroutine, which invokes next(…) or .send(…)
    on the outermost delegating generator, explicitly or implicitly (e.g., in 
    a for loop)

    The innermost subgenerator in the chain must be a simple generator that uses
    just yield—or an iterable object.


When using yield from with the asyncio API, both facts remain true, with the
following specifics:

    The coroutine chains we write are always driven by passing our outermost
    delegating generator to an asyncio API call, such as
    loop.run_until_complete(…). In other words, when using asyncio our code
    doesn’t drive a coroutine chain by calling next(…) or .send(…) on it, the
    asyncio event loop does that.

    The coroutine chains we write always end by delegating with yield from to
    some asyncio coroutine function or coroutine method (e.g., 
    yield from asyncio.sleep(…)) or coroutines from libraries that implement
    higher-level protocols (e.g., resp = yield from aiohttp.request('GET', url))
    In other words, the innermost subgenerator will be a library function that
    does the actual I/O, not something we write.
'''
import asyncio
import aiohttp

from flags import BASE_URL, save_flag, show, main

@asyncio.coroutine
def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())

    # Blocking operations are implemented as coroutines. Our code delegates to
    # them via yield from so they run asynchronously.
    resp = yield from aiohttp.request('GET', url)

    # Reading the response content is a seperate asynchronous operation.
    image = yield from resp.read()
    return image

@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc

def download_many(cc_list):
    loop = asyncio.get_event_loop()

    # Build a list of generator objects by calling download_one function once
    # for each flag to be retrieved.
    to_do = [download_one(cc) for cc in sorted(cc_list)]

    # wait() is not a blocking function. 
    # It is a coroutine accepting an iterable of futures or coroutines.
    # 'wait' wraps each coroutine in a Task. The end result is that all objects
    # managed by 'wait' become instances of Future. Becasue it is a coroutine 
    # function, calling wait(...) returns a coroutine/generator object, which is
    # held by 'wait_coro' variable. To drive the coroutine, passing it to
    # loop.run_until_complete(...)
    wait_coro = asyncio.wait(to_do)

    # Execute the event loop until wait_coro is done. The script will block here
    # while the event loop runs.
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()

    return len(res)


if __name__ == '__main__':
    main(download_many)
