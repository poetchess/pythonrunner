from collections import abc

"""Note that no caching or transformation of the original feed is done.
   As the feed is traversed, the nested data structures are converted again
   and again into FrozenJSON. But that's OK for a dataset of this size.
"""
class FrozenJSON:
    """A read-only facade for navigating a JSON-like object using attribute
       notation
    """
    def __init__(self, mapping):

        # Build a dict from the 'mapping' argument. It has two purposes:
        # 1. Ensures we got a dict.
        # 2. Makes a copy for safety.
        self.__data = dict(mapping)

    # __getattr__ is called only when there's no attribute with that name.
    def __getattr__(self, name):

        # If name matches an attribute of the instance __data, return that.
        # This is how calls to methods like 'keys' are handled.
        if hasattr(self.__data, name):
            return getattr(self.__data, name)

        # Otherwise, fetch the item with the key 'name' from self.__data, and
        # return the result of calling FrozenJSON.build() on that.
        # Here, a KeyError exception may occur, in the expression self.__data[name].
        # It should be handled and an AttributeError raised instead because that's
        # what is expected from __getattr__.
        else:
            return FrozenJSON.build(self.__data[name])

    # This is an alternate constructor, a common use for the @classmethod decorator.
    @classmethod
    def build(cls, obj):

        # If 'obj' is a mapping, build a FrozenJSON with it.
        if isinstance(obj, abc.Mapping):
            return cls(obj)

        # If it is a MutableSequence, it must be a list (data source is JSON,
        # where the only collection types are list and dict), so build a list
        # by passing every item in 'obj' recursively to .build().
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]

        # If it's not a dict or a list, return the item as it is.
        else:
            return obj



if __name__ == '__main__':
    from osconfeed import load
    raw_feed = load()
    feed = FrozenJSON(raw_feed)
    print(len(feed.Schedule.speakers))
    print(sorted(feed.Schedule.keys()))
    for key, value in sorted(feed.Schedule.items()):
        print('{:3} {}'.format(len(value), key))
    print(feed.Schedule.speakers[-1].name)
    talk = feed.Schedule.events[40]
    print(type(talk))
    print(talk.name)
    print(talk.speakers)
    try:
        print(talk.flavor)
    except KeyError:
        print("No key named 'flavor'")
