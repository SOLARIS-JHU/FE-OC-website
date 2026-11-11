# Verification record

Date: 2026-11-11. **Status: published; staged/live automated browser checks and desktop/mobile visual review completed.**

- Repository: https://github.com/SOLARIS-JHU/FE-OC-website
- Live site: https://solaris-jhu.github.io/FE-OC-website/
- First fully successful deployment and live verification: https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43075206058
- Final successful deployment and live verification: https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43077280785
- Verified published-content commit: `cc9cebc641c7cd8d68cd0a94e3f4e97ebf4b6a30`.
- All 66 committed files were compared with the local source using Git blob hashes; no differences were found.

## Completed

- Read arXiv v2 Sections I–VI, both algorithms, Tables I–III, figure captions, and the complete appendix.
- Verified six authors in order and paper affiliations; linked official/author profiles.
- Inspected all 15 released Python files and code README at commit `65337fde9b540b3ecb8f4f4b0771ad1efae71f6a`.
- Recorded source disagreements (2D cost norm, percentage statement, operator-loss description, bicycle normalization, README commands) in `SOURCE_MAP.md`; material 2D and operator distinctions are also public.
- All three HTML tables match the exact decimal strings transcribed from the paper. Chart uses Decimal arithmetic on those values and explicitly labels its ratio-of-means calculation.
- Kept dynamics fixed within each family, distinguished offline training from deployment, distinguished LS new-task data from data-free operator inference, and preserved state/time feedback.
- Inspected rasterized SVG abstract, generated chart, feedback diagram, and social preview; no overlapping labels or connectors were observed in these image renders.
- Original SOLARIS graphical abstract matches its Git blob SHA exactly; all 40 assets have SHA-256 checksums.
- Static validation passes: 6 images with alt text and dimensions, 50 page references, local HTML/CSS dependencies, anchors, single H1, language, author metadata, BibTeX consistency, all three tables, SVG integrity, no placeholders.
- All 23 LaTeX expressions render successfully with the locally shipped KaTeX 0.16.22 in strict validation.
- Staging succeeds and static dependency checks establish relative asset paths compatible with `/FE-OC-website/`.
- Responsive CSS, focus styles, skip link, keyboard-focusable scroll regions, semantic tables, native details, live citation-copy status, and reduced-motion handling are present. Figures are intentionally static.
- GitHub Actions workflow includes content validation, KaTeX validation, allowlist staging and Pages deployment with scoped permissions.
- No existing research or website repository was modified.
- GitHub Actions build and Pages deployment succeeded. The first run exposed an unsupported Ubuntu 26.04/Playwright combination; pinning the runner to Ubuntu 24.04 resolved it.
- Chromium passed all checks on both the staged site under `/FE-OC-website/` and the actual published HTTPS URL. The live test first confirmed fetched HTML matched the checked-out source.
- Browser configurations: 1440px desktop, 390px mobile, 320px mobile, and 1440px dark mode with reduced motion.
- Verified image decoding, local Inter/Fraunces/KaTeX font loading, rendered equations, no page-wide overflow (including expanded disclosures), scrollable wide content, skip/section links, visible keyboard focus, native disclosures, keyboard table scrolling, exact clipboard BibTeX, local resources/anchors, reduced motion and absence of console errors or failed page resources.
- Full-page initial/expanded screenshots and detailed JSON reports are attached to the workflow as `browser-qa-local` and `browser-qa-live` artifacts. Their retention is 14 days; compact public previews are also available in subsequent live-check logs.
- Author profile, arXiv and acceptance-announcement links were checked through official/author pages. Kelvin Kan's older `home.html` resolves through a move notice to `index.html`; the link is functional.
- Visually inspected full-page desktop and 390px mobile screenshots, including enlarged sections. No unintended overlap, clipping, missing graphics or unreadable body text was found. The feedback diagram's initially small mobile labels were improved with an 800px scrollable view and a full-size link; the revised mobile screenshot was inspected.
- Final staged and live desktop/mobile JPEG previews were byte-identical. The actual published page was opened and exercised in Chromium on the runner; source-matching preflight and all four live configurations passed.
- A repeat run exposed an intermittent keyboard test race during smooth scrolling. The test now waits for the target heading to be visible and for scroll geometry to settle before subsequent input, while preserving hash, focus and clipping assertions. Final staged and live checks passed with this correction.

## Source and verification limitations

- The local executor cannot reach external hosts or a loopback preview. Rendered browser and live HTTP checks therefore ran on GitHub Actions, using `scripts/browser_qa.cjs`. No local HTTP success is claimed.
- Visual review and automated layout checks do not establish complete accessibility conformance; browsers other than Chromium have not been tested. Wide figures, equations, tables and BibTeX intentionally use horizontal scrolling on narrow screens.
- IEEE returns robot verification, and the official conference-program domain blocks retrieval. ACC acceptance is confirmed by author sources; DBLP supplies conference bibliographic details. ArXiv v2 citation is verified; conference DOI is omitted.
- ArXiv full text was readable, but original figure-file bytes could not be fetched into this executor. The page uses the official SOLARIS vector abstract and clearly identified table replot; original experimental trajectories remain accessible through the paper link.
- Models were not retrained or reevaluated; external bicycle dataset downloads were not checked. No confidence intervals, timing benchmarks, or physical results are invented.

## Maintenance

Keep the paper/code pins, source map and asset provenance synchronized with intentional scientific edits. Changes to `main` rerun validation, browser checks, Pages deployment and live verification. Record material new findings here; a successful commit alone does not establish a successful deployment.
