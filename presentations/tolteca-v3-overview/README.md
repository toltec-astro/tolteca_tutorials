# TolTECA v3 overview

A 20-minute overview for TolTEC instrument and software developers, observers,
and data product curators. Sixteen slides connect data handling, execution,
products, and the developing science and operations helpdesk. Most slides use
diagrams; three show working interfaces and one includes a generated quicklook
plot.

## Present

- [HTML deck](tolteca-v3-overview.html): self-contained export, with embedded
  images and navigation. Open the file in a browser or use the local preview.
- [PDF](tolteca-v3-overview.pdf): static fallback.
- [Editable source](tolteca-v3-overview.md): slide content and speaker notes.
- [Evidence](tolteca-v3-overview-evidence.md): source references, screenshot
  provenance, verification and limits.

Use the arrow keys to move, `o` for the overview, `p` for presenter view, and `f`
for fullscreen. The final slide has topic links for questions. Each slide also
has a numbered URL fragment, such as `#14` for the helpdesk. Some embedded
browsers block the separate presenter window; open the HTML in a regular browser
or use the `?view=presenter` address.

## Timing

The notes total 19½ minutes, leaving brief transitions within a 20-minute slot.

| Slides | Subject | Minutes |
| --- | --- | ---: |
| 1–3 | Lifecycle and run modes | 3 |
| 4–6 | Data structure, KIDs processing and inspection | 3.75 |
| 7–8 | Live observing workflow and the MC quicklook API | 2.25 |
| 9–11 | Runs, calibration and Taco–Unity inventories | 4.25 |
| 12–13 | Slurm execution and run supervision | 2.5 |
| 14–15 | Helpdesk, portals and software assistants | 2.5 |
| 16 | Current scope | 1.25 |

## Build and preview

From this repository, with the shared slide tooling installed:

```console
node presentations/tolteca-v3-overview/build.mjs --pdf
```

This writes the HTML and PDF beside the source. `node slides/build-all.mjs`
writes them into `_build/slides/presentations/` with the other decks, and
`python3 slides/preview.py` serves that build at
<http://127.0.0.1:8951/index.html>. Add `--output DIR` to `build.mjs` to write
the exports elsewhere.

The build reuses Marp CLI 4.5.1 and Marp Core 5.0.2 from `slides/node_modules`.
Install the shared locked dependencies with `npm ci --prefix slides` when
needed. PDF generation requires the
browser supported by Marp. No model, running application service or external
font is needed to view the exported deck.

`diagrams.py` generates the editable SVG assets. `theme.css` defines the
presentation layout separately from content. `assets/` retains original browser
captures and the generated quicklook PNG. HTML/PDF exports and `.qa/` stay local;
publish them with the reviewed source revision. Screenshots are a dated example,
not a live status display.

## Further detail

The [architecture index](../../architecture/README.md) links the
domain decks for input discovery, KIDs, product publication, associations,
operational workflows, deployment and telescope files. The
[helpdesk specification](../../../tolteca_helpdesk/design/spec.md) owns portal,
human assistance and agent-access boundaries. The tutorials
[workflow collection](../../workflows/README.md) owns runnable teaching material.
