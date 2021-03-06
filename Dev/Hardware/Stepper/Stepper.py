__author__ = 'endru'

import time
import pigpio
import math


class Stepper:
    def __init__(self, dir_pin, pulse_pin, enable_pin, microsteps1_pin, microsteps2_pin, min_delay=400, max_delay=2000,
                 acc=100):
        self.dir_pin = dir_pin
        self.pulse_pin = pulse_pin
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.acc = acc
        self.microsteps1_pin = microsteps1_pin
        self.microsteps2_pin = microsteps2_pin
        self.enable_pin = enable_pin
        self.pi = pigpio.pi()
        self.set_enable(True)


    def init_pigpio_pins(self):
        self.pi.wave_tx_stop()
        self.pi.wave_clear()
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        self.pi.write(self.pulse_pin, 0)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 0)

    def __del__(self):
        print "del stepper"
        pi = pigpio.pi()
        pi.wave_tx_stop()
        pi.wave_clear()
        pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        pi.write(self.pulse_pin, 0)
        pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        pi.write(self.dir_pin, 0)

    def set_enable(self, enable):
        self.pi.set_mode(self.enable_pin, pigpio.OUTPUT)
        if enable:
            self.pi.write(self.enable_pin, 0)
        else:
            self.pi.write(self.enable_pin, 1)

    def set_fullstep(self):
        self.set_microsteps1(False)
        self.set_microsteps2(False)

    def set_microsteps(self):
        self.set_microsteps1(True)
        self.set_microsteps2(True)

    def set_microsteps1(self, do_microsteps):
        self.pi.set_mode(self.microsteps1_pin, pigpio.OUTPUT)
        if do_microsteps:
            self.pi.write(self.microsteps1_pin, 1)
        else:
            self.pi.write(self.microsteps1_pin, 0)

    def set_microsteps2(self, do_microsteps):
        self.pi.set_mode(self.microsteps2_pin, pigpio.OUTPUT)
        if do_microsteps:
            self.pi.write(self.microsteps2_pin, 1)
        else:
            self.pi.write(self.microsteps2_pin, 0)

    def move_steps(self, steps):
        print "move steps: " + str(steps)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        if steps < 0:
            self.pi.write(self.dir_pin, 0)
            steps = -steps
        else:
            self.pi.write(self.dir_pin, 1)
        self.run_steps(steps)

    def steps_right(self, steps):
        print "steps right: " + str(steps)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 1)
        self.run_steps(steps)

    def steps_left(self, steps):
        print "steps left: " + str(steps)
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.write(self.dir_pin, 0)
        self.run_steps(steps)

    def run_steps(self, steps):
        self.pi.wave_clear()
        self.pi.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.pulse_pin, pigpio.OUTPUT)
        wf = []

        final_delay = max(int(self.max_delay - int(float(steps) / 2) * self.acc), self.min_delay)
        print "final_delay: " + str(final_delay) + ", max_delay: " + str(self.max_delay) + ", min_delay: " + str(
            self.min_delay)
        ramp_steps = int(math.ceil(float(self.max_delay - final_delay) / self.acc))
        middle_steps = max(steps - 2 * ramp_steps, 0)

        # build initial ramp up
        for delay in range(self.max_delay, final_delay, -self.acc):
            wf.append(pigpio.pulse(1 << self.pulse_pin, 0, delay))
            wf.append(pigpio.pulse(0, 1 << self.pulse_pin, delay))

        # middle steps
        if middle_steps > 0:
            for delay in range(middle_steps):
                wf.append(pigpio.pulse(1 << self.pulse_pin, 0, final_delay))
                wf.append(pigpio.pulse(0, 1 << self.pulse_pin, final_delay))

        # build ramp down
        for delay in range(final_delay, self.max_delay, +self.acc):
            wf.append(pigpio.pulse(1 << self.pulse_pin, 0, delay))
            wf.append(pigpio.pulse(0, 1 << self.pulse_pin, delay))

        if len(wf)==0:
            print "no steps"
            return

        self.pi.wave_add_generic(wf)

        # add after existing pulses

        offset = self.pi.wave_get_micros()

        wid1 = self.pi.wave_create()

        # send ramp, stop when final rate reached

        self.pi.wave_send_once(wid1)
        print "wait offset: " + str(offset)
        time.sleep(float(offset + 200) / 1000000.0)  # make sure it's a float
        self.init_pigpio_pins()
        # while self.pi.wave_tx_busy():
        # offset = self.pi.wave_get_micros()
        # time.sleep(float(offset) / 1000000.0)


