import pytest
from numcertainties import nunc
from numcertainties import uunc
from numcertainties import munc

def test_single():
	x = [1]
	xcov = [0.5]
	for unc in nunc,uunc,munc:
		n = unc(x, xcov)
		nn = (n+2).propagate()
		print (nn.get_value(), nn.get_std())
		assert nn.get_value() == pytest.approx([3.], rel=1e-3 if unc is munc else 0)
		assert nn.get_std() == pytest.approx([0.5**0.5], rel=1e-3 if unc is munc else 0)
	print("test_single")
	x = [10]
	xcov = [1e-4**2]
	for unc in uunc,nunc,munc:
		n = unc(x, xcov)
		nn = (n**2).propagate()
		print (nn.get_value(), nn.get_std())
		assert nn.get_value() == pytest.approx([100], rel=1e-3 if unc is munc else 0)
		assert nn.get_std() == pytest.approx([0.002], rel=1e-3 if unc is munc else 0)

def test_double():
	x = [1, 2]
	xcov = [[3, 1],
	        [1, 4]]
	for unc in nunc,uunc:
		n = unc(x, xcov)
		nn = (n**4).propagate()
		print (nn.get_value(), nn.get_std())
		assert nn.get_value() == pytest.approx([1., 16.])
		assert nn.get_std() == pytest.approx([6.928203230275509,64.])
	print("test_double")
	x = [1, 2]
	xcov = [[0.03**2, 0],
	        [0, 0.04**2]]
	for unc in nunc,uunc,munc:
		n = unc(x, xcov)
		nn = (n**2).propagate()
		print (nn.get_value(), nn.get_std())
		assert nn.get_value() == pytest.approx([1., 4.], rel=1e-3 if unc is munc else 0)
		assert nn.get_std() == pytest.approx([0.06,0.16], rel=1e-3 if unc is munc else 0)

#def test_combined():
#	x = [1]
#	xcov = [0.5]
#	y = [1]
#	ycov = [0.5]
#	for unc in uunc,munc,nunc:
#		n = unc(x, xcov)
#		m = unc(y, ycov)
#		nn = (n+m).propagate()
#		print (nn.get_value(), nn.get_std())
#		assert nn.get_value() == pytest.approx([1.])
#		assert nn.get_std() == pytest.approx([2.**0.5])

	
test_single()
test_double()
#test_combined()
	