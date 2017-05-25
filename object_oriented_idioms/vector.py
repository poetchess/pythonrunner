from array import array
import reprlib
import math
import numbers

class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    # Adding __len__ and __getitem__ to support len(v) and v[i]
    #   as well as slicing
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

if __name__ =='__main__':
    v1 = Vector(range(6))
    print('repr:')
    print(repr(v1))
    print('str')
    print(v1)

    print('Testing slicing:')

    # stop at index 9, not a problem. slice object will be passed to array
    #   and array will use slice.indices() to normalize it.
    print(repr(v1[3:9]))
    print(repr(v1[3]))
    print(repr(v1[::3]))
    print(repr(v1[-1:]))

