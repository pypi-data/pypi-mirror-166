from numcertainties import identity
import warnings
import numpy as np
import mcerp
from numcertainties.base import base_uncertainty

# from https://gist.github.com/wiso/ce2a9919ded228838703c1c7c7dad13b
def correlation_from_covariance(covariance):
    v = np.sqrt(np.diag(covariance))
    outer_v = np.outer(v, v)
    correlation = covariance / outer_v
    correlation[covariance == 0] = 0
    return correlation

class monte_carlo_uncertainty(base_uncertainty):
	def __init__(self, x, xcov,stack=identity,store=True,rel=1e-2,warn=True,**params):
		x = np.atleast_1d(x)
		std = np.sqrt(np.diag(np.atleast_1d(xcov)))
		if warn and np.any([std[i]/x[i] > rel for i in range(len(x))]):
			warnings.warn("std/value > rel. Expect bad convergence. This may not agree with linear uncertainty propagation")
		super().__init__(x, xcov,stack,store=store,rel=rel,warn=warn,**params)

# We keep a stack of operations until we need to evaluate the result
	def _propagate(self):
		tnpts = mcerp.npts
		mcerp.npts = int(1./self.params["rel"]**2)
		# TODO maybe more complicted than this for higher dimensions
		var = np.diag(self.xcov)
		std = np.sqrt(var)
		assert len(std) == len(self.x)
		ux = [mcerp.N(self.x[i], std[i]) for i in range(len(self.x))]
		tux=ux
		print("pre cor",ux,ux[0]**2)

		# all cov diagonals are 1.0
		#print("pre",ux)
		if len(self.x) >1:
			mcerp.correlate(ux,correlation_from_covariance(self.xcov))
		print("post cor",ux)
		#print("post",ux)
		y = self.stack(np.array([*ux]))
		print("post stack",y,tux[0]**2)
		#y = self.stack(unumpy.uarray(unumpy.nominal_values(np.array([*ux])),unumpy.std_devs(np.array([*ux]))))
		#print("ux" ,ux)
		#print("y" ,y,y.__class__)
		ycov = mcerp.covariance_matrix([*y])
		#print ("ycov", ycov)
		mcerp.npts = tnpts
		return self.__class__([y[i].mean for i in range(len(y))],ycov,**self.params)