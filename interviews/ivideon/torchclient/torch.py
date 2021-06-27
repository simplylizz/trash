import logging
import os

import xtermcolor


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Torch(object):
    STATE_OFF = 0
    STATE_ON = 1

    # Bounds of color zone: line: (start col, end col).
    color_map = {
        9: (11, 18),
        10: (12, 17),
        11: (13, 16),
        12: (13, 16),
        13: (13, 16),
        14: (13, 16),
        15: (13, 16),
        16: (13, 16),
    }
    torch_on = open(os.path.join(BASE_DIR, 'torch_on.txt')).read()
    torch_off = open(os.path.join(BASE_DIR, 'torch_off.txt')).read()

    def __init__(self):
        self.state = self.STATE_OFF
        self.color = 0xffffff

        self.message_handlers_map = {
            0x12: self.process_on,
            0x13: self.process_off,
            0x20: self.process_color,
        }

    def process_on(self, message):
        logger.debug('got turn on command')
        if self.state == self.STATE_ON:
            logger.debug('torch already turned on')
            return
        self.state = self.STATE_ON
        self.draw_torch()

    def process_off(self, message):
        logger.debug('got turn off command')
        if self.state == self.STATE_OFF:
            logger.debug('torch already turned off')
            return
        self.state = self.STATE_OFF
        self.draw_torch()

    def process_color(self, message):
        logger.debug('got color command: %06x', message)
        if self.color == message:
            logger.debug('torch already the same color')
            return
        self.color = message
        self.draw_torch()

    def process_message(self, type_, message):
        if type_ in self.message_handlers_map:
            self.message_handlers_map[type_](message)
        else:
            logger.debug('skipping unknown message type: %s', type_)

    def draw_torch(self):
        if self.state == self.STATE_ON:
            torch = self.torch_on
        else:
            torch = self.torch_off

        os.system('cls' if os.name == 'nt' else 'clear')

        for line_no, line in enumerate(torch.splitlines()):
            if line_no in self.color_map:
                start, end = self.color_map[line_no]
                line = (line[:start] + xtermcolor.colorize(line[start:end], self.color) + line[end:])
            print line
