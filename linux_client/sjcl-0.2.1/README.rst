Python-SJCL
===========

|Travis CI| |Python versions| |new-style BSD|

Decrypt and encrypt messages compatible to the "Stanford Javascript
Crypto Library (SJCL)" message format. This is a wrapper around
pycrypto.

This module was created while programming and testing the encrypted blog
platform on cryptedblog.com which is based on sjcl.

Typical usage may look like this:

.. code:: python

        #!/usr/bin/env python

        from sjcl import SJCL

        cyphertext = SJCL().encrypt(b"secret message to encrypt", "shared_secret")

        print cyphertext
        print SJCL().decrypt(cyphertext, "shared_secret")

Public repository
-----------------

https://github.com/berlincode/sjcl

License
-------

Code and documentation copyright Ulf Bartel. Code is licensed under the
`new-style BSD license <./LICENSE.txt>`__.

.. |Travis CI| image:: https://travis-ci.org/berlincode/sjcl.svg?branch=master&style=flat
   :target: https://travis-ci.org/berlincode/sjcl
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/sjcl.svg
   :target: https://pypi.python.org/pypi/sjcl/
.. |new-style BSD| image:: https://img.shields.io/pypi/l/sjcl.svg
   :target: https://github.com/berlincode/sjcl/blob/master/LICENSE.txt
