from io import BytesIO

from audio_purifier import purify, purify_and_export
from pydub import AudioSegment


def test_purify_wav_file_successfully():
    raw_wav_audio_path = "tests/data/raw_audio.wav"
    raw_audio_segment = AudioSegment.from_file(raw_wav_audio_path)
    assert int(len(raw_audio_segment) / 1000) == 16

    result_byte_io = purify(raw_wav_audio_path)

    processed_audio_segment = AudioSegment.from_file(result_byte_io)
    assert int(len(processed_audio_segment) / 1000) == 5


def test_purify_other_than_wav_file_successfully():
    other_audio_path = "tests/data/raw_audio.m4a"
    other_audio_segment = AudioSegment.from_file(other_audio_path)
    assert int(len(other_audio_segment) / 1000) == 16

    result_byte_io = purify(other_audio_path, export_format="mp3")

    processed_audio_segment = AudioSegment.from_file(result_byte_io)
    assert int(len(processed_audio_segment) / 1000) == 5


def test_purify_silences_return_none():
    silences_audio_path = "tests/data/silences.m4a"
    raw_audio_segment = AudioSegment.from_file(silences_audio_path)
    assert int(len(raw_audio_segment) / 1000) == 4

    result_byte_io = purify(silences_audio_path, export_format="mp3")

    assert result_byte_io is None


def test_purify_and_export_wav_file_successfully():
    exported_wav_file = BytesIO()

    assert exported_wav_file.getvalue() == b""

    raw_wav_audio_path = "tests/data/raw_audio.wav"

    purify_and_export(raw_wav_audio_path, exported_wav_file)

    assert exported_wav_file.getvalue()
    exported_wav_file.seek(0)

    processed_audio_segment = AudioSegment.from_file(exported_wav_file)
    assert int(len(processed_audio_segment) / 1000) == 5


def test_purify_and_export_other_than_wav_file_successfully():
    exported_mp3_file = BytesIO()

    assert exported_mp3_file.getvalue() == b""

    raw_wav_audio_path = "tests/data/raw_audio.m4a"

    purify_and_export(raw_wav_audio_path, exported_mp3_file, export_format="mp3")

    assert exported_mp3_file.getvalue()
    exported_mp3_file.seek(0)

    processed_audio_segment = AudioSegment.from_file(exported_mp3_file)
    assert int(len(processed_audio_segment) / 1000) == 5
