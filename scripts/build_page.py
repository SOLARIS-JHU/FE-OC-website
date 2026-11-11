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
ABSTRACT = (ROOT/'assets/figures/graphical-abstract-animated.svg').read_text(encoding='utf-8').replace('data-paused="false"', 'data-paused="true"', 1)
FEEDBACK = (ROOT/'assets/figures/feedback-fragment.html').read_text(encoding='utf-8')
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
   <p class="eyebrow"><a class="pill" href="https://solaris-jhu.github.io/solaris-website/">SOLARIS</a> American Control Conference (ACC) · 2026</p>
   <h1>Zero-Shot Transferable Solution Method<br class="desktop-break"> for Parametric Optimal Control Problems</h1>
   <div class="authors">__AUTHORS__</div>
   <p class="affiliations"><sup>1</sup> Oden Institute, The University of Texas at Austin<br>
   <sup>2</sup> Department of Mathematics, University of California, Los Angeles (UCLA)<br><sup>3</sup> Department of Mathematical and Statistical Sciences, Clemson University<br>
   <sup>4</sup> Department of Civil and Systems Engineering, Johns Hopkins University</p>
   <nav class="buttons" aria-label="Paper resources">
    <a class="btn btn-primary" href="https://ieeexplore.ieee.org/document/11615530" title="Published paper in the Institute of Electrical and Electronics Engineers (IEEE) Xplore library">Paper ↗</a>
    <a class="btn" href="https://arxiv.org/abs/2509.18404">arXiv ↗</a>
    <a class="btn" href="https://github.com/XJ-LI/FE_OC">Code ↗</a>
    <a class="btn" href="#citation">BibTeX</a>
   </nav>
  </div>
  <div class="opening"><p class="summary"><strong>Learn a shared control-policy basis. Adapt its coefficients to a new objective.</strong><br>
  Function encoders separate offline imitation learning from task adaptation, enabling feedback policies to transfer without retraining their neural bases.</p></div>
  <figure class="overview-figure">
   <div class="abstract-scroll" tabindex="0" role="region" aria-label="Animated overview of function encoder training and transfer">__ANIMATED_ABSTRACT__</div>
   <div class="figure-controls"><button class="btn" id="toggle-abstract" type="button" aria-pressed="false" aria-controls="feoc-abstract" hidden>Pause animation</button><a href="assets/figures/overview.html">Open full-size overview</a></div>
   <figcaption>Learn shared policy bases from training tasks, then infer new-task coefficients from demonstrations or task parameters. The learned bases remain fixed during deployment.<span class="mobile-figure-hint">Scroll horizontally to follow every stage.</span></figcaption>
  </figure>
  <div class="logos">
   <a href="https://solaris-jhu.github.io/solaris-website/"><img class="square" src="assets/logos/solaris.png" width="500" height="500" alt="SOLARIS Lab"></a>
   <a href="https://engineering.jhu.edu/"><img src="assets/logos/jhu-whiting.svg" width="280" height="70" alt="Johns Hopkins Whiting School of Engineering"></a>
   <a href="https://oden.utexas.edu/"><img src="assets/logos/ut-austin.svg" width="280" height="70" alt="The University of Texas at Austin"></a>
   <a href="https://www.ucla.edu/"><img class="ucla-logo" src="assets/logos/ucla.svg" width="360" height="169" alt="University of California, Los Angeles"></a>
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
 <p class="source-note">Problem formulation: <a href="https://arxiv.org/abs/2509.18404v2">Section II, Equations (1)–(3)</a>.</p>
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
  <p class="detail">Here \(M\) is the number of demonstration samples. Algorithm 1 adds \(\lambda\sum_j\|\phi_j\|_{\mathcal H}^2\) to the reconstruction loss, with regularization weight \(\lambda\). Tikhonov regularization improves numerical stability of the coefficient solve.</p>
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
  <figure class="figure feedback-figure"><div class="feedback-scroll" tabindex="0" role="region" aria-label="State feedback with fixed policy bases">__FEEDBACK_DIAGRAM__</div><figcaption>Task coefficients remain fixed while the observed state changes.<span class="mobile-figure-hint">Scroll horizontally or <a href="assets/figures/feedback.html">open the full-size feedback diagram</a>.</span></figcaption></figure>
 </div>
 <p class="source-note">Method: Equations (7)–(8) and Algorithms 1–2.</p>
