# The result under python console is different.
# Python console automatically binds the _ variable to the result of expressions
#   that are not None. And this hidden, implicit assignment creates new references
#   to the object. Trackback objects are another common source of unexpected
#   references.

if __name__ == '__main__':
    import weakref

    a_set = {0, 1}
    wref = weakref.ref(a_set)
    print(wref)
    print(wref())
    a_set = {2, 3, 4}
    print(wref())
    print('{}'.format(wref() is None))
