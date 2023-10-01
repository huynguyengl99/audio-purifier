[![CI](https://github.com/huynguyengl99/audio-purifier/workflows/Test/badge.svg)](https://github.com/huynguyengl99/audio-purifier/actions?query=workflow%3ATest) [![PyPI version](https://badge.fury.io/py/audio-purifier.svg)](https://badge.fury.io/py/audio-purifier)

# Audio Purifier

**Audio Purifier** is a utility package that enables silent parts
removal from audio, exporting as new files. Inspired by
`faster-whisper`, which used SileroVAD for audio processing..

## Requirements

* Python 3.9 or greater


* You can open and save `WAV` files with pure python. For opening
and saving non-wav files – like mp3 – you'll need [ffmpeg](http://www.ffmpeg.org/)
or [libav](http://libav.org/) in order to install extra package
(PyDub).

## Installation

The module can be installed from [PyPI](https://pypi.org/project/audio-purifier/):

```bash
pip install audio-purifier
```

To have the ability to export output file as other than 'wav' format, please install
[ffmpeg](http://www.ffmpeg.org/) to your run time and install PyDub library as well.

```bash
pip install audio-purifier[extra]
```

<details>
<summary>Other installation methods (click to expand)</summary>

### Install the latest dev version from github (or replace `@master` with a [@release_version]

```bash
pip install git+https://github.com/huynguyengl99/audio-purifier@master
```

</details>

## Document
Please visit [Audio Purifier doc](https://audio-purifier.readthedocs.io/) for
documentation.
