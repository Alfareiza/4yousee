Medias
============

.. code:: python

    from fouryousee.fouryousee import FouryouseeAPI
    TOKEN = ''
    my = FouryouseeAPI(TOKEN)


Getting all the medias
------------

Now that the object `my` has been created. You can execute the next:

.. code:: python

    my.get_medias()

It will return all the contents of your account. It will be a list of dicts.

Filtering
----------
Inside the function `get_medias` is optiona pass the next params:

- id: (int, optional) - One and only id of a media
- name: (str, optional) - Full or part name
- categoryId: (int, optional) - ID media category. It's not allowed to send a list of categories id.
- metadata: (bool, optional) - set to true to retrieve media metadata (poster, thumbnail, meta-description)

If at least one of those params are passed, the result will be a list of dicts, where every dict depicts a media. If there is an media with the id, will return a dict. If the media was not found it'll raise an exception.

Filtering by id
~~~~

.. code:: python

    my.get_medias(id=3)

Filtering by name
~~~~

.. code:: python

    my.get_medias(name='4yousee')

Filtering by categoryId
~~~~

.. code:: python

    my.get_medias(categoryId=1)

Filtering by metadata
~~~~

.. code:: python

    my.get_medias(metadata=True)

Mixing filters
~~~~

.. code:: python

    my.get_medias(name='4yousee', categoryId=1, metadata=True)


