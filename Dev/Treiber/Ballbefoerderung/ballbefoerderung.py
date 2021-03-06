__author__ = 'Andri'
import Dev.Treiber.Ballbefoerderung.config as CFG
#import Dev.Hardware.DCMotor.WiringPiDC as DC
import Dev.Hardware.DCMotor.PigpioSWDC as DC
#import Dev.Hardware.DCMotor.PigpioDC as DC

class Ballbefoerderung:
    def __init__(self):
        self.config = CFG.BFConfig()
        self.dcMotor = None
        self.dcMotor = DC.DCController(self.config.pulse_length, self.config.freq, self.config.gpio_port)
        print "Ballbefoerderung inited"

    def run(self,pulse_length=0):
        if pulse_length==0:
            pulse_length=self.config.pulse_length
        self.dcMotor.set_pulse_length(pulse_length)
        self.dcMotor.run()
        print "Ballbefoerderung run"

    def set_speed(self, pulse_length):
        #self.config.set_pulse_length(pulse_length)
        self.dcMotor.set_pulse_length(pulse_length)

    def stop(self):
        self.dcMotor.stop()
        print "Ballbefoerderung stop"

    @property
    def get_config(self):
        return self.config

    def save_config(self):
        self.config.save_config()
        self.dcMotor = None
        self.dcMotor = DC.DCController(self.config.pulse_length, self.config.freq, self.config.gpio_port)