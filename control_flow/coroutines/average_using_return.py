from collections import namedtuple

Result = namedtuple('Result', 'count average')

def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    # Breaking out the loop to return the result.
    # The generator object will raise StopIteration, the value attribute of the
    # exception will carry the value returned.
    return Result(count, average)


if __name__ == '__main__':
    coro = averager()
    next(coro)
    coro.send(10)
    coro.send(30)
    coro.send(6.5)
    try:
        coro.send(None)
    except StopIteration as exc:
        print(exc.value)
