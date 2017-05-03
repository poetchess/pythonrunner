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


# PEP342, support was added for passing values into generators.
# 'bar = yield foo' means: yield 'foo' and when a value is sent to me, set 'bar'
# to that value.

# When using send() to start a generator (execute the code from the first line
# of the generator function up to the first yield statement), we must send None.
# Since by definition, at this moment, the generator hasn't reached the first
# yield statement, so there's no one to receive the value. Once the generator is
# started, we can send values.

def get_primes(number):
    while True:
        if is_prime(number):
            number = yield number
        number += 1

def print_successive_primes(iterations, base=10):
    prime_generator = get_primes(base)
    prime_generator.send(None)
    for power in range(iterations):
        print(prime_generator.send(base ** power))

if __name__ == '__main__':
    print_successive_primes(6)
