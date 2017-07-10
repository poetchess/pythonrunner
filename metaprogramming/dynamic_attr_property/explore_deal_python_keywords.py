import keyword
from collections import abc

class FrozenJSON:
    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            # Handling the special case where attribute names are Python keywords.
            # For example: grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982})
            # It doesn't work to read grad.class because 'class' is a reserved word.
            # But we can access like this: getattr(grad, 'class')

            # Similar problem may arise if a key in the JSON is not a valid
            # Python identifier: x = FrozenJSON({'2be':'or not'}), x.2be
            # The problematic keys can be detected in Python 3 using str.isidentifier().
            # Turning an invalid key into valid attribute name is not trivial,
            # two solution would be: raising an exception or replacing the invalid keys
            # with generic names like attr_0, attr_1, and so on.
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
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
