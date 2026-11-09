# Handbook framework comparison

> Moved on 2026-11-08 from `tolteca_helpdesk/design/probes/handbook-frameworks/` with the handbook.
> Recorded commands keep their earlier paths as history.

## Scope and recommendation

Evaluated 2026-10-26 against helpdesk HEAD `fffcf5c`. This experiment compares
Sphinx with MyST Parser and PyData against the MyST engine used by Jupyter
Book 2. It does not migrate the existing handbook, move the terminology draft,
change the portal, or publish to Unity. The unrelated pending change to
`src/tolteca_agent/data/learning.md` is preserved.

**Recommendation:** use a standalone Sphinx project, authored in MyST Markdown,
with PyData for the HTML reader. Keep its source in a proposed
`toltec_handbook/` directory in this repository, separate from `docs/`, which
documents the helpdesk software. Framework adoption and directory migration
remain proposals pending the user's decision.

The decisive evidence is glossary interoperability and complete PDF output. Both
engines met the tested static-hosting and outbound-reference requirements.
MyST's book interface and structured content exports are useful, but its tested
PDF path lost the glossary. Notebook execution was not evaluated; runnable
analysis recipes remain the responsibility of `tolteca_tutorials`.

## Inputs and controlled differences

- The chapter is adapted from the existing `handbook/products.md`.
- Three definition excerpts come from the current `tolteca/docs/terminology.md`
  draft: observation, acquisition, and calibration item. The acquisition entry
  drops the alternative name from its heading; the calibration item excerpt
  omits implementation-specific status. This is a frozen publishing fixture, not
  a second maintained glossary.
- Both builds use the same table, equation and figure. The figure contains
  explicitly synthetic, dimensionless values solely to test publication layout.
- The outbound link resolves `processed-kids` from the actual published
  `tolteca_web` inventory, version `0.1.dev86+g9db03d847.d20261016`. A local
  copy of the publication is served for this test; no package repository is
  edited.
- Sphinx and MyST use their respective glossary definition syntax and external
  reference syntax. The reading text is otherwise shared.
- Sphinx uses a small sidebar template to show all chapters. PyData's default
  sidebar starts below the selected top-level section. No custom CSS was added.

Tested versions: Python 3.13, Sphinx 9.1.0, MyST Parser 5.1.0, PyData 0.20.0,
Node 24.10.0, MyST CLI 1.11.0, and TeX Live 2025. The Python packages are the
existing deployment environment's versions; this is not a claim that every
dependency is the newest available version. MyST was installed only in the
experiment's local tools directory. Its site and LaTeX templates report 1.0.0;
their downloaded archive hashes are recorded in `evidence.json` because those
template names resolve to mutable upstream branches.

## Observed results

| Requirement                                               | Sphinx / PyData                       | MyST / book-theme                         |
| --------------------------------------------------------- | ------------------------------------- | ----------------------------------------- |
| Static HTML at `/dr/handbook/`                            | Passed with relative assets           | Passed with `BASE_URL=/dr/handbook`       |
| Handbook links to actual package inventory                | Passed                                | Passed                                    |
| Separate Sphinx consumer links to chapter and section     | Passed                                | Passed                                    |
| Separate Sphinx consumer uses a glossary `term` reference | Passed                                | Failed: inventory has no `std:term` entry |
| Consumer uses an explicit generic label for a term        | Available through normal Sphinx terms | Passed with `ref` to `term-observation`   |
| Deliberately missing package reference                    | Strict build exits 1                  | Strict site build exits 1                 |
| Browser search for `calibration`                          | Finds chapter and glossary            | Finds chapter and glossary                |
| PDF figure, equation, and six-row table                   | Rendered without clipping             | Rendered without clipping                 |
| PDF glossary definitions                                  | All three present                     | All three absent                          |

Both HTML layouts were inspected in the in-app browser, including their search
results. Local page links, fragments and assets were checked against generated
files; assets and main entry points were also requested over HTTP. See
`evidence.json` for counts. Sphinx's copied Jinja files under `_static` are
template sources, not rendered pages, and are excluded from that page scan. The
check does not validate every dynamically loaded JavaScript chunk, every
external URL, or the entire linked package documentation tree.

Both engines generated seven-page PDFs. Every page was rendered to PNG and
reviewed in an overview; chapter, table, figure and Sphinx glossary pages were
also inspected individually. Text extraction independently checks that each
complete definition survived export.

### MyST glossary findings

The MyST inventory publishes `term-observation` as `std:label`, not
`observation` as `std:term`. Package docs can link to that label, but their
normal semantic term references do not resolve. This is a compatibility
difference, not a claim that reverse linking is impossible.

The MyST PDF command `myst build --pdf --strict` exited 0 while logging
`Unknown glossary entry identifier` for all three terms. The resulting shared
glossary chapter is empty. Moving the glossary ahead of the chapter in the
export's article order reproduced the same errors and omission. These findings
apply to MyST 1.11.0 with the downloaded `plain_latex_book` template; they do
not establish that every template or Typst export has the same behavior. No
upstream patch or bespoke export workaround was attempted.

