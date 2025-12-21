import humidity as rh

def test_is_too_wet():
    assert(rh.is_too_wet(70,80)==False)
    assert(rh.is_too_wet(90,80)==True)
    assert(rh.is_too_wet(80,80)==False)

def test_calcavg():
    input=[10,20,30,40,50]
    assert(rh.calcavg(input)==30)

#added unit test for humidity calculations