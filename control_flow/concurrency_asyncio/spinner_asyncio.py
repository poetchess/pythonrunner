import asyncio
import itertools
import sys

# Coroutine intended for use with asyncio should be decorated with
# @asyncio.coroutine. Not mandatory.
@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        # output backspace char to move the cursor to the head
        write('\x08' * len(status))
        try:
            # sleep without blocking the event loop
            # By definition, a coroutine can only be cancelled when it's suspended
            # at a yield point.
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    # clear the status line
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine
def slow_function():

    # handles the control flow to the main loop, which will resume this
    # coroutine after the sleep delay.
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
def supervisor():

    # Schedule the spin coroutine to run, wrapping it in a Task object, which
    # is returned immediately.

    # Task drives a coroutine. When we get a Task object, it is already 
    # scheduled to run.
    spinner = asyncio.async(spin('thinking!'))
    print('spinner object:', spinner)

    # Drive the slow_function(). When that is done, get the returned value.
    # Meanwhile, the event loop will continue running because slow_function
    # ultimately uses yield from asyncio.sleep() to hand control back to the
    # main loop.
    result = yield from slow_function()

    # A task object can be cancelled. This raises asyncio.CancelledError at the
    # yield line where the coroutine is currently suspended. The coroutine may
    # catch the exception and delay or even refuse to cancel.
    spinner.cancel()
    return result

def main():
    loop = asyncio.get_event_loop()

    # Drive the supervisor coroutine to completion.
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
