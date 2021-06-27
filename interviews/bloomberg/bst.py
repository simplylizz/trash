


def is_bst(node, max_value=float('inf'), min_value=float('-inf')):
    #     50
    #   40  80
    # N  45
    #   N  49

    # print(f"{node.value} <= {max_value}?")
    if node.value > max_value:
        return False
    # print(f"{node.value} > {min_value}?")
    if node.value <= min_value:
        # print(f"failed: {node.value} <= {min_value}")
        return False

    if node.left is not None:
        # if node.left.value > node.value:
        #     return False

        if not is_bst(node.left, min_value=min_value, max_value=node.value):
            # print("1")
            return False

    if node.right is not None:
        # if node.right.value >= node.value:
        #     return False

        if not is_bst(node.right, max_value=max_value, min_value=node.value):
            # print("2")
            return False

    # print("3")
    return True


class Node(object):
    def __init__(self, v, l=None, r=None):
        self.value = v
        self.left = l
        self.right = r

#     5
#   4  8
# N  6
assert is_bst(
    Node(
        5,
        Node(4, None, Node(6)),
        Node(8),
    )
) == False

#     50
#   40  80
# N  45
#   N  51
assert is_bst(
    Node(
        50,
        Node(40, None, Node(45, None, Node(51))),
        Node(80),
    )
) == False


#     50
#   40  80
# N  45
#   N  49
assert is_bst(
    Node(
        50,
        Node(40, None, Node(45, None, Node(49))),
        Node(80),
    )
) == True


#     50
#   40  80
# N  45
#   39  49
assert is_bst(
    Node(
        50,
        Node(40, None, Node(45, Node(39), Node(49))),
        Node(80),
    )
) == False


#     5
#   3  8
# N  4
assert is_bst(
    Node(
        5,
        Node(3, None, Node(4)),
        Node(8),
    )
) == True
