def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        # 'count' is determined by python interpreter as local variable.
        # and the variable reference is before assignment.
        # Since it is not a free variable, it is not saved in the closure.
        count += 1
        total += new_value
        return total / count

    return averager

if __name__ == '__main__':
    avg = make_averager()
    print(avg(10))
    print(avg(11))
    print(avg(12))