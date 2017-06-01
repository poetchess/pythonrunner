import abc

class Tombola(abc.ABC):
    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.
            
        This method should raise `LookupError` when the instance is empty.
        """

        # The fact that pick() may raise LookupError is also part of its interface.
        # But there is no way to declare this in Python, except in the document.
        # By throwing LookupError, we can also deal with IndexError and KeyError,
        #   since they are subclasses of LookupError.

    def loaded(self):
        """Return `True` if there's at least 1 item, `False` otherwise."""

        # Expensive operation. A concrete subclass can override it.
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple with the items currently inside."""

        # We cannot know how concrete subclass will store the items. We can
        #   build the inspect() result by emptying the Tombola with successive
        #   calls to pick() and then use load() to put everything back.
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))
