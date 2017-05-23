class Demo:
    # classmethod defines a method that operates on the class instead of instances.
    # classmethod changes the way the method is called, so it reveives the class
    #   itself as the first argument. The most common use is for alternative
    #   constructors.
    @classmethod
    def klassmeth(*args):
        return args

    # staticmethod decorator changes a method so that it receives no special first
    #   argument.
    @staticmethod
    def statmeth(*args):
        return args

if __name__ == '__main__':
    print(Demo.klassmeth())
    print(Demo.klassmeth('spam'))
    print(Demo.statmeth())
    print(Demo.statmeth('spam'))
