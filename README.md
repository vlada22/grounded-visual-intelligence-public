# Grounded Visual Intelligence

Public, publication-focused companion repository for Article 01, **Ask the Video, Not Just the VLM**.

This repository is the sanitized public artifact bundle for the already-published article. It contains a credential-free static evidence explorer and compact reviewed measurements supporting the published cup-crossing result. It intentionally excludes model checkpoints, tokens, Colab notebooks and outputs, raw handoff archives, internal research/review material, and duplicate publication drafts.

- [Open the interactive evidence explorer](https://vlada22.github.io/grounded-visual-intelligence-public/)

## Published experiment

The explorer summarizes the validated Grounded SAM 2 and SAM 3 observations for the same ten-second controlled clip. It performs no model inference and makes no LLM request. The checked-in public payload contains only aggregate measurements and the exact cited transition frames/timestamps needed to inspect the published claim.

The reported deterministic answer is that the white cup is last observed in zone A at **3.75 s** and first observed in zone B at **4.00 s**, at a 4 fps sampling rate.

## Run the explorer locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000/demo/`.

## Repository layout

```text
demo/                         static aggregate-evidence explorer
scripts/validate_public_bundle.py
THIRD_PARTY.md                upstream model references
```

The public bundle contains derived experiment evidence, not third-party model weights or gated runtime material. Consult [THIRD_PARTY.md](THIRD_PARTY.md) for the upstream projects used to produce the recorded observations.
