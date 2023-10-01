from audio_purifier.faster_whisper_original.vad import get_vad_model


def preload_models():
    """Preload the model so that it won't need time to excuse on the first request.
    List of models will be preloaded:

    - VAD
    """
    get_vad_model()
