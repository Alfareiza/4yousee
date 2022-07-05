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
    TOKEN_APP_KEY = ''
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
    TOKEN_APP_KEY = ''
    my = FouryouseeAPI(TOKEN_APP_KEY, name='Client 1', account='https://4usee.com/pepe', account_type='self')

Best Practices
--------------

Always, when one of the next functions are executed witouth sending params on it:

`get_users`, `get_users_groups`, `get_uploads`, `get_medias`, `get_media_category`,
`get_players`, `get_playlists`, `get_templates`, `get_newsources`, `get_news` or `get_reports`.


You will be able to access to the attribute of the object according to that resource. For example:

.. code:: python

    >>> my.get_players()
    ...  # Will return a list of dicts where every dict depicts one player
    >>> my.players[-1]
    ... # Will return one dict, the last player of the list

Of course this way to access to the information, is local. So, be careful when you consult an resource.
This must be outdated.

Example:

.. code:: python

    >>> my.get_medias()
    ...  # List of dicts where every dict depicts one media
    >>> my.medias[-1]['id']
    129
    >>> my.delete_media(my.medias[-1]['id'])
    True
    >>> my.medias[-1]['id']
    129  # This media still exists in the context of the object
    >>> my.get_medias(id=129)  # Calling the API
    Exception: {"message":"Media with ID 129 was not found"}

This happens because attributes are locally. So, they might help you to avoid calls to the API.

Be ingenous in how to handle this behavior.