The failed PDF remains diagnostic evidence in the local run directory. It is not
a publishable handbook. A zero build exit status alone is insufficient for PDF
publication acceptance.

## Proposed publication design

The handbook should own shared, user-facing TolTEC terminology. Definitions
whose meaning is specific to one software API remain with that package. The
current glossary has not moved; migration must preserve reviewed wording and
replace package copies with references to the canonical definitions.

Use stable labels and glossary terms. Package documentation should refer to the
handbook through a named Intersphinx inventory; the handbook should refer back
to the package inventory for exact commands, schemas and viewer behavior. Prefer
inventories from the same staged publication so a build cannot silently mix a
new handbook with an unrelated package release.

Collect inventories before final strict builds, then publish the complete
handbook and package-documentation tree together. This accommodates references
in both directions without a network dependency on yesterday's public site. The
handbook edition should have its own review date and software/data applicability
rather than inherit the helpdesk package version.

Serve one canonical book at `/dr/handbook/`, reachable from both portals. The
present `/handbook/` route redirects into `/docs/handbook/`; the comparison uses
separate static servers and does not establish that the existing portal router
already serves the proposed canonical path. A production change must validate
that route, the Apache prefix, versioned inventories, redirects and atomic
publication together. No new Node runtime is needed to serve either static
output; MyST needs its Node toolchain during the build.

## Repository validation

Repository hooks passed for all comparison files, including Ruff, type checking,
spelling and documentation checks. The workspace review diff was regenerated.
The runtime test suite was not rerun: this change adds only isolated publishing
fixtures, verification scripts and design evidence.

## Reproduce

Run from the helpdesk checkout after loading the existing deployment
environment. The output directory is a sibling workspace `run/` directory; it is
not a production publication.

```sh
source ../toltec_astro_dev/.envrc
comparison=../run/handbook-frameworks-20261026
npm install --prefix "$comparison/tools" --save-exact mystmd@1.11.0 --no-audit --no-fund
MPLCONFIGDIR="$comparison/mpl-cache" python design/probes/handbook-frameworks/prepare.py \
  "$comparison" --package-docs ../toltec_astro_dev/run/tolteca_dr/docs/current/tolteca_web
```

In two separate terminals, serve the generated trees:

```sh
python -m http.server 8067 --bind 127.0.0.1 --directory "$comparison/sphinx-site"
python -m http.server 8068 --bind 127.0.0.1 --directory "$comparison/myst-site"
```

Build Sphinx from the helpdesk checkout:

```sh
sphinx-build -W -n -E -b html "$comparison/sphinx" "$comparison/sphinx/_build/html"
sphinx-build -M latexpdf "$comparison/sphinx" "$comparison/sphinx/_build" -W -n
```

Build MyST from the generated `myst/` directory:

```sh
../tools/node_modules/.bin/myst build --pdf --strict
BASE_URL=/dr/handbook ../tools/node_modules/.bin/myst build --html --strict
```

Run the comparison checks from the helpdesk checkout:

```sh
python design/probes/handbook-frameworks/verify.py "$comparison"
```

The verification writes isolated Sphinx consumer projects, deliberately invalid
reference variants, logs and `verification.json`. Its expected-failure builds
must fail; the diagnostic PDF's definition-presence results are reported
separately. PDF inspection uses `pdftotext`, `pdfinfo` and `pdftoppm`. The
scripts also use the existing matplotlib and Beautiful Soup dependencies.

Live local samples: [Sphinx](http://127.0.0.1:8067/dr/handbook/chapter.html) and
[MyST](http://127.0.0.1:8068/dr/handbook/chapter/). Generated outputs and logs
remain under the run directory. Maintained fixtures, build configuration,
verification code and this decision evidence are tracked.

## Primary references

- [Sphinx Intersphinx](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html):
  inventories and typed cross-project references.
- [PyData layout](https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html):
  reader layout and navigation configuration.
- [MyST external references](https://mystmd.org/guide/external-references):
  Sphinx inventory consumption.
- [MyST glossaries](https://mystmd.org/guide/glossaries-and-terms): glossary
  syntax differences.
- [MyST static deployment](https://mystmd.org/guide/deployment): static exports
  and the required subpath base URL.
- [MyST PDF exports](https://mystmd.org/guide/creating-pdf-documents): LaTeX
  book templates and article heading levels.
- [MyST theme API](https://mystmd.org/guide/theme-developer): structured
  content, search and inventory exports.
- [Jupyter Book FAQ](https://jupyterbook.org/latest/resources/faq/): the
  separate MyST engine used by Jupyter Book 2.

These references establish supported approaches. The local build evidence above
establishes the narrower behavior actually observed in this experiment.
