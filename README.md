# Open-LLM-VTuber, with RVC attached

> *"I've come from beyond the boundaries of science!"* 🩵  
> *(科学の限界を越えて、私は来たんだよ！)*

### 🩵 Dedicated to Hatsune Miku (初音ミク)
This fork is wholeheartedly dedicated to the world's favorite virtual diva, **Hatsune Miku**. By combining real-time LLM conversational intelligence, official Live2D Cubism expression acting, and an RVC voice conversion pipeline tuned for maximum *moe*, this project brings the eternal cyber idol to life on any desktop.

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

### Models & Assets

#### Live2D Model
- **Character**: Hatsune Miku (初音ミク) PRO Sample Model (`miku_pro`)
- **Source**: [Live2D Sample Data - Hatsune Miku](https://www.live2d.com/en/learn/sample/hatsune-miku/)
- **Illustration**: Crypton Future Media, INC. (クリプトン・フューチャー・メディア株式会社)
- **Modeling**: Live2D Inc.
- **Directory**: `live2d-models/miku_pro/` (configured in [`model_dict.json`](model_dict.json) and [`conf.yaml`](conf.yaml))

#### Base TTS Model (sherpa-onnx)
- **Model**: `vits-piper-en_US-glados` (GLaDOS VITS ONNX model)
- **Source**: [k2-fsa/sherpa-onnx TTS Models Release](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models)
- **Engine**: [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- **Directory**: `vits-piper-en_US-glados/`

#### RVC Voice Model
- **Model**: `infamous_miku_v2` (Weights: `infamous_miku_v2.pth`, Index: `added_IVF2983_Flat_nprobe_1_infamous_miku_v2_v2.index`)
- **Source**: [HuggingFace - javinfamous/infamous_miku_v2](https://huggingface.co/javinfamous/infamous_miku_v2)
- **Creator**: [javinfamous](https://huggingface.co/javinfamous)
- **Directory**: `models/rvc/infamous_miku_v2/`
