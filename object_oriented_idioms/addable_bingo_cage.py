import itertools
from tombola import Tombola
from bingocage import BingoCage

class AddableBingoCage(BingoCage):
    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    # No need to implement __radd__ since __add__ can only deal with
    #   AddableBingoCage object. If O1 is not an AddableBingoCage object and
    #   O2 is an AddableBingoCage object, O1 + O2 will enter O2.__radd__(O1), 
    #   and delegated to O2.__add__(O1), and the final result is the same:
    #   TypeError

    # In general, if a forward infix operator method is designed to work only
    #   with the same type as self, it's useless to implement the corresponding
    #   reverse method, because that, by definition, will only be invoked when
    #   dealing with an operand of a different type.

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operand in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))
        self.load(other_iterable)
        # Augmented assignment special methods must return self
        return self
