import operator
import itertools
from itertools import islice
from collections.abc import Container, Iterable, Sequence
from functools import reduce


def product(l):
    return reduce(operator.mul, l, 1)

def group_every_n(l, n):
    rest = l
    while True:
        group, rest = list(islice(rest, n)), islice(rest, n, None)
        if not group:
            break
        yield group


class NList:
    def __init__(self, other=None, shape=None, default=None):
        if other is not None:
            if shape is not None or default is not None:
                raise RuntimeError(
                    "'other' and 'shape'/'default' arguments are mutually exclusive"
                )

            if isinstance(other, NList):
                self._init_from_nlist(other)
            elif isinstance(other, Sequence):
                self._init_from_nested(other)
            else:
                raise TypeError("'other' must be either NList or a Sequence")
        else:
            if shape is None:
                shape = ()
            self._init_from_shape(shape, default)

    def _init_from_nlist(self, other):
        self._data = other._data.copy()
        self._shape = other.shape
        self._strides = other._strides

    def _init_from_nested(self, other):
        shape = [len(other)]
        values = other
        while True:
            if (all(isinstance(x, Sequence) for x in values) and
                    len({len(x) for x in values}) == 1):
                shape.append(len(values[0]))
                values = list(itertools.chain(*values))
            else:
                break
        self._shape = tuple(shape)
        self._build_strides()
        self._data = values

    def _init_from_shape(self, shape, default):
        self._check_shape(shape)

        self._shape = shape
        self._build_strides()
        self._data = [default] * self.size

    def _build_strides(self):
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
        return self._data[self._index_to_flat(key)]

    def __setitem__(self, key, value):
        self._data[self._index_to_flat(key)] = value

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        nested = self._to_nested()
        return 'NList(%s, shape=%s)' % (nested, self.shape)

    def __str__(self):
        return repr(self)

    def copy(self):
        return type(self)(other=self)

    def count(self, value):
        return self._data.count(value)

    def keys(self, start=None):
        if self.size == 0:
            return

        current = ([0] * self.rank) if start is None else start
        while True:
            yield tuple(current)

            i = self.rank - 1
            current[i] += 1
            while current[i] >= self.shape[i]:
                current[i] = 0
                i -= 1
                if i < 0:
                    return
                current[i] += 1

    def enumerate(self, start=None):
        for key in self.keys(start):
            yield (key, self[key])

    def _to_nested(self):
        if self.size == 0:
            return []

        nested = self._data
        for dim in reversed(self.shape[1:]):
            nested = group_every_n(nested, dim)
        return list(nested)

    def _check_index(self, index):
        if len(index) != self.rank:
            raise TypeError('NList index must be rank %s' % self.rank)
        for i, x in enumerate(index):
            if not isinstance(x, int):
                raise TypeError('Indexes must consist of integers')
            if not 0 <= x < self.shape[i]:
                raise IndexError('NList index out of range')

    def _index_to_flat(self, index):
        if isinstance(index, int):
            index = (index,)

        if self.rank == 0:
            raise TypeError('Cannot index 0-rank NList')
        self._check_index(index)

        return sum(self._strides[k] * index[k] for k in range(self.rank))

    @staticmethod
    def _check_shape(shape):
        for x in shape:
            if not isinstance(x, int):
                raise TypeError('Dimensions must be integers')
            if x < 0:
                raise ValueError('Dimensions cannot be negative')

Container.register(NList)
Iterable.register(NList)
