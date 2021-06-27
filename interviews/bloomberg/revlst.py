

class Node:
    NODES = 0

    def __init__(self, next=None):
        self.next = next
        self.node_num = Node.NODES
        Node.NODES += 1

    def __str__(self):
        return "Node#{} -> {}".format(self.node_num, str(self.next))


def reverse(head):
    current = head
    prev = None
    next = None
    while current is not None:
        next = current.next

        current.next = prev
        prev = current
        current = next

    return prev




lst = Node(Node(Node(Node())))

print(str(lst))
print(str(reverse(lst)))
