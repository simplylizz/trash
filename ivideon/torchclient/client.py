import logging
import socket
import struct

from tornado import gen
from tornado import ioloop
from tornado import iostream
from tornado import tcpclient

from . import torch
from . import utils


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@gen.coroutine
def comain():
    host = raw_input('host (default: 127.0.0.1): ')
    port = raw_input('port (default: 9999): ')

    if not host:
        host = '127.0.0.1'
    if not port:
        port = 9999
    else:
        port = int(port)

    logger.debug('connecting to server %s:%s', host, port)
    try:
        stream = yield tcpclient.TCPClient().connect(host, port)
    except socket.error:
        logger.error('failed to connect')
        utils.stop()
        return

    torch_ = torch.Torch()

    while not stream.closed():
        try:
            res = yield stream.read_bytes(3)
        except iostream.StreamClosedError:
            utils.stop()
            return

        type_, length = struct.unpack('>BH', res)

        if length > 0:
            try:
                value = yield stream.read_bytes(length)
            except iostream.StreamClosedError:
                logger.warning('connection closed in the middle of command')
                utils.stop()
                return
            value = int(value.encode('hex'), 16)
        else:
            value = None

        logger.debug('got message %s %s %s', type_, length, repr(value))
        torch_.process_message(type_, value)


def main():
    comain()
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
