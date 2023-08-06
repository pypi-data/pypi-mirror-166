from . import natural as su

# Here we just mirror natural, but without mass dimensions
for k in su.__dir__():
    v = su.__getattribute__(k)
    if isinstance(v, su.natural_unit):
        print(v)
        globals()[k] = v.value
    elif isinstance(v, float):
        print(v)
        globals()[k] = v
    elif isinstance(v, int):
        print(v)
        globals()[k] = v