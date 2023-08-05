import pytest
import math
from natural_units import *

def test_all():
	assert c0 == pytest.approx(299792458)
	assert hbar0 == pytest.approx(4.135667662e-15/(2*math.pi))
	assert kb0 == pytest.approx(8.617333262145e-5)
	assert joule == pytest.approx(1/(1.60218e-19))
	assert meter == pytest.approx(1/hbar0/c0)
	assert s == pytest.approx(second) == pytest.approx(1/hbar0)
	assert pi == pytest.approx(math.pi)
	assert eV == pytest.approx(1)
	assert c == pytest.approx(1)
	assert kb == pytest.approx(1)
	assert hbar == pytest.approx(1)
	assert barn == pytest.approx(1e-28*meter**2)
	assert u == pytest.approx(1/(6.022141e26)*kilo*gram)
	assert Bq == pytest.approx(1/s)
	assert Ci == pytest.approx(37*giga * Bq)
	assert year == pytest.approx(31556952 * s)  # inclusive
	assert ly == pytest.approx( year*c)


def test_ly():
	assert ly == pytest.approx( 9460730472580800.0 * meter,1e17)

