def simple_coro2(a):
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


if __name__ == '__main__':

    my_coro = simple_coro2(14)

    from inspect import getgeneratorstate

    # The coroutine has not started.
    print(getgeneratorstate(my_coro))

    # Advance coroutine to first yield
    print(next(my_coro))
    print(getgeneratorstate(my_coro))

    # Send number to suspended coroutine; the yield expression evaluates to 28
    # and that number is bound to b
    print(my_coro.send(28))

    try:
        # coroutine terminates, causing the generator object to raise exception:
        # StopIteration.
        my_coro.send(99)
    except StopIteration:
        print(getgeneratorstate(my_coro))

