

def get_parents(node):
    p = node.parent

    while p:
        yield p
        p = node.parent


def common_parent(first, second):
    first_parents = list(get_parents(first))
    second_parents = list(get_parents(second))

    last_common_parent = None
    for fp, sp in zip(first_parents[::-1], second_parents[::-1]):
        if fp != sp:
            return last_common_parent
        else:
            last_common_parent = fp