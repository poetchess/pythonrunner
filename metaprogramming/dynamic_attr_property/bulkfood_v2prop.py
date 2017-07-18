
# The storage_name argument determines where the data for each property is stored.
def quantity(storage_name):

    # The first argument of the qty_getter could be named 'self', but that would
    # be strange because this is not a class body; 'instance' refers to the
    # LineItem instance where the attribute will be stored.

    # qty_getter references storage_name, so it will be preserved in the closure
    # of this function. The value is retrieved directly from the instance.__dict__
    # to bypass the property and avoid an infinite recursion.
    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            # The value is stored directly in the instance.__dict__, again
            # bypassing the property.
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    # build a custom property object and return it.
    return property(qty_getter, qty_setter)


class LineItem:

    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description

        # Here the property is already active, making sure a negative or 0 weight
        # is rejected.
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


if __name__ == '__main__':
    nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    print(nutmeg.weight, nutmeg.price)
    print(sorted(vars(nutmeg).items()))
