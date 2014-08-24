import pytest
from nlist import NList


def test_init():
    NList()
    NList(shape=(2, 3))
    NList(shape=(2, 0))
    NList(shape=(2, 3), default=42)
    NList(default='useless')
    NList(other=NList(shape=(2, 3)))

    with pytest.raises(RuntimeError):
        NList(other=NList(), shape=(3, 2))
    with pytest.raises(RuntimeError):
        NList(other=NList(), default=42)
    with pytest.raises(RuntimeError):
        NList(other=NList(), shape=(3, 2), default=42)

    with pytest.raises(ValueError):
        NList(shape=(2, -1, 3))

    with pytest.raises(TypeError):
        NList(other=4)
    with pytest.raises(TypeError):
        NList(shape=(2, 'wat'))

def test_init_from_nlist():
    l = NList(shape=(2, 3), default=42)
    l[0, 1] = 7
    l2 = NList(other=l)

    assert l == l2
    assert l is not l2
    assert l.shape == l2.shape
    assert l.rank == l2.rank
    assert l.size == l2.size
    assert l[0, 1] == l2[0, 1] == 7
    assert l[0, 0] == l2[0, 0] == 42

    l2[0, 0] = 56
    assert l != l2
    assert l[0, 0] != l2[0, 0] == 56

def test_init_from_nested():
    l = NList(other=[[1, 2, 3], [4, 5, 6]])
    assert l.shape == (2, 3)
    assert l[0, 0] == 1
    assert l[0, 2] == 3
    assert l[1, 0] == 4
    assert l[1, 2] == 6

    l = NList(other=[[1, 2], [3]])
    assert l.shape == (2,)
    assert l[0] == [1, 2]
    assert l[1] == [3]

    assert NList(other=[]).shape == (0,)
    assert NList(other=[[], []]).shape == (2, 0)

def test_init_from_shape():
    l = NList(shape=(2, 3), default='d')
    assert l.shape == (2, 3)
    assert l.rank == 2
    assert l.size == 6
    assert l[0, 0] == 'd'

    assert NList().shape == ()
    assert NList(shape=(2, 3))[0, 0] == None

def test_shape():
    assert NList().shape == ()
    assert NList(shape=(3, 2)).shape == (3, 2)

    l = NList(shape=(5, 6))
    with pytest.raises(AttributeError):
        l.shape = (5, 7)

def test_rank():
    assert NList().rank == 0
    assert NList(shape=(3, 2)).rank == 2

    l = NList(shape=(5, 6))
    with pytest.raises(AttributeError):
        l.rank = 8

def test_size():
    assert NList().size == 0
    assert NList(shape=(3, 2)).size == 6
    assert NList(shape=(3, 0, 2)).size == 0
    assert NList(shape=(3,)).size == 3

    l = NList(shape=(5, 6))
    with pytest.raises(AttributeError):
        l.size = 4

def test_bool():
    assert bool(NList()) == False
    assert bool(NList(shape=(2, 3))) == True
    assert bool(NList(shape=(3, 0, 2))) == False

def test_indexing():
    l = NList(shape=(2, 3))
    l[0, 0] = 0
    l[0, 1] = 1
    l[0, 2] = 2
    l[1, 0] = 3
    l[1, 1] = 4
    l[1, 2] = 5
    with pytest.raises(IndexError):
        l[0, 3] = 42
    with pytest.raises(IndexError):
        l[2, 0] = 42
    with pytest.raises(IndexError):
        l[1, 3] = 42
    with pytest.raises(IndexError):
        l[1, -1] = 42
    with pytest.raises(TypeError):
        NList()[1, 1] = 42
    with pytest.raises(TypeError):
        NList(shape=(2, 3, 0, 6))[1, 1] = 42
    with pytest.raises(TypeError):
        l[1, 'wat'] = 42
    with pytest.raises(TypeError):
        NList()[()] = 42

    assert l[0, 0] == 0
    assert l[0, 2] == 2
    assert l[1, 0] == 3
    assert l[1, 2] == 5
    with pytest.raises(IndexError):
        l[0, 3]
    with pytest.raises(IndexError):
        l[2, 0]
    with pytest.raises(IndexError):
        l[1, 3]
    with pytest.raises(IndexError):
        l[1, -1]
    with pytest.raises(TypeError):
        NList()[1, 1]
    with pytest.raises(TypeError):
        NList(shape=(2, 3, 0, 6))[1, 1]
    with pytest.raises(TypeError):
        l[1, 'wat']
    with pytest.raises(TypeError):
        NList()[()]

    l = NList(shape=(3,), default=42)
    assert l[0] == 42
    l[1] = 1
    assert l[1] == 1
    with pytest.raises(IndexError):
        l[3]
    with pytest.raises(IndexError):
        l[-1]

