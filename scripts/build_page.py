"""Assemble the buildless page from audited metadata and transcribed paper tables.

This script is only needed when editing content. GitHub Pages serves index.html.
"""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parents[1]
D = json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))
TITLE = 'Zero-Shot Transferable Solution Method for Parametric Optimal Control Problems'
URL = 'https://solaris-jhu.github.io/FE-OC-website/'
DESCRIPTION = 'Function encoder policies learn reusable control bases offline and transfer to new objectives through least-squares or operator-based coefficient inference.'
AUTHORS = [
 ('Xingjian Li','1','https://oden.utexas.edu/people/directory/Xingjian-Li/'),
 ('Kelvin Kan','2','https://www.math.ucla.edu/~kelvin.kan/home.html'),
 ('Deepanshu Verma','3','https://www.clemson.edu/science/academics/departments/mathstat/about/profiles/dverma'),
 ('Krishna Kumar','1','https://www.geoelements.org/team/krishna-kumar'),
 ('Stanley Osher','2','https://math.ucla.edu/~sjo/'),
 ('Ján Drgoňa','4','https://drgona.github.io/')
]
BIB = (ROOT/'citation.bib').read_text(encoding='utf-8').strip()
author_html = '\n'.join(f'<span class="author"><a href="{url}">{name}</a><sup>{aff}</sup></span>' for name,aff,url in AUTHORS)
author_meta = '\n'.join(f'<meta name="citation_author" content="{name}">' for name,_,_ in AUTHORS)
structured = json.dumps({
 '@context':'https://schema.org','@type':'ScholarlyArticle','name':TITLE,
 'headline':TITLE,'url':URL,'description':DESCRIPTION,
 'author':[{'@type':'Person','name':n,'url':u} for n,_,u in AUTHORS],
 'datePublished':'2025-09-22','dateModified':'2026-03-11',
 'identifier':'arXiv:2509.18404v2','sameAs':'https://arxiv.org/abs/2509.18404v2',
 'image':URL+'assets/social-preview.png','inLanguage':'en'
},ensure_ascii=False)

def table(key,headers,caption):
    rows = ''.join('<tr>'+''.join(f'<th scope="row">{html.escape(c)}</th>' if j==0 else f'<td>{html.escape(c)}</td>' for j,c in enumerate(row))+'</tr>' for row in D[key])
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{caption}"><table class="results" id="{key}"><caption>{caption}</caption><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in headers)+'</tr></thead><tbody>'+rows+'</tbody></table></div>'

page = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ | SOLARIS</title>
<meta name="description" content="__DESCRIPTION__">
<link rel="canonical" href="__URL__">
<meta property="og:type" content="website"><meta property="og:site_name" content="SOLARIS Research">
<meta property="og:title" content="__TITLE__"><meta property="og:description" content="__DESCRIPTION__">
<meta property="og:url" content="__URL__"><meta property="og:image" content="__URL__assets/social-preview.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Function encoder policies: learn shared bases, infer task coefficients, evaluate feedback control.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESCRIPTION__"><meta name="twitter:image" content="__URL__assets/social-preview.png">
<meta name="citation_title" content="__TITLE__">
__AUTHOR_META__
<meta name="citation_publication_date" content="2026/03/11"><meta name="citation_arxiv_id" content="2509.18404">
<meta name="citation_pdf_url" content="https://arxiv.org/pdf/2509.18404v2">
<meta name="citation_doi" content="10.48550/arXiv.2509.18404">
<link rel="icon" href="assets/logos/solaris.png"><link rel="stylesheet" href="assets/fonts/fonts.css">
<link rel="stylesheet" href="template.css"><link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="assets/vendor/katex/katex.min.css">
<script type="application/ld+json">__SCHEMA__</script>
<script defer src="assets/vendor/katex/katex.min.js"></script>
<script defer src="assets/vendor/katex/auto-render.min.js"></script><script defer src="site.js"></script>
</head>
<body>
<a class="skip" href="#overview">Skip to research summary</a>
<header class="hero">
 <div class="wrap">
  <div class="hero-head">
   <p class="eyebrow"><a class="pill" href="https://solaris-jhu.github.io/solaris-website/">SOLARIS</a> American Control Conference · 2026</p>
   <h1>Zero-Shot Transferable Solution Method<br class="desktop-break"> for Parametric Optimal Control Problems</h1>
   <div class="authors">__AUTHORS__</div>
   <p class="affiliations"><sup>1</sup> Oden Institute, The University of Texas at Austin<br>
   <sup>2</sup> Department of Mathematics, UCLA &nbsp;·&nbsp; <sup>3</sup> Department of Mathematical and Statistical Sciences, Clemson University<br>
   <sup>4</sup> Department of Civil and Systems Engineering, Johns Hopkins University</p>
   <nav class="buttons" aria-label="Paper resources">
    <a class="btn btn-primary" href="https://arxiv.org/abs/2509.18404">arXiv ↗</a>
    <a class="btn" href="https://github.com/XJ-LI/FE_OC">Code ↗</a>
    <a class="btn" href="#citation">BibTeX</a>
   </nav>
  </div>
  <div class="opening"><p class="summary"><strong>Learn a shared control-policy basis. Adapt its coefficients to a new objective.</strong><br>
  Function encoders separate offline imitation learning from task adaptation, enabling feedback policies to transfer without retraining their neural bases.</p></div>
  <figure class="overview-figure">
   <a class="figure-link" href="assets/figures/graphical-abstract.svg" aria-label="Open the full-size graphical abstract"><img src="assets/figures/graphical-abstract.svg" width="760" height="392" alt="Offline demonstrations train shared policy basis functions. At deployment, least squares uses new task demonstrations or an optional operator maps task parameters to coefficients. The coefficients combine the fixed bases into a task-specific policy."></a>
   <figcaption>Shared bases, task-specific coefficients. The SOLARIS graphical abstract illustrates the two transfer routes in Section III; its \(\pi_\eta\) denotes the paper’s task-specific policy \(\mathbf u_{\boldsymbol\theta}\). Curves are conceptual, not experimental trajectories. <span class="mobile-figure-hint">Scroll the figure horizontally or open it at full size.</span></figcaption>
  </figure>
  <div class="logos">
   <a href="https://solaris-jhu.github.io/solaris-website/"><img class="square" src="assets/logos/solaris.png" width="500" height="500" alt="SOLARIS Lab"></a>
   <a href="https://engineering.jhu.edu/"><img src="assets/logos/jhu-whiting.svg" width="280" height="70" alt="Johns Hopkins Whiting School of Engineering"></a>
   <a href="https://oden.utexas.edu/"><img src="assets/logos/ut-austin.svg" width="280" height="70" alt="The University of Texas at Austin"></a>
  </div>
 </div>
</header>
<nav class="section-nav" aria-label="Page sections"><div class="wrap">
 <a href="#overview">Overview</a><a href="#method">Method</a><a href="#results">Results</a><a href="#scope">Scope</a><a href="#resources">Resources</a><a href="#citation">Citation</a>
