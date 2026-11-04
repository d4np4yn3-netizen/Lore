import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';

const buildDir = new URL('../.next/server/app/', import.meta.url);
const attributes = source => Object.fromEntries([...source.matchAll(/([\w:-]+)="([^"]*)"/g)].map(match => [match[1], match[2]]));
function htmlFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? htmlFiles(file) : entry.name.endsWith('.html') ? [file] : [];
  });
}
const files = htmlFiles(buildDir.pathname);
const pages = files.map(file => ({ file, html: fs.readFileSync(file, 'utf8') })).filter(page => page.html.includes('class="site-footer"'));

test('every shared footer includes one accessible link to the confirmed HISTROVE profile', () => {
  assert(pages.length > 4, 'Expected shared footer on the main routes and card pages');
  for (const { file, html } of pages) {
    const footer = html.match(/<footer\b[^>]*class="site-footer"[^>]*>(.*?)<\/footer>/s)?.[1];
    const links = [...footer.matchAll(/<a\b([^>]*)>(.*?)<\/a>/gs)].map(match => ({ ...attributes(match[1]), content: match[2] }));
    const social = links.filter(link => link.href === 'https://x.com/Histrove');
    assert.equal(social.length, 1, file);
    assert.equal(social[0]['aria-label'], 'Follow @Histrove on X (opens in a new tab)', file);
    assert(social[0].content.includes('@Histrove on X'), file);
    assert.equal(social[0].target, '_blank', file);
    assert.deepEqual(new Set(social[0].rel.split(' ')), new Set(['noopener', 'noreferrer']), file);
    assert(links.some(link => link.href === 'mailto:hello@histrove.co.uk'), file);
    assert(links.some(link => link.href === '#top'), file);
  }
});

test('main pages keep the shared footer and existing focus/target-size treatment', () => {
  for (const route of ['index.html', 'timeline.html', 'shop.html', 'season-two.html']) {
    assert(pages.some(page => page.file === path.join(buildDir.pathname, route)), route);
  }
  const source = fs.readFileSync(new URL('../app/components/SiteChrome.js', import.meta.url), 'utf8');
  assert(source.includes('className="footer-contact footer-social"'));
  const css = fs.readFileSync(new URL('../app/globals.css', import.meta.url), 'utf8');
  assert.match(css, /\.footer-right \.footer-contact\{[^}]*min-height:44px/);
  assert.match(css, /a:focus-visible[^}]*outline:2px solid var\(--gold\)/);
});

console.log(`Checked social footer across ${pages.length} rendered pages.`);
