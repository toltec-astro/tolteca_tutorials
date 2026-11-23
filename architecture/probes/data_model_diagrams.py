"""Render the data-model and product diagrams into their maintained decks."""

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INK, MUTED, TEAL, BLUE = "#17283d", "#516276", "#007c83", "#245bc0"


def box(x, y, w, title, detail, *, h=100, accent=TEAL):
    return f'''<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#f4f7fa" stroke="{accent}" stroke-width="2"/>
<text x="{x + 20}" y="{y + 38}" fill="{INK}" font-size="26" font-weight="600">{escape(title)}</text>
<text x="{x + 20}" y="{y + 72}" fill="{MUTED}" font-size="22">{escape(detail)}</text></g>'''


def edge(key, path, label="", x=0, y=0):
    # Labels sit in reserved whitespace outside node bounds and above connectors.
    return (
        f'<path d="{path}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#{key}-arrow)"/>'
        + (
            f'<rect x="{x - len(label) * 6}" y="{y - 22}" width="{len(label) * 12}" height="28" fill="white"/><text x="{x}" y="{y}" text-anchor="middle" fill="{MUTED}" font-size="22">{escape(label)}</text>'
            if label
            else ""
        )
    )


def svg(key, title, desc, body, height=280):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1120 {height}" role="img" aria-labelledby="{key}-title {key}-desc" style="font-family:Arial,Helvetica,sans-serif;width:100%;max-height:{height}px">
<title id="{key}-title">{escape(title)}</title><desc id="{key}-desc">{escape(desc)}</desc>
<defs><marker id="{key}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/></marker></defs>
{body}
</svg>'''


def three(key, title, nodes, labels):
    body = edge(key, "M 324 100 H 396", labels[0], 360, 72) + edge(
        key, "M 724 100 H 796", labels[1], 760, 72
    )
    body += "".join(
        box(x, 50, 324, *n) for x, n in zip([0, 400, 796], nodes, strict=True)
    )
    return svg(key, title, "; ".join(title for title, _ in nodes), body, 200)


def diagrams():
    yield (
        "owners",
        svg(
            "owners",
            "Domain modules depend on shared machinery",
            "LMT, TolTEC and dummy each depend on core; root entry points assemble their registrations.",
            "".join(
                edge("owners", f"M {x} 100 V 160", "uses", x + 35, 136)
                for x in [162, 560, 958]
            )
            + box(0, 0, 324, "LMT", "Telescope conventions")
            + box(398, 0, 324, "TolTEC", "KIDs and HWPR layouts")
            + box(796, 0, 324, "Dummy instrument", "Reference extension")
            + box(
                0,
                160,
                1120,
                "core + Tollan",
                "Shared validation, projection, dispatch, stores and query machinery",
            ),
            280,
        ),
    )
    yield (
        "open_read",
        three(
            "open_read",
            "Resource and data access",
            [
                ("Source", "Path or borrowed resource"),
                ("io_obj", "Format-specific container"),
                ("accessor_obj", "Domain-specific data view"),
            ],
            ["open", "bind"],
        ),
    )
    k = "product_records"
    body = (
        edge(k, "M 290 60 H 410", "contains", 350, 42)
        + edge(k, "M 145 110 V 242 Q 145 250 153 250 H 410", "has", 190, 228)
        + edge(k, "M 700 250 H 820", "targets", 760, 230)
    )
    body += (
        box(0, 10, 290, "Product", "UID + domain metadata", accent=BLUE)
        + box(410, 10, 290, "Item", "Metadata + source", accent=BLUE)
        + box(410, 200, 290, "Association", "Type + relation fields", accent=BLUE)
        + box(820, 200, 300, "Product reference", "UID + namespace", accent=BLUE)
    )
    yield (
        k,
        svg(
            k,
            "Product record relationships",
            "A product contains items and has associations. Each association targets a product reference.",
            body,
            320,
        ),
    )
    k = "versions"
    body = edge(k, "M 304 100 H 396", "member", 350, 78) + edge(
        k,
        "M 304 128 H 340 Q 348 128 348 136 V 242 Q 348 250 356 250 H 396",
        "member",
        350,
        220,
    )
    body += (
        box(0, 60, 304, "Version group", "Stable logical result", accent=BLUE)
        + box(396, 50, 324, "Realization A", "Exact product + run A", accent=BLUE)
        + box(396, 200, 324, "Realization B", "Exact product + run B", accent=BLUE)
        + box(796, 200, 324, "Tag: main", "Selects realization B", accent=TEAL)
    )
    body = edge(k, "M 796 250 H 724", "selects", 760, 228) + body
    yield (
        k,
        svg(
            k,
            "Version-group alternatives",
            "A group has two exact realizations. Its main tag selects realization B.",
            body,
            320,
        ),
    )
    k = "dummy_context"
    body = (
        edge(k, "M 700 110 H 420", "summarizes", 560, 88)
        + box(
            60,
            60,
            360,
            "signal · measurement",
            "Acquisition / voltage stream",
            accent=BLUE,
        )
        + box(700, 60, 360, "mean · summary", "Result / mean_voltage", accent=BLUE)
    )
    yield (
        k,
        svg(
            k,
            "Dummy context binding",
            "The mean summary member names the voltage measurement member it summarizes.",
            body,
            220,
        ),
    )
    k = "raw_context"
    body = (
        edge(k, "M 320 70 H 800", "model_key", 560, 48)
        + edge(
            k, "M 160 120 V 262 Q 160 270 168 270 H 400", "calibration_key", 280, 248
        )
        + edge(
            k, "M 960 120 V 262 Q 960 270 952 270 H 720", "calibration_key", 840, 248
        )
    )
    body += (
        box(0, 20, 320, "signal · source", "Raw acquisition / block 1", accent=BLUE)
        + box(800, 20, 320, "fit · model", "Processed result / artifact", accent=BLUE)
        + box(400, 220, 320, "cal · sweep", "Raw acquisition / block 0", accent=TEAL)
    )
    yield (
        k,
        svg(
            k,
            "Raw-observation context bindings",
            "The source names a model and a sweep. The model names the same sweep. Labels are local member keys.",
            body,
            340,
        ),
    )


if __name__ == "__main__":
    rendered = dict(diagrams())
    for name in ["tolteca-datamodels-input-workflow", "toltec-data-products"]:
        path = ROOT / name / f"{name}.md"
        source = path.read_text()
        for key, diagram in rendered.items():
            marker = f'data-diagram="{key}"'
            if marker not in source:
                continue
            assets = path.parent / "assets"
            assets.mkdir(exist_ok=True)
            (assets / f"{key}.svg").write_text(diagram + "\n")
            pattern = rf'<div class="diagram(?: small)?" data-diagram="{key}">.*?</div>'
            css = "diagram small" if key == "dummy_context" else "diagram"
            source = re.sub(
                pattern,
                f'<div class="{css}" data-diagram="{key}">' + diagram + "</div>",
                source,
                flags=re.S,
            )
        path.write_text(source)