</div></nav>
<main>
<section id="overview"><div class="wrap wrap-narrow">
 <h2>One dynamical system, changing objectives</h2>
 <p class="summary-label">Research summary</p>
 <p>A new destination or obstacle configuration changes the optimal control problem. Solving a fresh trajectory optimization for every objective and initial condition can be expensive. This paper learns a reusable representation of the family of feedback policies, with the dynamics held fixed within each problem family.</p>
 <div class="math">$$\min_{\mathbf u\in\mathcal U}\;\mathcal J(\mathbf u;\boldsymbol\eta)=\int_0^T L(\mathbf x(t),\mathbf u(t),t;\boldsymbol\eta)\,dt+G(\mathbf x(T);\boldsymbol\eta)$$</div>
 <div class="math">$$\dot{\mathbf x}(t)=f(\mathbf x(t),\mathbf u(t),t),\qquad \mathbf x(0)=\mathbf x_0.$$</div>
 <p>The task parameter \(\boldsymbol\eta\) changes the running or terminal cost. A function encoder (FE) represents the corresponding policy using neural basis functions of state and time. Adaptation changes their coefficients; the learned bases remain fixed.</p>
 <div class="pillars">
  <div><span class="num">1</span><h3>Reusable policy representation</h3><p>Learn a common set of vector-valued basis functions from demonstrations across training tasks.</p></div>
  <div><span class="num">2</span><h3>Two transfer routes</h3><p>Infer coefficients by least squares (LS) from task data, or with an optional learned parameter-to-coefficient operator.</p></div>
  <div><span class="num">3</span><h3>Feedback across initial states</h3><p>Evaluate a state-and-time policy repeatedly in a rollout, tested on new initial conditions and objectives.</p></div>
 </div>
 <p class="source-note">Formulation: Section II, Eqs. (1)–(3). Contributions: Sections I and III. Scientific content follows <a href="https://arxiv.org/abs/2509.18404v2">arXiv v2, 11 March 2026</a>.</p>
</div></section>
<section id="method" class="alt"><div class="wrap wrap-narrow">
 <h2>Learn the bases offline. Infer the coefficients online.</h2>
 <p>The representation separates the part shared across tasks from the part that changes with the objective:</p>
 <div class="math">$$\mathbf u_{\boldsymbol\theta}(\mathbf x,t;\boldsymbol\eta)=\sum_{j=1}^{p}c_j(\boldsymbol\eta)\,\phi_j(\mathbf x,t;\boldsymbol\theta_j).$$</div>
 <p>Here \(\phi_j\) is a learned policy basis function, \(c_j\) is its task-dependent coefficient, and \(p\) is the basis size. This is an approximation to the target feedback policy.</p>
 <div class="method-step">
  <div class="step-label"><span>01</span><span>Offline · demonstrations and basis learning</span></div>
  <h3>Fit a common control space</h3>
  <p>Collect state–time–control demonstrations \(\mathcal D_{S_k}\) for each training task, using numerical optimal control solvers or existing policies. For the current bases, solve for each task’s LS coefficients. Then update the basis parameters by gradient descent on reconstruction error plus basis-norm regularization. Repeat these steps during training.</p>
  <div class="math">$$C(\mathbf c,\mathcal D)=\frac{1}{M}\sum_{i=1}^{M}\left\|\mathbf u_i-\sum_{j=1}^{p}c_j\phi_j(\mathbf x_i,t_i)\right\|_2^2.$$</div>
  <p class="detail">Algorithm 1 adds \(\lambda\sum_j\|\phi_j\|_{\mathcal H}^2\) to the reconstruction loss. The implementation uses the FunctionEncoder library; Section II also describes Tikhonov regularization for numerical stability of the coefficient solve.</p>
 </div>
 <div class="method-step">
  <div class="step-label"><span>02</span><span>Optional offline stage · operator learning</span></div>
  <h3>Learn to predict coefficients from task parameters</h3>
  <p>Once the bases are trained, an additional network \(\psi_{\boldsymbol\gamma}\) can map a structured task specification to coefficients. Algorithm 2 trains it against LS coefficient targets while holding the bases fixed.</p>
  <div class="math">$$\min_{\boldsymbol\gamma}\;\sum_k\left\|\mathbf c_{S_k}^{\rm LS}-\psi_{\boldsymbol\gamma}(\boldsymbol\eta_{S_k})\right\|_2^2.$$</div>
  <p class="detail">This stage adds offline training and data requirements. The paper evaluates the operator for target-location tasks; its bicycle experiments use LS only.</p>
 </div>
 <div class="method-step">
  <div class="step-label"><span>03</span><span>Online · new task, fixed bases</span></div>
  <h3>Choose how to adapt</h3>
  <div class="scope-grid">
   <div><h3>LS: new task demonstrations</h3><div class="math">$$\mathbf c(\boldsymbol\eta)=\arg\min_{\mathbf c}C(\mathbf c,\mathcal D_{\rm new})$$</div><p>Project demonstrated controls onto the learned bases. New task data are required, but the neural bases are not retrained.</p></div>
   <div><h3>Operator: task specification</h3><div class="math">$$\mathbf c(\boldsymbol\eta)=\psi_{\boldsymbol\gamma}(\boldsymbol\eta)$$</div><p>Use the separately trained operator to predict coefficients. No demonstrations from the new task are needed during inference.</p></div>
  </div>
 </div>
 <div class="method-step">
  <div class="step-label"><span>04</span><span>Online · state feedback</span></div>
  <h3>Evaluate, apply control, observe the next state</h3>
  <p>At each rollout step, the current state and time enter the fixed bases. Combine their outputs with the inferred coefficients, apply the resulting control to the dynamics, and feed the updated state into the next policy evaluation. The coefficients describe the task; the basis evaluations respond to the changing state.</p>
  <figure class="figure"><img src="assets/figures/feedback.svg" width="1000" height="310" alt="Current state and time enter fixed policy basis functions. Task coefficients weight the basis outputs to produce control. The dynamical system evolves, returning its state to the policy in a closed feedback loop."><figcaption>Deployment structure from Eq. (7) and the released rollout scripts. The diagram is a static explanation of the feedback computation.</figcaption></figure>
 </div>
 <p class="source-note">Method: Eq. (7), Eq. (8), Algorithms 1–2 and Section III. The operator coefficient-target loss shown here follows Algorithm 2 and the released training code; the adjacent paper prose describes it differently.</p>
