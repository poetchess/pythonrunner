import model_v4 as model

class LineItem:
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

    # Read the storage attributes directly. 
    print(getattr(raisins, '_Quantity#0'), getattr(raisins, '_Quantity#1'))

    print(LineItem.price)

    try:
        raisins.weight = -20
        print(raisins.subtotal())
    except ValueError:
        print('invalid input')
