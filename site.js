'use strict';
document.addEventListener('DOMContentLoaded', () => {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [{left: '$$', right: '$$', display: true}, {left: '\\(', right: '\\)', display: false}],
      throwOnError: true,
      strict: 'warn'
    });
  }
  const abstract = document.getElementById('feoc-abstract');
  const animationControl = document.getElementById('toggle-abstract');
  if (abstract && animationControl) {
    const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
    let userPaused = false;
    const updateAnimation = () => {
      const paused = motionPreference.matches || userPaused;
      abstract.dataset.paused = String(paused);
      animationControl.hidden = false;
      animationControl.disabled = motionPreference.matches;
      animationControl.setAttribute('aria-pressed', String(paused));
      animationControl.textContent = motionPreference.matches ? 'Animation off (reduced motion)' : paused ? 'Play animation' : 'Pause animation';
    };
    animationControl.addEventListener('click', () => { userPaused = !userPaused; updateAnimation(); });
    motionPreference.addEventListener('change', updateAnimation);
    updateAnimation();
  }
  const copy = document.getElementById('copy-bibtex');
  const status = document.getElementById('copy-status');
  if (copy && status) copy.addEventListener('click', async () => {
    const code = document.getElementById('bibtex');
    try {
      await navigator.clipboard.writeText(code.textContent.trim() + '\n');
      status.textContent = 'BibTeX copied.';
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = 'Citation selected. Copy it or download the .bib file.';
    }
  });
});
