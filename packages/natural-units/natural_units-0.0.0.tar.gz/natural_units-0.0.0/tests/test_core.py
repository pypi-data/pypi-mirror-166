import pytest
from natural_units import *

def test_conversions():
	assert convert(meter, centi*meter) == pytest.approx(100)
	assert kilo*gram*to(gram) == pytest.approx(1000)
	