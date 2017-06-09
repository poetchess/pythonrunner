'''
    Demonstrating the filtering generator functions in standard library 
'''

def vowel(c):
    return c.lower() in 'aeiou'

if __name__ == '__main__':

    import itertools

    # Apply predicate to each item of iterable, yielding the item if predicate(item)
    # is truthy; if predicate is None, only truthy items are yielded.
    print(list(filter(vowel, 'Aardvark')))

    # Oppesite to the filter, with the predicate logic negated: yields items
    # whenever predicate computes falsy.
    print(list(itertools.filterfalse(vowel, 'Aardvark')))

    # Consume iterable skipping items while predicate computes truthy, then yields
    # every remaining item.
    print(list(itertools.dropwhile(vowel, 'Aardvark')))

    # Opposite operation, yields items while predicate computes truthy, then stops.
    print(list(itertools.takewhile(vowel, 'Aardvark')))

    # Consume two iterable in parallel, yields items from 1st iterable whenever the
    # corresponding item in 2nd iterable is truthy.
    print(list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1))))

    # Yields items from a slice of iterable, similar to s[:stop] or s[start:stop:step]
    # except accepting any iterable and the operation is lazy.
    print(list(itertools.islice('Aardvark', 4)))
    print(list(itertools.islice('Aardvark', 4, 7)))
    print(list(itertools.islice('Aardvark', 1, 7, 2)))
