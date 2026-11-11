'use strict';
document.addEventListener('DOMContentLoaded', () => {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [{left: '$$', right: '$$', display: true}, {left: '\\(', right: '\\)', display: false}],
      throwOnError: true,
      strict: 'warn'
    });
  }
  const copy = document.getElementById('copy-bibtex');
  const status = document.getElementById('copy-status');
  copy.addEventListener('click', async () => {
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
