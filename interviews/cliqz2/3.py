def solution(N):
    if N <= 1:
        return 0
    elif N == 2:
        return 1

    a, b = 0, 1

    for i in xrange(N-1):
        a, b = b, (a + b) % 1000000

#        if b >= 1000000:
#            b -= 1000000

    return b

import datetime
s1 = datetime.datetime.now()
print solution(50000000)
print datetime.datetime.now() - s1