def test_equality():
    assert NList() == NList(shape=())
    assert NList(shape=(3, 2), default=1) == NList(shape=(3, 2), default=1)
    assert NList(shape=(3, 2), default=1) != NList(shape=(3, 2), default=2)
    assert NList(shape=(3, 2)) != NList(shape=(2, 3))

    l = NList(shape=(2, 3), default=5)
    l[1, 2] = 8
    l2 = NList(l)
    assert l == l2
    l2[0, 1] = 7
    assert l != l2

    assert NList(shape=(3,)) != [None] * 3
    assert NList() != []
    assert NList() != 42

def test_copy():
    l = NList(shape=(2, 3), default=42)
    l[0, 1] = 7
    l2 = l.copy()

    assert l == l2
    assert l is not l2
    assert l.shape == l2.shape
    assert l.rank == l2.rank
    assert l.size == l2.size
    assert l[0, 1] == l2[0, 1] == 7
    assert l[0, 0] == l2[0, 0] == 42

    l2[0, 0] = 56
    assert l != l2
    assert l[0, 0] != l2[0, 0] == 56

def test_count():
    assert NList().count('wat') == 0

    l = NList(shape=(2, 3), default=7)
    assert l.count(7) == 6
    l[0, 1] = 5
    assert l.count(7) == 5
    assert l.count(5) == 1

def test_iter():
    l = NList([1, 2, 3])
    assert list(iter(l)) == [1, 2, 3]
    assert list(NList()) == []
    assert list(NList([[1, 2, 3], [4, 5, 6]])) == [1, 2, 3, 4, 5, 6]
    assert max(NList([[5, 2, 3], [1, 2, 5], [7, 9, 2]])) == 9

    assert None not in NList()
    assert 56 in NList([[1, 2, 3], [4, 56, 42]])
    assert 78 not in NList([5, 8, 9])
    assert 7 in NList(shape=(5, 8), default=7)

def test_str():
    l = NList()
    assert str(l) == repr(l) == 'NList([], shape=())'
    l = NList([1, 2, 3])
    assert str(l) == repr(l) == 'NList([1, 2, 3], shape=(3,))'
    l = NList([[1, 2, 3], [4, 5, 6]])
    assert str(l) == repr(l) == 'NList([[1, 2, 3], [4, 5, 6]], shape=(2, 3))'
    l = NList([])
    assert str(l) == repr(l) == 'NList([], shape=(0,))'
    l = NList(shape=(5, 3, 0))
    assert str(l) == repr(l) == 'NList([], shape=(5, 3, 0))'

def test_keys():
    assert list(NList().keys()) == []
    assert list(NList(shape=(5, 0, 3)).keys()) == []
    assert list(NList([1, 2, 3]).keys()) == [(0,), (1, ), (2, )]
    assert list(NList([[1, 2, 3], [4, 5, 6]]).keys()) == [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2)
    ]

def test_enumerate():
    assert list(NList().enumerate()) == []
    assert list(NList(shape=(5, 0, 3)).enumerate()) == []
    assert list(NList([1, 2, 3]).enumerate()) == [((0,), 1), ((1,), 2), ((2, ), 3)]
    assert list(NList([[1, 2, 3], [4, 5, 6]]).enumerate()) == [
        ((0, 0), 1), ((0, 1), 2), ((0, 2), 3),
        ((1, 0), 4), ((1, 1), 5), ((1, 2), 6)
    ]
