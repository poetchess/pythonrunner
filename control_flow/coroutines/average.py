def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count


if __name__ == '__main__':

    print('calculating the running average:')
    coro = average()
    next(coro)

    print('sending 10 ...')
    print(coro.send(10))

    print('sending 30 ...')
    print(coro.send(30))

    print('sending 5 ...')
    print(coro.send(5))

