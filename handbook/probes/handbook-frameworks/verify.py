"""Record cross-reference, strict-build and static-subpath comparison results."""

# Standalone evidence tool. Assertions encode the observed comparison checks.
# ruff: noqa: INP001, T201, S101

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import urlopen

from bs4 import BeautifulSoup
from sphinx.util.inventory import InventoryFile


def _run(command: list[str], directory: Path, log: Path) -> int:
    with log.open("w") as stream:
        # Only fixed build commands and this experiment's output paths are passed.
        result = subprocess.run(  # noqa: S603
            command, cwd=directory, stdout=stream, stderr=stream, check=False
        )
    return result.returncode


def main() -> None:  # noqa: C901, PLR0912, PLR0915 - sequential comparison protocol
    """Run both builders' consumer, failure and publication checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    root = args.output.resolve()
    results = {}
    sphinx = [sys.executable, "-m", "sphinx", "-W", "-n", "-b", "html"]
    for engine, port in (("sphinx", 8067), ("myst", 8068)):
        project = root / engine
        html = project / "_build/html"
        base = f"http://127.0.0.1:{port}/dr/handbook/"
        with (html / "objects.inv").open("rb") as stream:
            inventory = InventoryFile.load(stream, base, urljoin)
        current = {
            "inventory": {
                domain: {name: item.uri for name, item in entries.items()}
                for domain, entries in inventory.items()
            }
        }
        consumer = root / f"consumer-{engine}"
        consumer.mkdir(exist_ok=True)
        (consumer / "conf.py").write_text(
            "project='Package reference consumer'\n"
            "extensions=['sphinx.ext.intersphinx']\n"
            f"intersphinx_mapping={{'handbook': ({base!r}, "
            f"{str(html / 'objects.inv')!r})}}\n"
        )
        common = """Package guide linking to handbook
=================================

See :external+handbook:doc:`chapter` and
:external+handbook:ref:`inspection-checklist`.

"""
        (consumer / "index.rst").write_text(
            common + "Use :external+handbook:term:`observation`.\n"
        )
        current["typed_term_consumer_exit"] = _run(
            [*sphinx, "-E", ".", "_build/typed"],
            consumer,
            root / f"consumer-{engine}-typed.log",
        )
        if engine == "myst":
            (consumer / "index.rst").write_text(
                common
                + "Use :external+handbook:ref:`observation <term-observation>`.\n"
            )
            current["generic_label_consumer_exit"] = _run(
                [*sphinx, "-E", ".", "_build/label"],
                consumer,
                root / f"consumer-{engine}-label.log",
            )

        # Missing external targets must be observable build failures.
        negative = root / f"negative-{engine}"
        shutil.copytree(
            project,
            negative,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("_build", "exports"),
        )
        page = negative / "chapter.md"
        extra = (
            "\n{external+web:doc}`missing-comparison-target`\n"
            if engine == "sphinx"
            else "\n[Missing target](xref:web#missing-comparison-target)\n"
        )
        page.write_text(page.read_text() + extra)
        command = (
            [*sphinx, "-E", ".", "_build/html"]
            if engine == "sphinx"
            else [
                str(root / "tools/node_modules/.bin/myst"),
                "build",
                "--site",
                "--strict",
            ]
        )
        current["missing_reference_exit"] = _run(
            command, negative, root / f"negative-{engine}.log"
        )

        # Check the emitted local href/src targets and fragments, independent
        # of the web app's client-side router. This includes PDF/JSON assets.
        errors = []
        checked = set()
        http_checked = set()
        for page in html.rglob("*.html"):
            # Theme template sources copied into _static are not rendered pages.
            if "_static" in page.relative_to(html).parts:
                continue
            relative = page.relative_to(html).as_posix()
            document_url = urljoin(base, relative)
            tree = BeautifulSoup(page.read_text(), "html.parser")
            for element in tree.select("[href], [src]"):
                value = element.get("href", element.get("src", ""))
                url = urlsplit(urljoin(document_url, value))
                if url.netloc != f"127.0.0.1:{port}" or not url.path.startswith(
                    "/dr/handbook/"
                ):
                    continue
                path = html / unquote(url.path.removeprefix("/dr/handbook/"))
                if path.is_dir():
                    path /= "index.html"
                checked.add(str(path))
                if not path.is_file():
                    errors.append(f"{relative}: missing {url.path}")
                elif url.fragment and path.suffix == ".html":
                    target = BeautifulSoup(path.read_text(), "html.parser")
                    if not target.find(id=unquote(url.fragment)):
                        errors.append(
                            f"{relative}: missing fragment {url.path}#{url.fragment}"
                        )
                if element.name in ("script", "img", "link") and path.is_file():
                    http_checked.add(url._replace(fragment="").geturl())
        http_checked.update(
            [
                base,
                base + "objects.inv",
                base + ("chapter.html" if engine == "sphinx" else "chapter/"),
            ]
        )
        for url in sorted(http_checked):
            # Every URL above has this experiment's loopback HTTP origin.
            with urlopen(url, timeout=10) as response:  # noqa: S310
                if response.status != 200:  # noqa: PLR2004
                    errors.append(f"HTTP {response.status}: {url}")
        current.update(
            static_targets_checked=len(checked),
            http_targets_checked=len(http_checked),
            static_errors=sorted(set(errors)),
        )
        pdf = (
            project / "_build/latex/handbook.pdf"
            if engine == "sphinx"
            else project / "exports/handbook.pdf"
        )
        text = subprocess.check_output(  # noqa: S603 - generated PDF only
            [shutil.which("pdftotext"), str(pdf), "-"], text=True
        )
        text = unicodedata.normalize("NFKC", " ".join(text.split()))
        terms = json.loads((Path(__file__).parent / "glossary.json").read_text())
        current["pdf_glossary_definitions"] = {
            term: definition in text for term, definition in terms.items()
        }
        results[engine] = current
    (root / "verification.json").write_text(json.dumps(results, indent=2) + "\n")
    print(
        json.dumps(
            {
                key: {k: v for k, v in value.items() if k != "inventory"}
                for key, value in results.items()
            },
            indent=2,
        )
    )
    assert all(not item["static_errors"] for item in results.values())
    assert all(item["missing_reference_exit"] != 0 for item in results.values())
    assert results["sphinx"]["typed_term_consumer_exit"] == 0
    assert results["myst"]["generic_label_consumer_exit"] == 0


if __name__ == "__main__":
    main()
