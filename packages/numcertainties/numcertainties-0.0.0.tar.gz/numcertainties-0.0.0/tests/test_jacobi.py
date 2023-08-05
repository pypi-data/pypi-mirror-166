import jacobi as jb
import pytest 
import numpy as np
from numcertainties import nunc
from numcertainties import uunc

def test_jacobi():
	x = [1, 2]
	xcov = [[3, 1],
	        [1, 4]]

	y, ycov = jb.propagate(lambda x:x**2, x, xcov)
	z,zcov = jb.propagate(lambda x:x**2, y, ycov)
	a,acov = jb.propagate(lambda x:x**4, x, xcov)
	print (a , z)
	print(acov , zcov)
#	assert np.all(a == z)
#	assert np.all(acov == zcov)

	n = nunc(x, xcov)
	print("nstd",n.get_std())
	nn = n**4
	print("nnval",nn)
	print("nnstd",nn.get_std())

	n = uunc(x, xcov)
	print("ustd",n.get_std())
	nn = n**4
	print("uval",nn)
	print("uustd",nn.get_std())

test_jacobi()