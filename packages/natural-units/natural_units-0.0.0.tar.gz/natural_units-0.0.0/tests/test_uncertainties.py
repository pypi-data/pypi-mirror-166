from uncertainties import ufloat
from natural_units import si_units as si

def test_unc():
	f = ufloat(1, 0.1)*si.meter
	assert str(f) == "1.00+/-0.10 m"
	
