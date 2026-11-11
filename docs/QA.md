# Verification record

Date: 2026-11-11. **Status: original SOLARIS artwork and shared logo styling published; staged/live browser checks and desktop/mobile visual review completed.**

- Repository: https://github.com/SOLARIS-JHU/FE-OC-website
- Live site: https://solaris-jhu.github.io/FE-OC-website/
- First fully successful deployment and live verification: https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43075206058
- Previous successful deployment and live verification: https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43077280785
- Previously verified content commit: `cc9cebc641c7cd8d68cd0a94e3f4e97ebf4b6a30`.
- Previous presentation's successful deployment and live verification: https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43082617288
- Previous presentation's verified content commit: `c29888f8c25bea3384d5b2f8451ba8b1265dbe5e`.
- That workflow and its desktop/mobile review passed; it predates the restoration described below.

## Original-artwork restoration

- The main and full-size overview pages now embed the exact SOLARIS papers-page SVG, Git blob `a5d6c72b02d5b6f9756fc7ec97e15efe62d893fb`, without changing its artwork.
- The original site's `v9-policyfe` animation is reused: three existing trajectories and endpoint markers progress on a nine-second cycle. The custom replacement artwork and its generator were removed.
- UCLA inherits the same grayscale/opacity, hover and keyboard-focus rules as the other institutional logos; the official SVG bytes remain unchanged.
- [Run 43084941556](https://github.com/SOLARIS-JHU/FE-OC-website/actions/runs/43084941556) completed successfully for content commit `de1d61cbf00581fa5552c2c5d4764228dc8aacb5`; build, Pages deployment and actual live-site checks passed.
- Staged and live Chromium checks passed at 1440px, 390px, 320px, and 1440px dark mode with reduced motion. Live HTML matched the checked-out source.
- Browser checks verified the exact original SVG hash; actual trajectory path/tip changes during playback; frozen geometry on keyboard pause; changes after resume; and exact original complete geometry under reduced motion. UCLA's filter matched every other institutional logo at rest and changed to full color on hover and keyboard focus.
- Desktop and native-width mobile screenshots were visually reviewed. The original artwork remains legible within its intended scroll container; UCLA is muted gray at rest. The actual published desktop overview was also inspected. No unintended overlap or page-wide overflow was observed.
- The existing IEEE publication link, seven LaTeX feedback equations, navigation, local resources, citations, math rendering and other browser checks also passed. Screenshot animation phases may differ; byte-identical preview images are not required for this revision.

## Scientific audit and completed local checks

- Read arXiv v2 Sections I–VI, both algorithms, Tables I–III, figure captions, and the complete appendix.
- Verified six authors in order and paper affiliations; linked official/author profiles.
- Inspected all 15 released Python files and code README at commit `65337fde9b540b3ecb8f4f4b0771ad1efae71f6a`.
- Recorded source disagreements (2D cost norm, percentage statement, operator-loss description, bicycle normalization, README commands) in `SOURCE_MAP.md`; material 2D and operator distinctions are also public.
- All three HTML tables match the exact decimal strings transcribed from the paper. Chart uses Decimal arithmetic on those values and explicitly labels its ratio-of-means calculation.
- Kept dynamics fixed within each family, distinguished offline training from deployment, distinguished LS new-task data from data-free operator inference, and preserved state/time feedback.
- The embedded original SOLARIS graphical abstract matches its recorded Git blob SHA. The static asset remains complete and readable without JavaScript.
- All 44 assets have SHA-256 checksums in `assets/manifest.json`.
- Static validation passes: 5 images with alt text and dimensions, 215 page references (including SVG glyph references), local HTML/CSS dependencies, anchors, single H1, language, author metadata, BibTeX consistency, all three tables, SVG integrity, no placeholders.
- All 23 page LaTeX expressions render successfully with the locally shipped KaTeX 0.16.22 in strict validation. Seven additional feedback-diagram equations are pre-rendered as HTML and MathML by `scripts/build_feedback.cjs`.
- The feedback diagram now uses HTML/MathML equations over vector connectors in a 1000px scrollable layout, with a full-size link. The former 800px SVG presentation is no longer the embedded feedback diagram.
- The source-site animation changes only the three illustrative trajectories and their endpoint markers; bases, coefficients and diagram connections remain as in the original artwork. Reduced motion restores the original complete paths. The no-JavaScript fallback was inspected in source, but was not separately browser-tested with scripting disabled.
- Added the official UCLA campus-logo artwork from UCLA Design System 2.7.0, preserving its colors and proportions. Its provenance and trademark treatment are recorded in `ASSET_PROVENANCE.md` and `NOTICE`.
- The Paper button links to https://ieeexplore.ieee.org/document/11615530, confirmed through DBLP's electronic-edition link. The separate arXiv link and citation retain the revision used for the scientific summary.
- Method labels and captions explain the algorithm without diagram-production commentary. Technical acronyms are defined, including American Control Conference (ACC), University of California, Los Angeles (UCLA), Institute of Electrical and Electronics Engineers (IEEE), function encoder (FE), least squares (LS), two-dimensional (2D), graphics processing unit (GPU), and adaptive moment estimation (Adam).
- Preserved qualifications for fixed dynamics and bases, LS data requirements, numerical references, simulated experiments, soft obstacle penalties, rounded means, and finite-sample theory.
- Staging succeeds and static dependency checks establish relative asset paths compatible with `/FE-OC-website/`.
- Responsive CSS, focus styles, skip link, keyboard-focusable scroll regions, semantic tables, native details, live citation-copy status, and reduced-motion handling are present.
- GitHub Actions workflow includes content validation, KaTeX validation, allowlist staging, browser checks, Pages deployment with scoped permissions, and live verification.
- No research-code repository or other SOLARIS website repository was modified.

## Previous presentation's deployment and visual verification

- Run `43082617288` completed successfully for content commit `c29888f8c25bea3384d5b2f8451ba8b1265dbe5e`. Both the build job's staged browser checks and the deployment job's actual live-site checks passed.
- All 74 files at that content commit matched the prepared local source by raw-byte Git blob hashes, with zero differences. Subsequent verification-record updates affect documentation only.
- Chromium passed 1440px desktop, 390px mobile, 320px mobile, and 1440px dark-mode/reduced-motion configurations. No failed checks were reported.
- The live preflight confirmed that the published HTML hash matched the checked-out source. Staged/live desktop and 390px mobile JPEG previews were byte-identical.
- Browser checks covered the animation's pause/resume behavior and reduced-motion presentation, image decoding, local fonts, all page equations and the seven pre-rendered feedback equations, scrollable content, keyboard navigation, disclosures, citation copying, local resources/anchors, page-wide overflow, console errors and failed resources.
- Visually reviewed the current desktop header and feedback diagram: the UCLA logo renders correctly, animated operation markers are visible, and the feedback mathematics is clean and legible.
- Visually reviewed the current 390px mobile screenshots at native resolution, including the header buttons, UCLA logo, animated overview and feedback diagram. KaTeX rendered correctly; no unintended overlap was found, and wide figures remain within their intentional horizontal scroll regions.
- The Paper button targets the verified IEEE document URL. IEEE's robot verification still limits inspection of the destination's content, as recorded below.

## Previous deployment verification

The following historical results apply to earlier published revisions. Verification of the latest overview, feedback diagram, publication link and logo changes is recorded above.

- GitHub Actions build and Pages deployment succeeded. The first run exposed an unsupported Ubuntu 26.04/Playwright combination; pinning the runner to Ubuntu 24.04 resolved it.
- Chromium passed all checks on both the staged site under `/FE-OC-website/` and the actual published HTTPS URL. The live test first confirmed fetched HTML matched the checked-out source.
- Browser configurations: 1440px desktop, 390px mobile, 320px mobile, and 1440px dark mode with reduced motion.
- Verified image decoding, local Inter/Fraunces/KaTeX font loading, rendered equations, no page-wide overflow (including expanded disclosures), scrollable wide content, skip/section links, visible keyboard focus, native disclosures, keyboard table scrolling, exact clipboard BibTeX, local resources/anchors, reduced motion and absence of console errors or failed page resources.
- Full-page initial/expanded screenshots and detailed JSON reports are attached to the workflow as `browser-qa-local` and `browser-qa-live` artifacts. Their retention is 14 days; compact public previews are also available in subsequent live-check logs.
- Author profile, arXiv and acceptance-announcement links were checked through official/author pages. Kelvin Kan's older `home.html` resolves through a move notice to `index.html`; the link is functional.
- Visually inspected full-page desktop and 390px mobile screenshots of the earlier revision, including enlarged sections. No unintended overlap, clipping, missing graphics or unreadable body text was found. These screenshots predate the current animated overview and HTML/MathML feedback diagram.
- The earlier published page was opened and exercised in Chromium on the runner; source-matching preflight and all four live configurations passed. This does not establish successful deployment or visual correctness of the latest revision.
- A repeat run exposed an intermittent keyboard test race during smooth scrolling. The test now waits for the target heading to be visible and for scroll geometry to settle before subsequent input, while preserving hash, focus and clipping assertions. Final staged and live checks passed with this correction.

## Source and verification limitations

- The local executor cannot reach external hosts or a loopback preview. Rendered browser and live HTTP checks ran on GitHub Actions using `scripts/browser_qa.cjs`, including the latest successful workflow. No local HTTP success is claimed.
- Visual review and automated layout checks do not establish complete accessibility conformance; browsers other than Chromium have not been tested. Wide figures, equations, tables and BibTeX intentionally use horizontal scrolling on narrow screens.
- IEEE returns robot verification, and the official conference-program domain blocks retrieval. ACC acceptance is confirmed by author sources; DBLP supplies conference bibliographic details and the IEEE link. ArXiv v2 citation is verified; conference DOI is omitted.
- ArXiv full text was readable, but original experimental figure-file bytes could not be fetched into this executor. The page uses the original SOLARIS vector abstract with its source-site animation and a clearly identified table replot. Original experimental trajectories remain accessible through the paper resources.
- Models were not retrained or reevaluated; external bicycle dataset downloads were not checked. No confidence intervals, timing benchmarks, or physical results are invented.

## Maintenance

Keep the paper/code pins, source map and asset provenance synchronized with intentional scientific edits. Changes to `main` rerun validation, browser checks, Pages deployment and live verification. Record material new findings here; a successful commit alone does not establish a successful deployment.
