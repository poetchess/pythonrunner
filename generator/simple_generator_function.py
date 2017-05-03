# This is a 'generator function' which can create 'generators' (generator iterators).

# If the function body contains 'yield', the function automatically becomes a
# generator function.

# A generator is a special type of iterator. To be considered as an iterator,
# generators must define a few methods, one of which is __next__(). To get the
# next value from a generator, we use the same built-in function as for
# iterator:next().

# When a generator function calls 'yield', the state of the generator function
# is frozen: the values of all variables are saved and the next line of code to
# be executed is recorded until next() is called again. Once it is, the
# generator function simply resumes where it left off. If next() is never called
# again, the state recorded during the 'yield' call is eventually discarded.

# If a generator function calls 'return' or reaches the end of the definition, a
# 'StopIteration' exception is raised. This signals to whoever was calling next()
# that the generator is exhausted (The normal iterator behavior). Once a generator
# has been exhausted, calling next() on it will result in an error. We can only
# consume all the values of a generator once.

def simple_generator_function():
    yield 1
    yield 2
    yield 3

import math
def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for current in range(3, int(math.sqrt(number) + 1), 2):
            if number % current == 0:
                return False
        return True
    return False

def get_primes(number):
    while True:
        if is_prime(number):
            yield number
        number += 1

def solve_number_10():
    total = 2
    for next_prime in get_primes(3):
        if next_prime < 2000000:
            total += next_prime
        else:
            print(total)
            return

if __name__ == '__main__':
    for value in simple_generator_function():
        print(value)


    print('Solve Project Euler #10')
    solve_number_10()
