import math
from decimal import Decimal


def fib(n, mod):
    phi = (1 + math.sqrt(5)) / 2
    powed_phi = phi
    for i in xrange(n):
        powed_phi = (powed_phi * phi) % mod
    return int(powed_phi  / math.sqrt(5) + .5)


for i in xrange(1, 31):
    print i, fib(i, 9999999), fib(i, 1000)

#print 10**10, fib(10**10)
