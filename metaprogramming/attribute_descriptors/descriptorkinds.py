# A descriptor that implements the __set__ method is called an overriding
# descriptor, because although it is a class attribute, a descriptor
# implementing __set__ will override attempts to assign to instance attributes.

# Properties are also overriding descriptors: if we don't provide a setter
# function, the default __set__ from the 'property' class will raise AttributeError
# to signal that the attribute is read-only.

# It's possible for overriding descriptors to implement only __set__ method. In
# this case, only writing is handled by the descriptor. Reading the descriptor
# through an instance will return the descriptor object itself because there is
# no __get__ to handle that access. If a namesake instance attribute is created
# with a new value via direct access to the instance __dict__, the __set__ method
# will still override further attempts to set that attribute, but reading that
# attribute will simply return the new value from the instance, instead of
# returning the descriptor object. In other words, the instance attribute will
# shadow the descriptor, but only when reading.

# If a descriptor does not implement __set__, then it's a nonoverriding descriptor.
# Setting an instance attribute with the same name will shadow the descriptor,
# rendering it ineffective for handling that attribute in that specfic instance.
# Methods are implemented as nonoverriding descriptors.

# auxiliary functions for display only
def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return '<class {}>'.format(obj.__name__)
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return '<{} object>'.format(cls_name(obj))

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print('-> {}.__{}__({})'.format(cls_name(args[0]), name, pseudo_args))


# essential classes for this example

# A typical overriding descriptor class with __get__ and __set__.
class Overriding:
    """a.k.a data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)

# An overriding descriptor without a __get__ method.
class OverridingNoGet:
    """an overriding descriptor without ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)

# No __set__ method here, so this is a nonoverriding descriptor.
class NonOverriding:
    """a.k.a non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    # Used here for comparison, methods are also descriptors.
    def spam(self):
        print('-> Managed.spam({})'.format(display(self)))


if __name__ == '__main__':

    print('Overriding with __set__ and __get__:')
    print('====================================')
    obj = Managed()

    print('obj.over:')
    obj.over
    print()

    print('Managed.over:')
    Managed.over
    print()

    print('obj.over = 7')
    obj.over = 7
    print()

    print('obj.over:')
    obj.over
    print()

    print('set instance attribute using __dict__:')
    obj.__dict__['over'] = 8
    print(vars(obj))
    print()

    print('obj.over:')
    obj.over
    print()

    print('Overriding without __get__:')
    print('====================================')
    print('obj.over_no_get:')
    print(obj.over_no_get)
    print()

    print('Managed.over_no_get:')
    print(Managed.over_no_get)
    print()

    print('obj.over_no_get = 7:')
    obj.over_no_get = 7
    print()

    print('obj.over_no_get:')
    print(obj.over_no_get)
    print()

    print("set instance attribute using __dict__:")
    obj.__dict__['over_no_get'] = 9
    print(vars(obj))
    print()

    print('obj.over_no_get:')
    print(obj.over_no_get)
    print()

    print('obj.over_no_get = 7:')
    obj.over_no_get = 7
    print()

    print('obj.over_no_get:')
    print(obj.over_no_get)
    print()

    print('Non overriding:')
    print('===============')
    print('obj.non_over:')
    obj.non_over
    print()

    # Here, the 'obj' now has an instance attribute named 'non_over', which
    # shadows the namesake descriptor attribute in the 'Managed' class.
    print('obj.non_over = 7:')
    obj.non_over = 7
    print('obj.non_over: {}'.format(obj.non_over))
    print()

    print('Managed.non_over:')
    Managed.non_over
    print()

    print('del obj.non_over:')
    del obj.non_over
    print('obj.non_over:')
    obj.non_over
    print()