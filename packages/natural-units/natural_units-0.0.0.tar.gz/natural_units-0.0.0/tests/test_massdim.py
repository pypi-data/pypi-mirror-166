import pytest 
from natural_units.natural_units import *

def test_massdimensions_value():
	assert eV.units["massdimension"] == 1

def test_massdimension_type():
	meter.check(natural_unit(massdim='length'))
	s.check(natural_unit(massdim='time'))
	gram.check(natural_unit(massdim='mass'))
	kelvin.check(natural_unit(massdim='temperature'))
	barn.check(natural_unit(massdim='length')**2)
	u.check(natural_unit(massdim='mass'))