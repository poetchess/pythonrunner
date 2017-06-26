import threading
import itertools
import time
import sys

class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        # output backspace char to move the cursor to the head
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break

    # clear the status line
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    # Calling sleep will block the main thread, but GIL will be released so the
    # secondary thread will proceed.
    time.sleep(3)
    return 42

def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=('thinking!', signal))
    print('spinner object:', spinner)
    spinner.start()
    result = slow_function()
    signal.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
