# Open-LLM-VTuber, with RVC attached

> *"I've come from beyond the boundaries of science!"* 🩵  
> *(科学の限界を越えて、私は来たんだよ！)*

### 🩵 Dedicated to Hatsune Miku (初音ミク)
This fork is wholeheartedly dedicated to the world's favorite virtual diva, **Hatsune Miku**. By combining real-time LLM conversational intelligence, official Live2D Cubism expression acting, and an RVC voice conversion pipeline tuned for maximum *moe*, this project brings the eternal cyber idol to life on any desktop.

## Demo

[![Hatsune Miku Open-LLM-VTuber RVC Demo](https://img.youtube.com/vi/uDnJTcILzDU/maxresdefault.jpg)](https://youtu.be/uDnJTcILzDU)

*(Note: Noise is due to recorder)*

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

## Installation Guide (Hatsune Miku Setup)

Follow these steps to set up the full conversational pipeline with Hatsune Miku:

### 1. Environment & Dependencies
Clone the repository and install dependencies in a Python virtual environment:
```bash
git clone https://github.com/SinsuSquid/Open-LLM-VTuber_RVC.git
cd Open-LLM-VTuber_RVC

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```
*(Note: `rvc-python` requires `setuptools<70`, which is pinned in `requirements.txt` and `pyproject.toml`)*.

### 2. Download Model Assets

#### A. Live2D Model (`miku_pro`)
1. Download the Hatsune Miku PRO sample model from [Live2D Sample Data](https://www.live2d.com/en/learn/sample/hatsune-miku/).
2. Extract the archive into `live2d-models/miku_pro/` such that the runtime files are located at:
   ```
   live2d-models/miku_pro/
   └── runtime/
       ├── miku_sample_t04.model3.json
       ├── miku_sample_t04.moc3
       ├── miku_sample_t04.physics3.json
       ├── miku_sample_t04.cdi3.json
       ├── miku_sample_t04.2048/
       └── motion/
   ```
   *(Pre-configured under `"miku_pro"` in [`model_dict.json`](model_dict.json))*.

#### B. Base TTS Model (`sherpa-onnx` GLaDOS)
1. Download `vits-piper-en_US-glados.tar.bz2` from the [sherpa-onnx TTS models release](https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models).
2. Extract directly into the project root:
   ```bash
   tar -xvf vits-piper-en_US-glados.tar.bz2
   ```
   *(This extracts the folder `vits-piper-en_US-glados/` containing `en_US-glados.onnx`, `tokens.txt`, and `espeak-ng-data`)*.

#### C. RVC Voice Model (`infamous_miku_v2`)
1. Download `infamous_miku_v2.pth` and `added_IVF2983_Flat_nprobe_1_infamous_miku_v2_v2.index` from [HuggingFace - javinfamous/infamous_miku_v2](https://huggingface.co/javinfamous/infamous_miku_v2).
2. Place them into `models/rvc/infamous_miku_v2/`:
   ```
   models/rvc/infamous_miku_v2/
   ├── infamous_miku_v2.pth
   └── added_IVF2983_Flat_nprobe_1_infamous_miku_v2_v2.index
   ```

### 3. Configuration
Ensure `conf.yaml` has Miku and RVC configured:
```yaml
character_config:
  live2d_model_name: 'miku_pro'
  character_name: 'miku_pro'
  rvc_config:
    enabled: true
    model_path: 'models/rvc/infamous_miku_v2/infamous_miku_v2.pth'
    index_path: 'models/rvc/infamous_miku_v2/added_IVF2983_Flat_nprobe_1_infamous_miku_v2_v2.index'
    device: 'cpu:0' # Runs on CPU or CUDA
    f0_up_key: 5    # Pitch shift (+5 semitones for certified Moe!)
    f0_method: 'pm' # 'pm' is optimized for fast CPU inference

tts_config:
  tts_model: 'sherpa_onnx_tts'
```

### 4. Run & Interact
Start the server:
```bash
uv run run_server.py
# or
.venv/bin/python run_server.py
```
Open your browser at `http://localhost:12393`. Click or tap Miku on the canvas to trigger her reactive motions and blushing! 🩵

