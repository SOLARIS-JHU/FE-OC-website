"""Stage the public site using an explicit allowlist."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'_site'
DEST.mkdir(exist_ok=True)
for name in ['index.html','template.css','style.css','site.js','citation.bib','.nojekyll','LICENSE','NOTICE']:
    shutil.copy2(ROOT/name, DEST/name)
shutil.copytree(ROOT/'assets', DEST/'assets', dirs_exist_ok=True)
print('Staged public site in _site/')
