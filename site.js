'use strict';
document.addEventListener('DOMContentLoaded', () => {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [{left: '$$', right: '$$', display: true}, {left: '\\(', right: '\\)', display: false}],
      throwOnError: true,
      strict: 'warn'
    });
  }

  const abstract = document.getElementById('solaris-abstract');
  const animationControl = document.getElementById('toggle-abstract');
  const svg = abstract?.querySelector('svg');
  if (svg && animationControl) {
    const prefix = 'v9-policyfe';
    const get = id => svg.querySelector('#' + prefix + '-' + id);
    const paths = Array.from({ length: 3 }, (_, index) => get('trajectory' + index));
    const tips = Array.from({ length: 3 }, (_, index) => get('tip' + index));
    if (paths.every(Boolean) && tips.every(Boolean)) {
      const original = paths.map(node => ({ node, attributes: { d: node.getAttribute('d') } }))
        .concat(tips.map(node => ({ node, attributes: { cx: node.getAttribute('cx'), cy: node.getAttribute('cy') } })));
      const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
      let userPaused = false;
      let paused = true;
      let time = 2;
      let lastTimestamp = null;
      let paintElapsed = 0;
      let frame = null;

      // Original SOLARIS v13 updater; source commit b8a7ebab0a24bd43c6f60e9dc78de4b338be58d9.
      // Only the three existing trajectory paths and their endpoint markers change.
      const draw = t => {
        const set = (id, attribute, value) => get(id).setAttribute(attribute, value);
        const q = Math.min(1, (t % 9) / 9 / .9);
        const dp = points => 'M' + points.map(point => point.join(' ')).join(' L');
        for (let j = 0; j < 3; j++) {
          const points = Array.from({ length: 81 }, (_, i) => [534 + 180 * i / 80, 272 - (83 + j * 22) * (i / 80) ** 2 + 13 * Math.sin(Math.PI * i / 80) * (j - 1)]);
          const i = Math.floor(q * 80);
          set('trajectory' + j, 'd', dp(points.slice(0, Math.max(2, i + 1))));
          set('tip' + j, 'cx', points[i][0]);
          set('tip' + j, 'cy', points[i][1]);
        }
      };
      const restoreOriginal = () => original.forEach(({ node, attributes }) => {
        for (const [name, value] of Object.entries(attributes)) {
          if (value === null) node.removeAttribute(name);
          else node.setAttribute(name, value);
        }
      });
      const tick = timestamp => {
        frame = null;
        if (paused) return;
        if (lastTimestamp !== null) {
          const dt = Math.min((timestamp - lastTimestamp) / 1000, .1);
          time += dt;
          paintElapsed += dt;
          if (paintElapsed >= .033) {
            draw(time);
            paintElapsed %= .033;
          }
        }
        lastTimestamp = timestamp;
        frame = requestAnimationFrame(tick);
      };
      const updateAnimation = () => {
        paused = motionPreference.matches || userPaused;
        abstract.dataset.paused = String(paused);
        animationControl.hidden = false;
        animationControl.disabled = motionPreference.matches;
        animationControl.setAttribute('aria-pressed', String(paused));
        animationControl.textContent = motionPreference.matches ? 'Animation off (reduced motion)' : paused ? 'Play animation' : 'Pause animation';
        if (frame !== null) cancelAnimationFrame(frame);
        frame = null;
        lastTimestamp = null;
        paintElapsed = 0;
        if (motionPreference.matches) restoreOriginal();
        else if (!paused) {
          draw(time);
          frame = requestAnimationFrame(tick);
        }
      };
      animationControl.addEventListener('click', () => { userPaused = !userPaused; updateAnimation(); });
      motionPreference.addEventListener('change', updateAnimation);
      updateAnimation();
    }
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
