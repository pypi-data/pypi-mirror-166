def expand_range(s: str) -> list:
    """Returns a list of integers from string input representing a range."""
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l, h = map(int, i.split('-'))
            r += range(l, h + 1)
    return r
