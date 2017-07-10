import keyword
from collections import abc

'''The special method that actually constructs an instance is __new__,
   which is a class method and must return an instance.

   __init__ gets an instance when called, and is forbidden from returning
   anything, so it is really an initializer.

   pseudo code for object construction
      def object_maker(the_class, some_arg):
          new_object = the_class.__new__(some_arg)
          if isinstance(new_object, the_class):
              the_class.__init__(new_object, some_arg)
          return new_object

   The __new__ method can also return an instance of a different class, when that
   happens, the interpreter does not call __init__.
'''

class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            # the __class__ attribute of the new instance will hold a reference
            # to FrozenJSON, even though the actual construction is performed by
            # object.__new__
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])



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
