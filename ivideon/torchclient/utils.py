import logging
import signal

from tornado import ioloop


logger = logging.getLogger(__name__)


def stop(*args, **kwargs):
    logger.info('stopping instance')
    ioloop.IOLoop.instance().stop()


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
