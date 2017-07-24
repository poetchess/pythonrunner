
# Descriptor class:
#   A class implementing the descriptor protocol.

# Managed class:
#   The class where the descriptor instances are declared as class attributes.

# Descriptor instance:
#   Each instance of a descriptor class, declared as a class attribute of the
#   managed class.

# Managed instance:
#   One instance of the managed class

# Storage attribute:
#   An attribute of the managed instance that will hold the value of a managed
#   attribute for that particular instance.

# Managed attribute
#   A public attribute in the managed class that will be handled by a descriptor
#   instance, with values stored in storage attributes. A descriptor instance
#   and a storage attribute provide the infrastructure for a managed attribute.


# This is a descriptor class.
# Descriptor is a protocol-based feature; no subclassing is needed to implement one.
class Quantity:

    def __init__(self, storage_name):

        # Each Quantity instance will have a 'storage_name' attribute, that's
        # the name of the attribute that will hold the value in the managed
        # instances.
        self.storage_name = storage_name

    # __set__ is called when there is an attemp to assign to the managed attribute.
    # Here 'self' is the descriptor instance, 'instance' is the managed instance,
    # and 'value' is the value being assigned.
    def __set__(self, instance, value):
        if value > 0:

            # we must handle the managed instance __dict__ directly; trying to
            # use the 'setattr' built-in would trigger the __set__ method again,
            # leading to infinite recursion.
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError('value must be > 0')


class LineItem:

    # The first descriptor instance is bound to the 'weight' attribute.
    # The second descriptor instance is bound to the 'price' attribute.
    weight = Quantity('weight')
    price = Quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price



if __name__ == '__main__':
    raisins = LineItem('Golden raisins', 10, 6.95)
    print(raisins.subtotal())

    try:
        raisins.weight = -20
        print(raisins.subtotal())
    except ValueError:
        print('invalid input')
