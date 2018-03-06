Anvil Test Library
==================

A library to facilitate automated testing of `Anvil <https://anvil.works>`_
applications.

Installation
------------
.. code-block::

    pip install anvil_test

Usage
-----
The library contains a module of functions which you can import to use within
your testing suite.

Example code using pytest to login to an anvil and run a trivial (failing)
test:

.. code-block::

    import pytest

    from anvil_test import session

    browser = 'firefox'
    url = 'https://<your-app>.anvilapp.net/'
    email = 'user@abc.com'
    password = 'password'


    @pytest.fixture
    def test_session():
        session.init(browser, url)
        session.login(email, password)


    def test_login(test_session):
        assert 1 == 2
