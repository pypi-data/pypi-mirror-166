import numpy as np

def identity(x):
    return x

# TODO take missing operators from https://github.com/tisimst/mcerp/blob/master/mcerp/__init__.py
class unc:
# We keep a stack of operations until we need to evaluate the result
    def __init__(self, x, xcov,stack=identity,store=False,**params):
        """
        params store
        """
        self.x= np.array(x)
        self.xcov= np.atleast_1d(xcov)
        self.params = params
        self.params["store"] = store
        self.stack= stack

    def propagate(self):
        if self.params["store"]:
            if self.stack is identity:
                return self
            update = self._propagate()
            self.x = update.x
            self.xcov = update.xcov
            self.stack = identity
            self.params= update.params
            return self
        else:
            return self._propagate()

    def _propagate(self):
        raise Exception("_propagate() not implemented")
    

    def get_value(self):
        return self.propagate().x

    def get_cov(self):
        return self.propagate().xcov

    def get_std(self):
        return np.sqrt(np.diag(self.get_cov()))

    def __pow__(self, other, modulo=None):
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)**other,**self.params)

    def __rpow__(self, other, modulo=None):
        return self.__class__(self.x,self.xcov, lambda x:other**self.stack(x),**self.params)

    def __radd__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:other+self.stack(x),**self.params)

    def __add__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)+other,**self.params)

    def __rsub__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:other-self.stack(x),**self.params)

    def __sub__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)-other,**self.params)

    def __rmul__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:other*self.stack(x),**self.params)

    def __mul__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)*other,**self.params)

    def __rtruediv__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:other/self.stack(x),**self.params)

    def __truediv__(self, other):
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)/other,**self.params)

    def __str__(self):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"

    def __repr__(self):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"

    def __format__(self, fmt):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"