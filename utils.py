import argparse
from contextlib import contextmanager

import RPi.GPIO as GPIO


@contextmanager
def autocleanup():
    try:
        yield
    finally:
        GPIO.cleanup()


@contextmanager
def pwm(port, frequency=2, duty=50):
    GPIO.setup(port, GPIO.OUT)
    p = GPIO.PWM(port, frequency)
    p.start(duty)
    yield p
    p.stop()


class SensorArgs(object):
    def __init__(self, component_names, description='Command line interface for GPIO example.'):
        self.parser = argparse.ArgumentParser(description)
        self.parser.add_argument('--board-mode', default=False, help="Whether to use BOARD port numbering", action='store_true')
        self.component_names = component_names

        self.parsed = False

        best_ports = [17, 18, 22, 23, 24, 25, 4]
        if len(component_names) > len(best_ports):
             raise ValueError('Cannot provide default ports for more than {} components'.format(len(best_ports)))

        for default_port, name in zip(best_ports, component_names):
            self.parser.add_argument('--{}-port'.format(name), type=int,
                        help='The port in which the {} is plugged. (default: %(default)s)'.format(name),
                        default=default_port)

    def __getitem__(self, component):
        if self.parsed == False:
            self.args = self.parser.parse_args()
        name = '{}_port'.format(component).replace('-', '_')
        return vars(self.args)[name]

    @property
    def board_mode(self):
        if self.parsed == False:
            self.args = self.parser.parse_args()
        return self.args.board_mode


