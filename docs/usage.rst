Usage
=====

.. _installation:

Installation
------------

First install it using `pip` (or `poetry`, `conda`):

.. code-block:: console

   (.venv) $ pip install audio-purifier

Purify audio
----------------

To purify and get the BytesIO result you can use the ``audio_purifier.purify()`` function:

.. code-block:: python

    from audio_purifier import purify

    result = purify('my_raw_file_path', export_format='mp3')


To purify and export to a new file destination, you can use the ``audio_purifier.purify_and_export()`` function:

.. code-block:: python

    from audio_purifier import purify_and_export

    purify_and_export('my_raw_file_path', 'my_dest_path', export_format='mp3')
