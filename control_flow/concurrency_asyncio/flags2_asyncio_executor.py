import asyncio
import collections
import concurrent

import aiohttp
from aiohttp import web
import tqdm

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):
    def __init__(self, country_code):
        self.country_code = country_code

@asyncio.coroutine
def get_flag(base_url, cc):
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = yield from aiohttp.request('GET', url)
    if resp.status == 200:
        image = yield from resp.read()
        return image
    elif resp.status == 404:
        raise web.HTTPNotFound()
    else:
        raise aiohttp.HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)

@asyncio.coroutine
def download_one(cc, base_url, semaphore, verbose):
    try:

        # Ensure that no more than concur_req instances of get_flags coroutines
        # will be started at any time.
        with (yield from semaphore):
            image = yield from get_flag(base_url, cc)

    except web.HTTPNotFound:
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc
    else:

        '''
        exception calling callback for <Future at 0x7f0ba2434710 state=finished returned NoneType>
        Traceback (most recent call last):
        File "/usr/lib/python3.5/concurrent/futures/_base.py", line 297, in _invoke_callbacks
            callback(self)
        File "/usr/lib/python3.5/asyncio/futures.py", line 442, in _call_set_state
            dest_loop.call_soon_threadsafe(_set_state, destination, source)
        File "/usr/lib/python3.5/asyncio/base_events.py", line 532, in call_soon_threadsafe
            handle = self._call_soon(callback, args)
        File "/usr/lib/python3.5/asyncio/base_events.py", line 506, in _call_soon
            self._check_closed()
        File "/usr/lib/python3.5/asyncio/base_events.py", line 334, in _check_closed
            raise RuntimeError('Event loop is closed')
        RuntimeError: Event loop is closed
        '''
        # Bug filed at https://github.com/python/asyncio/issues/258
        # Workaround at https://stackoverflow.com/questions/32598231/asyncio-runtimeerror-event-loop-is-closed
        loop = asyncio.get_event_loop()
        executor = concurrent.futures.ThreadPoolExecutor(5)
        loop.set_default_executor(executor)
        loop.run_in_executor(None, save_flag, image, cc.lower() + '.gif')
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)

@asyncio.coroutine
def downloader_coro(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()

    # Create an asyncio.Semaphore.
    semaphore = asyncio.Semaphore(concur_req)

    # Create a list of coroutine objects, one per call to 'download_one' coroutine.
    to_do = [download_one(cc, base_url, semaphore, verbose)
             for cc in sorted(cc_list)]

    # Get an iterator that will return futures as they are done.
    to_do_iter = asyncio.as_completed(to_do)
    if not verbose:
        # Wrap the iterator in the tqdm function.
        to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))

    # Iterate over the completed futures.
    for future in to_do_iter:
        try:

            # The easiest way to retrieve the result of an asyncio.Future,
            # instead of calling future.result()
            res = yield from future
        except FetchError as exc:
            country_code = exc.country_code
            try:
                error_msg = exc.__cause__.args[0]
            except IndexError:
                error_msg = exc.__cause__.__class__.__name__
            if verbose and error_msg:
                msg = '*** Error for {}: {}'
                print(msg.format(country_code, error_msg))
            status = HTTPStatus.error
        else:
            status = res.status

        counter[status] += 1

    return counter

def download_many(cc_list, base_url, verbose, concur_req):
    loop = asyncio.get_event_loop()
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
    loop.close()

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
