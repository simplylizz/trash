import string
import random

zone = '.ru'
symbols = string.ascii_lowercase + string.digits + '-'

domains = set()


with open('output.txt', 'wb') as output:
    for i in xrange(10 * 1000 * 1000):
         domain = ''.join(random.choice(symbols) for _ in xrange(random.randint(5, 15))) + zone
         if domain not in domains:
            domains.add(domain)
            output.write('%s 1970-01-01 1971-01-01 Some Domain Registrator Name\n' % domain)
            if i % 100000 == 0:
                print i
