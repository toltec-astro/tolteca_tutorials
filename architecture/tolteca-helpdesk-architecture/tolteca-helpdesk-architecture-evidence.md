# Helpdesk architecture deck evidence

> Moved on 2026-11-07 from `tolteca_helpdesk/design/` to `tolteca_tutorials/architecture/tolteca-helpdesk-architecture/`.
> Commands below record earlier runs with the old paths. Today, run this
> deck's probes from `architecture/tolteca-helpdesk-architecture/probes/` and build from `slides/`.

## Scope and inspected state

The [deck](tolteca-helpdesk-architecture.md) presents the current implementation
of `tolteca_dr`, `tolteca_helpdesk` and `tolteca_agent`. It follows
[the specification](../../../tolteca_helpdesk/design/spec.md). Inspected implementation: commit `c35fa0a`, plus
the accompanying documentation and deck changes, on 2026-10-19. The
implementation commit is deployed on Unity. The presentation does not certify
production answer quality.

Slide 9 was subsequently updated from baseline `b1bec40` plus the accompanying
optimization changes. The
[optimization evaluation](../../../tolteca_helpdesk/design/helpdesk-optimization-20261019.md) records FAQ
routing, the retained fuller context and the default review of every generated
answer. The original verification record below is historical. The changed slide
was rebuilt as HTML and PDF and visually checked at 1280 × 720; the other slide
layouts were retained.

## Claims and owning evidence

| Slides                          | Contract or implementation source                                                                 |
| ------------------------------- | ------------------------------------------------------------------------------------------------- |
| 3–5: workflows and ownership    | `src/tolteca_agent/material.py`, `data/use_cases/`, `data/learning.md`, `pyproject.toml`          |
| 6–8: sources and retrieval      | `src/tolteca_agent/sources.py`, `catalog.py`, `data/package-guides.json`, `tests/test_catalog.py` |
| 9–10: answers and conversations | `src/tolteca_helpdesk/answers.py`, `src/tolteca_dr/chat.py`, `tests/test_services.py`             |
| 11: agent interfaces            | `src/tolteca_agent/cli/`, `http.py`, `mcp.py`                                                     |
| 12–13: deployment and modes     | `deploy/`, `src/tolteca_dr/config.py`, `web.py`, `src/tolteca_helpdesk/config.py`                 |
| 14: limitations                 | [Answer validation record](../../../tolteca_helpdesk/design/helpdesk-validation-20261019.md) and package-owned planning/QA guides  |

One catalog supports different retrieval policies. The science human context
filter does not restrict the document HTTP API. An enabled review uses the same
provider model; reference validation does not establish semantic accuracy. The
deployment diagram distinguishes request direction from the Mac-initiated SSH
connection. These boundaries must remain visible in later revisions.

## Reproduction

From the repository in the activated v3 location environment:

```sh
python design/probes/helpdesk_architecture.py
node design/slides/build.mjs
node design/slides/build.mjs --pdf
```

The wrapper uses the sibling `tolteca/design/slides` toolchain: Marp CLI 4.5.1,
Marp Core 5.0.2 and the `kids-review` theme. The shared renderer removes remote
font imports from its integrated Mermaid output. Generated exports stay local;
source, probe, build wrapper and this evidence note are tracked.

## Verification record

The final package QA passed 52 behavioral tests, two documentation examples and
a strict Sphinx build. The public science portal completed a browser question
through Apache and Unity to the Mac provider and returned the planning guide
citation. A separate Unity CLI request returned the PSD guide's units and
segment default through the same tunnel.

The displayed Python, YAML and CLI examples ran without inference. All 14 PDF
pages were rendered with Poppler and visually inspected at 1280 × 720. All 14
HTML slides were inspected at 960 × 600; no content required scrolling or was
clipped. DOM bounds were 1280 × 720 for every slide. Keyboard movement, contents
links, deep links and overview worked in the browser. The presenter view
rendered slide notes; its popup shortcut did not open a new tab in the in-app
browser, so the framework's explicit presenter URL was checked.

The HTML has no external script, stylesheet or image dependencies. Direct
`file:` navigation is blocked by the inspection browser, so offline reopening
was not verified. The HTML was tested through the local HTTP preview server.

The separate validation record preserves unresolved command-answer failures;
slide claims must not imply that these have been corrected.

## Reading assistant update (2026-11-08)

The deck now presents the reading-only assistant that replaced generated
answers on 2026-10-20 (helpdesk spec, "Human helpdesk"). The verification
record above describes the earlier generated-answer deck and is historical.

| Slides | Change | Source |
| --- | --- | --- |
| 1, 4 | Subtitle and `tolteca_helpdesk` role: selects existing sections | spec, "Repository and package boundaries" |
| 5 | Handbook and decks owned by `tolteca_tutorials`; `tolteca_dr` publishes guides, handbook and decks | spec, "Purpose and content ownership", "Published package documentation" |
| 9 | "Reading suggestions" replaces "Human answer path": FAQ match, or Llama selects up to three section IDs; no generated text, no review | `tolteca_helpdesk.answers.ask`, `reading.py`; [reading change record](../../../tolteca_helpdesk/design/helpdesk-reading-20261020.md) |
| 10 | Launcher and drawer labels; only recent questions inform follow-ups; cards checked against the catalog | `tolteca_dr/chat.py`, `web.py`; spec, "Chat session" |
| 13 | Production row names the reading assistant | `tolteca_dr/web.py` |
| 14 | Reading relevance replaces command accuracy; shared account access not yet deployed | reading change record; spec, "Shared account access" |

Slides 6–8 and 11–12 were checked against `tolteca_agent.sources.Source`,
`catalog.Passage` and the spec and are unchanged. Inspected state:
`tolteca_helpdesk` HEAD `2b95902` with uncommitted changes (Claude's
documentation publication; Codex's shared account access).

Checks: `probes/helpdesk_architecture.py` runs the displayed Python, YAML and
CLI examples and passes with the development location's Python. The deck was
rebuilt with `slides/build-all.mjs`; see the boundary task record for the
rendered review.
