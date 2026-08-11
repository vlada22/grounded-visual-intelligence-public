# Grounded Visual Intelligence

Public, publication-focused companion repository for Article 01, **Ask the Video, Not Just the VLM**.

This repository is the sanitized public artifact bundle for the already-published article. The browser demo is a mirror of the original published evidence explorer, including the recorded source video, frame-level evidence payload, model switching, mask/box/zone overlays, timeline scrubbing, cited transition frames, and matched-model comparison. Repository links inside the mirrored demo point to this public repository.

The public boundary is around the research/runtime workspace rather than the published demo itself: model checkpoints, credentials, Colab notebooks and outputs, raw handoff archives, internal research/review material, and duplicate publication drafts remain excluded.

- [Open the interactive evidence explorer](https://vlada22.github.io/grounded-visual-intelligence-public/)

## Published experiment

The explorer replays the validated Grounded SAM 2 and SAM 3 observations for the same ten-second controlled clip. It performs no live model inference and makes no LLM request. The checked-in demo includes the same recorded video and frame-level RLE evidence used by the original published explorer.

The reported deterministic answer is that the white cup is last observed in zone A at **3.75 s** and first observed in zone B at **4.00 s**, at a 4 fps sampling rate.

## Run the explorer locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/demo/`.

## Repository layout

```text
demo/                         mirrored original published explorer
  assets/sample.mp4           original published source clip
  data/evidence.json          original frame-level evidence payload
  data/results.json           compact publication summary used by validation
scripts/validate_public_bundle.py
THIRD_PARTY.md                upstream model references
```

The public bundle contains published experiment evidence, not third-party model weights or gated runtime material. Consult [THIRD_PARTY.md](THIRD_PARTY.md) for the upstream projects used to produce the recorded observations.
