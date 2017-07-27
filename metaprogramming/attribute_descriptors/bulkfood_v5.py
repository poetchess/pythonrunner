import model_v5 as model

class LineItem:
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

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
        stuff = LineItem('   ', 20, 9.95)
    except ValueError as e:
        print(e)

    print(LineItem.price)

    try:
        raisins.weight = -20
        print(raisins.subtotal())
    except ValueError as e:
        print(e)
