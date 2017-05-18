import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

# clock is the parameterized decorator factory
def clock(fmt=DEFAULT_FMT):

    # decorate is the actual decorator
    def decorate(func):

        # clock wraps the decorated function
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate

if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
