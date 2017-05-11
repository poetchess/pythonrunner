if __name__ == '__main__':
    from clip_info import clip
    from inspect import signature
    sig = signature(clip)
    #print(sig)
    print(str(sig))
    for name, param in sig.parameters.items():
        print(param.kind, ':', name, '=', param.default)