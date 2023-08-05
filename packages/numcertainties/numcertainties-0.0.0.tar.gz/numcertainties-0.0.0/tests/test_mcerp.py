import pytest
from numcertainties import munc as unc

def test_fail_rel():
	x = [10]
	xcov = [1e-1**2]

	n = unc(x, xcov,rel=1.)
	nn = (n**2).propagate()
	print (nn.get_value(), nn.get_std())
	assert nn.get_value() != pytest.approx([100]),"Retry if it fails (very unlikely)"
	assert nn.get_std() != pytest.approx([0.002], rel=1e-3)

def test_success_rel():
	x = [10]
	xcov = [1e-4**2]
	for rel in [1e-1,1e-2,1e-3]:
		n = unc(x, xcov,rel=rel)
		nn = (n**2).propagate()
		print (nn.get_value(), nn.get_std())
		assert nn.get_value() == pytest.approx([100], rel=rel),"rel=%g"%rel
		assert nn.get_std() == pytest.approx([0.002], rel=rel),"rel=%g"%rel