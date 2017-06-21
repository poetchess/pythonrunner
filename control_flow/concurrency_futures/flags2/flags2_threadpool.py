import collections
from  concurrent import futures

import requests
import tqdm

from flags2_common import main, HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000

def download_many(cc_list, base_url, verbose, concur_req):
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:

        # The dict will map each Future instance to the respective country code.
        to_do_map = {}

        # Order of the results will depend on the timing of the HTTP responses.
        for cc in sorted(cc_list):

            # Schedule the execution of one callable and returns an instance.
            future = executor.submit(download_one, cc, base_url, verbose)
            to_do_map[future] = cc

        done_iter = futures.as_completed(to_do_map)

        if not verbose:
            # Wrap the result of 'as_completed' with tqdm to display the progress.
            # Since 'done_iter' has no 'len', we must provide it.
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))

        # Iterate over the futures as they are completed.
        for future in done_iter:

            try:
                # Calling 'result' method on a future either returns the value
                # returned by the callable, or raises whatever exception was
                # caught when the callable was executed. This method may block
                # waiting for a resolution, but not here since 'as_complete'
                # only returns futures that are done.
                res = future.result()

            except requests.exceptions.HTTPError as exc:
                error_msg = 'HTTP {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=exc.response)
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.error

            counter[status] += 1
            if verbose and error_msg:

                # Retrieve the context from dict, using current future as a key.
                cc = to_do_map[future]
                print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
