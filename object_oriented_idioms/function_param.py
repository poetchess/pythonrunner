class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        # The internal handling of the passenger list will not affect the argument.
        # Since the list constructor accepts any iterable, the argument passed to
        #   the passengers parameter may be a tuple or any other iterable. As we
        #   create our own list to manage, we ensure that it supports .remove()
        #   and .append() operations.
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


if __name__ == '__main__':
    basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
    # The constructor of Bus class will receive a mutable parameter.
    bus = Bus(basketball_team)
    bus.drop('Tina')
    bus.drop('Pat')
    print(bus.passengers)
    print(basketball_team)
