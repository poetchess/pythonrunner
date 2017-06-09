'''
    This is used to show that iterator can also be used to produce items on the
    fly, instead of retriving from a collection.
'''
class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):

        # produce a result value equal to self.begin, but coerced to the type
        # of the subsequent additions.
        result = type(self.begin + self.step)(self.begin)

        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1

            # using index here to reduce the cumulative effect of errors when
            # working with floats.
            result = self.begin + self.step * index

# Same effect as the class listed above
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


if __name__ == '__main__':
    from fractions import Fraction
    from decimal import Decimal
    
    print('Using class')
    ap = ArithmeticProgression(0, 1, 3)
    print(list(ap))

    ap = ArithmeticProgression(1, .5, 3)
    print(list(ap))

    ap = ArithmeticProgression(0, Fraction(1, 3), 1)
    print(list(ap))

    ap = ArithmeticProgression(0, Decimal('.1'), .3)
    print(list(ap))

    print('Using function')
    gen = aritprog_gen(0, 1, 3)
    print(list(gen))

    gen = aritprog_gen(1, .5, 3)
    print(list(gen))

    gen = aritprog_gen(0, Fraction(1, 3), 1)
    print(list(gen))
    
    gen = aritprog_gen(0, Decimal('.1'), .3)
    print(list(gen))
