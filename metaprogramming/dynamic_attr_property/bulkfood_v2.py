class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    # @property decorates the getter method
    # The methods that implement a property all have the name of the public attribute
    @property
    def weight(self):
        return self.__weight

    # The decorated getter has a .setter attribute, which is also a decorator;
    # This ties the getter and setter together.
    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


if __name__ == '__main__':
    raisins = LineItem('Golden raisins', 10, 6.95)
    print(raisins.subtotal())

    try:
        raisins.weight = -20
        print(raisins.subtotal())
    except ValueError:
        print('invalid input')
