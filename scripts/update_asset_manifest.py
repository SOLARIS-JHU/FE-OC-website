"""Record SHA-256 checksums after intentional, provenance-reviewed asset edits."""
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
manifest = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'assets').rglob('*')) if p.is_file() and p.name != 'manifest.json'}
(ROOT/'assets/manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(f'Recorded {len(manifest)} asset checksums.')
