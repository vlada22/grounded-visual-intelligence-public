# Grounded Visual Intelligence

Public, publication-focused companion repository for Article 01, **Ask the Video, Not Just the VLM**.

This repository is the sanitized public artifact bundle for the already-published article. The browser explorer preserves the published demo, recorded source video, frame-level evidence payload, model switching, overlays, timeline scrubbing, cited transition frames, and matched-model comparison. The only intentional demo change is that repository navigation points here rather than to the research repository.

The public boundary is around the research/runtime workspace rather than the published demo itself: model checkpoints, credentials, Colab notebooks and outputs, raw handoff archives, internal research/review material, and duplicate publication drafts remain excluded.

- [Open the interactive explorer](https://vlada22.github.io/grounded-visual-intelligence-public/)

## Published experiment

The explorer replays the validated Grounded SAM 2 and SAM 3 observations for the same ten-second controlled clip. It performs no live model inference and makes no LLM request. The checked-in bundle includes the recorded video and frame-level RLE observations used by the published explorer.

The reported deterministic answer is that the white cup is last observed in zone A at **3.75 s** and first observed in zone B at **4.00 s**, at a 4 fps sampling rate.

## Verify the published result

```bash
python scripts/validate_public_bundle.py
python scripts/verify_published_results.py
```

The verification script recomputes the published transition and cross-model agreement metrics from the checked-in observations. It does not download or execute gated models.

## Run the explorer locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/web/`.

## Repository layout

```text
web/                           published browser explorer
  data/evidence.json           frame-level published observations
assets/article-01/sample.mp4   published source clip
scripts/validate_public_bundle.py
scripts/verify_published_results.py
PUBLICATION_SOURCE.json        source-repository commit provenance
THIRD_PARTY.md                 upstream model references
```

The public bundle contains published experiment observations and deterministic verification, not third-party model weights or gated runtime material. Consult [THIRD_PARTY.md](THIRD_PARTY.md) for the upstream projects used to produce the recorded observations.
