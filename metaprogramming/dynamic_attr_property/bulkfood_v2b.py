class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')

    # build the property and assign it to a public class attribute.
    weight = property(get_weight, set_weight)


if __name__ == '__main__':
    raisins = LineItem('Golden raisins', 10, 6.95)
    print(raisins.subtotal())

    try:
        raisins.weight = -20
        print(raisins.subtotal())
    except ValueError:
        print('invalid input')
