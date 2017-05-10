import random

'''
    There are seven flavors of callable objects, 'class instances' is one of
    them. If a class defines a '__call__' method, then its instance may be
    invoked as functions. 
'''
class BingoCage:

    # An instance is built from any iterable, and stores an internal list of
    # items, in random order.
    def __init__(self, items):
        self._items = list(items)
        # shuffle is guaranteed to work because self._items is a list.
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    # Shortcut to bingo.pick(): bingo()
    def __call__(self):
        return self.pick()

if __name__ == '__main__':
    bingo = BingoCage(range(3))
    print(bingo.pick())
    print(bingo())
    print(callable(bingo))