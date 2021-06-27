import time
import string
import random

import pymongo


symbols = string.ascii_lowercase + string.digits + '-'


collection = pymongo.MongoClient().domains.ru_expiring
# collection.drop()
# collection = pymongo.MongoClient().domains.ru_expiring
# collection.drop_index('*')


last_time = start_time = None
last_lines = 0


def get_times():
    """Return pair: time from last, total"""
    global last_time, start_time

    if start_time is None:
        start_time = last_time = time.time()
        return 0, 0
    else:
        old_last_time = last_time
        last_time = time.time()
        return last_time - old_last_time, last_time - start_time


def print_timings(lines=0, comment=''):
    global last_lines, last_time, start_time

    if lines == 0:
        last_time = start_time = None
        last_lines = 0

    time_ = get_times()
    print 'lines: %s, time: %.0f (total: %.0f), speed: %.0f (total: %.0f) [%s]' % (
        lines,
        time_[0],
        time_[1],
        (lines - last_lines) / time_[0] if time_[0] else 0,
        lines / time_[1] if time_[1] else 0,
        comment,
    )
    last_lines = lines


with open('output.txt', 'rb') as input_:
    domains = [''.join(random.choice(symbols) for _ in xrange(random.randint(5, 15))) for _ in xrange(1000000)]

    #print_timings(0, 'start find one')
    #for domain in domains:
    #    collection.find_one({'name': domain})
    #print_timings(1000000, 'finished')

    print_timings(0, 'start find many like')
    for line_no, domain in enumerate(domains):
        [x for x in collection.find({'name': {'$regex': domain}}).limit(20)]
        if line_no % 1 == 0:
            print_timings(line_no, 'querying...')
    print_timings(line_no, 'finished')
