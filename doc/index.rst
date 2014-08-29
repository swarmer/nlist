Welcome to nlist's documentation!
=================================
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
``pip install nlist``
Or just grab ``nlist.py``.


License
-------
MIT (see LICENSE.txt)


Contents
--------
.. toctree::
   :maxdepth: 2

   api


Indices and tables
------------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

