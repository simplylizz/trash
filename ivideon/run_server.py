#!/usr/bin/env python

import logging
import random
import struct
import time

from tornado import ioloop
from tornado import iostream
from tornado import tcpserver

# required to set signal handlers
from torchclient import utils  # noqa


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def int_to_bytes(int_, bytes_=3):
    int_ = ('%0' + str(bytes_*2) + 'x') % int_
    return ''.join(chr(int(int_[i:i+2], 16)) for i in xrange(0, len(int_), 2))


class TorchTestServer(tcpserver.TCPServer):
    def handle_stream(self, stream, address):
        logger.info('torch %s connected', address)
        for _ in xrange(20):
            msg = random.choice([
                self.get_on, self.get_off, self.get_color, self.get_unknown])()
            try:
                stream.write(struct.pack('>BH', *msg[:2]) + msg[2])
            except iostream.StreamClosedError:
                logger.warning(
                    'connection with %s closed unexpectedly', address)
                return
            time.sleep(.5)
        logger.info('closing connection with %s', address)

    def get_on(self):
        logger.info('generating on message')
        return 0x12, 0, ''

    def get_off(self):
        logger.info('generating off message')
        return 0x13, 0, ''

    def get_color(self):
        color = random.randint(0, 0xffffff)
        logger.info('generating color #%06X message', color)
        return 0x20, 3, int_to_bytes(color)

    def get_unknown(self):
        logger.info('generating unknown message')
        return 0xff, 10, int_to_bytes(0, 10)


if __name__ == '__main__':
    server = TorchTestServer()
    server.listen(9999)
    logger.info('starting torch test server on 127.0.0.1:9999')
    instance = ioloop.IOLoop.instance()
    instance.start()
