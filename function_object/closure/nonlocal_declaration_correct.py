def make_averager():
    count = 0
    total = 0

    # nonlocal declaration was introduced in python 3.
    # It allows to flag a variable as a free variable even when it is assigned
    #   a new value within the function. If a new value is assigned to a nonlocal
    #   variable, the binding stored in the closure is changed.
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count

    return averager

if __name__ == '__main__':
    avg = make_averager()
    print(avg(10))
    print(avg(11))
    print(avg(12))