</div></section>
<section id="results"><div class="wrap wrap-narrow">
 <h2>Transfer across targets and obstacle costs</h2>
 <p>Three simulated problem families—two-dimensional (2D) path planning, quadcopter control, and bicycle control—test the learned policies against discretization-based numerical optimal control solutions. Experiments use an NVIDIA A100 graphics processing unit (GPU). Function encoder transfer with least-squares coefficients is labeled FE–LS; FE–operator uses the learned coefficient network. Values are reported means in the paper's objective units; confidence intervals and variability across training seeds are not reported.</p>
 <figure class="figure"><a class="figure-link" href="assets/figures/objective-comparison.svg" aria-label="Open full-size objective comparison"><img src="assets/figures/objective-comparison.svg" width="1000" height="480" alt="Relative increases in mean objective from Tables I and II. New 2D interpolation: LS 0.65 percent, operator 2.66 percent; extrapolation: LS 4.04 percent, operator 9.09 percent. New quadcopter targets: LS 0.44 percent, operator 7.38 percent."></a><figcaption>Relative increase in mean objective: \(100(\bar J_{\rm FE}/\bar J_{\rm ref}-1)\), computed from the published means in Tables I–II. These are ratios of rounded means; per-trajectory error distributions and uncertainty estimates are not reported.<span class="mobile-figure-hint">Scroll horizontally to read the figure at full size.</span></figcaption></figure>
 <h3 id="path-planning">2D path planning: new destinations</h3>
 <p>A planar integrator \(\dot{\mathbf x}=\mathbf u\) navigates a Gaussian obstacle cost. Sixteen target locations form the training set, with 200 numerically solved trajectories per target. The horizon is \(T=1\), discretized into 20 steps. Tests include seen targets, new interpolated targets, and extrapolation, all with new initial states.</p>
 __TABLE1__
 <p class="detail">The paper’s objective combines control effort, a Gaussian obstacle penalty, and quadratic terminal cost. Its published means average over target states and initial conditions. The released LS evaluation script samples 500 state–time–control points from 40 trajectories per task for coefficient inference, then evaluates those 40 initial states.</p>
 <details><summary>Training setup and objective</summary><p>Training uses 100 bases, a four-layer multilayer perceptron with hidden width 256, adaptive moment estimation (Adam) at learning rate 0.001, and 20,000 training steps.</p><p>The reported objective uses squared control norms. The released 2D evaluation script accumulates unsquared control norms, so its cost calculation differs from the paper's formulation.</p></details>
 <h3 id="quadcopter">Quadcopter: nonlinear dynamics in 12 states</h3>
 <p>The quadcopter has 12 states and four control inputs: thrust and three torques. Training uses 64 target locations with 80 trajectories per target. Testing introduces 27 new targets, each with 25 trajectories. The horizon is \(T=2\), with 50 integration steps.</p>
 __TABLE2__
 <p class="detail">The released LS test script fits coefficients using five trajectories per new target and evaluates feedback rollouts on the other 20. For new targets, the published LS and reference means are close; the operator’s mean is higher. These are comparisons with the numerical reference, not certificates of global optimality.</p>
 <details><summary>Training setup</summary><p>Section V-B uses the same 100-basis, four-layer, width-256 architecture and optimizer settings as the 2D example, with 100,000 iterations. The objective combines quadratic control effort with a terminal state penalty weighted by 500.</p></details>
 <h3 id="bicycle">Bicycle: changing the running cost</h3>
 <p>A nonlinear bicycle model changes its route as one or two Gaussian obstacle penalties vary. This experiment uses LS transfer only. The single-obstacle study has 144 training and 36 test configurations. The double-obstacle study splits 576 configurations into 544 for training and 32 for testing. Each configuration has 100 trajectories; the horizon is \(T=5\).</p>
 __TABLE3__
 <p class="detail">Table III averages over unseen configurations. Terminal position deviation is the reported position-error metric; the released evaluation code computes squared Euclidean error in \(x,y\). The LS scripts use 50 trajectories to estimate coefficients and evaluate the other 50. The obstacle is a smooth cost penalty, so these results do not establish collision-free operation.</p>
 <p class="source-note">Results: Tables I–III. Numerical references use SciPy or CasADi. The paper provides no end-to-end timing table, inference batch-size benchmark, or repeated-run statistics.</p>
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
  <a class="resource-card" href="https://ieeexplore.ieee.org/document/11615530"><strong>Published paper · ACC 2026 <span aria-hidden="true">↗</span></strong><span>Institute of Electrical and Electronics Engineers (IEEE) Xplore</span></a>
 </div>
 <p class="source-note">Reproducible implementation: <a href="https://github.com/XJ-LI/FE_OC/tree/65337fde9b540b3ecb8f4f4b0771ad1efae71f6a">research code version 65337fd</a>, with FunctionEncoder 0.1.1 and PyTorch 2.8.0. The bicycle examples use separately hosted datasets linked from the code.</p>
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
replacements = {'__TITLE__':TITLE,'__URL__':URL,'__DESCRIPTION__':DESCRIPTION,'__AUTHORS__':author_html,'__AUTHOR_META__':author_meta,'__SCHEMA__':structured,'__BIB__':html.escape(BIB),'__ANIMATED_ABSTRACT__':ABSTRACT,'__FEEDBACK_DIAGRAM__':FEEDBACK,
 '__TABLE1__':table('table1',['Evaluation','Numerical reference','FE–LS','FE–operator'],'Table I · mean objective, 2D path planning'),
 '__TABLE2__':table('table2',['Evaluation','Numerical reference','FE–LS','FE–operator'],'Table II · mean objective, quadcopter'),
 '__TABLE3__':table('table3',['Setting','Method','Control cost','Obstacle cost','Terminal position deviation'],'Table III · bicycle, means on unseen configurations')}
for key,value in replacements.items(): page=page.replace(key,value)
(ROOT/'index.html').write_text(page,encoding='utf-8')
overview = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Function encoder training and transfer | SOLARIS</title>
<link rel="stylesheet" href="../fonts/fonts.css"><link rel="stylesheet" href="../../template.css"><link rel="stylesheet" href="../../style.css">
<script defer src="../../site.js"></script></head><body><main class="wrap" style="padding-block:2rem">
<p><a href="../../">Return to the research page</a></p><h1>Learn shared bases. Transfer to new objectives.</h1>
<figure class="overview-figure"><div class="abstract-scroll" tabindex="0" role="region" aria-label="Function encoder training and transfer">'''+ABSTRACT+'''</div>
<div class="figure-controls"><button class="btn" id="toggle-abstract" type="button" aria-pressed="false" aria-controls="feoc-abstract" hidden>Pause animation</button></div>
<figcaption>Training learns shared policy bases; new-task inference changes the coefficients while keeping those bases fixed.</figcaption></figure>
</main></body></html>'''
(ROOT/'assets/figures/overview.html').write_text(overview,encoding='utf-8')
print('Built index.html from audited content and table data.')
