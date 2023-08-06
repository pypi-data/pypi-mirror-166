import uuid
import numpy as np

def identity(x):
    return x

def uuid_merge(list_uuids1,list_uuids2):
    combined_uuids = list(set(list_uuids1+ list_uuids2))
    index_combined = [i for i in range(len(combined_uuids))]
    index_list1 = [combined_uuids.index(i) for i in list_uuids1]
    index_list2 = [combined_uuids.index(i) for i in list_uuids2]
    ind_list2 = [list_uuids2.index(i) for i in list_uuids2 if i not in list_uuids1]
    return combined_uuids,index_list1,index_list2,ind_list2

def indices_to_bool(indices, length):
    bool_list = [False]*length
    for i in indices:
        bool_list[i] = True
    return bool_list



# TODO take missing operators from https://github.com/tisimst/mcerp/blob/master/mcerp/__init__.py
class base_uncertainty:
# We keep a stack of operations until we need to evaluate the result
    def __init__(self, x, xcov,stack=identity,store=False,uuids=None,**params):
        """
        params store
        """
        self.x= np.atleast_1d(x)
        self.xcov= np.atleast_1d(xcov)
        if self.xcov.shape[0] != len(self.x):
            raise Exception("xcov must have same length as x")
        if self.xcov.shape != (len(self.x),len(self.x)):
            self.xcov = np.zeros((len(self.x),len(self.x)))
            np.fill_diagonal(self.xcov, np.atleast_1d(xcov))
        self.params = params
        self.params["store"] = store
        self.params["uuids"] = uuids
        if uuids is None:
            self.params["uuids"] = [uuid.uuid4() for _ in range(len(self.x))]
        self.stack= stack

    def _merge(self,other):
        c, i1, i2,ind = uuid_merge(self.params["uuids"],other.params["uuids"])
        sub = other.x[ind]
        x = np.concatenate((self.x ,sub))
        xcov = np.zeros((len(c),len(c)))
        xcov[:len(self.x),:len(self.x)] = self.xcov
        xcov[len(self.x):,len(self.x):] = other.xcov[ind,:][:,ind]
        # TODO: merge params
        params = self.params
        params["uuids"] = c
        return self.__class__(x,xcov, **params),i1,i2

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
        ret_value = self.propagate().x
        return ret_value

    def get_cov(self):
        ret_value = self.propagate().xcov
        return ret_value

    def get_std(self):
        return np.sqrt(np.diag(self.get_cov()))

    def __pow__(self, other, modulo=None):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:self.stack(x[i1])**other.stack(x[i2])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)**other,**self.params)

    def __rpow__(self, other, modulo=None):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:other.stack(x[i2])**self.stack(x[i1])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:other**self.stack(x),**self.params)

    def __radd__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:other.stack(x[i2])+self.stack(x[i1])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:other+self.stack(x),**self.params)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:self.stack(x[i1])+other.stack(x[i2])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)+other,**self.params)

    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:other.stack(x[i2])-self.stack(x[i1])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:other-self.stack(x),**self.params)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:self.stack(x[i1])-other.stack(x[i2])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)-other,**self.params)

    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:other.stack(x[i2])*self.stack(x[i1])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:other*self.stack(x),**self.params)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:self.stack(x[i1])*other.stack(x[i2])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)*other,**self.params)

    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:other.stack(x[i2])/self.stack(x[i1])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:other/self.stack(x),**self.params)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            new,i1,i2 = self._merge(other)
            new.stack = lambda x:self.stack(x[i1])/other.stack(x[i2])
            return new
        elif isinstance(other,base_uncertainty):
            raise Exception("Not implemented")
        return self.__class__(self.x,self.xcov, lambda x:self.stack(x)/other,**self.params)

    def __str__(self):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"

    def __repr__(self):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"

    def __format__(self, fmt):
        return str(self.get_value()) + "[" + str(self.get_cov()) + "]"