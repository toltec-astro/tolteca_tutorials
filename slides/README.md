# Slide toolchain

All decks in `architecture/`, `presentations/` and `workshops/` build with this
toolchain: Markdown sources with the shared Marp theme. The toolchain uses
**Marp Core 5.0.2** (a prerelease, accepted by the maintainer on 2026-10-04) and
Marp CLI, pinned in `package.json` and `package-lock.json`.

| File | Purpose |
| --- | --- |
| `themes/` | Shared typography, tables, code and trees |
| `marp.config.mjs` | Renderer and theme registration |
| `build-all.mjs` | Builds every deck |
| `index.html` | Deck index with HTML, PDF, source and evidence links |
| `preview.py` | Local preview server |

Exports go to `../_build/slides/<collection>/<deck>.{html,pdf}`.

- Marp Core 5 renders Mermaid into vector diagrams in HTML and PDF. Keep literal
  data-tree paths in editable monospace trees; use Mermaid for data flow and
  relationships. The renderer supports a Mermaid subset: check a diagram type
  before you use it (no Gantt or timeline; use generated SVG for those).
- Do not replace the Core 5 engine with stable v4 or a separate diagram
  pipeline without a decision.
- Use the framework's navigation, overview, presenter mode and deep links
  instead of custom controls.

References: [Marp Core v5 announcement](https://github.com/orgs/marp-team/discussions/625),
[releases](https://github.com/marp-team/marp-core/releases),
[v5 Markdown features](https://github.com/marp-team/marp-core/blob/v5.0.0/docs/markdown.md),
[Marp CLI](https://github.com/marp-team/marp-cli).
