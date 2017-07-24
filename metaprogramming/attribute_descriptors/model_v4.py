class Quantity:
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter

        # Using the hash character in the prefix guarantees the 'storage_name'
        # will not clash with attributes created by the user using dot notation,
        # because nutmeg._Quantity#0 is not invalid Python syntax, but we can
        # always get and set attributes with such "invalid" identifiers using
        # the getattr and seattr built-in functions, or by the instance __dict__.
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    # We need ot implement __get__ because the name of the managed attribute is
    # not the same as the 'storage_name'.

    # The 'owner' argument is a reference to the managed class and it's handy when
    # the descriptor is used to get attributes from the class. If a managed attribute,
    # such as 'weight', is retrieved via the class Like LineItem.weight, the descriptor
    # __get__ method receives 'None' as the value for the 'instance' argument.
    # To support introspection and other metaprogramming tricks by the user, it's a
    # good practice to make __get__ return the descriptor instance when the managed
    # attribute is accessed through the class.
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.storage_name, value)
        else:
            raise ValueError('value must be > 0')


