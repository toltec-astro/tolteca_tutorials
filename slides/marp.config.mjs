import { Marp } from '@marp-team/marp-core/full';

function localDiagramFonts(md) {
  const render = md.renderer.rules.marp_mermaid;
  // beautiful-mermaid 1.1.3 embeds Google Fonts imports in every SVG.
  // Keep the native Marp renderer, but use the theme's local font stack.
  md.renderer.rules.marp_mermaid = (...args) => render(...args)
    .replace(/@import url\('https:\/\/fonts\.googleapis\.com\/[^']*'\);/g, '')
    .replace(/'Inter', system-ui, sans-serif/g, 'Arial, Helvetica, sans-serif')
    .replace(/'JetBrains Mono', /g, '');
}

export default {
  engine: (options) => new Marp(options).use(localDiagramFonts),
  themeSet: './themes',
  html: true,
  bespoke: { progress: true },
};
