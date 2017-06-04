from array import array
import reprlib
import math
import numbers
import functools
import operator
import itertools

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
    # No meaning to allow Vector([1.0, 2.0, 3.0]) == tuple(1, 2, 3)
    def __eq__(self, other):
        if isinstance(other, Vector):
            return len(self) == len(other) and \
                all(a==b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __hash__(self):
        # A perfect example of a map-reduce computation
        hashes = (hash(x) for x in self._components)
        # When using reduce, it's a good pratice to provide the third
        #   argument. It will be the value returned if the sequence is
        #   empty and is used as the first argument in reducing loop.
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    '''
        Special methods implementing unary or infix operators should never change
        their operands. Expressions with such operators are expected to produce
        results by creating new objects. Only augmented assignment operators may
        change the first operand (self).
    '''
    # special method for the '-' unary operator
    # returns a new instance
    def __neg__(self):
        return Vector(-x for x in self)

    # special method for the '+' unary operator
    # returns a new instance
    def __pos__(self):
        return Vector(self)

    # if two vector instances are of different length, fill out shorter one
    #   with zeros.
    # Can be called with any iterable that produces numbers.
    #   (i.e. Vector2d, tuplei, ...)
    # In the spirit of duck typing, we refrain from testing the type of the
    #   'other' operand, or the type of its elements. We'll catch the exception
    #   and return NotImplemented. This way, we leave the door open for the
    #   implementor of the other operand type to perform the operation when
    #   Python tries the reversed method call.
    def __add__(self, other):
        try :
            # pairs is a generator that will produce tuples (a, b)
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            # returns a new instance
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        # delegating to __add__
        return self + other

    def __mul__(self, scalar):
        # goose typing, check the type of scalar against the numbers.Real ABC
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

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

    def angle(self, n):
        r = math.sqrt(sum(x * x for x in self[n:]))
        a = math.atan2(r, self[n-1])
        if (n == len(self) -1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

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
