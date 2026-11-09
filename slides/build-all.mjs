// Build every architecture deck, the teaching presentations and the deck index.
// HTML (and PDF with --pdf) go to ../_build/slides/, or to --output DIR;
// sources stay unchanged.
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const tooling = path.dirname(fileURLToPath(import.meta.url));
const tutorials = path.resolve(tooling, '..');
const architecture = path.join(tutorials, 'architecture');
const option = process.argv.indexOf('--output');
const root = option === -1
  ? path.join(tutorials, '_build/slides')
  : path.resolve(process.argv[option + 1]);
const output = path.join(root, 'architecture');
const pdf = process.argv.includes('--pdf');
const marp = path.join(tooling, 'node_modules/.bin/marp');

function run(command, args, options) {
  // Marp reads Markdown from stdin when stdin is not a terminal; ignore it.
  const result = spawnSync(command, args, { stdio: ['ignore', 'inherit', 'inherit'], ...options });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}

mkdirSync(output, { recursive: true });
const decks = readdirSync(architecture, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .map((entry) => path.join(architecture, entry.name, `${entry.name}.md`))
  .filter((source) => existsSync(source))
  .sort();
for (const source of decks) {
  const stem = path.basename(source, '.md');
  const common = ['--config-file', 'marp.config.mjs', source];
  run(marp, [...common, '-o', path.join(output, `${stem}.html`)], { cwd: tooling });
  if (pdf) {
    run(marp, [...common, '--pdf', '--allow-local-files', '-o', path.join(output, `${stem}.pdf`)],
      { cwd: tooling });
  }
}
run(process.execPath, [
  path.join(tutorials, 'presentations/tolteca-v3-overview/build.mjs'),
  '--output', path.join(root, 'presentations'),
  ...(pdf ? ['--pdf'] : []),
]);
copyFileSync(path.join(tooling, 'index.html'), path.join(root, 'index.html'));
