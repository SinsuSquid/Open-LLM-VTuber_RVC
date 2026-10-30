import os
import asyncio
import torch
from loguru import logger

# Ensure torch.load can load legacy fairseq / RVC checkpoints in PyTorch >= 2.6
_orig_torch_load = torch.load


def _patched_torch_load(*args, **kwargs):
    if "weights_only" not in kwargs:
        kwargs["weights_only"] = False
    return _orig_torch_load(*args, **kwargs)


torch.load = _patched_torch_load

from rvc_python.infer import RVCInference


class RVCEngine:
    """Manages RVC model inference for audio voice conversion."""

    def __init__(
        self,
        model_path: str,
        index_path: str = "",
        device: str = "cpu:0",
        f0_up_key: int = 0,
        f0_method: str = "pm",
        index_rate: float = 0.75,
        filter_radius: int = 3,
        resample_sr: int = 0,
        rms_mix_rate: float = 0.25,
        protect: float = 0.33,
    ):
        self.model_path = model_path
        self.index_path = index_path
        self.device = device
        self.f0_up_key = f0_up_key
        self.f0_method = f0_method
        self.index_rate = index_rate
        self.filter_radius = filter_radius
        self.resample_sr = resample_sr
        self.rms_mix_rate = rms_mix_rate
        self.protect = protect

        self.rvc: RVCInference | None = None
        self._initialize()

    def _initialize(self):
        """Initialize RVC inference instance and load model."""
        if not self.model_path or not os.path.exists(self.model_path):
            logger.warning(f"RVC model path not found: {self.model_path}")
            return

        try:
            logger.info(
                f"Initializing RVC engine with model '{self.model_path}' on {self.device}..."
            )
            self.rvc = RVCInference(device=self.device)
            self.rvc.load_model(
                self.model_path,
                index_path=self.index_path if os.path.exists(self.index_path) else "",
            )
            self.rvc.set_params(
                f0up_key=self.f0_up_key,
                f0method=self.f0_method,
                index_rate=self.index_rate,
                filter_radius=self.filter_radius,
                resample_sr=self.resample_sr,
                rms_mix_rate=self.rms_mix_rate,
                protect=self.protect,
            )
            logger.info("RVC engine initialized successfully! (≧▽≦)✨")
        except Exception as e:
            logger.critical(f"Failed to initialize RVC engine: {e}")
            self.rvc = None

    def convert_file(self, input_path: str, output_path: str | None = None) -> str:
        """
        Synchronously convert an audio file to the target RVC voice.
        Returns the output audio file path, or input_path if conversion fails.
        """
        if not self.rvc:
            return input_path

        if not os.path.exists(input_path):
            logger.error(f"RVC input audio file does not exist: {input_path}")
            return input_path

        if not output_path:
            dir_name, base_name = os.path.split(input_path)
            output_path = os.path.join(dir_name, f"rvc_{base_name}")

        try:
            self.rvc.infer_file(input_path, output_path)
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                logger.debug(f"RVC conversion successful: {output_path}")
                return output_path
            else:
                logger.warning(
                    "RVC output file empty or not created. Falling back to original audio."
                )
                return input_path
        except Exception as e:
            logger.error(f"Error during RVC voice conversion: {e}. Falling back to original audio.")
            return input_path

    async def async_convert_file(
        self, input_path: str, output_path: str | None = None
    ) -> str:
        """Asynchronously convert audio file in a worker thread."""
        return await asyncio.to_thread(self.convert_file, input_path, output_path)
