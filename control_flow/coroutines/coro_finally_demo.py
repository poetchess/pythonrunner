class DemoException(Exception):
    '''An exception type for the demonstration.'''

def demo_exc_handling():

    print('-> coroutine started', flush=True)
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...', flush=True)
            else:
                print('-> conroutine received: {!r}'.format(x), flush=True)
    # wrap part of the coroutine body in try/finally block, to do some cleanup
    # no matter how the coroutine ends.
    finally:
        print('-> coroutine ending', flush=True)


if __name__ == '__main__':

    from inspect import getgeneratorstate
     
    print('Demonstrate generator.close():')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)
    coro.send(22)
    coro.close()
    print(getgeneratorstate(coro))
    print()

    print('Demonstrate generator.throw() with handled exception:')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)
    coro.throw(DemoException)
    print(getgeneratorstate(coro))
    

    print('Demonstrate generator.throw() with unhandled exception:')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)
    try:
        coro.throw(ZeroDivisionError)
    except ZeroDivisionError:
        print(getgeneratorstate(coro))
