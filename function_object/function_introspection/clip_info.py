def clip(text, max_len=80):
    """ Return text clipped at the last space before or after max_len
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:     # no space were found
        end = len(text)
    return text[:end].rstrip()

"""
    The argument names appear in __code__.co_varnames, but that also includes
    the names of the local variables created in the body of the function. 
    Therefore, the argument names are the first N strings, where N is given by
    __code__.co_argcount which, by the way, does not include any variable
    arguments prefixed with * or **. The default values are identified only by
    their position in the __defaults__ tuple, so to link each with the
    respective argument, you have to scan from last to first. In the example,
    we have two arguments, text and max_len, and one default, 80, so it must
    belong to the last argument, max_len. This is awkward.
"""
if __name__ == '__main__':
    print(clip.__defaults__)
    print(clip.__code__)
    print(clip.__code__.co_varnames)
    print(clip.__code__.co_argcount)