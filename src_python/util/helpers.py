def tuples_equal(tuple_a, tuple_b):
    if not type(tuple_a) == type(tuple_b) == tuple:
        return False
    if len(tuple_a) != len(tuple_b):
        return False
    for (a, b) in zip(tuple_a, tuple_b):
        if type(a) != type(b):
            return False
        if a != b:
            return False
    return True
