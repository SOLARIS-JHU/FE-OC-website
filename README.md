# Function encoder policies for parametric optimal control

Dedicated SOLARIS research page for **Zero-Shot Transferable Solution Method for Parametric Optimal Control Problems**, by Xingjian Li, Kelvin Kan, Deepanshu Verma, Krishna Kumar, Stanley Osher and Ján Drgoňa.

- Primary science: [arXiv:2509.18404v2](https://arxiv.org/abs/2509.18404v2), including the appendix.
- Research implementation: [XJ-LI/FE_OC](https://github.com/XJ-LI/FE_OC), inspected at `65337fde9b540b3ecb8f4f4b0771ad1efae71f6a`.
- Public repository: [SOLARIS-JHU/FE-OC-website](https://github.com/SOLARIS-JHU/FE-OC-website).
- Live website: [solaris-jhu.github.io/FE-OC-website](https://solaris-jhu.github.io/FE-OC-website/).
- **Published and verified on 11 November 2026:** [successful deployment and live browser checks](https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43077280785). Desktop/mobile screenshots were visually reviewed. See `docs/QA.md` for evidence and source limitations.

The implementation uses buildless HTML/CSS/JS, the Apache-licensed TQPNet foundation, locally hosted Inter/Fraunces fonts and KaTeX, an animated method overview, LaTeX-rendered feedback equations, and a replot of paper tables. The primary Paper button links to the IEEE conference publication. The research-code repository is separate and unchanged.

## Preview and validate

Open this directory with a static web server, for example `python -m http.server 8000`, and visit `http://localhost:8000/`. No package installation is needed to serve the site.

Validation uses Python 3.10+ standard library and Node.js:

```sh
python scripts/validate_site.py
node scripts/validate_math.cjs
python scripts/stage_site.py
```

For a project-path preview, serve the parent directory and visit `/FE-OC-website/`. All local links are relative and work under GitHub Pages' repository prefix.

GitHub Actions additionally installs Playwright 1.56.1 on Ubuntu 24.04 for CI-only Chromium checks. It tests the staged site before deployment and the actual published URL afterward at 1440px, 390px and 320px, plus dark/reduced-motion preferences. Each stage saves JSON reports and full-page screenshots as workflow artifacts for 14 days. Compact public-page previews are also emitted in live-check logs for inspection when artifact downloads are unavailable. The site itself has no Playwright or npm runtime dependency.

## Content and maintenance

- `scripts/build_page.py` is the editable page source; it writes the committed `index.html`. It is not a runtime dependency.
- `data/results.json` preserves the exact strings transcribed from Tables I–III.
- `scripts/generate_figures.py` reproduces the table replot and feedback SVG using only Python's standard library.
- `scripts/generate_abstract.py` reproduces the animated overview and its static fallback. Then run `scripts/build_page.py` to embed the overview and generate its full-size page.
- `node scripts/build_feedback.cjs` generates the seven feedback equations through bundled KaTeX and writes the inline fragment and full-size page. Run it before `scripts/build_page.py` when changing this diagram. The older feedback SVG is retained as a legacy asset.
- The overview's pause/play control respects reduced-motion preferences. Without JavaScript, the embedded overview remains paused with every stage visible.
- `scripts/make_social_preview.py` reproduces the social image using Pillow and local fonts.
- After intentional asset edits, run `scripts/update_asset_manifest.py`, then validation.
- `docs/SOURCE_MAP.md` maps claims, equations, numbers and code paths to sources, and records disagreements.
- `docs/ASSET_PROVENANCE.md` records asset origins and licenses.
- `docs/QA.md` records completed and pending checks.

Do not silently merge a future paper revision or code version with these results. The 2D cost script differs from the paper's objective, the operator-loss prose differs from Algorithm 2, and source details matter for interpreting LS samples. Paper values remain the primary displayed results. The page makes no runtime, hard-safety, universal-transfer or physical-experiment claim.

## Publish to GitHub Pages

Commit changes to `main` in this repository. Pages is configured to use **GitHub Actions**. The included workflow validates local dependencies, asset integrity, all table transcriptions, author metadata, citation and KaTeX rendering, stages only the public files, checks the rendered page, and deploys with `actions/deploy-pages`.

The workflow uses minimal permissions: read-only contents in build, `pages: write` and `id-token: write` only in deployment. Pull requests validate without deployment. Internal maintenance files are not staged.

Finish by confirming the deployment job succeeds and by visiting the actual Pages URL. Check mobile/desktop, equation scrolling, image loading, keyboard focus, citation copying, outgoing links and browser errors. A commit or successful build alone does not establish publication.

## Attribution

See `LICENSE`, `NOTICE`, and `docs/ASSET_PROVENANCE.md`. The Apache license for website code does not replace the paper's CC BY 4.0 attribution, bundled third-party licenses, or institutional-mark rights.
