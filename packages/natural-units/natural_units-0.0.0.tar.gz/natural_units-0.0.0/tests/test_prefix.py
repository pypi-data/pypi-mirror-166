from natural_units.prefix import *
import pytest

def test_milli():
    pytest.approx(milli, 0.001)
    pytest.approx(m*1, 0.001)
    pytest.approx(T*p,1)