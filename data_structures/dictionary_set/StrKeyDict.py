"""StrKeyDict always converts non-string keys to str - on insertion, update,
   and lookup
"""

import collections

# UserDict subclasses MutableMapping, the remaining methods that make
# StrKeyDict a full-fledged mapping are inherited from UserDict,
# MutableMapping, or Mapping.
class StrKeyDict(collections.UserDict):
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError('Key {} is missing'.format(key))
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item        

if __name__ == '__main__':
    d = StrKeyDict([('2', 'two'), ('4', 'four')])
    print('Tests using `d[key]` notation:')
    print(d['2'])
    print(d[4])
    try:
        print(d[1])
    except KeyError as e:
        print(e)

    # We inherit Mapping.get which is implemented exactly like StrKeyDict0.get.
    print('Tests using `d.get(key)` notation:')
    print(d.get('2'))
    print(d.get(4))
    print(d.get(1, 'N/A'))

    print('Tests the `in` operation:')
    print(2 in d)
    print(1 in d)

