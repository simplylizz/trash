import collections
import operator
import re


OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,  # so, -1 / 2 = -1
}


def eval_expression(expression):
    def _real_eval_expression(tokens):
        if not tokens:
            raise ValueError()

        token = tokens.popleft()

        if token not in OPS:
            assert token.isdigit()
            return int(token)

        left, right = _real_eval_expression(tokens), _real_eval_expression(tokens)

        return OPS[token](left, right)

    tokens = collections.deque(expression.split())
    res = _real_eval_expression(tokens)

    if res is not None and tokens:  # not all token was consumed
        raise ValueError()

    return res


def eval_expression(expression):
    tokens = expression.split()

    stack = []
    for token in tokens[::-1]:
        if token in OPS:
            res = OPS[token](stack.pop(), stack.pop())
            stack.append(res)
        else:
            stack.append(int(token))

    assert len(stack) == 1

    return stack[0]


def max_result_expression(expression, variables=None):
    """
    >>> max_result_expression("* + 2 x y", {"x": (0, 2), "y": (2, 4)})
    9
    >>> max_result_expression("+ 1 2")
    3
    >>> max_result_expression("-+1 5 3") is None
    True
    >>> max_result_expression("+ 6 * - 4 + 2 3 8")
    -2
    >>> max_result_expression("* + 1 2 3")
    9
    >>> max_result_expression("9")
    9
    >>> max_result_expression("+ 1") is None
    True
    >>> max_result_expression("+ 1 2 3") is None
    True
    >>> max_result_expression("+ + 1 2") is None
    True
    """

    if not variables:
        try:
            return eval_expression(expression)
        except Exception:
            return None

    # just prepare string to use .format
    for var in variables:
        expression = re.sub(r"\b%s\b" % (var, ), "{%s}" % (var, ), expression)

    vars_grid = {k: v[0] for k, v in variables.items()}

    max_val = None
    while True:
        sub_expression = expression.format(**vars_grid)

        try:
            current_val = eval_expression(sub_expression)
        except Exception:
            pass
        else:
            if max_val is None or current_val > max_val:
                max_val = current_val

        # next step in search
        for k, v in vars_grid.items():
            if v+1 == variables[k][1]:
                vars_grid[k] = variables[k][0]
            else:
                vars_grid[k] += 1
                break
        else:
            return max_val
