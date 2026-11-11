'use strict';

// Rebuild the inline diagram and its full-size page with the shipped KaTeX.
// No browser, TeX installation, network request, or npm installation is needed.
// The surrounding policy representation is Eq. (7); dynamics follow Eq. (1).
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const katex = require(path.join(root, 'assets/vendor/katex/katex.min.js'));
const directory = path.join(root, 'assets/figures');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const math = (tex, className = '') => `<span class="feedback-diagram__math ${className}" data-tex="${escape(tex)}">${katex.renderToString(tex, { displayMode: false, output: 'htmlAndMathml', throwOnError: true, strict: 'error' })}</span>`;

const styles = `<style>
.feedback-diagram { position: relative; width: 1000px; height: 355px; max-width: none; box-sizing: border-box; overflow: hidden; background: #fff; color: #1a1f2b; font-family: Inter, system-ui, sans-serif; font-size: 18px; line-height: 1.35; }
.feedback-diagram *, .feedback-diagram *::before, .feedback-diagram *::after { box-sizing: border-box; }
.feedback-diagram__wires { position: absolute; inset: 0; width: 1000px; height: 355px; max-width: none; }
.feedback-diagram__heading { position: absolute; top: 24px; left: 24px; font-size: 20px; font-weight: 600; color: #002d72; }
.feedback-diagram__fixed { position: absolute; top: 58px; left: 24px; font-size: 16px; color: #5b6470; }
.feedback-diagram__node { position: absolute; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 15px; text-align: center; }
.feedback-diagram__label { font-size: 17px; font-weight: 600; color: #002d72; }
.feedback-diagram__input { left: 17px; top: 144px; width: 138px; height: 80px; gap: 12px; }
.feedback-diagram__input .feedback-diagram__label { font-size: 16px; font-weight: 500; color: #1a1f2b; }
.feedback-diagram__bases { left: 185px; top: 130px; width: 250px; height: 110px; }
.feedback-diagram__sum { left: 495px; top: 130px; width: 230px; height: 110px; }
.feedback-diagram__dynamics { left: 785px; top: 130px; width: 195px; height: 110px; }
.feedback-diagram__coefficients { left: 500px; top: 20px; width: 220px; height: 76px; gap: 9px; }
.feedback-diagram__coefficients .feedback-diagram__label { color: #0b7069; }
.feedback-diagram__math { display: inline-block; font-size: 22px; line-height: normal; white-space: nowrap; }
.feedback-diagram__math .katex { font-size: 1em; }
.feedback-diagram__dynamics .feedback-diagram__math { font-size: 19px; }
.feedback-diagram__wire-label { position: absolute; top: 148px; text-align: center; font-size: 19px; }
.feedback-diagram__basis-output { left: 437px; width: 56px; }
.feedback-diagram__control-output { left: 727px; width: 56px; }
.feedback-diagram__return-label { position: absolute; top: 316px; left: 200px; width: 590px; text-align: center; font-size: 17px; color: #5b6470; }
.feedback-diagram__sr { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; border: 0; }
</style>`;

