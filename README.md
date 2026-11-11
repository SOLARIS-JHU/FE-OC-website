# Function encoder policies for parametric optimal control

Dedicated SOLARIS research page for **Zero-Shot Transferable Solution Method for Parametric Optimal Control Problems**, by Xingjian Li, Kelvin Kan, Deepanshu Verma, Krishna Kumar, Stanley Osher and Ján Drgoňa.

- Primary science: [arXiv:2509.18404v2](https://arxiv.org/abs/2509.18404v2), including the appendix.
- Research implementation: [XJ-LI/FE_OC](https://github.com/XJ-LI/FE_OC), inspected at `65337fde9b540b3ecb8f4f4b0771ad1efae71f6a`.
- Intended new public repository: `SOLARIS-JHU/FE-OC-website`.
- Intended Pages URL: `https://solaris-jhu.github.io/FE-OC-website/`.
- **Publication pending:** this package has not yet been uploaded or deployed. Repository creation and browser controls were unavailable in the authoring session. Do not represent the intended URL as a live deployment until `docs/QA.md` records verification.

The implementation uses buildless HTML/CSS/JS, the Apache-licensed TQPNet foundation, locally hosted Inter/Fraunces fonts and KaTeX, the existing SOLARIS graphical abstract, and a transparent replot of paper tables. The research-code repository is separate and unchanged.

## Preview and validate

Open this directory with a static web server, for example `python -m http.server 8000`, and visit `http://localhost:8000/`. No package installation is needed to serve the site.

Validation uses Python 3.10+ standard library and Node.js:

```sh
python scripts/validate_site.py
node scripts/validate_math.cjs
python scripts/stage_site.py
```

For a project-path preview, serve the parent directory and visit `/FE-OC-website/`. All local links are relative and work under GitHub Pages' repository prefix.

## Content and maintenance

- `scripts/build_page.py` is the editable page source; it writes the committed `index.html`. It is not a runtime dependency.
- `data/results.json` preserves the exact strings transcribed from Tables I–III.
- `scripts/generate_figures.py` reproduces the table replot and feedback SVG using only Python's standard library.
- `scripts/make_social_preview.py` reproduces the social image using Pillow and local fonts.
- After intentional asset edits, run `scripts/update_asset_manifest.py`, then validation.
- `docs/SOURCE_MAP.md` maps claims, equations, numbers and code paths to sources, and records disagreements.
- `docs/ASSET_PROVENANCE.md` records asset origins and licenses.
- `docs/QA.md` records completed and pending checks.

Do not silently merge a future paper revision or code version with these results. The 2D cost script differs from the paper's objective, the operator-loss prose differs from Algorithm 2, and source details matter for interpreting LS samples. Paper values remain the primary displayed results. The page makes no runtime, hard-safety, universal-transfer or physical-experiment claim.

## Publish to GitHub Pages

Create a new **public** `SOLARIS-JHU/FE-OC-website` repository, initialize its default branch, then commit this source. Select **GitHub Actions** as its Pages source. The included workflow validates local dependencies, asset integrity, all table transcriptions, author metadata, citation and KaTeX rendering, stages only the public files, and deploys with `actions/deploy-pages`.

The workflow uses minimal permissions: read-only contents in build, `pages: write` and `id-token: write` only in deployment. Pull requests validate without deployment. Internal maintenance files are not staged.

Finish by confirming the deployment job succeeds and by visiting the actual Pages URL. Check mobile/desktop, equation scrolling, image loading, keyboard focus, citation copying, outgoing links and browser errors. A commit or successful build alone does not establish publication.

## Attribution

See `LICENSE`, `NOTICE`, and `docs/ASSET_PROVENANCE.md`. The Apache license for website code does not replace the paper's CC BY 4.0 attribution, bundled third-party licenses, or institutional-mark rights.
