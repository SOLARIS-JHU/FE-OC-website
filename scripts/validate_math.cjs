// Strict KaTeX validation using the same local release shipped with the website.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const katex = require(path.join(root, 'assets/vendor/katex/katex.min.js'));
const html = fs.readFileSync(path.join(root, 'index.html'),'utf8');
let count=0;
for(const m of html.matchAll(/\$\$([\s\S]*?)\$\$|\\\(([\s\S]*?)\\\)/g)) {
  katex.renderToString(m[1] ?? m[2], {displayMode: m[1] !== undefined, throwOnError: true, strict: 'error'});
  count++;
}
if(count < 15) throw new Error('Unexpectedly few math expressions found.');
let diagramCount=0;
for(const m of html.matchAll(/data-tex="([^"]+)"/g)) {
  const tex=m[1].replaceAll('&quot;','"').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&');
  katex.renderToString(tex, {throwOnError:true,strict:'error'});
  diagramCount++;
}
if(diagramCount!==7) throw new Error('Expected seven LaTeX equations in the feedback diagram.');
console.log(`PASS: ${count} page equations and ${diagramCount} feedback equations render with local KaTeX.`);
