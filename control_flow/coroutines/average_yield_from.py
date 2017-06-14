from collections import namedtuple

Result = namedtuple('Result', 'count average')

# The subgenerator
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term  is None:
            break
        total += term
        count += 1
        average = total / count
    return Result(count, average)


# The delegating generator
def grouper(results, key):
    while True:
        # Whenever grouper is sent a value, it's piped into the averager instance
        # by the yield from. grouper will be suspended here as long as the averager
        # instance is consuming values sent by the client. When an averager instance
        # runs to the end, the value it returns is bound to result[key]. The while
        # loop then proceeds to create another averager instance to consume more
        # values.
        results[key] = yield from averager()


# The client, a.k.a the caller
def main(data):
    results = {}

    for key, values in data.items():

        group = grouper(results, key)

        # Prime the grouper delegating generator, which enters its while loop
        # and suspends at the yield from, after calling the subgenerator averager.
        next(group)

        for value in values:
            # Send each value into the grouper. That value ends up in the
            # term = yield line of averager; grouper never has a chance to see it.
            group.send(value)

        # Here the execution loops back to the top of the outer for loop, a new
        # grouper instance is created and bound to `group`. The previous grouper
        # instance is garbage collected together with its own unfinished averager
        # subgenerator instance.

        # Sending None into grouper causes the current averager instance to terminate,
        # and allows grouper to run again, which creates another averager for the next
        # group of values.
        group.send(None)

    # print(results)
    report(results)

# output report
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(result.count, group,
              result.average, unit))

data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

if __name__ == '__main__':
    main(data)
