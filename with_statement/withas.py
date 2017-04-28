class TraceBlock:

    def message(self, arg):
        print('running ' + arg)

    # The return value is assigned to the variable in the as clause if present.
    def __enter__(self):
        print('starting with block')
        return self
        
    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            print('exit normally\n')
        else:
            print('raise an exception! ' + str(exc_type))
            return False        #propagate the exception

if __name__ == '__main__':
    with TraceBlock() as action:
        action.message('test 1')
        print('reached')

    with TraceBlock() as action:
        action.message('test 2')
        raise TypeError
        print('not reached')    
