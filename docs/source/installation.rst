Installation
============

fouryousee is a package on `PyPI <https://pypi.python.org>`__, so you can install
with pip::

    pip install fouryousee

Usage
-----

Before start, is mandatory get an API key from your 4yousee account. Follow the official documentation: `How to get a Token to integrate with the API of 4YouSee Manager
<https://suporte.4yousee.com.br/en/support/solutions/articles/72000532960-how-to-get-a-token-to-integrate-with-the-api-of-4yousee-manager>`__.

.. code:: python

    from fouryousee.fouryousee import FouryouseeAPI
    TOKEN = ''
    my = FouryouseeAPI(TOKEN_APP_KEY)

Once it has been instantiated, you will be able to consult all the information
of your 4yousee account.

Besides the token, it's optional pass the next params:

.. code::

    name  # Depicts an alias to the account, Ex.: 'Test Account', or 'Client 1'
    account  # Depicts the url of the account.
    account_type  # Depicts the type account if it is 'self' or 'enterprise'.

Sending those params, ex.:

.. code:: python

    from fouryousee.fouryousee import FouryouseeAPI
    TOKEN = ''
    my = FouryouseeAPI(TOKEN_APP_KEY, name='Client 1', account='https://4usee.com/pepe', account_type='self')
