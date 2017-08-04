
def record_factory(cls_name, field_names):
    try:
        # Duck typing: try to split field_names by commas or spaces; if that
        # fails, assume it'a already an iterable, with one name per item.
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        pass

    # Build a tuple of attribute names, this will be the __slots__ attribute of
    # the new class; this also sets the order of the fields for unpacking and
    # __repr__.    
    field_names = tuple(field_names)

    # This function will be the __init__ method in the new class. It accepts
    # positional and/or keyword arguments.
    def __init__(self, *args, **kwargs):
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)
        for name, value in attrs.items():
            setattr(self, name, value)

    # Implement an __iter__ so the class instances will be iterable; yield the
    # field values in the order given by __slots__.
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    # Produce the nice repr, iterating over __slots__ and self.
    def __repr__(self):
        values = ', '.join('{}={!r}'.format(*i) for i
                           in zip(self.__slots__, self))

        return '{}({})'.format(self.__class__.__name__, values)

    # Assemble dictionary of class attributes.
    # We could have named the __slots__ class attribute anything else, but then
    # we'd have to implement __setattr__ to validate the names of attributes being
    # assigned, because for this record-like classes we want the set of attributes
    # to be always the same and in the same order.
    cls_attrs = dict(__slots__ = field_names,
                     __init__  = __init__,
                     __iter__  = __iter__,
                     __repr__  = __repr__)

    # Build and return the new class, calling the 'type' constructor.
    # 'type' behaves like a class that creates a new class when invoked with three
    # arguments: 'name', 'base', 'dict'. The instance of 'type' are classes.
    return type(cls_name, (object,), cls_attrs)


if __name__ == '__main__':
    Dog = record_factory('Dog', 'name weight owner')
    rex = Dog('Rex', 30, 'Bob')
    print(rex)
    
    name, weight, _ = rex
    print(name, weight)

    print("{2}'s dog weighs {1}kg".format(*rex))

    rex.weight = 32
    print(rex)

    print(Dog.__mro__)

    # Not permitted
    try:
        rex.hi = 'hi'
    except AttributeError as e:
        print(e)
