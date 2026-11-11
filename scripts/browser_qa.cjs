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
  'report-dir': { type: 'string', default: '.qa-tmp/browser' },
  'emit-preview': { type: 'boolean', default: false }
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
  let officialTrajectoryGeometry;
  page.setDefaultTimeout(15000);
  page.on('console', message => { if (message.type() === 'error') result.consoleErrors.push(message.text()); });
  page.on('pageerror', error => result.pageErrors.push(error.message));
  page.on('requestfailed', req => result.requestFailures.push({ url: req.url(), error: req.failure()?.errorText }));
  page.on('response', response => { if (response.status() >= 400) result.badResponses.push({ url: response.url(), status: response.status() }); });
  async function check(name, operation) {
    try { const evidence = await operation(); result.checks.push({ name, status: 'passed', evidence }); return true; }
    catch (error) { result.checks.push({ name, status: 'failed', error: error.message, ...(error.diagnostics ? { diagnostics: error.diagnostics } : {}) }); return false; }
  }
  async function navigationState(selector) {
    return page.evaluate(selector => {
      const target = document.querySelector(selector);
      const active = document.activeElement;
      const rect = element => {
        if (!element) return null;
        const box = element.getBoundingClientRect();
        return { top: box.top, right: box.right, bottom: box.bottom, left: box.left, width: box.width, height: box.height };
      };
      const targetRect = rect(target);
      const targetStyle = target && getComputedStyle(target);
      return {
        selector, hash: location.hash, scrollX, scrollY, viewport: { width: innerWidth, height: innerHeight },
        targetText: target?.textContent.trim().slice(0, 160), targetRect,
        targetVisible: !!targetRect && targetRect.width > 0 && targetRect.height > 0 &&
          targetRect.top >= -1 && targetRect.left >= -1 && targetRect.bottom <= innerHeight + 1 && targetRect.right <= innerWidth + 1 &&
          targetStyle.display !== 'none' && targetStyle.visibility !== 'hidden',
        targetFocused: target === active,
        active: active ? { tag: active.tagName, id: active.id, class: active.className, href: active.getAttribute('href'), text: active.textContent.trim().slice(0, 160), rect: rect(active), withinMain: !!active.closest('main') } : null
      };
    }, selector);
  }
  async function waitForNavigationSettled(phase, selector, requirements = {}) {
    // A heading can enter the viewport before smooth scrolling ends. Require
    // stable geometry before the next key/focus event can start another scroll.
    const started = Date.now();
    let previousGeometry, stableSince = started;
    const recentSamples = [];
    while (Date.now() - started < 15000) {
      const state = await navigationState(selector);
      const geometry = JSON.stringify([state.scrollX, state.scrollY, state.viewport, state.targetRect]);
      const matches = (!requirements.hash || state.hash === requirements.hash) &&
        (!requirements.visible || state.targetVisible) && (!requirements.focused || state.targetFocused);
      if (geometry !== previousGeometry || !matches) stableSince = Date.now();
      previousGeometry = geometry;
      recentSamples.push({ elapsedMs: Date.now() - started, ...state });
      if (recentSamples.length > 8) recentSamples.shift();
      if (matches && Date.now() - stableSince >= 250) return { phase, settledForMs: Date.now() - stableSince, ...state };
      await delay(50);
    }
    const error = new Error(`Keyboard navigation did not settle during: ${phase}`);
    error.diagnostics = { phase, requirements, recentSamples };
    throw error;
  }
  async function screenshot(suffix) {
    const filename = `${configuration.name}-${suffix}.png`;
    await page.screenshot({ path: path.join(out, filename), fullPage: true });
    result.screenshots.push(filename);
    // Public-page previews can be inspected through Actions logs when artifact
    // downloads are unavailable to a reviewer. No browser storage is captured.
    if (options['emit-preview'] && suffix === 'initial' && ['desktop', 'mobile-390'].includes(configuration.name)) {
      const previewName = `${configuration.name}-preview.jpg`;
      const bytes = await page.screenshot({ path: path.join(out, previewName), fullPage: true, type: 'jpeg', quality: 55 });
      const encoded = bytes.toString('base64');
      for (let offset = 0; offset < encoded.length; offset += 4096) console.log(`FEOC_PREVIEW ${previewName} ${offset / 4096} ${encoded.slice(offset, offset + 4096)}`);
    }
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

    await check('Paper button and UCLA logo are present', async () => {
      const evidence = await page.evaluate(() => ({
        paperLinks: [...document.querySelectorAll('.buttons a')].filter(link => /^Paper(?:\s|$)/.test(link.textContent.trim())).map(link => ({ text: link.textContent.trim(), href: link.href })),
        uclaImages: [...document.images].filter(img => /ucla/i.test(img.getAttribute('src') + ' ' + img.alt) || /University of California,?\s+Los Angeles/i.test(img.alt))
          .map(img => ({ src: img.getAttribute('src'), alt: img.alt, complete: img.complete, width: img.naturalWidth, height: img.naturalHeight }))
      }));
      assert(evidence.paperLinks.length === 1 && evidence.paperLinks[0].href === 'https://ieeexplore.ieee.org/document/11615530', 'Paper button does not target the publication record', evidence.paperLinks);
      assert(evidence.uclaImages.length > 0 && evidence.uclaImages.every(img => img.complete && img.width > 0 && img.height > 0), 'UCLA logo is missing or failed to decode', evidence.uclaImages);
      return evidence;
    });

    await check('Graphical abstract is the exact official SOLARIS asset', async () => {
      const abstract = page.locator('#solaris-abstract');
      assert(await abstract.count() === 1, 'Official graphical abstract is missing');
      const evidence = await abstract.evaluate(wrapper => {
        const svg = wrapper.querySelector(':scope > svg');
        return { svgCount: wrapper.querySelectorAll('svg').length, designSystem: svg?.getAttribute('data-design-system'), viewBox: svg?.getAttribute('viewBox'), trajectoryPresent: !!svg?.querySelector('#v9-policyfe-trajectory0'), url: new URL('assets/figures/graphical-abstract.svg', location.href).href };
      });
      assert(evidence.svgCount === 1 && evidence.designSystem === 'solaris-v9' && evidence.viewBox === '0 0 760 392' && evidence.trajectoryPresent, 'Inline graphic does not retain the official SOLARIS structure', evidence);
      assert(await page.locator('#feoc-abstract').count() === 0, 'Replacement diagram remains instead of the official abstract');
      const response = await context.request.get(evidence.url);
      assert(response.ok(), 'Official SVG request failed', response.status());
      const bytes = await response.body();
      evidence.gitBlobSha1 = crypto.createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${bytes.length}\0`), bytes])).digest('hex');
      assert(evidence.gitBlobSha1 === 'a5d6c72b02d5b6f9756fc7ec97e15efe62d893fb', 'Served graphical abstract differs from the official SOLARIS file', evidence.gitBlobSha1);
      officialTrajectoryGeometry = await page.evaluate(source => {
        const svg = new DOMParser().parseFromString(source, 'image/svg+xml');
        const paths = [...svg.querySelectorAll('[id^="v9-policyfe-trajectory"]')].map(path => ({ id: path.id, d: path.getAttribute('d') }));
        const tips = [...svg.querySelectorAll('[id^="v9-policyfe-tip"]')].map(tip => ({ id: tip.id, cx: tip.getAttribute('cx'), cy: tip.getAttribute('cy') }));
        return JSON.stringify({ paths, tips });
      }, bytes.toString('utf8'));
      return evidence;
    });

    await check('Feedback diagram equations are typeset with KaTeX', async () => {
      const evidence = await page.evaluate(() => {
        const diagram = document.querySelector('.feedback-diagram');
        const equations = [...(diagram?.querySelectorAll('[data-tex]') || [])].map(element => ({
          tex: element.dataset.tex, rendered: !!element.querySelector(':scope > .katex .katex-html'),
          errors: element.querySelectorAll('.katex-error').length,
          rawDirectText: [...element.childNodes].filter(node => node.nodeType === Node.TEXT_NODE).map(node => node.textContent).join('').trim()
        }));
        const rawText = [];
        if (diagram) {
          const walker = document.createTreeWalker(diagram, NodeFilter.SHOW_TEXT);
          while (walker.nextNode()) {
            const node = walker.currentNode;
            if (!node.parentElement.closest('.katex') && /\\(?:mathbf|phi|sum|dot|boldsymbol|theta|eta)\b/.test(node.textContent)) rawText.push(node.textContent.trim());
          }
        }
        return { equations, rawText };
      });
      assert(evidence.equations.length === 7 && evidence.equations.every(equation => equation.tex && equation.rendered && !equation.errors && !equation.rawDirectText), 'Feedback equations are missing or not rendered', evidence.equations);
      assert(evidence.rawText.length === 0, 'Raw LaTeX appears outside rendered math', evidence.rawText);
      return evidence;
    });

    await check('No page-wide horizontal overflow', async () => {
      const measurements = await page.evaluate(() => ({
        viewport: innerWidth, document: document.documentElement.scrollWidth, body: document.body.scrollWidth,
        scrollRegions: [...document.querySelectorAll('.math, .table-wrap, .figure-link, .abstract-scroll, .feedback-scroll, pre')].map(el => ({ class: el.className || el.tagName, width: el.clientWidth, contentWidth: el.scrollWidth, overflowX: getComputedStyle(el).overflowX }))
      }));
      assert(measurements.document <= measurements.viewport + 1 && measurements.body <= measurements.viewport + 1, 'Page overflows horizontally', measurements);
      assert(measurements.scrollRegions.every(el => el.contentWidth <= el.width + 1 || ['auto', 'scroll'].includes(el.overflowX)), 'Wide content cannot be scrolled', measurements.scrollRegions);
      return measurements;
    });
    await check('Capture initial layout', () => screenshot('initial'));

    await check('Skip link and section links work from the keyboard', async () => {
      const phases = [];
      try {
        phases.push(await waitForNavigationSettled('Initial viewport', 'h1', { visible: true }));
        await page.keyboard.press('Tab');
        const skip = await navigationState('.skip');
        phases.push({ phase: 'First Tab reaches skip link', ...skip });
        assert(skip.targetFocused, 'Skip link is not first in keyboard order', skip);
        assert(skip.targetVisible, 'Focused skip link is clipped', skip);
        await page.keyboard.press('Enter');
        phases.push(await waitForNavigationSettled('Skip link reaches research heading', '#overview h2', { hash: '#overview', visible: true }));
        await page.keyboard.press('Tab');
        const contentFocus = await waitForNavigationSettled('Tab after skip link', '#overview h2', { hash: '#overview' });
        phases.push(contentFocus);
        assert(contentFocus.active?.withinMain, 'Tab navigation did not move into the research content after skipping', contentFocus);
        const resultsLink = page.getByRole('navigation', { name: 'Page sections' }).getByRole('link', { name: 'Results', exact: true });
        await resultsLink.focus();
        phases.push(await waitForNavigationSettled('Results link receives focus', '.section-nav a[href="#results"]', { visible: true, focused: true }));
        const focusStyle = await resultsLink.evaluate(el => ({ style: getComputedStyle(el).outlineStyle, width: getComputedStyle(el).outlineWidth }));
        assert(focusStyle.style !== 'none' && parseFloat(focusStyle.width) > 0, 'Keyboard focus indicator is missing', focusStyle);
        await page.keyboard.press('Enter');
        phases.push(await waitForNavigationSettled('Results link reaches results heading', '#results h2', { hash: '#results', visible: true }));
        return { skipTarget: '#overview', sectionTarget: '#results', focusStyle, phases };
      } catch (error) {
        error.diagnostics = { phases, failure: error.diagnostics || null, overview: await navigationState('#overview h2'), results: await navigationState('#results h2') };
        throw error;
      }
    });

    await check('UCLA logo shares the muted institution style and reveals color on interaction', async () => {
      await page.mouse.move(0, 0);
      const logos = await page.locator('.logos img').evaluateAll(images => images.map((image, index) => ({ index, src: image.getAttribute('src'), alt: image.alt, filter: getComputedStyle(image).filter })));
      const ucla = logos.find(logo => /ucla/i.test(logo.src + ' ' + logo.alt));
      assert(ucla && logos.length > 1, 'Institution logo group is incomplete', logos);
      assert(ucla.filter !== 'none' && logos.every(logo => logo.filter === ucla.filter), 'UCLA does not match the other muted institution logos', logos);
      const image = page.locator('.logos img').nth(ucla.index);
      const link = image.locator('..');
      assert(await link.evaluate(element => element.tagName === 'A'), 'UCLA logo is not inside its institutional link');
      await image.hover();
      await page.waitForFunction(index => getComputedStyle(document.querySelectorAll('.logos img')[index]).filter === 'none', ucla.index);
      const hoverFilter = await image.evaluate(element => getComputedStyle(element).filter);
      await page.mouse.move(0, 0);
      await page.waitForFunction(({ index, filter }) => getComputedStyle(document.querySelectorAll('.logos img')[index]).filter === filter, { index: ucla.index, filter: ucla.filter });
      await link.focus();
      // An actual keyboard round trip activates :focus-visible after hovering.
      await page.keyboard.press('Tab');
      await page.keyboard.press('Shift+Tab');
      assert(await link.evaluate(element => element === document.activeElement), 'Keyboard navigation did not return to the UCLA link');
      await page.waitForFunction(index => getComputedStyle(document.querySelectorAll('.logos img')[index]).filter === 'none', ucla.index);
      const focusFilter = await image.evaluate(element => getComputedStyle(element).filter);
      await page.keyboard.press('Tab');
      await page.waitForFunction(({ index, filter }) => getComputedStyle(document.querySelectorAll('.logos img')[index]).filter === filter, { index: ucla.index, filter: ucla.filter });
      return { logosAtRest: logos, hoverFilter, focusFilter };
    });

    await check('Official abstract trajectories pause and resume through the keyboard', async () => {
      const button = page.locator('#toggle-abstract');
      assert(await button.count() === 1, 'Graphical abstract playback control is missing');
      const sample = () => page.evaluate(() => {
        const wrapper = document.querySelector('#solaris-abstract');
        const control = document.querySelector('#toggle-abstract');
        const paths = [...wrapper.querySelectorAll('[id^="v9-policyfe-trajectory"]')].map(path => ({ id: path.id, d: path.getAttribute('d') }));
        const tips = [...wrapper.querySelectorAll('[id^="v9-policyfe-tip"]')].map(tip => ({ id: tip.id, cx: tip.getAttribute('cx'), cy: tip.getAttribute('cy') }));
        return { paused: wrapper.dataset.paused, disabled: control.disabled, text: control.textContent.trim(), pressed: control.getAttribute('aria-pressed'), paths, tips, geometry: JSON.stringify({ paths, tips }) };
      });
      const compact = state => ({ paused: state.paused, disabled: state.disabled, text: state.text, pressed: state.pressed, paths: state.paths.map(path => ({ id: path.id, characters: path.d?.length || 0 })), tips: state.tips, geometrySha256: hash(state.geometry) });
      async function waitForGeometryChange(phase, before) {
        const started = Date.now();
        let current;
        while (Date.now() - started < 15000) {
          current = await sample();
          if (current.geometry !== before.geometry) return current;
          await delay(100);
        }
        assert(false, `Official trajectory geometry did not change during ${phase}`, { before: compact(before), after: compact(current) });
      }
      const initial = await sample();
      assert(initial.paths.length === 3 && initial.tips.length === 3 && initial.paths.every(path => path.d), 'Official trajectory paths or tips are missing', compact(initial));
      if (configuration.reducedMotion === 'reduce') {
        assert(initial.disabled && initial.paused === 'true' && initial.pressed === 'true', 'Reduced motion must disable playback and retain a static figure', compact(initial));
        assert(initial.geometry === officialTrajectoryGeometry, 'Reduced motion does not preserve the original SVG trajectory geometry', compact(initial));
        await delay(300);
        const after = await sample();
        assert(after.geometry === initial.geometry, 'Official trajectories move with reduced motion enabled', { before: compact(initial), after: compact(after) });
        return { initial: compact(initial), after: compact(after), reducedMotion: true };
      }
      assert(!initial.disabled && initial.paused === 'false' && initial.text === 'Pause animation' && initial.pressed === 'false', 'Playback control state is inconsistent', compact(initial));
      const running = await waitForGeometryChange('playback', initial);
      await button.focus();
      await waitForNavigationSettled('Official animation control receives focus', '#toggle-abstract', { visible: true, focused: true });
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => document.querySelector('#solaris-abstract').dataset.paused === 'true');
      await delay(100);
      const paused = await sample();
      assert(paused.text === 'Play animation' && paused.pressed === 'true', 'Paused control label or pressed state is incorrect', compact(paused));
      await delay(300);
      const held = await sample();
      assert(held.geometry === paused.geometry, 'Official trajectories continue changing while paused', { before: compact(paused), after: compact(held) });
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => document.querySelector('#solaris-abstract').dataset.paused === 'false');
      const resumed = await waitForGeometryChange('resumed playback', held);
      assert(resumed.text === 'Pause animation' && resumed.pressed === 'false', 'Resumed control label or pressed state is incorrect', compact(resumed));
      return { initial: compact(initial), running: compact(running), paused: compact(paused), held: compact(held), resumed: compact(resumed) };
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

    await check('Overflowing figures and result tables scroll with arrow keys', async () => {
      const selector = '.table-wrap, .abstract-scroll, .feedback-scroll';
      const regions = page.locator(selector);
      let overflowing = 0;
      for (let i = 0; i < await regions.count(); i++) {
        const region = regions.nth(i);
        if (await region.evaluate(el => el.scrollWidth > el.clientWidth + 1)) {
          overflowing++;
          await region.focus();
          await page.keyboard.press('ArrowRight');
          await page.waitForFunction(({ selector, index }) => document.querySelectorAll(selector)[index].scrollLeft > 0, { selector, index: i });
          await region.evaluate(el => { el.scrollLeft = 0; });
        }
      }
      return { keyboardScrolledRegions: overflowing };
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
