'''
    Demonstrating the filtering generator functions in standard library 
'''

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]

if __name__ == '__main__':

    import itertools
    import operator

    # Yield accumulated sums; if func is provided, yields the result of applying
    # it to the first pair of items, then to the result and next item, etc.
    print(list(itertools.accumulate(sample)))
    print(list(itertools.accumulate(sample, min)))
    print(list(itertools.accumulate(sample, max)))
    print(list(itertools.accumulate(sample, operator.mul)))
    # factorials from 1! to 10!
    print(list(itertools.accumulate(range(1, 11), operator.mul)))

    print(list(enumerate('albatroz', 1)))
    print(list(map(operator.mul, range(11), range(11))))
    print(list(map(operator.mul, range(11), [2, 4, 8])))
    print(list(map(lambda a, b: (a, b), range(11), [2, 4, 8])))
    print(list(itertools.starmap(operator.mul, enumerate('albatroz', 1))))
    print(list(itertools.starmap(lambda a, b: b/a, enumerate(itertools.accumulate(sample), 1))))

