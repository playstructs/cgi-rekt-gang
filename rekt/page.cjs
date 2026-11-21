// Renders structs-webapp's game page (templates/game/index.html.twig on
// templates/base.html.twig) to static HTML, with the Rekt Gang overlay applied.
//
// Only what those two templates use is understood: blocks, comments and the
// webpack asset() call. Anything else Twig-shaped stops the build, so a
// template change upstream is noticed rather than shipped half-rendered.
const fs = require('node:fs');
const path = require('node:path');
const {UPSTREAM_SRC, patch} = require('./overlay.cjs');

const BASE = 'templates/base.html.twig';
const GAME = 'templates/game/index.html.twig';
const BLOCK = /{%\s*block\s+(\w+)\s*%}([\s\S]*?){%\s*endblock\s*%}/g;

const HEAD = `<meta name="description" content="Rekt Gang's Structs guild: Rekt Today, Stronger Tomorrow.">
        <link rel="icon" href="/favicon.ico" sizes="48x48">
        <link rel="icon" type="image/png" href="/rekt/img/favicon-32x32.png" sizes="32x32">
        <link rel="apple-touch-icon" href="/rekt/img/apple-touch-icon.png">
        <link rel="stylesheet" href="/rekt/rekt.css">
    </head>`;

function read(rel, stale) {
  const result = patch(rel, fs.readFileSync(path.join(UPSTREAM_SRC, rel), 'utf8'));
  result.stale.forEach(text => stale.push(`${rel} no longer contains ${JSON.stringify(text)}`));
  return result.code.replace(/{#[\s\S]*?#}/g, '');
}

/**
 * @param {string} indexBundle the built entry, relative to the site root
 * @return {{html: string, stale: string[], dependencies: string[]}}
 */
function renderPage(indexBundle) {
  const stale = [];
  const child = read(GAME, stale);
  const blocks = {};
  for (const [, name, body] of child.matchAll(BLOCK)) {
    blocks[name] = body;
  }

  let html = read(BASE, stale)
    .replace(BLOCK, (match, name, fallback) => blocks[name] ?? fallback)
    .replace(/{{\s*asset\('js\/index\.js',\s*'webpack'\)\s*}}/g, '/' + indexBundle)
    .replace('</head>', HEAD);

  const leftover = html.match(/{[{%][\s\S]*?[}%]}/);
  if (leftover) {
    throw new Error(`rekt: page: unrendered Twig ${JSON.stringify(leftover[0])}`);
  }

  const dependencies = [BASE, GAME].map(rel => path.join(UPSTREAM_SRC, rel));
  return {html, stale, dependencies};
}

module.exports = {renderPage};
