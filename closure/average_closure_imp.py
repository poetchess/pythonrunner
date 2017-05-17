# Within averager, series is a free variable: a variable not bound in the local scope.
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager


if __name__ == "__main__":

    avg = make_averager()    
    print(avg(10))
    print(avg(11))
    print(avg(12))
    print()

    print('Inspecting the function created by make_averager:')
    print()
    print('Names of local variables:')
    print(avg.__code__.co_varnames)
    print('Names of free variables:')
    print(avg.__code__.co_freevars)
    print('Binding for the free variables:')
    print(avg.__closure__)
    print('Contents for the free variables:')
    print(avg.__closure__[0].cell_contents)
