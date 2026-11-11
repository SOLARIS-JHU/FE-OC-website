# Scientific source map

Audit date: 2026-11-11. This record is maintenance material; it is not staged for the public page.

## Source precedence and versions

1. Primary scientific source: [arXiv:2509.18404v2](https://arxiv.org/abs/2509.18404v2), revised 11 March 2026, 11 pages, 6 figures, 3 tables, including the complete appendix. [HTML](https://arxiv.org/html/2509.18404v2), [PDF](https://arxiv.org/pdf/2509.18404v2). First submission: 22 September 2025. The user supplied the SOLARIS papers index, whose entry links this arXiv identifier without a fixed revision; the latest revision was therefore selected and pinned. License recorded by arXiv: CC BY 4.0.
2. Implementation: [XJ-LI/FE_OC at 65337fde9b540b3ecb8f4f4b0771ad1efae71f6a](https://github.com/XJ-LI/FE_OC/tree/65337fde9b540b3ecb8f4f4b0771ad1efae71f6a), latest available commit, 7 February 2026. No paper-specific release tag was established. Treat code details as version-specific, not as independent reproduction of the paper tables. All 15 Python files were downloaded for inspection; no model training or benchmark evaluation was run.
3. Publication: [author announcement](https://drgona.github.io/news/) dated 15 February 2026 confirms ACC 2026 acceptance. [DBLP bibliographic record](https://dblp.org/rec/conf/amcc/LiKVKOD26.html?view=bibtex) identifies ACC 2026, New Orleans, May 26–29, pages 2003–2010 and links [IEEE document 11615530](https://ieeexplore.ieee.org/document/11615530). IEEE returns a JavaScript/robot-verification page. The conference program domain blocks retrieval. Thus publisher/conference metadata were sought but could not be independently verified from their full official records. Public citation and scholarly metadata identify the arXiv revision; no conference DOI is invented.
4. Design sources are not scientific evidence. The TQPNet template and the SOLARIS index graphic are reused with their provenance recorded separately.

## Identity

Exact title: **Zero-Shot Transferable Solution Method for Parametric Optimal Control Problems**.

| Order | Paper author | Paper affiliation | Linked verified profile |
|---|---|---|---|
| 1 | Xingjian Li | Oden Institute, UT Austin | https://oden.utexas.edu/people/directory/Xingjian-Li/ |
| 2 | Kelvin Kan | Department of Mathematics, UCLA | https://www.math.ucla.edu/~kelvin.kan/home.html |
| 3 | Deepanshu Verma | Department of Mathematical and Statistical Sciences, Clemson University | https://www.clemson.edu/science/academics/departments/mathstat/about/profiles/dverma |
| 4 | Krishna Kumar | Oden Institute, UT Austin | https://www.geoelements.org/team/krishna-kumar |
| 5 | Stanley Osher | Department of Mathematics, UCLA | https://math.ucla.edu/~sjo/ |
| 6 | Ján Drgoňa | Department of Civil and Systems Engineering, Johns Hopkins University | https://drgona.github.io/ |

The older UCLA-hosted PDF spells the first author “Xinjian”; arXiv v2 and the official UT profile agree on **Xingjian**, used here. DBLP normalizes Osher to “Stanley J. Osher” and loses Drgoňa's caron; displayed authors follow the primary paper exactly. Affiliations follow the paper, not inferred current job titles.

## Claim and equation map

| Website element | Primary location | Implementation/evidence | Qualification retained |
|---|---|---|---|
| Motivation: repeated solves as objectives change | Introduction; Section III opening | Numerical trajectory datasets in all three code directories | Dynamics are fixed within each task family |
| Parametric running/terminal objective and dynamics | Eqs. (1)–(3), Section II | Simulation dynamics in evaluation scripts | Admissible control set is notation, not an enforcement mechanism in the learned approximation |
| Shared policy bases, task coefficients | Eq. (7) | `compute_representation`, `predict` calls | Approximate target policy; bases fixed online |
| Finite-data LS reconstruction | Eq. (8); Section II regularization paragraph | FunctionEncoder 0.1.1 called by training/evaluation scripts | New-task demonstrations needed for LS |
| Offline alternating coefficient inference and basis updates | Algorithm 1 | `train_ctrhill.py`, `train_quad.py`, `train_bike.py` call library `train_model` | Imitation learning, offline training; basis-norm penalty as written in Algorithm 1 |
| Optional operator targets | Algorithm 2, lines 5–7 | `loss_fun` in `train_ctrhill_operator.py` and `train_quad_operator.py`: mean squared coefficient discrepancy | Separately trained operator, frozen bases; extra data/training |
| LS versus operator deployment | Section III Online Phase | Separate `*_operator.py` evaluation scripts | Operator needs explicit structured task parameters; bicycle tested with LS only |
| State/time feedback and plant loop | Eq. (7), Eq. (1) | 2D rollout loops; `quad_dynamics`; `bicycle_dynamics` | Coefficients are task-level; state/time changes each policy call |
| Policy-space approximation statement | Theorem 1, cited FE result | No independent guarantee from finite training | Continuous target, compact domain, separable Hilbert space, existence of sufficiently many bases |
| LS coefficient convergence | Theorem 2 and complete appendix, Eqs. (11)–(38) | Analysis only | IID samples, bounded bases/targets, positive-definite population Gram, sample size sufficient for Eq. (23); fixed basis; conditioning-dependent constants |
| Soft obstacles, no hard safety claim | V-A Gaussian Q; V-C one/two Gaussian Q; evaluation code | Costs penalize state location | No collision, feasibility, stability, or physical-deployment certificate |
| Simulations, NVIDIA A100 | Section V introductory paragraph and examples | No physical data/hardware deployment found | No timing/speedup/“real time” claims on page |

## Every displayed benchmark number

The exact decimal values are preserved as strings in `data/results.json`; validation compares all three HTML tables to these strings. Table I/II columns were transposed to put LS and operator side by side, without changing values. Paper “True Objective Loss” is called “Numerical reference” to avoid implying a certified global optimum.

| Display | Source and statistical context |
|---|---|
| 2D: 4.8609, 4.8737, 4.9625; 4.8295, 4.8608, 4.9578; 4.8782, 5.0751, 5.3214 | Table I: means over targets and initial conditions; seen/interpolation/extrapolation; reference/LS/operator |
| Quad: 276.9546, 278.8933, 278.4307; 274.3089, 275.5074, 294.5629 | Table II: means over targets and initial conditions; seen/new; reference/LS/operator |
| Bike single: 2.6789, 0.0463, 0.0012; reference 2.6480, 0.0385, 0.00005 | Table III: control cost, obstacle cost, terminal position deviation; unseen configurations |
| Bike double: 3.0370, 0.5750, 0.0046; reference 2.9668, 0.5286, 0.00004 | Table III, same metrics |
| Chart: 0.65%, 2.66%, 4.04%, 9.09%, 0.44%, 7.38% | Newly computed ratios of rounded reported means: `100*(FE/reference-1)`. These are not new experiments or per-trajectory mean errors. Script uses Decimal and records source. No uncertainty was published, so none is fabricated. |
| 2D: 16 targets × 200 trajectories, T=1, 20 steps; 100 bases, 4 layers, width 256, Adam 0.001, 20,000 steps | Section V-A; architecture and optimization described by paper |
| 2D: 500 sample points from 40 trajectories; 40 rollout initial states | `2D_toy_control/plotter_dataset_test.py` lines around 135–180. Random points are drawn with replacement from 40×20 points; this is not a disjoint held-out-trajectory split. |
| Quad: 12 states, 4 controls; 64 train targets × 80 trajectories; 27 new targets × 25 trajectories; T=2, 50 steps; 100,000 iterations; terminal weight 500 | Section V-B, Eq. (9), objective and data paragraphs |
| Quad: 5 representation trajectories + 20 evaluation trajectories per test target | `Quadcopter_control/eval_quadcopter_test.py` slices `:5`, `5:`; operator evaluates same remaining 20 |
| Bike: 144 train + 36 new single-obstacle settings; 576 double-obstacle settings split 544/32; 100 trajectories per setting; T=5 | Section V-C |
| Bike: 50 representation + 50 evaluation trajectories | `Bike_control/eval_plotter_1_obs.py`, `eval_plotter_2_obs.py` `num_inference=50` and remaining rollouts |
| Terminal position metric is squared Euclidean x,y error | Table III wording plus `term_dev_pred = torch.norm(... :2 ...)**2` in both bicycle evaluation scripts. No physical unit supplied by paper. |
| FunctionEncoder 0.1.1, PyTorch 2.8.0 | Research-code README dependency list, not independently installed/reproduced here |

Batch sizes for an inference timing benchmark, CPU model, seed variability, confidence intervals, and end-to-end solve latency are not reported in the paper. A100 is the reported experimental platform, not proof all computation occurs on GPU. Code uses CPU operations for some dynamics updates.

## Consequential discrepancies and exclusions

1. **Table I versus prose:** Section V-A says errors are below 4% across all test cases. Its extrapolation entries imply about 4.04% for LS and 9.09% for operator using a ratio of reported means. The blanket statement is omitted; actual values and the discrepancy are available on the page.
2. **2D cost code versus paper:** both 2D evaluation scripts accumulate `torch.norm(u, dim=1)` without squaring, whereas Section V-A specifies half squared norm. The source map and public result note flag this. Published tables are not presented as independently reproduced code output.
3. **Operator loss prose versus Algorithm 2:** adjacent prose describes reconstruction loss; Algorithm 2 and both released operator trainers regress LS coefficient targets. The page follows the algorithm and implementation and notes the discrepancy.
4. **Bike cost normalization:** evaluation scripts include `0.5*dt*A*exp(...)` for obstacle costs; the written paper defines Q without this 0.5. The printed terminal formula includes `0.5*alpha_G`, whose dataset value must be read before comparing. Do not silently derive alternate Table III numbers from code.
5. **Theorem statement versus appendix:** the theorem display has a malformed closing parenthesis and condensed constants; the appendix retains both square-root and inverse-M terms and explicitly imposes empirical Gram invertibility through Eq. (23). Page gives only the qualified asymptotic rate, not exact constants or a finite-sample numerical certificate. Separate coefficient estimation, representation bias, and closed-loop performance.
6. **README command mismatch:** quadcopter instructions name `train_ctrhill.py` / `train_ctrhill_operator.py`; actual directory contains `train_quad.py` / `train_quad_operator.py`. Resource links target directory/code rather than copying incorrect commands.
7. **Bike data distribution:** train/test .mat files are referenced by code using external Google-hosted downloads, not tracked in the inspected repository. Download availability was not verified. 2D and quad datasets and model weights are tracked. No private download token is copied into the website.
8. **Paper assets:** full text/appendix and figure captions were readable; downloadable arXiv image/PDF bytes were unavailable to the local executor. Use the exact official SOLARIS vector abstract and an explicitly labelled replot of published table means. Do not claim the new chart is an original paper figure. Link the full paper for original experimental trajectories.
9. **Publication metadata:** official IEEE page couldn't be read past robot verification. ACC acceptance is author-verified; page numbers are only independently indexed by DBLP. Citation explicitly uses arXiv v2. Older UCLA mirror's first-author spelling is not copied.

## Maintenance rules

Update the paper version, code commit, claims, data, provenance and metadata together. Keep scientific tables primary when prose conflicts with them, flag conflicts, and do not upgrade empirical results into guarantees. Never relabel the current conceptual graphic or table replot as measured trajectories. Run validation before deployment. Record a successful Pages run and verify the actual live site before reporting publication.
