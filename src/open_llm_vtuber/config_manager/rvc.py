# config_manager/rvc.py
from pydantic import Field
from typing import Dict, ClassVar, Optional
from .i18n import I18nMixin, Description


class RVCConfig(I18nMixin):
    """Configuration for RVC (Retrieval-based Voice Conversion) post-processing."""

    enabled: bool = Field(default=False, alias="enabled")
    model_path: str = Field(default="", alias="model_path")
    index_path: str = Field(default="", alias="index_path")
    device: str = Field(default="cpu:0", alias="device")
    f0_up_key: int = Field(default=0, alias="f0_up_key")
    f0_method: str = Field(default="pm", alias="f0_method")
    index_rate: float = Field(default=0.75, alias="index_rate")
    filter_radius: int = Field(default=3, alias="filter_radius")
    resample_sr: int = Field(default=0, alias="resample_sr")
    rms_mix_rate: float = Field(default=0.25, alias="rms_mix_rate")
    protect: float = Field(default=0.33, alias="protect")

    DESCRIPTIONS: ClassVar[Dict[str, Description]] = {
        "enabled": Description(
            en="Enable RVC voice conversion", zh="启用 RVC 声音转换"
        ),
        "model_path": Description(
            en="Path to the RVC .pth model file", zh="RVC .pth 模型文件路径"
        ),
        "index_path": Description(
            en="Path to the RVC .index file (optional)", zh="RVC .index 特征索引文件路径（可选）"
        ),
        "device": Description(
            en="Device to run inference on (e.g. cpu:0 or cuda:0)",
            zh="运行推理的设备（例如 cpu:0 或 cuda:0）",
        ),
        "f0_up_key": Description(
            en="Pitch shift in semitones (+12 for female, -12 for male)",
            zh="变调（半音，+12升高一个八度，-12降低一个八度）",
        ),
        "f0_method": Description(
            en="Pitch extraction algorithm: pm (fastest on CPU), harvest, crepe, rmvpe",
            zh="音高提取算法：pm（CPU上最快），harvest，crepe，rmvpe",
        ),
        "index_rate": Description(
            en="Search feature ratio (0-1)", zh="检索特征占比（0-1）"
        ),
        "filter_radius": Description(
            en="Median filtering radius for pitch (>=3 reduces breathiness)",
            zh="中值滤波半径（>=3 可减少呼吸杂音）",
        ),
        "resample_sr": Description(
            en="Resample target audio to this sample rate (0 for model default)",
            zh="后处理重采样目标采样率（0 表示模型默认）",
        ),
        "rms_mix_rate": Description(
            en="Volume envelope scaling (0-1, 1 means use converted volume)",
            zh="音量包络混合比（0-1，1 表示使用转换后音量）",
        ),
        "protect": Description(
            en="Protect voiceless consonants and breath sounds (0-0.5)",
            zh="保护清辅音和呼吸声（0-0.5）",
        ),
    }
