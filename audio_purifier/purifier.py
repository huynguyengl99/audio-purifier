import io
import logging
import shutil
from pathlib import Path
from typing import BinaryIO, Optional, Union

import numpy as np
from scipy.io.wavfile import write

from audio_purifier.faster_whisper_original.audio import decode_audio
from audio_purifier.faster_whisper_original.utils import format_timestamp, get_logger
from audio_purifier.faster_whisper_original.vad import (
    VadOptions,
    collect_chunks,
    get_speech_timestamps,
)

try:
    from pydub import AudioSegment

    installed_pydub = True
except ImportError:
    installed_pydub = False

logger = get_logger()


def purify(
    audio: Union[str, BinaryIO, np.ndarray],
    export_format: Optional[str] = "wav",
    vad_parameters: Optional[Union[dict, VadOptions]] = None,
    sampling_rate: int = 16000,
) -> Optional[io.BytesIO]:
    """Purify an audio file.

    Arguments:
      audio: Path to the input file (or a file-like object), or the audio waveform.
      export_format: Default result file format is 'wav', require Pydub to convert to other format.
      vad_parameters: Dictionary of Silero VAD parameters or VadOptions class (see available
        parameters and default values in the class `VadOptions`).
      sampling_rate: Resample the audio to this sample rate.
    Returns:
      A BytesIO object that contains the processed audio, and None in case the initial audio
       contains full of silences.
    """
    if export_format != "wav" and not installed_pydub:
        raise ImportError(
            "Only support 'wav' natively. To support your format please install Pydub. "
            "You can install by using [extra] option."
        )

    if not isinstance(audio, np.ndarray):
        audio = decode_audio(audio, sampling_rate=sampling_rate)

    duration = audio.shape[0] / sampling_rate

    if vad_parameters is None:
        vad_parameters = VadOptions()
    elif isinstance(vad_parameters, dict):
        vad_parameters = VadOptions(**vad_parameters)
    speech_chunks = get_speech_timestamps(audio, vad_parameters)
    audio = collect_chunks(audio, speech_chunks)
    duration_after_vad = audio.shape[0] / sampling_rate

    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(
            "VAD filter removed %s of audio",
            format_timestamp(duration - duration_after_vad),
        )
        logger.debug(
            "VAD filter kept the following audio segments: %s",
            ", ".join(
                "[{} -> {}]".format(
                    format_timestamp(chunk["start"] / sampling_rate),
                    format_timestamp(chunk["end"] / sampling_rate),
                )
                for chunk in speech_chunks
            ),
        )

    if not audio.size:
        return

    output = io.BytesIO()
    write(output, sampling_rate, audio)

    if export_format != "wav":
        audio = AudioSegment.from_file(output)

        output = audio.export(format=export_format)

    return output


def purify_and_export(
    audio: Union[str, BinaryIO, np.ndarray],
    export: Union[str, BinaryIO],
    export_format: Optional[str] = "wav",
    vad_parameters: Optional[Union[dict, VadOptions]] = None,
    sampling_rate: int = 16000,
) -> bool:
    """Purify an audio file and then export it.

    Arguments:
      audio: Path to the input file (or a file-like object), or the audio waveform.
      export: Path or byte-like object that the result should be saved to.
      export_format: Default result file format is 'wav', require Pydub to convert to other format.
        Will be overridden if export exist.
      vad_parameters: Dictionary of Silero VAD parameters or VadOptions class (see available
        parameters and default values in the class `VadOptions`).
      sampling_rate: Resample the audio to this sample rate.
    Returns:
      True if the audio is successfully processed and written to the export file, otherwise False.
    """
    if export and isinstance(export, str):
        extension = Path(export).suffix
        if not extension:
            raise ValueError("")
        export_format = extension[1:]

    processed_audio = purify(audio, export_format, vad_parameters, sampling_rate)

    if not processed_audio:
        return False

    if hasattr(export, "write"):
        fid = export
    else:
        fid = open(export, "wb")

    shutil.copyfileobj(processed_audio, fid)

    if not hasattr(export, "write"):
        fid.close()
    else:
        fid.seek(0)

    return True
