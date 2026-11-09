"""Prepare an isolated publishing comparison; never modify the live handbook."""

# Standalone evidence tool, not a package API.
# ruff: noqa: INP001, T201

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt


def _plot(output: Path) -> None:
    """Generate an explicitly synthetic figure for layout comparison."""
    with plt.rc_context({"font.size": 11}):
        fig, ax = plt.subplots(figsize=(6.4, 2.8), layout="constrained")
        ax.errorbar(
            [1, 2, 3, 4, 5],
            [1.0, 1.3, 0.9, 1.2, 1.1],
            yerr=[0.15, 0.2, 0.1, 0.18, 0.14],
            fmt="o",
            capsize=4,
            color="#24587b",
        )
        ax.set(
            xlabel="Illustrative sample",
            ylabel="Dimensionless value",
            xticks=[1, 2, 3, 4, 5],
            ylim=(0.5, 1.7),
        )
        ax.grid(alpha=0.2)
        fig.savefig(output / "uncertainty.png", dpi=200)
        plt.close(fig)


def main() -> None:
    """Write the sample projects and record their source hashes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--package-docs", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    source = Path(__file__).resolve().parent
    output.mkdir(parents=True, exist_ok=True)
    terms = json.loads((source / "glossary.json").read_text())
    chapter = (source / "chapter.md").read_text()

    _plot(output)

    inventory = args.package_docs / "objects.inv"
    package_url = "http://127.0.0.1:8067/dr/packages/tolteca_web/"
    index = """# TolTEC Data Handbook

Publishing comparison - 26 October 2026

Identify the meaning, provenance, and limitations of a data product before
making a scientific measurement. Start with [product inspection](chapter.md)
and consult the [shared glossary](glossary.md).

This short sample compares two documentation frameworks. It is not a released
handbook or a new source of approved instrument guidance.
"""
    for engine in ("sphinx", "myst"):
        project = output / engine
        project.mkdir(exist_ok=True)
        root = output / f"{engine}-site" / "dr"
        root.mkdir(parents=True, exist_ok=True)
        (root / "packages").mkdir(exist_ok=True)
        package_link = root / "packages" / "tolteca_web"
        if not package_link.exists():
            package_link.symlink_to(
                args.package_docs.resolve(), target_is_directory=True
            )
        html = project / "_build" / "html"
        html.mkdir(parents=True, exist_ok=True)
        handbook_link = root / "handbook"
        if not handbook_link.exists():
            handbook_link.symlink_to(html, target_is_directory=True)
        shutil.copy2(output / "uncertainty.png", project / "uncertainty.png")
        glossary = "(shared-glossary)=\n# Shared glossary\n\n```{glossary}\n"
        for term, definition in terms.items():
            prefix = "  " if engine == "sphinx" else ": "
            glossary += f"{term}\n{prefix}{definition}\n\n"
        glossary += "```\n"
        (project / "glossary.md").write_text(glossary)

        if engine == "sphinx":
            (project / "_templates").mkdir(exist_ok=True)
            shutil.copy2(
                source / "handbook-nav.html", project / "_templates/handbook-nav.html"
            )
            viewer = "{external+web:doc}`processed KIDs viewer guide <processed-kids>`"
            (project / "index.md").write_text(
                index + "\n```{toctree}\n:maxdepth: 2\n\nchapter\nglossary\n```\n"
            )
            (project / "conf.py").write_text(f"""project = 'TolTEC Data Handbook'
author = 'TolTEC team'
copyright = '2026, TolTEC team'
release = 'Framework comparison'
extensions = ['myst_parser', 'sphinx.ext.intersphinx']
source_suffix = {{'.md': 'markdown'}}
exclude_patterns = ['_build']
html_theme = 'pydata_sphinx_theme'
html_title = project
# A book needs the complete chapter list in its sidebar. PyData's default
# sidebar starts below the active top-level section.
templates_path = ['_templates']
html_sidebars = {{'**': ['sidebar-collapse', 'handbook-nav']}}
html_theme_options = {{
    'announcement': 'Publishing comparison - 26 October 2026', 'navbar_center': []
}}
intersphinx_mapping = {{'web': ({package_url!r}, {str(inventory.resolve())!r})}}
myst_enable_extensions = ['dollarmath']
numfig = True
latex_engine = 'pdflatex'
latex_documents = [('index', 'handbook.tex', project, author, 'manual')]
latex_elements = {{
    'papersize': 'a4paper', 'pointsize': '11pt',
    'extraclassoptions': 'openany,oneside'
}}
""")
        else:
            viewer = "[processed KIDs viewer guide](xref:web#processed-kids)"
            (project / "index.md").write_text(index)
            (project / "myst.yml").write_text(f"""version: 1
project:
  title: TolTEC Data Handbook
  authors:
    - name: TolTEC team
  date: 2026-10-26
  toc:
    - file: index.md
    - file: chapter.md
    - file: glossary.md
  references:
    web:
      url: {package_url}
  exports:
    - format: pdf
      template: plain_latex_book
      output: exports/handbook.pdf
      articles:
        - file: index.md
          level: 0
        - file: chapter.md
          level: 0
        - file: glossary.md
          level: 0
site:
  template: book-theme
  options:
    logo_text: TolTEC Data Handbook
""")
        (project / "chapter.md").write_text(chapter.replace("@@VIEWER_LINK@@", viewer))

    evidence = {
        "package_docs": str(args.package_docs.resolve()),
        "inventory_sha256": hashlib.sha256(inventory.read_bytes()).hexdigest(),
        "chapter_sha256": hashlib.sha256(
            (source / "chapter.md").read_bytes()
        ).hexdigest(),
        "glossary_sha256": hashlib.sha256(
            (source / "glossary.json").read_bytes()
        ).hexdigest(),
    }
    (output / "inputs.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()
