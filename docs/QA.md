# Verification record

Date: 2026-11-11. **Status: implemented and locally validated; not published.**

## Completed

- Read arXiv v2 Sections I–VI, both algorithms, Tables I–III, figure captions, and the complete appendix.
- Verified six authors in order and paper affiliations; linked official/author profiles.
- Inspected all 15 released Python files and code README at commit `65337fde9b540b3ecb8f4f4b0771ad1efae71f6a`.
- Recorded source disagreements (2D cost norm, percentage statement, operator-loss description, bicycle normalization, README commands) in `SOURCE_MAP.md`; material 2D and operator distinctions are also public.
- All three HTML tables match the exact decimal strings transcribed from the paper. Chart uses Decimal arithmetic on those values and explicitly labels its ratio-of-means calculation.
- Kept dynamics fixed within each family, distinguished offline training from deployment, distinguished LS new-task data from data-free operator inference, and preserved state/time feedback.
- Inspected rasterized SVG abstract, generated chart, feedback diagram, and social preview; no overlapping labels or connectors were observed in these image renders.
- Original SOLARIS graphical abstract matches its Git blob SHA exactly; all 40 assets have SHA-256 checksums.
- Static validation passes: 6 images with alt text and dimensions, 49 page references, local HTML/CSS dependencies, anchors, single H1, language, author metadata, BibTeX consistency, all three tables, SVG integrity, no placeholders.
- All 23 LaTeX expressions render successfully with the locally shipped KaTeX 0.16.22 in strict validation.
- Staging succeeds and static dependency checks establish relative asset paths compatible with `/FE-OC-website/`.
- Responsive CSS, focus styles, skip link, keyboard-focusable scroll regions, semantic tables, native details, live citation-copy status, and reduced-motion handling are present. Figures are intentionally static.
- GitHub Actions workflow includes content validation, KaTeX validation, allowlist staging and Pages deployment with scoped permissions.
- No existing research or website repository was modified.

## Pending / external limitations

- The GitHub connector permits file operations but does not expose repository creation or Pages settings. `SOLARIS-JHU/FE-OC-website` returned 404 when checked. Browser controls and an authenticated local GitHub CLI were unavailable; local executor network access could not resolve external hosts. The new repository has **not** been created.
- Consequently no remote workflow run, deployment job, or published-site verification has occurred. The intended Pages URL must not be advertised as live.
- Browser tooling is unavailable. Full desktop/mobile layout, clipboard interaction, keyboard navigation in a rendered browser, and browser-console checks remain pending. Image inspection and static checks are not substitutes for those checks.
- Local HTTP verification was attempted, but the executor denied the loopback socket connection with Windows error 10013. The server was shut down and temporary staging files were cleaned up. `scripts/check_local_http.py` is provided for a later environment with local socket access; no HTTP success is claimed.
- IEEE returns robot verification, and the official conference-program domain blocks retrieval. ACC acceptance is confirmed by author sources; DBLP supplies conference bibliographic details. ArXiv v2 citation is verified; conference DOI is omitted.
- ArXiv full text was readable, but original figure-file bytes could not be fetched into this executor. The page uses the official SOLARIS vector abstract and clearly identified table replot; original experimental trajectories remain accessible through the paper link.
- Models were not retrained or reevaluated; external bicycle dataset downloads were not checked. No confidence intervals, timing benchmarks, or physical results are invented.

## Complete after access is restored

1. Create public `SOLARIS-JHU/FE-OC-website`, initialized with default branch `main`.
2. Upload this package using the connected GitHub API; enable Pages with GitHub Actions.
3. Verify both build and deployment jobs succeed; record their URL and commit SHA here.
4. Visit the actual Pages URL; test desktop, 390px and 320px layouts, resource links, equation/figure scrolling, image fidelity, focus order, native disclosures, citation copying and console errors.
5. Update README and this record to the verified deployment status only after the above succeeds.
