__author__ = 'Andri'
from abc import ABCMeta
from abc import abstractproperty
from abc import abstractmethod
import Dev.Treiber.Zielerfassung.zielerfassung as ZF
import Dev.Treiber.Ballbefoerderung.ballbefoerderung as BF
import Dev.Treiber.Balldepot.balldepot as BD
import Dev.Treiber.Ausrichtung.ausrichtung as AR


class Steuerung:

    def __init__(self):
        self.init()

    def init(self):
        self.zielerfassung = ZF.Zielerfassung()
        self.ausrichtung=AR.

    def start(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()

    @property
    def get_zielerfassung(self):
        raise NotImplementedError()

    @property
    def get_ausrichtung(self):
        raise NotImplementedError()

    @property
    def get_ballbeförderung(self):
        raise NotImplementedError()

    @property
    def get_balldepot(self):
        raise NotImplementedError()