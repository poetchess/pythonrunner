import model_v6 as model

# LineItem class will be evaluated by the interpreter and the resulting class
# object will be passed to the model.entity function. Python will bind the
# global name LineItem to whatever the model.entity function returns.
# In this example, model.entity returns the same LineItem class with the
# storage_name attribute of each descriptor instance changed.

@model.entity
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
    print(dir(raisins)[:3])
    print(LineItem.description.storage_name)
    print(raisins.description)
    print(getattr(raisins, '_NonBlank#description'))
