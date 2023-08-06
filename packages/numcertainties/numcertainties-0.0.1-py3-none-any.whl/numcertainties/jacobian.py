import jacobi as jb
import numpy as np

from numcertainties.base import base_uncertainty
class jacobian_uncertainty(base_uncertainty):
# We keep a stack of operations until we need to evaluate the result
    def _propagate(self):
        y,ycov=jb.propagate(self.stack, self.x, self.xcov)
        #print("ycov",ycov)
        return self.__class__(y,ycov,**self.params)