import collections


def check_palindrome(s, substitutions):
    """
    Check that we could build a palindrome from s with at most `substitutions` of substitutions.

    return '1' or '0' as Ture/False.

    >>> check_palindrome("abc", 0)
    '0'
    >>> check_palindrome("abc", 1)
    '1'
    >>> check_palindrome("a", 0)
    '1'
    >>> check_palindrome("aa", 0)
    '1'
    >>> check_palindrome("aaa", 0)
    '1'
    >>> check_palindrome("aaabb", 0)
    '1'
    >>> check_palindrome("aaabb", 0)
    '1'
    >>> check_palindrome("aaabbb", 0)
    '0'
    >>> check_palindrome("aaabbb", 1)
    '1'
    >>> check_palindrome("aaabbc", 0)
    '0'
    >>> check_palindrome("aaabbc", 1)
    '1'
    >>> check_palindrome("aaabcd", 1)
    '0'
    >>> check_palindrome("aaabcd", 2)
    '1'
    """

    if len(s) < 2:
        return '1'

    # the main idea:
    # 1 - count all symbols
    # 2 - drop off even counters, they doesn't make sense;
    # 3 - count odd counters - this is how many symbols have no pair;
    # 4 - if length of s is even than we are allowed to have 1
    # non-paired symbol to build a palindrome - it would be in the
    # center of it;
    # 5 - if there is still some non-paired symbols then we can make
    # them paired by substitutions, 1 substitution allow to transform
    # 2 unpaired symbols into 1 pair, so may have no more than
    # substitutions*2 unpaired symbols

    max_need_pairs = substitutions * 2
    need_pairs = 0 if len(s) % 2 == 0 else -1
    for counter in collections.Counter(s).values():
        if counter % 2:
            need_pairs += 1

            if need_pairs > max_need_pairs:
                return '0'

    return '1'


def palindromeChecker(s, l, r, k):
    res = []
    for left_index, right_index, substitutions in zip(s, l, r, k):
        res.append(check_palindrome(s[left_index, right_index + 1], substitutions))
    return "".join(res)


# if __name__ == '__main__':
