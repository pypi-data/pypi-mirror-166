import numpy as np
from natural_units import si_units as si

def test_numpy():
    assert str(np.array([1,2,3])*si.meter) == "[1 m 2 m 3 m]"
    assert str(si.si_unit(np.array([1,2,3]),{"metre":1})) == "[1 2 3] m"
    assert str(si.si_unit(np.array([1,2,3]),{"metre":1})*si.meter) == "[1 2 3] m^2"