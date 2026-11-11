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
console.log(`PASS: ${count} math expressions render with local KaTeX.`);
