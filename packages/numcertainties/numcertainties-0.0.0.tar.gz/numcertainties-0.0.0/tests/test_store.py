import pytest 
import numpy as np
import numpy.testing as npt
from numcertainties import munc
from numcertainties import uunc
from numcertainties import nunc

def test_store():
	x = [1, 2]
	xcov = [[3, 0],
	        [0, 4]]

	for unc in munc,:

		print("test_store")

		n = unc(x, xcov,store=True)
		npt.assert_array_equal(n.get_value(), [1,2])
		npt.assert_array_equal(n.get_std(), [3**0.5,4**0.5])
		npt.assert_array_equal(n.get_value(), n.get_value())
		npt.assert_array_equal(n.get_std(), n.get_std())

		n = unc(x, xcov,store=False)
		npt.assert_raises(AssertionError,npt.assert_array_equal,n.get_value(), n.get_value())
		npt.assert_raises(AssertionError,npt.assert_array_equal,n.get_std(), n.get_std())



test_store()