class DemoException(Exception):
    '''An exception type for the demonstration.'''

def demo_exc_handling():
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> conroutine received: {!r}'.format(x))

    # unhandled exception will abort the while loop and terminates the coroutine
    # immediately.
    raise RuntimeError('This line should never run.')


if __name__ == '__main__':

    print('Demonstrate generator.close():')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)
    coro.send(22)
    coro.close()

    from inspect import getgeneratorstate
    print(getgeneratorstate(coro))
    print()

    print('Demonstrate generator.throw() with handled exception:')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)
    coro.throw(DemoException)
    print(getgeneratorstate(coro))
    print()

    print('Demonstrate generator.throw() with unhandled exception:')
    coro = demo_exc_handling()
    next(coro)

    coro.send(11)

    try:
        coro.throw(ZeroDivisionError)
    except ZeroDivisionError:
        print(getgeneratorstate(coro))
