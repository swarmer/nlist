nlist
=====
|travis|   |coveralls|

.. |travis| image:: http://img.shields.io/travis/swarmer/nlist.svg
.. |coveralls| image:: http://img.shields.io/coveralls/swarmer/nlist.svg

nlist is a lightweight multidimensional list in Python.

nlist supports Python 3.4+.


Example code
------------
::

    from nlist import NList
    
    l = NList([[1, 2], [3, 4]])
    l[1, 0] = '42'
    print(l.index('42')) #=> (1, 0)


Installation
------------
Just grab ``nlist.py``.


License
-------
MIT (see LICENSE.txt)
