import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, dirname, resolve, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const here = dirname(fileURLToPath(import.meta.url));
const cli = resolve(here, '../../slides/node_modules/@marp-team/marp-cli/marp-cli.js');
const source = resolve(here, 'tolteca-v3-overview');
// Exports go beside the source unless --output DIR names another directory.
const option = process.argv.indexOf('--output');
const out = option === -1 ? here : resolve(process.argv[option + 1]);
mkdirSync(out, {recursive: true});
const stem = resolve(out, basename(source));
execFileSync('python3', [resolve(here, 'diagrams.py')], {stdio:['ignore', 'inherit', 'inherit']});
const common = ['--config-file', resolve(here, 'marp.config.mjs'), `${source}.md`];
execFileSync(process.execPath, [cli, ...common, '-o', `${stem}.html`], {stdio:['ignore', 'inherit', 'inherit']});
// Embed the local images so the exported HTML travels as one offline file.
let html = readFileSync(`${stem}.html`, 'utf8');
html = html.replace(/src="(assets\/[^"?#]+)"/g, (_, path) => {
  const mime = {'.svg':'image/svg+xml', '.jpg':'image/jpeg', '.png':'image/png'}[extname(path)];
  if (!mime) throw new Error(`Unsupported slide image: ${path}`);
  return `src="data:${mime};base64,${readFileSync(resolve(here, path)).toString('base64')}"`;
});
writeFileSync(`${stem}.html`, html);
if (process.argv.includes('--pdf')) {
  execFileSync(process.execPath, [cli, ...common, '--pdf', '--allow-local-files', '-o', `${stem}.pdf`], {stdio:['ignore', 'inherit', 'inherit']});
}
