# A better way to create a user-defined mapping type is to subclass
# collections.UserDict instead of dict. Here, the point is to show that
# '__missing__' is supported by the built-in dict.__getitem__ method.

# '__missing__' method is not defined in the base 'dict' class, but 'dict' is
# aware of it. If we subclass 'dict' and provide a '__missing__' method, the
# standard dict.__getitem__ will call it whenever a key is not found, instead
# of raising KeyError.
class StrKeyDict0(dict):
    def __missing__(self, key):
        if isinstance(key, str):
            # Check is needed to avoid potencial infinite recursion.
            raise KeyError('key {} is missing'.format(key))
        return self[str(key)]

    # The 'get' method delegates to __getitem__ by using the self[key]
    # notation; that gives the opportunity for our __missing_ to act.
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            # If a KeyError was raised, __missing_ already failed, so we return
            # the 'default'.
            return default

    # This method is needed for consistent behavior.
    def __contains__(self, key):
        # Search for unmodified key, then for a str built from the key.
        # A subtle detail in the implementation: we do not check for the key
        #   in the usual Pythonic way, k in mydict, because that would
        #   recursively call __contains__. We avoid this by explicitly looking
        #   up the key in self.keys().
        return key in self.keys() or str(key) in self.keys()


if __name__ == '__main__':
    d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    print('Tests using `d[key]` notation:')
    print(d['2'])
    print(d[4])
    try:
        print(d[1])
    except KeyError as e:
        print(e)

    print('Tests using `d.get(key)` notation:')
    print(d.get('2'))
    print(d.get(4))
    print(d.get(1, 'N/A'))

    print('Tests the `in` operation:')
    print(2 in d)
    print(1 in d)