</div></section>
<section id="results"><div class="wrap wrap-narrow">
 <h2>Transfer across targets and obstacle costs</h2>
 <p>Three simulated problem families test the learned policies against discretization-based numerical optimal control solutions. The paper reports experiments on an NVIDIA A100 GPU. The values below are reported means, in the paper’s objective units; no confidence intervals or variability across training seeds are supplied.</p>
 <figure class="figure"><a class="figure-link" href="assets/figures/objective-comparison.svg" aria-label="Open full-size objective comparison"><img src="assets/figures/objective-comparison.svg" width="1000" height="480" alt="Relative increases in mean objective from Tables I and II. New 2D interpolation: LS 0.65 percent, operator 2.66 percent; extrapolation: LS 4.04 percent, operator 9.09 percent. New quadcopter targets: LS 0.44 percent, operator 7.38 percent."></a><figcaption>Replot of published means from Tables I–II, not a new experiment. Each percentage is \(100(\bar J_{\rm FE}/\bar J_{\rm ref}-1)\), computed from the rounded table entries. It is a ratio of means, not a mean of per-trajectory errors. No uncertainty bars are available. <span class="mobile-figure-hint">Scroll horizontally to read the figure at full size.</span></figcaption></figure>
 <h3 id="path-planning">2D path planning: new destinations</h3>
 <p>A planar integrator \(\dot{\mathbf x}=\mathbf u\) navigates a Gaussian obstacle cost. Sixteen target locations form the training set, with 200 numerically solved trajectories per target. The horizon is \(T=1\), discretized into 20 steps. Tests include seen targets, new interpolated targets, and extrapolation, all with new initial states.</p>
 __TABLE1__
 <p class="detail">The paper’s objective combines control effort, a Gaussian obstacle penalty, and quadratic terminal cost. Its published means average over target states and initial conditions. The released LS evaluation script samples 500 state–time–control points from 40 trajectories per task for coefficient inference, then evaluates those 40 initial states.</p>
 <details><summary>Training setup and source qualifications</summary><p>Section V-A specifies 100 bases, a four-layer multilayer perceptron with hidden width 256, Adam at learning rate 0.001, and 20,000 training steps. The paper’s prose states that errors are below 4% across test cases, but Table I gives larger relative differences for extrapolation, especially for the operator. This page uses the table values without that blanket claim.</p><p>The released 2D evaluation script accumulates control norms, whereas the paper specifies squared control norms. Table I is reproduced from the paper; these values have not been independently reproduced from that script.</p></details>
 <h3 id="quadcopter">Quadcopter: nonlinear dynamics in 12 states</h3>
 <p>The quadcopter has 12 states and four control inputs: thrust and three torques. Training uses 64 target locations with 80 trajectories per target. Testing introduces 27 new targets, each with 25 trajectories. The horizon is \(T=2\), with 50 integration steps.</p>
 __TABLE2__
 <p class="detail">The released LS test script fits coefficients using five trajectories per new target and evaluates feedback rollouts on the other 20. For new targets, the published LS and reference means are close; the operator’s mean is higher. These are comparisons with the numerical reference, not certificates of global optimality.</p>
 <details><summary>Training setup</summary><p>Section V-B uses the same 100-basis, four-layer, width-256 architecture and optimizer settings as the 2D example, with 100,000 iterations. The objective combines quadratic control effort with a terminal state penalty weighted by 500.</p></details>
 <h3 id="bicycle">Bicycle: changing the running cost</h3>
 <p>A nonlinear bicycle model changes its route as one or two Gaussian obstacle penalties vary. This experiment uses LS transfer only. The single-obstacle study has 144 training and 36 test configurations. The double-obstacle study splits 576 configurations into 544 for training and 32 for testing. Each configuration has 100 trajectories; the horizon is \(T=5\).</p>
 __TABLE3__
 <p class="detail">Table III averages over unseen configurations. Terminal position deviation is the reported position-error metric; the released evaluation code computes squared Euclidean error in \(x,y\). The LS scripts use 50 trajectories to estimate coefficients and evaluate the other 50. The obstacle is a smooth cost penalty, so these results do not establish collision-free operation.</p>
 <p class="source-note">Results: Section V-A / Table I; Section V-B / Table II; Section V-C / Table III. Numerical references are produced with SciPy or CasADi. The paper provides no end-to-end timing table, inference batch-size benchmark, or repeated-run statistics; no runtime or speedup claim is made here.</p>
