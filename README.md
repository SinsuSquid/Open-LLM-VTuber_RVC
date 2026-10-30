# Open-LLM-VTuber, with RVC attached

> *"I've come from beyond the boundaries of science!"* 🩵  
> *(科学の限界を越えて、私は来たんだよ！)*

## Introduction
This fork integrates an RVC (Retrieval-based Voice Conversion) post-processing hook directly into the TTS audio synthesis pipeline of Open-LLM-VTuber.

### Verified Pipeline
- **TTS Generation**: Base voice synthesized via lightweight TTS (e.g., `sherpa-onnx` on CPU).
- **RVC Post-Processing Hook**: Audio is transparently intercepted and converted into the target character voice using `rvc-python`.
- **WebSocket Streaming**: Transformed audio and computed lip-sync volumes are encoded and streamed to the Live2D frontend over WebSocket.

### Configuration
Enable and configure RVC under `character_config.rvc_config` in `conf.yaml`:
```yaml
rvc_config:
  enabled: true
  model_path: 'models/rvc/infamous_miku_v2/infamous_miku_v2.pth'
  index_path: 'models/rvc/infamous_miku_v2/added_IVF2983_Flat_nprobe_1_infamous_miku_v2_v2.index'
  device: 'cpu:0' # Runs on CPU or CUDA
  f0_up_key: 5    # Pitch shift (+5 semitones for certified Moe!)
  f0_method: 'pm' # 'pm' is optimized for fast CPU inference
  index_rate: 0.75
  filter_radius: 3
  resample_sr: 0
  rms_mix_rate: 0.25
  protect: 0.33
```