const fragment = `${styles}
<div class="feedback-diagram" role="group" aria-labelledby="feedback-diagram-title" aria-describedby="feedback-diagram-description">
 <span id="feedback-diagram-title" class="feedback-diagram__heading">Feedback control</span>
 <span class="feedback-diagram__fixed">Basis parameters stay fixed</span>
 <span id="feedback-diagram-description" class="feedback-diagram__sr">Current state and time enter the fixed neural basis functions. Coefficients inferred for the task weight the basis outputs to produce a control input. The dynamics evolve under that input, and the updated state returns for the next policy evaluation.</span>
 <svg class="feedback-diagram__wires" viewBox="0 0 1000 355" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="feedback-diagram-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#002d72"/></marker></defs>
  <g fill="#f1f6fc" stroke="#bdcde0" stroke-width="1.4">
   <rect x="185" y="130" width="250" height="110" rx="12"/>
   <rect x="495" y="130" width="230" height="110" rx="12"/>
   <rect x="785" y="130" width="195" height="110" rx="12"/>
  </g>
  <g fill="none" stroke="#002d72" stroke-width="2.2" marker-end="url(#feedback-diagram-arrow)">
   <path d="M155 185 H185"/>
   <path d="M435 185 H495"/>
   <path d="M725 185 H785"/>
   <path d="M610 96 V130"/>
   <path d="M882.5 240 V297 H120 V220 H185"/>
  </g>
 </svg>
 <div class="feedback-diagram__node feedback-diagram__input"><span class="feedback-diagram__label">State and time</span>${math(String.raw`\mathbf{x}(t),\,t`)}</div>
 <div class="feedback-diagram__node feedback-diagram__bases"><span class="feedback-diagram__label">Evaluate fixed bases</span>${math(String.raw`\phi_j(\mathbf{x},t;\boldsymbol{\theta}_j)`)}</div>
 <div class="feedback-diagram__node feedback-diagram__coefficients"><span class="feedback-diagram__label">Task coefficients</span>${math(String.raw`c_j(\boldsymbol{\eta})`)}</div>
 <div class="feedback-diagram__node feedback-diagram__sum"><span class="feedback-diagram__label">Weight and sum</span>${math(String.raw`\mathbf{u}=\sum_{j=1}^{p}c_j\phi_j`)}</div>
 <div class="feedback-diagram__node feedback-diagram__dynamics"><span class="feedback-diagram__label">Evolve dynamics</span>${math(String.raw`\dot{\mathbf{x}}=f(\mathbf{x},\mathbf{u},t)`)}</div>
 ${math(String.raw`\phi_j`, 'feedback-diagram__wire-label feedback-diagram__basis-output')}
 ${math(String.raw`\mathbf{u}(t)`, 'feedback-diagram__wire-label feedback-diagram__control-output')}
 <span class="feedback-diagram__return-label">Updated state for the next policy evaluation</span>
</div>
`;

const standalone = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Feedback control with fixed policy bases | SOLARIS</title>
<meta name="description" content="Feedback computation for function encoder control policies: fixed neural bases, task coefficients, control input, and state evolution.">
<link rel="stylesheet" href="../fonts/fonts.css"><link rel="stylesheet" href="../vendor/katex/katex.min.css">
<style>
body{margin:0;padding:28px 20px;background:#fbfbfd;color:#1a1f2b;font-family:Inter,system-ui,sans-serif;line-height:1.6}main{max-width:1060px;margin:auto}h1{font-family:Fraunces,Georgia,serif;font-size:clamp(1.45rem,3vw,2rem);line-height:1.25;color:#002d72}a{color:#002d72;text-underline-offset:.15em}.feedback-scroll{overflow-x:auto;border:1px solid #dfe3ea;border-radius:14px;background:#fff;padding:14px}.feedback-scroll:focus-visible{outline:3px solid #002d72;outline-offset:3px}.feedback-caption{max-width:80ch}.feedback-scroll-hint{font-size:.9rem;color:#5b6470}@media(min-width:1080px){.feedback-scroll-hint{display:none}}
</style></head><body><main>
<p><a href="../../#method">Return to the research page</a></p><h1>Feedback control with fixed policy bases</h1>
<div class="feedback-scroll" tabindex="0" role="region" aria-label="Feedback control diagram, horizontally scrollable">${fragment}</div>
<p class="feedback-scroll-hint">Scroll horizontally to follow the full computation.</p>
<p class="feedback-caption">Task coefficients are inferred for the new objective before this feedback loop. At each step, the current state and time enter the fixed basis functions; the resulting control drives the dynamics and produces the next state.</p>
</main></body></html>
`;

fs.mkdirSync(directory, { recursive: true });
fs.writeFileSync(path.join(directory, 'feedback-fragment.html'), fragment);
fs.writeFileSync(path.join(directory, 'feedback.html'), standalone);
console.log('Generated feedback-fragment.html and feedback.html with seven strict KaTeX equations.');
