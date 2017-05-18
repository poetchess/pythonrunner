registry = []

def register(func):
    print('running registry(%s)' % func)
    registry.append(func)
    return func

# Function decorators are executed as soon as the module is imported.
# But decorated functions only run when they are explicitly invoked.
@register
def f1():
    print('running f1()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f3()')

def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()