</div></section>
<section id="scope" class="alt"><div class="wrap wrap-narrow">
 <h2>What the results establish—and their scope</h2>
 <div class="scope-grid">
  <div><h3>Transfer within a problem family</h3><p>The dynamics stay fixed within each family; objectives and initial conditions vary. The experiments support transfer on the tested distributions. Extrapolation success in selected cases is not a guarantee for arbitrary new tasks.</p></div>
  <div><h3>Policy approximation theory</h3><p>The paper invokes an existence result for approximating continuous functions in a separable Hilbert space on a compact domain. This does not guarantee that a finite trained network achieves a specified control performance.</p></div>
  <div><h3>Finite-sample LS analysis</h3><p>Theorem 2 and its appendix analyze coefficient estimation under independent, identically distributed samples, bounded bases and targets, and a positive-definite population Gram matrix. The proof also requires enough samples to control the empirical Gram perturbation.</p></div>
  <div><h3>Costs and constraints</h3><p>The benchmarks use numerical simulation and soft obstacle penalties. They do not certify closed-loop stability, hard constraint satisfaction, collision avoidance, or physical deployment performance.</p></div>
 </div>
 <details><summary>How to interpret the sample convergence result</summary><p>The appendix gives an asymptotic \(\mathcal O(M^{-1/2})\) coefficient-error rate for a fixed basis, with conditioning-dependent constants and additional finite-sample terms. It concerns unregularized population and empirical LS solutions. It is not an exact-optimality claim, and does not directly certify correlated trajectory samples or the optional operator network.</p></details>
