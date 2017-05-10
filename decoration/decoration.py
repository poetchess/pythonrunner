# A special kind of function: a kind of function that takes one function object
# as an argument, and returns another function object as a result.
def helloSolar(original_function):
    def new_function(*args, **kwargs):
        print('*** Entering [Solar system] ***')
        original_function(*args, **kwargs)
        print('*** Leaving [Solar system] ***')
    return new_function

def helloGalaxy(original_function):
    def new_function(*args, **kwargs):
        print('*** Entering [ Galaxy system] ***')
        original_function(*args, **kwargs)
        print('*** Leaving [Galaxy system] ***')
    return new_function

# When the interpreter sees these lines of code, it will:
#   It pushes helloGalaxy onto the annotation stack.
#   It pushes helloSolarSystem onto the annotation stack.
#   It compiles the code for hello into a function object (lets call it
#       functionObject1)
#   It binds the name 'hello' to functionObject1.
#   It pops helloSolarSystem off of the annotation stack.
#   passes functionObject1 to helloSolarSystem
#   helloSolarSystem returns a new function object (lets call it
#       functionObject2), and
#   the interpreter binds the original name 'hello' to functionObject2
#   It pops helloGalaxy off of the annotation stack
#   passes functionObject2 to helloGalaxy
#   helloGalaxy returns a new function object (lets call it functionObject3), and
#   the interpreter binds the original name 'hello' to functionObject3

# The '@' sign creates a decoration line, calls the decorators defined above.
@helloGalaxy
@helloSolar
def hello(target=None):
    print('{}: Entering [Earth]'.format(target))
    print('Hello world!')
    print('Leaving [Earth]')

if __name__ == '__main__':
    # 'hello' actually refers to the new_function object returned by helloGalaxy()
    hello('Alians')
