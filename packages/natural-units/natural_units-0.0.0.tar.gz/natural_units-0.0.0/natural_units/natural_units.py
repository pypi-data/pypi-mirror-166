import math

from .prefix import *
from . import base_units as bu

num = dict({'length': -1, 'mass': 1, 'time': -1,
           'temperature': 1, 'momentum': 1, 'energy': 1})
rev_num = dict([reversed(i) for i in num.items()])


class natural_unit(bu.base_unit):
    def __init__(self, val=1, units= None,massdim=0):
        self.value = val
        if(massdim in num):
            massdim = num[massdim]
        if units is None:
            units = {}
        self.units = units 
        if "massdimension" not in self.units.keys():
            print("set",self.units)
            self.units["massdimension"] = massdim
        
    def __str__(self):
        if self.units.keys() == {"massdimension"}:
            return self.value.__str__() + "[" + self.units["massdimension"].__str__() + "]"
        else:
            return super().__str__()

    def __repr__(self):
        if self.units.keys() == {"massdimension"}:
            return self.value.__repr__() + "[" + self.units["massdimension"].__repr__() + "]"
        else:
            return super().__repr__()

    def __format__(self, fmt):
        if self.units.keys() == {"massdimension"}:
            return self.value.__format__(fmt) + "[" + self.units["massdimension"].__repr__() + "]"
        else:
            return super().__format__(fmt)

pi = math.pi

eV = natural_unit(massdim='energy')
c = natural_unit(massdim='length')/natural_unit(massdim='time')
kb = natural_unit(massdim='energy')/natural_unit(massdim='temperature')
hbar = natural_unit(massdim='energy')*natural_unit(massdim='time')


# fundamental
c0 = 299792458 * c  # m/s
hbar0 = 4.135667662e-15/(2*pi)*hbar
kb0 = 8.617333262145e-5*kb

# from wikipedia https://de.wikipedia.org/wiki/Nat%C3%BCrliche_Einheiten
J = joule = 1/(1.60218e-19)*eV

meter = 1/hbar0/c0 * natural_unit(massdim='length')

s = second = 1/hbar0*natural_unit(massdim='time')

gram = 1/kilo*(1/1.78266e-36) * natural_unit(massdim='mass')

# *c0*c0
kelvin = 1*kb0*natural_unit(massdim='temperature')

# composite
barn = 1e-28*meter**2

u = 1/(6.022141e26)*kilo*gram

Bq = 1/s
Ci = 37*giga * Bq
year = 31556952 * s  # inclusive
Hz = hertz = 1/s
W = watt = J/s

ly = year * c