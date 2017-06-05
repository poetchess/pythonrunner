if __name__ == '__main__':

    s = 'ABC'

    # Build an iterator from the iterable.
    iterator = iter(s)

    while True:
        try:
            # Call next on the iterator to obtain the next item.
            print(next(iterator))

        # The iterator raises StopIteration when there are no further items.
        except StopIteration:

            # Release reference, the iterator object is discarded.
            del iterator
            break