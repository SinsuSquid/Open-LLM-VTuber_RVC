# Open-LLM-VTuber, with RVC attached

## Introduction
The idea of this fork is to add RVC(Retrieval-based Voice Conversion) hook to TTS module of the original project.
This idea has not been fully verified, however.

Expected pipeline is
  - hook output audio of TTS voice (from `sherpa-onnx` for example)
  - wire it to `rvc-python` module, to generate new voice output
  - return it to websocket

We are expecting a lightweight approach to more user friendly sound output on a device which does not utilize GPU.
This message will be refined once proof-of-concept edits have fully been applied.
