from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

promos = []

def promotion(promo_func):
    promos.append(promo_func)
    return promo_func

# Any function decorated by @promotion will be added into 'promos'
@promotion    
def fidelity_promo(order):
    """ 5% discount for customers with 1000 or more fidelity points """
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion    
def bulk_item_promo(order):
    """ 10% discount for each LineItem with 20 or more units """
    discount  = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion    
def large_order_promo(order):
    """ 7% discount for orders with 10 or more distince items """
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    """ Select the best discount availabe """
    return max(promo(order) for promo in promos)

if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = [LineItem('banana', 4, .5), LineItem('apple', 10, 1.5),
            LineItem('watermellon', 5, 5.0)]
    cart_banana = [LineItem('banana', 30, .5), LineItem('apple', 10, 1.5)]
    long_order = [LineItem(str(item_code), 20, 1.0) for item_code in range(10)]
    joe_order = Order(joe, cart, fidelity_promo)
    ann_order = Order(ann, cart, fidelity_promo)
    joe_order_banana = Order(joe, cart_banana, bulk_item_promo)
    joe_order_long = Order(joe, long_order, large_order_promo)
    joe_order_wrong_promo = Order(joe, cart, large_order_promo)
    print(joe_order)
    print(ann_order)
    print(joe_order_banana)
    print(joe_order_long)
    print(joe_order_wrong_promo)
    print('Best promotion for Joe with long cart: {:.2f}'.format(best_promo(joe_order_long)))