</div></section>
<section id="resources"><div class="wrap wrap-narrow">
 <h2>Paper, implementation, and experimental material</h2>
 <div class="resource-grid">
  <a class="resource-card" href="https://arxiv.org/abs/2509.18404v2"><strong>Full paper and appendix <span aria-hidden="true">↗</span></strong><span>Version 2 · 11 March 2026 · open access</span></a>
  <a class="resource-card" href="https://github.com/XJ-LI/FE_OC"><strong>Research code <span aria-hidden="true">↗</span></strong><span>PyTorch implementation, evaluation scripts, and pretrained models</span></a>
  <a class="resource-card" href="https://github.com/XJ-LI/FE_OC/tree/65337fde9b540b3ecb8f4f4b0771ad1efae71f6a/2D_toy_control/Dataset"><strong>Released trajectory data <span aria-hidden="true">↗</span></strong><span>2D datasets; quadcopter datasets are also included in the repository</span></a>
  <a class="resource-card" href="https://ieeexplore.ieee.org/document/11615530"><strong>ACC publication record <span aria-hidden="true">↗</span></strong><span>IEEE Xplore record linked by the bibliographic index</span></a>
 </div>
 <p class="source-note">Code inspected at <a href="https://github.com/XJ-LI/FE_OC/tree/65337fde9b540b3ecb8f4f4b0771ad1efae71f6a">commit 65337fd</a>. The bicycle scripts refer to separately hosted datasets; their downloads were not verified. The repository README lists FunctionEncoder 0.1.1 and PyTorch 2.8.0. Reproduction requires checking those dependencies and the documented data paths.</p>
 <p class="source-note">ACC 2026 acceptance is confirmed by the <a href="https://drgona.github.io/news/">authors’ announcement</a>; the <a href="https://dblp.org/rec/conf/amcc/LiKVKOD26.html?view=bibtex">bibliographic record</a> lists pages 2003–2010. IEEE blocks automated metadata retrieval, so this page’s citation identifies the verified arXiv revision rather than asserting an unverified conference DOI.</p>
</div></section>
<section id="citation" class="alt"><div class="wrap wrap-narrow">
 <h2>Cite the paper</h2><p>BibTeX for the arXiv revision summarized on this page.</p>
 <div class="citation-actions"><button class="btn" id="copy-bibtex" type="button">Copy BibTeX</button><a class="btn" href="citation.bib" download>Download .bib</a><span id="copy-status" role="status" aria-live="polite"></span></div>
 <pre tabindex="0" aria-label="BibTeX citation"><code id="bibtex">__BIB__</code></pre>
</div></section>
</main>
<footer><div class="wrap"><p><a href="https://solaris-jhu.github.io/solaris-website/">SOLARIS Lab</a> · Johns Hopkins University<br>Website foundation adapted from <a href="https://solaris-jhu.github.io/TQPNet/">TQPNet</a> under the Apache License 2.0. <a href="NOTICE">Attribution and asset notices</a>.</p></div></footer>
</body></html>
'''
replacements = {'__TITLE__':TITLE,'__URL__':URL,'__DESCRIPTION__':DESCRIPTION,'__AUTHORS__':author_html,'__AUTHOR_META__':author_meta,'__SCHEMA__':structured,'__BIB__':html.escape(BIB),
 '__TABLE1__':table('table1',['Evaluation','Numerical reference','FE–LS','FE–operator'],'Table I · mean objective, 2D path planning'),
 '__TABLE2__':table('table2',['Evaluation','Numerical reference','FE–LS','FE–operator'],'Table II · mean objective, quadcopter'),
 '__TABLE3__':table('table3',['Setting','Method','Control cost','Obstacle cost','Terminal position deviation'],'Table III · bicycle, means on unseen configurations')}
for key,value in replacements.items(): page=page.replace(key,value)
(ROOT/'index.html').write_text(page,encoding='utf-8')
print('Built index.html from audited content and table data.')
