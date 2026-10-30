import os
from loguru import logger
from ..tts.tts_interface import TTSInterface
from .rvc_engine import RVCEngine


class RVCTTSWrapper(TTSInterface):
    """
    Wraps any TTSInterface instance to apply RVC voice conversion on the synthesized speech.
    Provides complete drop-in compatibility with the rest of the application.
    """

    def __init__(self, base_tts: TTSInterface, rvc_engine: RVCEngine):
        self.base_tts = base_tts
        self.rvc_engine = rvc_engine

    async def async_generate_audio(self, text: str, file_name_no_ext=None) -> str:
        """Generate speech via base TTS, then apply RVC conversion asynchronously."""
        raw_audio_path = await self.base_tts.async_generate_audio(
            text, file_name_no_ext
        )
        if not raw_audio_path or not os.path.exists(raw_audio_path):
            return raw_audio_path

        try:
            dir_name, base_name = os.path.split(raw_audio_path)
            converted_audio_path = os.path.join(dir_name, f"rvc_{base_name}")

            result_path = await self.rvc_engine.async_convert_file(
                input_path=raw_audio_path,
                output_path=converted_audio_path,
            )

            # Clean up the intermediate raw TTS audio if conversion created a new file
            if result_path != raw_audio_path and os.path.exists(result_path):
                self.base_tts.remove_file(raw_audio_path, verbose=False)
                return result_path

            return raw_audio_path
        except Exception as e:
            logger.error(
                f"RVC conversion failed in RVCTTSWrapper: {e}. Falling back to base TTS audio."
            )
            return raw_audio_path

    def generate_audio(self, text: str, file_name_no_ext=None) -> str:
        """Synchronous audio generation and RVC conversion."""
        raw_audio_path = self.base_tts.generate_audio(text, file_name_no_ext)
        if not raw_audio_path or not os.path.exists(raw_audio_path):
            return raw_audio_path

        try:
            dir_name, base_name = os.path.split(raw_audio_path)
            converted_audio_path = os.path.join(dir_name, f"rvc_{base_name}")

            result_path = self.rvc_engine.convert_file(
                input_path=raw_audio_path,
                output_path=converted_audio_path,
            )

            if result_path != raw_audio_path and os.path.exists(result_path):
                self.base_tts.remove_file(raw_audio_path, verbose=False)
                return result_path

            return raw_audio_path
        except Exception as e:
            logger.error(
                f"RVC conversion failed in RVCTTSWrapper: {e}. Falling back to base TTS audio."
            )
            return raw_audio_path

    def remove_file(self, filepath: str, verbose: bool = True) -> None:
        """Delegate file removal to base TTS engine."""
        self.base_tts.remove_file(filepath, verbose=verbose)
