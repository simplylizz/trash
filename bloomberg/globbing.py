#!/usr/bin/env python3

import re


def glob(pattern, string):
    """
    >>> glob("a/*/c", "a/qwe/c")
    True
    >>> glob("a/*/c", "a//c")
    True
    >>> glob("a/*/c", "a/qwe/cd")
    False
    >>> glob("a/*/c", "a/qwe/cdc")
    False
    >>> glob("a/*/c", "a/qwe/cd/c")
    True
    >>> glob("*a/*/c", "a/qwe/c")
    True
    >>> glob("*a/*/c", "qwea/qwe/c")
    True
    >>> glob("a*a", "aaaa")
    True
    >>> glob("aa", "aaa")
    False
    >>> glob("*", "aaa")
    True
    >>> glob("*", "")
    True
    >>> glob("*", "")
    True
    """
    assert pattern, "empty pattern isn't allowed"

    parts = re.sub("\*+", "*", pattern).split("*")

    def real_glob(parts, string):  # Possible optimization: string -> origin string indices
        if len(parts) == 1:
            return parts[0] in ('', string)  # either equal to string or boundary star
        elif not string.startswith(parts[0]):
            return False
        else:
            next_part = parts[1]

            next_i = string.find(next_part, len(parts[0]))
            while next_i != -1:
                string = string[next_i:]

                if real_glob(parts[1:], string):
                    return True
                else:
                    next_i = string.find(next_part, 1)
            return False  # nothing matched

    return real_glob(parts, string)


# TODO: implement through NFA
