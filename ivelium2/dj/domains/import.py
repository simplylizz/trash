import time
import datetime

from django.db import connection

from . import models


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


def import_():
    cursor = connection.cursor()

    with open('~/repos/ivelium2/output.txt', 'rb') as input_:
        for line_no, line in enumerate(input_):
            cursor.execute(
                'INSERT INTO domains_domain ('
                'name, date_registered, date_free, last_seen, registrator'
                ') VALUES (%s, %s, %s, %s, %s) ON CONFLICT UPDATE')
