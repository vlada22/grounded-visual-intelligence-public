# Grounded Visual Intelligence

Public, publication-focused companion repository for Article 01, **Ask the Video, Not Just the VLM**.

This bundle contains the canonical article, the static evidence explorer, the publishable source clip, and the recorded evidence needed to inspect the reported cup-crossing result. It intentionally excludes model checkpoints, tokens, Colab notebooks and outputs, raw handoff archives, internal research/review material, and duplicate publication drafts.

- [Read the article](ARTICLE.md)
- [Open the interactive evidence explorer](https://vlada22.github.io/grounded-visual-intelligence-public/)

## Published experiment

The explorer replays the validated Grounded SAM 2 and SAM 3 observations for the same ten-second controlled clip. It performs no model inference and makes no LLM request. The browser renders the recorded masks, boxes, zones, transition evidence, and aggregate run provenance from the checked-in public evidence payload.

The reported deterministic answer is that the white cup is last observed in zone A at **3.75 s** and first observed in zone B at **4.00 s**, at a 4 fps sampling rate.

## Run the explorer locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/demo/`.

## Repository layout

```text
ARTICLE.md                    canonical Article 01 text
assets/                       publication media
demo/                         static evidence explorer
scripts/validate_public_bundle.py
THIRD_PARTY.md                upstream model references and license notes
```

The public bundle contains derived experiment evidence, not third-party model weights. See [THIRD_PARTY.md](THIRD_PARTY.md) for the upstream projects used to produce the recorded observations.
