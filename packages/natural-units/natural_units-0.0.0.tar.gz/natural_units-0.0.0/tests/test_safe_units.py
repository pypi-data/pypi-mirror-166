from natural_units.base_units import IncompatibleUnitsException
import pytest
from natural_units import natural_units as nu
from natural_units import si_units as si

def test_must_fail():
	with pytest.raises(IncompatibleUnitsException):
		x = si.meter + si.second
	with pytest.raises(IncompatibleUnitsException):
		x = nu.meter + nu.joule
	x = nu.meter + nu.second

