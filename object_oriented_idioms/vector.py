from array import array
import reprlib
import math
import numbers
import functools
import operator

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

    '''
    # For a large multidimensional vector, this method is very inefficient.
    # It builds two tuples copying the entire contents of the operands just
    #   to use the __eq__ of the tuple type.
    def __eq__(self, other):
        return tuple(self) == tuple(other)
    '''

    '''
    def __eq__(self, other):
        if len(self) != len(other):
            return false
        # zip produces a generator of tuples made from the items in each
        #   iterable argument. It stops producing values without warning
        #   as soon as one of the inputs is exhausted.
        for a, b in zip(self, other):
            if a != b:
                return False
        return True
    '''

    # Same logic as above, less code.
    def __eq__(self, other):
        return len(self) == len(other) and \
            all(a==b for a, b in zip(self, other))

    def __hash__(self):
        # A perfect example of a map-reduce computation
        hashes = (hash(x) for x in self._components)
        # When using reduce, it's a good pratice to provide the third
        #   argument. It will be the value returned if the sequence is
        #   empty and is used as the first argument in reducing loop.
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    # Adding __len__ and __getitem__ to support len(v) and v[i]
    #   as well as slicing
    def __len__(self):
        return len(self._components)

    # index can be a slice object
    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    # __getattr__ method is invoked by the interpreter when attribute lookup
    #   fails. 'xyzt' can be seen as virtual attributes.
    shortcut_names = 'xyzt'
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    # In order to avoid the inconsistency (reading v.x will retrive component
    #   from the underlying array while writing v.x will only create a new 
    #   instance attribute rather than updating the array), we raise an 
    #   exception with any attempt at assigning to all single-letter lowercase
    #   attribute names.
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

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

    print(hash(v1))
    print(v1 == Vector(range(5)))
