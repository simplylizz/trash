import time

import pymongo


collection = pymongo.MongoClient().domains.ru_expiring
collection.drop()
collection = pymongo.MongoClient().domains.ru_expiring
collection.drop_index('*')


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
    global last_lines

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
    bulk = collection.initialize_unordered_bulk_op()

    print_timings(0, 'start')

    for line_no, line in enumerate(input_, 1):
        domain, reg_date, exp_date, reg_name = line.split(' ', 3)
        domain = domain.split('.', 1)[0]

        # domains.append({
        #     'name': domain,
        #     'exp_date': exp_date,
        #     'reg_date': reg_date,
        #     'last_seen': update_time,
        # })

        # bulk.find({'name': domain}).upsert().update({'$set': {
        #     'exp_date': exp_date,
        #     'reg_date': reg_date,
        #     'last_seen': update_time,
        #     'reg_name': reg_name,
        # }})
        bulk.insert({
            '_id': domain,
            'exp_date': exp_date,
            'reg_date': reg_date,
            'reg_name': reg_name,
        })
        if line_no % 1000000 == 0:
            res = bulk.execute()
            print_timings(line_no, 'inserted')
            bulk = collection.initialize_unordered_bulk_op()

    res = bulk.execute()
    print_timings(line_no, 'finished inserts')
    #collection.create_index('name')
    #print_timings(line_no, 'finished building index')
