

class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right



def rdfs(node):
    if not node:
        return

    yield node

    for n in rdfs(node.left):
        yield n
    for n in rdfs(node.right):
        yield n


def dfs(node):
    to_check = [node]

    while to_check:
        node = to_check.pop()
        yield node
        if node.right:
            to_check.append(node.right)
        if node.left:
            to_check.append(node.left)

import collections


def bfs(node):
    to_check = collections.deque([node])

    while to_check:
        node = to_check.popleft()

        yield node

        if node.left:
            to_check.append(node.left)
        if node.right:
            to_check.append(node.right)
