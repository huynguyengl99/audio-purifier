Usage
=====

.. _installation:

Installation
------------

If you can use `wav` file after purifying, you just need to install normal package
by using `pip` (or `poetry`, `conda`):

.. code-block:: console

   (.venv) $ pip install audio-purifier

In case you want to transform the output audio format to other than `wav`
then you need to install `ffmpeg <http://www.ffmpeg.org>`_ or
`libav <http://libav.org/>`_ first and then install extra package (Pydub) by
running this command:

.. code-block:: console

   (.venv) $ pip install audio-purifier[extra]

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

Preload models
--------------

In case you want to preload model(s) on app startup, you can use the ``audio_purifier.preload_models()``:

.. code-block:: python

    from audio_purifier import preload_models

    preload_models()
