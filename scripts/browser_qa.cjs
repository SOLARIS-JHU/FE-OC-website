'use strict';

// CI-only browser checks. The public site has no npm or Playwright dependency.
// Local: node scripts/browser_qa.cjs --serve _site --report-dir .qa-tmp/browser-local
// Live:  node scripts/browser_qa.cjs --url https://solaris-jhu.github.io/FE-OC-website/ --expected-file index.html --report-dir .qa-tmp/browser-live
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { parseArgs } = require('node:util');
const { chromium, request } = require('playwright');
const { values: options } = parseArgs({ options: {
  serve: { type: 'string' }, url: { type: 'string' },
  'base-path': { type: 'string', default: '/FE-OC-website/' },
  'expected-file': { type: 'string', default: 'index.html' },
  'report-dir': { type: 'string', default: '.qa-tmp/browser' }
} });
const out = path.resolve(options['report-dir']);
const report = {
  startedAt: new Date().toISOString(), commit: process.env.GITHUB_SHA || null,
  mode: options.serve ? 'staged-local' : 'published', preflight: [], cases: [],
  limits: 'Automated Chromium checks and screenshots; not a manual visual audit or an external-source availability audit.'
};
const hash = text => crypto.createHash('sha256').update(text.replace(/\r\n/g, '\n')).digest('hex');
const assert = (condition, message, evidence) => {
  if (!condition) throw new Error(message + (evidence ? ': ' + JSON.stringify(evidence) : ''));
};
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

