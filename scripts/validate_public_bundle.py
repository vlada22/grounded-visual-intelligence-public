from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {'.ipynb', '.safetensors', '.pt', '.pth', '.bin', '.onnx', '.zip', '.tar', '.gz'}
FORBIDDEN_NAMES = {'HF_TOKEN', 'GITHUB_TOKEN'}


def main() -> None:
    violations: list[str] = []
    required = [
        ROOT / 'README.md',
        ROOT / 'THIRD_PARTY.md',
        ROOT / 'web/index.html',
        ROOT / 'web/styles.css',
        ROOT / 'web/app.js',
        ROOT / 'web/data/evidence.json',
        ROOT / 'assets/article-01/sample.mp4',
    ]
    for path in required:
        if not path.is_file():
            violations.append(f'missing required public file: {path.relative_to(ROOT)}')

    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            violations.append(f'forbidden artifact type: {path.relative_to(ROOT)}')
        if path.suffix.lower() in {'.md', '.py', '.js', '.html', '.json', '.txt', '.css'}:
            text = path.read_text(encoding='utf-8', errors='ignore')
            for name in FORBIDDEN_NAMES:
                if name in text and path.name != 'validate_public_bundle.py':
                    violations.append(f'credential/runtime token reference in {path.relative_to(ROOT)}: {name}')

    if violations:
        raise SystemExit('PUBLIC BUNDLE VALIDATION FAILED\n' + '\n'.join(f'- {v}' for v in violations))
    print('public bundle validation passed')


if __name__ == '__main__':
    main()
