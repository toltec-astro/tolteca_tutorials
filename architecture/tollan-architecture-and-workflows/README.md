# Tollan presentation build

The deck is `tollan-architecture-and-workflows.md`. Its HTML export embeds the
styles, scripts and SVG diagrams. It uses the shared toolchain in
`../../slides/` and its theme `tollan-review` (`../../slides/themes/`), which
follows the architecture-review theme with 22 px code.

## Build

From `../../slides/`:

```sh
npm run build -- ../architecture/tollan-architecture-and-workflows/tollan-architecture-and-workflows.md \
  -o ../_build/slides/architecture/tollan-architecture-and-workflows.html
```

## Preview and controls

Use the shared preview (`npm run preview:all` in `../../slides/`), or open the
exported HTML in `../../_build/slides/architecture/` directly.

- Arrow keys change slides. `o` opens the overview. `p` requests presenter mode.
- The Topics footer returns to the section index. Hashes such as `#8` select a slide.
- If the browser does not open presenter popups, open the deck URL with
  `?view=presenter` before the hash. A separately opened presenter view is usable
  for notes and local navigation; synchronization with another tab is unverified.

## Example checks

Run from the Python workspace root:

```sh
toltec_astro_dev/.venv/bin/python \
  tolteca_tutorials/architecture/tollan-architecture-and-workflows/probes/tollan_architecture_and_workflows.py
```

The probe executes each displayed Python fragment with setup from the public
guides. It checks the displayed CLI command and API-level examples. See the
companion evidence record for the last executed checks and limitations.