async function serveSite(directory, basePath) {
  assert(basePath.startsWith('/') && basePath.endsWith('/'), 'Base path must begin and end with /');
  const root = path.resolve(directory);
  const mime = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.ttf': 'font/ttf', '.woff2': 'font/woff2', '.woff': 'font/woff', '.bib': 'text/plain; charset=utf-8' };
  const server = http.createServer(async (req, res) => {
    try {
      const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      if (!pathname.startsWith(basePath)) { res.writeHead(404).end(); return; }
      const filename = path.resolve(root, pathname.slice(basePath.length) || 'index.html');
      if (filename !== root && !filename.startsWith(root + path.sep)) { res.writeHead(403).end(); return; }
      if (!(await fsp.stat(filename)).isFile()) { res.writeHead(404).end(); return; }
      res.writeHead(200, { 'Content-Type': mime[path.extname(filename)] || 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
      fs.createReadStream(filename).on('error', () => res.destroy()).pipe(res);
    } catch { res.writeHead(404).end(); }
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  return { server, url: `http://127.0.0.1:${server.address().port}${basePath}` };
}

async function awaitPublishedContent(siteUrl, expected) {
  const api = await request.newContext();
  const deadline = Date.now() + (options.serve ? 10000 : 90000);
  try {
    do {
      const target = new URL(siteUrl);
      target.searchParams.set('qa', `${process.env.GITHUB_SHA || 'local'}-${report.preflight.length}`);
      try {
        const response = await api.get(target.href, { timeout: 10000, headers: { 'Cache-Control': 'no-cache' } });
        const actual = hash(await response.text());
        report.preflight.push({ status: response.status(), htmlSha256: actual });
        if (response.ok() && actual === expected) return target.href;
      } catch (error) { report.preflight.push({ error: error.message }); }
      if (options.serve) break;
      await delay(3000);
    } while (Date.now() < deadline);
    throw new Error('Fetched HTML did not match the checked-out source; see preflight records.');
  } finally { await api.dispose(); }
}

async function runCase(browser, target, configuration) {
  const result = { ...configuration, checks: [], screenshots: [], consoleErrors: [], pageErrors: [], requestFailures: [], badResponses: [] };
  report.cases.push(result);
  const context = await browser.newContext({
    viewport: { width: configuration.width, height: 1000 },
    colorScheme: configuration.colorScheme, reducedMotion: configuration.reducedMotion,
    permissions: ['clipboard-read', 'clipboard-write']
  });
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  page.on('console', message => { if (message.type() === 'error') result.consoleErrors.push(message.text()); });
  page.on('pageerror', error => result.pageErrors.push(error.message));
  page.on('requestfailed', req => result.requestFailures.push({ url: req.url(), error: req.failure()?.errorText }));
  page.on('response', response => { if (response.status() >= 400) result.badResponses.push({ url: response.url(), status: response.status() }); });
  async function check(name, operation) {
    try { const evidence = await operation(); result.checks.push({ name, status: 'passed', evidence }); return true; }
    catch (error) { result.checks.push({ name, status: 'failed', error: error.message }); return false; }
  }
  async function screenshot(suffix) {
    const filename = `${configuration.name}-${suffix}.png`;
    await page.screenshot({ path: path.join(out, filename), fullPage: true });
    result.screenshots.push(filename);
  }
  try {
    const loaded = await check('Page and rendered mathematics load', async () => {
      const response = await page.goto(target, { waitUntil: 'networkidle', timeout: 30000 });
      assert(response?.ok(), 'Page did not load successfully', response?.status());
      await page.locator('.katex').first().waitFor();
      await page.evaluate(() => document.fonts.ready);
      const counts = await page.evaluate(() => ({
        inlineAndDisplay: document.querySelectorAll('.katex').length,
        display: document.querySelectorAll('.katex-display').length,
        errors: document.querySelectorAll('.katex-error').length,
        unrenderedBlocks: [...document.querySelectorAll('.math')].filter(el => !el.querySelector('.katex')).length
      }));
      assert(counts.inlineAndDisplay > counts.display && counts.display > 0 && counts.errors === 0 && counts.unrenderedBlocks === 0, 'Incomplete mathematics rendering', counts);
      return counts;
    });
    if (!loaded) return;

    await check('Images decode and local typography loads', async () => {
      const evidence = await page.evaluate(async () => {
        const images = await Promise.all([...document.images].map(async img => {
          let error = null;
          try { await img.decode(); } catch (failure) { error = failure.message; }
          return { src: img.getAttribute('src'), width: img.naturalWidth, height: img.naturalHeight, complete: img.complete, error };
        }));
        return { images, fonts: [...document.fonts].map(font => ({ family: font.family.replace(/['"]/g, ''), weight: font.weight, status: font.status })) };
      });
      assert(evidence.images.length > 0 && evidence.images.every(img => img.complete && img.width > 0 && img.height > 0 && !img.error), 'Image decode failed', evidence.images);
      for (const family of ['Inter', 'Fraunces', 'KaTeX_Main']) assert(evidence.fonts.some(font => font.family === family && font.status === 'loaded'), `Font not loaded: ${family}`);
      assert(!evidence.fonts.some(font => font.status === 'error'), 'Font loading failed', evidence.fonts);
      return evidence;
    });

    await check('No page-wide horizontal overflow', async () => {
      const measurements = await page.evaluate(() => ({
        viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth,
        scrollRegions: [...document.querySelectorAll('.math, .table-wrap, .figure-link, pre')].map(el => ({ class: el.className || el.tagName, width: el.clientWidth, contentWidth: el.scrollWidth, overflowX: getComputedStyle(el).overflowX }))
      }));
      assert(measurements.document <= measurements.viewport + 1 && measurements.body <= measurements.viewport + 1, 'Page overflows horizontally', measurements);
      assert(measurements.scrollRegions.every(el => el.contentWidth <= el.width + 1 || ['auto', 'scroll'].includes(el.overflowX)), 'Wide content cannot be scrolled', measurements.scrollRegions);
      return measurements;
    });
    await check('Capture initial layout', () => screenshot('initial'));

    await check('Skip link and section links work from the keyboard', async () => {
      await page.keyboard.press('Tab');
      assert(await page.locator('.skip').evaluate(el => el === document.activeElement), 'Skip link is not first in keyboard order');
      const box = await page.locator('.skip').boundingBox();
      assert(box && box.x >= 0 && box.y >= 0 && box.x + box.width <= configuration.width + 1, 'Focused skip link is clipped', box);
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => location.hash === '#overview' && Math.abs(document.querySelector('#overview').getBoundingClientRect().top) < 60);
      await page.keyboard.press('Tab');
      assert(await page.evaluate(() => !!document.activeElement.closest('main')), 'Tab navigation did not move into the research content after skipping');
      const resultsLink = page.getByRole('navigation', { name: 'Page sections' }).getByRole('link', { name: 'Results', exact: true });
      await resultsLink.focus();
      const focusStyle = await resultsLink.evaluate(el => ({ style: getComputedStyle(el).outlineStyle, width: getComputedStyle(el).outlineWidth }));
      assert(focusStyle.style !== 'none' && parseFloat(focusStyle.width) > 0, 'Keyboard focus indicator is missing', focusStyle);
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => location.hash === '#results' && Math.abs(document.querySelector('#results').getBoundingClientRect().top) < 60);
      return { skipTarget: '#overview', sectionTarget: '#results', focusStyle };
    });

    await check('Every native disclosure opens and closes by keyboard', async () => {
      const summaries = page.locator('details > summary');
      const count = await summaries.count();
      assert(count > 0, 'No disclosure controls found');
      for (let i = 0; i < count; i++) {
        const summary = summaries.nth(i);
        await summary.focus();
        await page.keyboard.press('Enter');
        assert(await summary.evaluate(el => el.parentElement.open), `Disclosure ${i + 1} did not open`);
        assert(await summary.evaluate(el => el.parentElement.querySelector('p').getBoundingClientRect().height > 0), `Disclosure ${i + 1} content is not visible`);
        await page.keyboard.press('Space');
        assert(!(await summary.evaluate(el => el.parentElement.open)), `Disclosure ${i + 1} did not close`);
      }
      return { count };
    });

    await check('Overflowing result tables scroll with arrow keys', async () => {
      const regions = page.locator('.table-wrap');
      let overflowing = 0;
      for (let i = 0; i < await regions.count(); i++) {
        const region = regions.nth(i);
        if (await region.evaluate(el => el.scrollWidth > el.clientWidth + 1)) {
          overflowing++;
          await region.focus();
          await page.keyboard.press('ArrowRight');
          await page.waitForFunction(index => document.querySelectorAll('.table-wrap')[index].scrollLeft > 0, i);
          await region.evaluate(el => { el.scrollLeft = 0; });
        }
      }
      return { keyboardScrolledTables: overflowing };
    });

    await check('Citation button copies the actual BibTeX', async () => {
      const expected = (await page.locator('#bibtex').textContent()).trim() + '\n';
      await page.locator('#copy-bibtex').focus();
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => document.querySelector('#copy-status').textContent === 'BibTeX copied.');
      const actual = await page.evaluate(() => navigator.clipboard.readText());
      assert(actual === expected, 'Clipboard text does not match the displayed citation');
      return { copiedCharacters: actual.length, liveStatus: await page.locator('#copy-status').textContent() };
    });

    await check('Local resource links and section anchors resolve', async () => {
      const links = await page.evaluate(() => [...new Set([...document.querySelectorAll('a[href]')].map(a => a.href))].filter(href => {
        const url = new URL(href);
        return url.origin === location.origin && url.pathname.startsWith(location.pathname);
      }));
      const resources = new Set();
      for (const href of links) {
        const url = new URL(href);
        if (url.pathname === new URL(target).pathname && url.hash) {
          assert(await page.evaluate(id => !!document.getElementById(id), decodeURIComponent(url.hash.slice(1))), 'Broken section anchor', href);
        } else { url.hash = ''; resources.add(url.href); }
      }
      const responses = [];
      for (const href of resources) {
        const response = await context.request.get(href);
        responses.push({ url: href, status: response.status() });
        assert(response.ok(), 'Local resource link failed', responses.at(-1));
      }
      return { anchorsAndResources: links.length, responses };
    });

    await check('Reduced-motion preference is respected', async () => {
      const evidence = await page.evaluate(() => ({
        reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
        scrollBehavior: getComputedStyle(document.documentElement).scrollBehavior,
        animated: [...document.querySelectorAll('body *')].filter(el => {
          const style = getComputedStyle(el);
          return style.animationName !== 'none' || style.transitionDuration.split(',').some(duration => parseFloat(duration) > 0);
        }).length
      }));
      assert(evidence.reduced === (configuration.reducedMotion === 'reduce'), 'Browser motion emulation mismatch', evidence);
      if (evidence.reduced) assert(evidence.scrollBehavior === 'auto' && evidence.animated === 0, 'Motion persists with reduced-motion preference', evidence);
      return evidence;
    });

    await check('Expanded qualifications remain within the viewport', async () => {
      await page.locator('details').evaluateAll(elements => elements.forEach(el => { el.open = true; }));
      await screenshot('expanded');
      const measurements = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth }));
      assert(measurements.document <= measurements.viewport + 1 && measurements.body <= measurements.viewport + 1, 'Expanded page overflows horizontally', measurements);
      return measurements;
    });
    await check('No browser errors or failed page resources', async () => {
      assert(!result.consoleErrors.length && !result.pageErrors.length && !result.requestFailures.length && !result.badResponses.length, 'Browser/resource failures recorded', {
        consoleErrors: result.consoleErrors, pageErrors: result.pageErrors, requestFailures: result.requestFailures, badResponses: result.badResponses
      });
      return { consoleErrors: 0, pageErrors: 0, failedRequests: 0, badResponses: 0 };
    });
  } finally {
    if (result.checks.some(check => check.status === 'failed')) await screenshot('failure').catch(() => {});
    result.status = result.checks.some(check => check.status === 'failed') ? 'failed' : 'passed';
    await context.close();
  }
}

(async () => {
  await fsp.mkdir(out, { recursive: true });
  let server, browser;
  try {
    assert(Boolean(options.serve) !== Boolean(options.url), 'Provide exactly one of --serve or --url');
    let siteUrl = options.url;
    if (options.serve) ({ server, url: siteUrl } = await serveSite(options.serve, options['base-path']));
    report.url = siteUrl;
    const expectedFile = options.serve ? path.join(options.serve, 'index.html') : options['expected-file'];
    report.expectedHtmlSha256 = hash(await fsp.readFile(expectedFile, 'utf8'));
    const target = await awaitPublishedContent(siteUrl, report.expectedHtmlSha256);
    report.testedUrl = target;
    browser = await chromium.launch({ headless: true });
    report.browser = browser.version();
    for (const configuration of [
      { name: 'desktop', width: 1440, colorScheme: 'light', reducedMotion: 'no-preference' },
      { name: 'mobile-390', width: 390, colorScheme: 'light', reducedMotion: 'no-preference' },
      { name: 'mobile-320', width: 320, colorScheme: 'light', reducedMotion: 'no-preference' },
      { name: 'desktop-dark-reduced-motion', width: 1440, colorScheme: 'dark', reducedMotion: 'reduce' }
    ]) await runCase(browser, target, configuration);
    report.status = report.cases.every(test => test.status === 'passed') ? 'passed' : 'failed';
  } catch (error) { report.status = 'failed'; report.fatalError = error.stack; }
  finally {
    if (browser) await browser.close();
    if (server) await new Promise(resolve => server.close(resolve));
    report.finishedAt = new Date().toISOString();
    await fsp.writeFile(path.join(out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify({ status: report.status, url: report.url, cases: report.cases.map(test => ({ name: test.name, status: test.status, failed: test.checks.filter(check => check.status === 'failed') })), fatalError: report.fatalError, report: path.join(out, 'report.json') }, null, 2));
    if (report.status !== 'passed') process.exitCode = 1;
  }
})();
