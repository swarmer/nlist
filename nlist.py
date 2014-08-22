import operator
from collections.abc import Container, Iterable
from functools import reduce


def product(l):
    return reduce(operator.mul, l, 1)


class NList:
    def __init__(self, other=None, shape=None, default=None):
        if other is not None:
            if shape is not None or default is not None:
                raise RuntimeError(
                    "'other' and 'shape'/'default' arguments are mutually exclusive"
                )

            self._data = other._data.copy()
            self._shape = other.shape
            self._strides = other._strides
        else:
            if shape is None:
                shape = ()
            self._check_shape(shape)

            self._shape = shape
            self._data = [default] * self.size
            self._strides = tuple(
                product(self.shape[j] for j in range(k + 1, self.rank))
                for k in range(self.rank)
            )

    @property
    def shape(self):
        return self._shape

    @property
    def rank(self):
        return len(self.shape)

    @property
    def size(self):
        if self.shape == ():
            return 0
        else:
            return product(self.shape)

    def __bool__(self):
        return self.size != 0

    def __eq__(self, other):
        return (
            isinstance(other, NList) and
            self.shape == other.shape and
            self._data == other._data
        )

    def __getitem__(self, key):
        self._check_index(key)
        return self._data[self._index_to_flat(key)]

    def __setitem__(self, key, value):
        self._check_index(key)
        self._data[self._index_to_flat(key)] = value

    def copy(self):
        return type(self)(other=self)

    def count(self, value):
        return self._data.count(value)

    def _index_to_flat(self, index):
        return sum(self._strides[k] * index[k] for k in range(self.rank))

    def _check_index(self, index):
        if not all(0 <= x < self.shape[i] for i, x in enumerate(index)):
            raise IndexError('NList index out of range')

    @staticmethod
    def _check_shape(shape):
        if not all(x >= 0 for x in shape):
            raise ValueError('Dimensions cannot be negative')

#Container.register(NList)
#Iterable.register(NList)
