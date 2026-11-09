"""Render the figures of the OT and reduction workflow deck.

Run from the Python workspace root:

    toltec_astro_dev/.venv/bin/python tolteca_tutorials/architecture/toltec-ot-reduction-workflow/probes/render_ot_reduction_workflow.py

Acquisition times come from read-only reference data for obsnums 145605–145612
(2025-10-31): the ToltecDB and LMTMC slices and the toltec0 and telescope file
headers. Durations measured in the local Docker comparison are constants cited
to ``python/run/v2v3-overhead-20261102/comparison-3way.md`` and its README.
The power-setup figures read the published drive-fit and commit products of the
detector setup specification's network-0 example (fit 145484, target 145485).
Each figure replaces the deck's ``<svg id="fig-...">`` block of the same name.
"""

# Standalone deck build tool, outside the importable package.
# ruff: noqa: INP001

import csv
import re
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from html import escape
from pathlib import Path

import netCDF4
import numpy as np
import xarray as xr

DESIGN = Path(__file__).resolve().parents[1]
WORKSPACE = DESIGN.parents[2]
DECK = DESIGN / "toltec-ot-reduction-workflow.md"
DATA_LMT = WORKSPACE / "toltec_astro_dev/run/data_lmt"
FIXTURES = WORKSPACE / "tolteca_ref_data/test_fixtures"
OBSNUMS = (145605, 145612)

W = 1148
INK = "#17283d"
MUTED = "#516276"
RULE = "#dce4eb"
FONT = "Arial, Helvetica, sans-serif"
MONO = "SFMono-Regular, Menlo, Consolas, monospace"
# (fill, stroke) per role, shared with the v3 overview deck's palette.
ROLE = {
    "acq": ("#e9f1ff", "#316cc5"),
    "inline": ("#e6f5f0", "#008278"),
    "ql": ("#f0eafd", "#7653b7"),
    "operator": ("#fff2de", "#a45b0b"),
    "db": ("#f0f4f8", "#52677b"),
}
BAR = {
    "VnaSweep": "#245bc0",
    "TargSweep": "#7aa3e6",
    "Tune": "#008278",
    "Lissajous": "#52677b",
}

# One inline request per network, all 10 recorded networks of a block at once, as
# Tlaloc calls reduce.sh (python/run/inline-full-20261102, summary.json "burst").
# (variant, clip side, Taca side) in seconds; Taca side is the slowest network.
# Clip side: v2 native v1 kids (host-measured, as the v2 replay modelled it); v3
# hook (Docker, one at a time) plus the native fit for Target/Tune (host).
# v3: inline steps, then the KidsFind and tone tables staged for one version
# per acquisition ("burst-stage").
INLINE_REQUEST = [
    ("VNA 145605", [("v2", 2.2, 12.87), ("v3", 2.22, 8.86)]),
    ("Target 145606", [("v2", 0.7, 8.68), ("v3", 2.92, 5.7)]),
    ("Target 145607", [("v2", 0.7, 8.2), ("v3", 2.9, 5.53)]),
    ("Tune 145609 block 0", [("v2", 0.7, 7.72), ("v3", 2.81, 5.71)]),
    ("Tune 145609 block 1", [("v2", 0.7, 8.29), ("v3", 2.9, 5.51)]),
]
INLINE_COLOR = {"v2": ("#d7dee6", "#8a9aab"), "v3": ("#bfe3dd", "#008278")}
# Quicklook: Valid = 1 -> MC can return the result, as (start, end, stage).
# v2 composition from the README; v3 stages from comparison-3way.md.
QL_TIME = [
    (
        "VNA 145605",
        [
            ("v2", [(0, 3.5, "trigger"), (3.5, 58.3, "other"), (58.3, 64.7, "ql")]),
            (
                "v3 previous",
                [
                    (0, 10.7, "trigger"),
                    (10.7, 49.0, "recompute"),
                    (49.0, 57.7, "register"),
                ],
            ),
            (
                "v3",
                [(0, 10.2, "trigger"), (10.2, 19.7, "ql"), (19.7, 20.0, "register")],
            ),
        ],
    ),
    (
        "Tune 145609",
        [
            ("v2", [(0, 3.5, "trigger"), (3.5, 46.8, "other"), (46.8, 52.7, "ql")]),
            (
                "v3 previous",
                [
                    (0, 6.8, "trigger"),
                    (6.8, 41.9, "recompute"),
                    (41.9, 49.3, "register"),
                ],
            ),
            (
                "v3",
                [(0, 6.8, "trigger"), (6.8, 10.3, "ql"), (10.3, 13.3, "register")],
            ),
        ],
    ),
]
QL_STAGE = {
    "trigger": ("#e4e9ef", "#8a9aab", "sensor, queue, run start"),
    "other": ("#cfd8e3", "#6d7f93", "earlier toltecpipe ops"),
    "recompute": ("#bfe3dd", "#008278", "re-reduce all blocks"),
    "ql": ("#ddd0f5", "#7653b7", "collect, plot, publish"),
    "register": ("#f7dcb5", "#a45b0b", "DPDB registration"),
}
# Valid -> quicklook for Tune 145609 scan 1 (comparison-3way.md, MC column).
QL_TUNE_V2, QL_TUNE_V3 = 52.7, 13.3
# reduce.sh for Tune 145609 blocks 0 and 1: slowest of 10 networks started at once,
# clip side included (INLINE_REQUEST, v2 and v3).
REDUCE_PER_NETWORK = {"v2": [8.4, 9.0], "v3": [8.5, 8.4]}
# Pointing map after the Lissajous closes, as (seconds, stage): run start from
# the Docker Tune quicklook (comparison-3way.md); preparation, input projection
# and Citlali in pointing mode measured on obsnum 152434, 11 networks, local host,
# 12 threads (python/run/pointing-reduction-20261102).
QL_POINTING = [(6.8, "start"), (15.2, "prepare"), (25.8, "Citlali")]


def _utc(value):
    return datetime.fromtimestamp(float(value), UTC)


@dataclass
class Acquisition:
    obsnum: int
    scan: int
    program: str
    start: datetime
    end: datetime | None = None
    blocks: list[tuple[datetime, datetime]] = field(default_factory=list)
    end_source: str = "estimate"

    @property
    def key(self):
        return (self.obsnum, self.scan)


def load_acquisitions():
    """Return the recorded acquisitions with start, end and block times."""
    with sqlite3.connect(
        f"file:{FIXTURES / 'toltecdb_slice.sqlite'}?mode=ro", uri=True
    ) as db:
        rows = db.execute(
            "select ObsNum, ScanNum, Date, Time from toltec"
            " where RoachIndex = 0 and ObsNum between ? and ? order by id",
            OBSNUMS,
        ).fetchall()
    with (FIXTURES / "lmtmc_slice.csv").open() as f:
        program = {}
        for rec in csv.DictReader(f):
            obsnum, _, scan = rec["ObsNum"].split(".")
            program[int(obsnum), int(scan)] = rec["ObsPgm"]
    acqs = []
    for obsnum, scan, date, time in rows:
        start = datetime.fromisoformat(f"{date}T{time}+00:00")
        acq = Acquisition(obsnum, scan, program[obsnum, scan], start)
        files = sorted(
            (DATA_LMT / "toltec/tcs/toltec0").glob(
                f"toltec0_{obsnum}_000_{scan:04d}_*.nc"
            )
        )
        tel = sorted((DATA_LMT / "tel").glob(f"tel_toltec_*_{obsnum}_00_{scan:04d}.nc"))
        if files:
            with netCDF4.Dataset(files[0]) as ds:
                v = ds.variables
                acq.start = _utc(v["Header.Toltec.ObsStartTime"][...])
                acq.end = _utc(v["Header.Toltec.ObsEndTime"][...])
                recv = np.asarray(v["Data.Toltec.RecvTime"][...]).ravel()
            # Sweep blocks are separated by the reduce/load interval (> 2 s).
            for seg in np.split(recv, np.where(np.diff(recv) > 2)[0] + 1):
                acq.blocks.append((_utc(seg[0]), _utc(seg[-1])))
            acq.end_source = "header"
        elif tel:
            with netCDF4.Dataset(tel[0]) as ds:
                acq.end = _utc(
                    np.asarray(ds.variables["Data.TelescopeBackend.TelTime"][...]).max()
                )
            acq.end_source = "tel"
        acqs.append(acq)
    by_key = {a.key: a for a in acqs}
    tune, liss = by_key[145609, 1], by_key[145609, 2]
    targ = by_key[145606, 1]
    tune_to_liss = (liss.start - tune.end).total_seconds()
    for acq in acqs:
        if acq.end is not None:
            continue
        if acq.program == "TargSweep":
            acq.end = acq.start + (targ.end - targ.start)
        elif acq.program == "Tune" and (acq.obsnum, 2) in by_key:
            acq.end = by_key[acq.obsnum, 2].start - (liss.start - tune.end)
        elif acq.program == "Lissajous":
            acq.end = acq.start + (liss.end - liss.start)
    tune_offsets = (
        (tune.blocks[0][1] - tune.start),
        (tune.end - tune.blocks[1][1]),
    )
    return acqs, tune_offsets, tune_to_liss


def reduce_times(acq, tune_offsets):
    """Return when Tlaloc calls reduce.sh for one acquisition."""
    if acq.program in ("VnaSweep", "TargSweep"):
        return [acq.end]
    if acq.program == "Tune":
        if acq.blocks:
            return [acq.blocks[0][1], acq.blocks[1][1]]
        return [acq.start + tune_offsets[0], acq.end - tune_offsets[1]]
    return []


class Fig:
    def __init__(self, name, title, height, width=W):
        self.name, self.width, self.height = name, width, height
        self.parts = []
        self.title = title

    def text(
        self,
        x,
        y,
        s,
        size=21,
        color=INK,
        weight=400,
        anchor="middle",
        font=FONT,
        halo=False,
    ):
        extra = (
            ' paint-order="stroke" stroke="#fff" stroke-width="7" stroke-linejoin="round"'
            if halo
            else ""
        )
        for i, line in enumerate(str(s).split("\n")):
            self.parts.append(
                f'<text x="{x:.1f}" y="{y + i * (size + 6):.1f}" text-anchor="{anchor}" font-family="{font}"'
                f' font-size="{size}" font-weight="{weight}" fill="{color}"{extra}>{escape(line)}</text>'
            )

    def rect(self, x, y, w, h, fill, stroke="none", rx=6, dash=False, sw=2):
        d = ' stroke-dasharray="6 5"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 1):.1f}" height="{h:.1f}" rx="{rx}"'
            f' fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def line(self, x1, y1, x2, y2, color=MUTED, sw=2, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.name}-arrow)"' if arrow else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}"'
            f' stroke-width="{sw}"{d}{m}/>'
        )

    def poly(self, points, color=MUTED, sw=2.5, dash=None, arrow=True):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#{self.name}-arrow)"' if arrow else ""
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.parts.append(
            f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}"'
            f' stroke-linecap="round" stroke-linejoin="round"{d}{m}/>'
        )

    def diamond(self, x, y, r, fill, stroke=None, hollow=False):
        f = "#fff" if hollow else fill
        self.parts.append(
            f'<path d="M{x:.1f} {y - r:.1f}L{x + r:.1f} {y:.1f}L{x:.1f} {y + r:.1f}L{x - r:.1f} {y:.1f}Z"'
            f' fill="{f}" stroke="{stroke or fill}" stroke-width="2.5"/>'
        )

    def dot(self, x, y, r, fill, stroke="none"):
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        )

    def tri(self, x, y, r, fill):
        self.parts.append(
            f'<path d="M{x - r:.1f} {y - r:.1f}L{x + r:.1f} {y - r:.1f}L{x:.1f} {y + r * 0.7:.1f}Z" fill="{fill}"/>'
        )

    def box(self, x, y, w, h, title, subtitle="", role="acq", size=23):
        fill, stroke = ROLE[role]
        self.rect(x, y, w, h, fill, stroke, rx=12)
        n = title.count("\n") + 1
        top = (
            y + h / 2 - (n - 1) * (size + 6) / 2 + size * 0.35 - (13 if subtitle else 0)
        )
        self.text(x + w / 2, top, title, size, stroke, 700)
        if subtitle:
            self.text(x + w / 2, y + h - 16, subtitle, 18, MUTED)

    def svg(self):
        head = (
            f'<svg id="fig-{self.name}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}"'
            f' width="{self.width}" height="{self.height}" role="img" aria-label="{escape(self.title)}">'
            # The opening tag stands alone on its line so Markdown keeps the
            # figure as one HTML block (no blank lines inside).
            f"\n<title>{escape(self.title)}</title>"
            f'<defs><marker id="{self.name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7"'
            ' markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>'
        )
        return "\n".join([head, *self.parts, "</svg>"])


def text_width(s, size):
    return 0.55 * size * len(s)


class Sequence(Fig):
    """A sequence diagram with lifelines, messages and activity boxes."""

    def __init__(
        self, name, title, lanes, rows, *, x0=90, x1=W - 90, row=46, spans=None
    ):
        self.lanes = {}
        n = len(lanes)
        for i, (key, label, role) in enumerate(lanes):
            self.lanes[key] = (x0 + i * (x1 - x0) / (n - 1), label, role)
        height = 78 + sum(r.get("h", row) for r in rows) + 18
        super().__init__(name, title, height)
        for x, label, role in self.lanes.values():
            fill, stroke = ROLE[role]
            w = max(150, text_width(label, 20) + 30)
            self.rect(x - w / 2, 6, w, 48, fill, stroke, rx=10)
            self.text(x, 37, label, 20, stroke, 700)
            self.line(x, 54, x, height - 8, RULE, 2, "4 6")
        y = 78
        tops = []
        for r in rows:
            h = r.get("h", row)
            tops.append((y, y + h))
            yc = y + h / 2 + 6
            kind = r["kind"]
            if kind == "msg":
                xa, xb = self.lanes[r["a"]][0], self.lanes[r["b"]][0]
                color = r.get("color", INK)
                self.line(
                    xa,
                    yc,
                    xb - 8 * np.sign(xb - xa),
                    yc,
                    color,
                    2.5,
                    "7 6" if r.get("dashed") else None,
                    True,
                )
                self.text((xa + xb) / 2, yc - 9, r["text"], 19, color, 400, halo=True)
            elif kind == "act":
                x, _, role = self.lanes[r["a"]]
                fill, stroke = ROLE[r.get("role", role)]
                lines = r["text"].split("\n")
                w = max(text_width(s, 19) for s in lines) + 28
                bh = 14 + 25 * len(lines)
                self.rect(x - w / 2, yc - bh / 2 - 4, w, bh, fill, stroke, rx=8)
                self.text(x, yc - bh / 2 + 18, r["text"], 19, stroke, 700)
            y += h
        if spans:
            label, items = spans
            self.text(W - 50, 37, label, 19, MUTED, 700, font=MONO)
            for first, last, text in items:
                ya, yb = tops[first][0] + 12, tops[last][1] - 4
                self.line(W - 92, ya, W - 92, yb, MUTED, 2)
                self.line(W - 100, ya, W - 92, ya, MUTED, 2)
                self.line(W - 100, yb, W - 92, yb, MUTED, 2)
                self.text(W - 80, (ya + yb) / 2 + 7, text, 20, INK, 700, "start")


def fig_workflows():
    f = Fig(
        "workflows",
        "An acquisition feeds inline reduction, quicklook and ingestion",
        400,
    )
    f.box(0, 150, 230, 100, "Acquisition", "Tlaloc writes toltecN.nc", "acq")
    rows = [
        (
            30,
            "Inline reduction",
            "reduce.sh, called by the OT script",
            "inline",
            "during the script",
            "adds to observing time",
        ),
        (
            150,
            "Quicklook",
            "Dagster run → QL server",
            "ql",
            "file valid",
            "operator waits at script end",
        ),
        (
            270,
            "Raw ingestion",
            "Dagster runs → DPDB",
            "db",
            "file valid",
            "portal; may lag",
        ),
    ]
    for y, title, sub, role, edge, need in rows:
        f.poly([(234, 200), (300, 200), (300, y + 50), (440, y + 50)], ROLE[role][1])
        f.text(372, y + 40, edge, 18, MUTED, halo=True)
        f.box(450, y, 380, 100, title, sub, role)
        f.text(860, y + 58, need, 22, ROLE[role][1], 700, "start")
    return f


def fig_night(acqs, tune_offsets):
    t0 = datetime(2025, 10, 31, 9, 19, 40, tzinfo=UTC)
    t1 = datetime(2025, 10, 31, 9, 45, 20, tzinfo=UTC)
    x0, x1 = 250, W - 12
    span = (t1 - t0).total_seconds()

    def X(t):
        return x0 + (t - t0).total_seconds() * (x1 - x0) / span

    f = Fig("night", "Acquisitions of 2025-10-31 grouped by OT script", 400)
    lx = x0
    for label, color in [
        ("VNA sweep", BAR["VnaSweep"]),
        ("target sweep", BAR["TargSweep"]),
        ("Tune", BAR["Tune"]),
        ("Lissajous", BAR["Lissajous"]),
    ]:
        f.rect(lx, 8, 22, 22, color, rx=4)
        f.text(lx + 30, 26, label, 19, MUTED, anchor="start")
        lx += text_width(label, 19) + 62
    f.tri(lx + 10, 18, 9, INK)
    f.text(lx + 26, 26, "reduce.sh", 19, MUTED, anchor="start")
    lx += 132
    f.diamond(lx + 10, 18, 10, ROLE["operator"][1])
    f.text(lx + 26, 26, "QL query", 19, MUTED, anchor="start")
    groups = [
        ("10 · init coarse", "145605", [145605], False),
        ("12 · tune ×3", "145606–145608", [145606, 145607, 145608], False),
        ("01 · pointing ×4", "145609–145612", [145609, 145610, 145611, 145612], True),
    ]
    for i, (label, sub, obsnums, per_obsnum) in enumerate(groups):
        y = 78 + i * 92
        f.text(0, y + 20, label, 22, INK, 700, "start")
        f.text(0, y + 46, sub, 19, MUTED, anchor="start", font=MONO)
        members = [a for a in acqs if a.obsnum in obsnums]
        for a in members:
            f.rect(X(a.start), y, X(a.end) - X(a.start), 38, BAR[a.program], rx=3)
            for t in reduce_times(a, tune_offsets):
                f.tri(X(t), y - 8, 8, INK)
        ends = (
            [max(a.end for a in members if a.obsnum == o) for o in obsnums]
            if per_obsnum
            else [members[-1].end]
        )
        for end in ends:
            f.diamond(X(end) + 18, y + 19, 10, ROLE["operator"][1])
        if per_obsnum:
            for o in obsnums:
                start = min(a.start for a in members if a.obsnum == o)
                f.text(X(start), y + 64, str(o), 18, MUTED, anchor="start", font=MONO)
    ya = 352
    f.line(x0, ya, x1, ya, MUTED, 1.5)
    minute = datetime(2025, 10, 31, 9, 20, tzinfo=UTC)
    while minute <= t1:
        x = X(minute)
        major = minute.minute % 5 == 0
        f.line(x, ya, x, ya + (10 if major else 5), MUTED, 1.5)
        if major:
            f.line(x, 60, x, ya, RULE, 1)
            f.text(x, ya + 32, minute.strftime("%H:%M"), 19, MUTED)
        minute += timedelta(minutes=1)
    f.text(x0 - 46, ya + 32, "UTC", 19, MUTED, anchor="end")
    return f


def fig_pointing(acqs):
    by = {a.key: a for a in acqs}
    tune, liss = by[145609, 1], by[145609, 2]
    t_pointing = sum(d for d, _ in QL_POINTING)
    t0 = tune.start.replace(second=50)
    t1 = liss.end + timedelta(seconds=t_pointing + 22)
    x0, x1 = 250, W - 10
    span = (t1 - t0).total_seconds()

    def X(t):
        return x0 + (t - t0).total_seconds() * (x1 - x0) / span

    def dt(a, b):
        return (b - a).total_seconds()

    f = Fig(
        "pointing",
        "Pointing obsnum 145609: Tune scan 1, Lissajous scan 2, and quicklook",
        490,
    )
    rows = [
        "toltec0 data",
        "Tlaloc waits",
        "reduce.sh",
        "file closed",
        "QL, v3",
        "QL, v2",
        "operator",
    ]
    ys = [28, 88, 148, 208, 268, 328, 388]
    for label, y in zip(rows, ys, strict=True):
        f.text(0, y + 26, label, 21, INK, 700, "start")
    f.text(0, ys[1] + 48, "recorded: reduce, load", 16, MUTED, anchor="start")
    v2c, v3c = "#9fb0c3", ROLE["inline"][1]
    f.text(0, ys[2] + 48, "slowest of 10, Docker", 16, MUTED, anchor="start")
    y = ys[0]
    (b0s, b0e), (b1s, b1e) = tune.blocks
    for a, b, lab in [(b0s, b0e, "b0"), (b1s, b1e, "b1")]:
        f.rect(X(a), y, X(b) - X(a), 40, BAR["Tune"], rx=3)
        f.text((X(a) + X(b)) / 2, y + 27, lab, 17, "#fff", 700)
    ls, le = liss.blocks[0]
    f.rect(X(ls), y, X(le) - X(ls), 40, BAR["Lissajous"], rx=3)
    f.text(
        (X(ls) + X(le)) / 2, y + 27, f"Lissajous · {dt(ls, le):.0f} s", 20, "#fff", 700
    )
    f.text(X(tune.start), y - 8, "scan 1 Tune", 19, BAR["Tune"], 700, "start")
    f.text(X(liss.start), y - 8, "scan 2 Lissajous", 19, BAR["Lissajous"], 700, "start")
    y = ys[1]
    for a, b in [(b0e, b1s), (b1e, tune.end)]:
        f.rect(X(a), y, X(b) - X(a), 40, ROLE["inline"][0], v3c, rx=4)
        f.text((X(a) + X(b)) / 2, y + 27, f"{dt(a, b):.1f} s", 20, v3c, 700)
    y = ys[2]
    for i, start in enumerate((b0e, b1e)):
        for dy, version, color in [(0, "v2", v2c), (22, "v3", v3c)]:
            seconds = REDUCE_PER_NETWORK[version][i]
            end = start + timedelta(seconds=seconds)
            f.rect(X(start), y + dy, X(end) - X(start), 16, color, rx=3)
            f.text(
                X(end) + 6,
                y + dy + 14,
                f"{version} {seconds:.1f} s",
                16,
                INK if version == "v2" else v3c,
                700,
                "start",
            )
    y = ys[3]
    for t, lab in [(tune.end, "scan 1"), (liss.end, "scan 2")]:
        f.line(X(t), ys[0], X(t), ys[6] + 40, "#8a9aab", 1.5, "5 5")
        f.diamond(X(t), y + 20, 11, ROLE["db"][1])
        f.text(
            X(t) + 18, y + 27, f"{lab} {t:%H:%M:%S}", 19, ROLE["db"][1], 700, "start"
        )
    qs = ROLE["ql"][1]
    y = ys[4]
    t_int = _utc(tune.end.timestamp() + QL_TUNE_V3)
    f.diamond(X(t_int), y + 20, 11, qs)
    f.text(X(t_int) + 18, y + 27, f"Tune QL, +{QL_TUNE_V3:.0f} s", 19, qs, 700, "start")
    fills = {
        "start": ("#e4e9ef", "#8a9aab"),
        "prepare": ("#ddd0f5", qs),
        "Citlali": (qs, qs),
    }
    t = liss.end
    for seconds, stage in QL_POINTING:
        end = t + timedelta(seconds=seconds)
        fill, stroke = fills[stage]
        f.rect(X(t), y + 6, X(end) - X(t), 28, fill, stroke, rx=3, sw=1.5)
        t = end
    f.text(X(t) - 16, y + 26, "Citlali", 16, "#fff", 700, "end")
    f.diamond(X(t), y + 20, 11, qs)
    f.text(X(t) + 16, y + 27, f"+{t_pointing:.0f} s", 19, qs, 700, "start")
    f.text(
        X(liss.end),
        y + 54,
        " · ".join(f"{stage} {seconds:.1f}" for seconds, stage in QL_POINTING) + " s",
        16,
        MUTED,
        anchor="start",
    )
    y = ys[5]
    t_v2 = _utc(tune.end.timestamp() + QL_TUNE_V2)
    f.diamond(X(t_v2), y + 20, 11, "#a796c9")
    f.text(
        X(t_v2) - 18, y + 27, f"Tune QL, +{QL_TUNE_V2:.0f} s", 19, "#7f6aa8", 700, "end"
    )
    f.text(
        X(liss.end) + 18,
        y + 27,
        "pointing map: not measured",
        17,
        MUTED,
        anchor="start",
    )
    y = ys[6]
    f.diamond(X(liss.end) + 30, y + 20, 11, ROLE["operator"][1])
    f.text(
        X(liss.end) + 48, y + 27, "query 145609", 19, ROLE["operator"][1], 700, "start"
    )
    ya = 452
    f.line(x0, ya, x1, ya, MUTED, 1.5)
    t = t0.replace(second=0) + timedelta(minutes=1)
    while t <= t1:
        x = X(t)
        f.line(x, ya, x, ya + 8, MUTED, 1.5)
        f.text(x, ya + 28, t.strftime("%H:%M:%S"), 18, MUTED)
        t += timedelta(seconds=30)
    return f


def fig_inline_time():
    f = Fig(
        "inline-time",
        "Inline reduction per OT step: slowest of 10 networks started at once",
        410,
    )
    x0, x1, vmax = 250, W - 90, 16.0

    def X(v):
        return x0 + v * (x1 - x0) / vmax

    x = 0
    for name, (light, dark) in INLINE_COLOR.items():
        f.rect(x, 4, 12, 20, light, rx=2)
        f.rect(x + 12, 4, 14, 20, dark, rx=2)
        f.text(x + 34, 21, name, 18, MUTED, anchor="start")
        x += 60 + text_width(name, 18)
    f.text(W - 2, 21, "light: clip side · dark: Taca", 18, MUTED, anchor="end")
    y = 46
    for label, bars in INLINE_REQUEST:
        f.text(0, y + 32, label, 21, INK, 700, "start")
        for dy, (name, clip, taca) in zip((0, 28), bars, strict=True):
            light, dark = INLINE_COLOR[name]
            f.rect(X(0), y + dy, X(clip) - X(0), 22, light, rx=2)
            f.rect(X(clip), y + dy, X(clip + taca) - X(clip), 22, dark, rx=2)
            f.text(
                X(clip + taca) + 8,
                y + dy + 18,
                f"{clip + taca:.1f} s",
                18,
                INK,
                anchor="start",
            )
        y += 66
    for v in range(0, int(vmax) + 1, 4):
        f.line(X(v), 38, X(v), y - 4, RULE, 1)
        f.text(X(v), y + 20, f"{v} s", 18, MUTED)
    return f


def fig_ql_time():
    f = Fig("ql-time", "Valid to quicklook available: v2, v3 previous, v3", 490)
    x0, x1, vmax = 290, W - 70, 70.0

    def X(v):
        return x0 + v * (x1 - x0) / vmax

    for i, key in enumerate(("trigger", "other", "recompute", "ql", "register")):
        fill, stroke, label = QL_STAGE[key]
        lx, ly = x0 + (i % 3) * 290, 4 + (i // 3) * 30
        f.rect(lx, ly, 22, 22, fill, stroke, rx=4)
        f.text(lx + 30, ly + 18, label, 18, MUTED, anchor="start")
    y = 76
    for acq_label, variants in QL_TIME:
        f.text(0, y + 18, acq_label, 22, INK, 700, "start")
        y += 30
        for name, stages in variants:
            f.text(20, y + 26, name, 20, MUTED, 700, "start")
            for a, b, key in stages:
                fill, stroke, _ = QL_STAGE[key]
                f.rect(X(a), y, X(b) - X(a), 36, fill, stroke, rx=3, sw=1.5)
            total = stages[-1][1]
            f.text(X(total) + 8, y + 25, f"{total:.1f} s", 20, INK, 700, "start")
            y += 46
        y += 14
    for v in range(0, 71, 10):
        f.line(X(v), 50, X(v), y - 8, RULE, 1)
        f.text(X(v), y + 16, f"{v} s", 18, MUTED)
    return f


def fig_inline_steps():
    f = Fig("inline-steps", "Inline reduction of one sweep block", 420)
    acq, inl = ROLE["acq"][1], ROLE["inline"][1]
    f.box(0, 20, 200, 84, "Tlaloc", "reduce_do, waits", "acq")
    f.box(250, 20, 250, 84, "reduce.sh", "clip: bind, then install", "inline")
    f.poly([(202, 62), (242, 62)], acq)
    f.poly([(502, 50), (566, 50)], inl)
    f.text(534, 38, "SSH", 18, MUTED, halo=True)
    f.rect(574, 0, W - 576, 236, ROLE["inline"][0], inl, rx=16, dash=True)
    f.text(596, 34, "Taca worker", 22, inl, 700, "start")
    for i, step in enumerate(["SweepCheck", "KidsFind", "TonePrep", "TlalocOutput"]):
        x = 596 + i * 136
        f.rect(x, 56, 124, 56, "#fff", inl, rx=10)
        f.text(x + 62, 91, step, 18, inl, 700)
        if i:
            f.poly([(x - 12, 84), (x - 2, 84)], inl, 2)
    f.text(596, 142, "every sweep: tones for the next load", 19, MUTED, anchor="start")
    f.rect(596, 162, 180, 52, "#fff", inl, rx=10, dash=True)
    f.text(686, 195, "native fit", 19, inl, 700)
    f.text(790, 195, "Target, Tune: model", 19, MUTED, anchor="start")
    f.poly([(574, 190), (450, 190), (450, 108)], inl, 2.5, "7 6")
    f.text(512, 180, "result", 18, MUTED, halo=True)
    f.box(230, 270, 290, 70, "etc/: tones + model", "", "inline", 21)
    f.poly([(330, 104), (330, 264)], inl)
    f.poly([(226, 305), (100, 305), (100, 110)], acq)
    f.text(0, 372, "targ_read_file: tones + model", 19, acq, 700, "start")
    db = ROLE["db"][1]
    f.box(574, 300, W - 576, 64, "KidsFind + tone tables, staged", "", "db", 20)
    f.poly([(860, 238), (860, 294)], db, 2, "6 5")
    f.text(
        574,
        400,
        "one version per acquisition, registered after Valid",
        19,
        db,
        700,
        "start",
    )
    return f


def fig_ql_versions():
    f = Fig(
        "ql-versions",
        "Quicklook version groups for one pointing obsnum and its lineage",
        400,
    )
    q = ROLE["ql"]
    tag = ROLE["operator"][1]
    groups = [
        (
            "obsnum 145609",
            20,
            250,
            [
                ("v1", "Tune feedback", "after scan 1"),
                ("v2", "pointing + Tune", "after scan 2"),
            ],
        ),
        (
            "lineage since VNA",
            210,
            140,
            [
                ("v1", "VNA", "145605"),
                ("v2", "+ target", "145606"),
                ("v3", "+ target", "145607"),
                ("v4", "+ Tune", "145608"),
                ("v5", "+ Tune", "145609"),
            ],
        ),
    ]
    for label, y, w, versions in groups:
        f.text(0, y + 50, label, 22, INK, 700, "start")
        f.text(0, y + 78, "dp_quicklook", 19, MUTED, anchor="start", font=MONO)
        x = 300
        for i, (v, what, when) in enumerate(versions):
            last = i == len(versions) - 1
            f.rect(
                x, y + 14, w, 84, q[0] if last else "#fff", q[1], rx=10, dash=not last
            )
            f.text(x + w / 2, y + 46, f"{v} · {what}", 19, q[1], 700)
            f.text(
                x + w / 2,
                y + 76,
                when,
                18,
                MUTED,
                font=MONO if when[0].isdigit() else FONT,
            )
            if not last:
                f.poly([(x + w + 4, y + 56), (x + w + 20, y + 56)], q[1], 2)
                x += w + 26
        cx = x + w / 2
        f.parts.append(f'<path d="M{cx:.1f} {y + 102}l-10 14h20z" fill="{tag}"/>')
        label = "tag: current → QL server"
        f.text(min(cx, W - text_width(label, 19) / 2), y + 140, label, 19, tag, 700)
    return f


# Detector power setup (part 2): the detector setup specification's worked
# network-0 example, fit 145484 (subobservations 1-7, 16-4 dB) and commit target
# 145485, replayed by run/detector-power-setup-20261022 (results.json).
POWER_PRODUCTS = (
    WORKSPACE
    / "run/detector-power-setup-20261022/replayed-example/dataprod_toltec/scratch"
)
POWER_CHANNEL = 450
POWER_RAMP = [
    "#c6dbef",
    "#9ecae1",
    "#6baed6",
    "#4292c6",
    "#2171b5",
    "#08519c",
    "#08306b",
]


def _power_result(pattern, node):
    (path,) = POWER_PRODUCTS.glob(f"{pattern}/*/artifacts/toltec0/*/result.zarr")
    return xr.open_datatree(path, engine="zarr")[node].to_dataset()


def _axis(f, x0, x1, y0, y1, xticks, yticks, X, Y, xlabel, ylabel):
    """Frame, ticks and labels of one data panel."""
    for v in yticks:
        f.line(x0, Y(v), x1, Y(v), RULE, 1)
        f.text(x0 - 10, Y(v) + 6, f"{v:g}", 17, MUTED, anchor="end")
    f.line(x0, y1, x1, y1, MUTED, 1.5)
    for v in xticks:
        f.line(X(v), y1, X(v), y1 + 7, MUTED, 1.5)
        f.text(X(v), y1 + 27, f"{v:g}", 17, MUTED)
    f.text((x0 + x1) / 2, y1 + 54, xlabel, 18, MUTED)
    f.text(x0 - 4, y0 - 14, ylabel, 18, MUTED, anchor="start")


def fig_power_fit():
    d = _power_result("145484-1-1/*", "drive_fit")
    c = POWER_CHANNEL
    atten = -d.power.to_numpy()
    f = Fig(
        "power-fit",
        f"Drive fit of network 0 channel {c}: sweeps and nonlinearity per attenuation",
        400,
    )
    # (a) |S21| per attenuation, relative to the first sample.
    x0, x1, y0, y1 = 70, 500, 50, 320
    fp = float(d.f_chan[c])

    def XA(v):
        return x0 + (v + 180) * (x1 - x0) / 360

    def YA(v):
        return y0 + (0.2 - v) * (y1 - y0) / 1.8

    _axis(
        f,
        x0,
        x1,
        y0,
        y1,
        (-150, -75, 0, 75, 150),
        (0, -0.5, -1, -1.5),
        XA,
        YA,
        "frequency − probe (kHz)",
        "|S21| (dB)",
    )
    for k in range(len(atten)):
        z = d.I.to_numpy()[k, c] + 1j * d.Q.to_numpy()[k, c]
        mag = 20 * np.log10(np.abs(z) / np.abs(z[0]))
        dx = (d.frequency.to_numpy()[k, c] - fp) / 1e3
        f.poly(
            [(XA(u), YA(v)) for u, v in zip(dx, mag, strict=True)],
            POWER_RAMP[k],
            2.2,
            arrow=False,
        )
    f.text(x1 - 92, y0 - 14, f"{atten[0]:.0f} dB", 18, POWER_RAMP[1], 700, "end")
    f.text(x1 - 70, y0 - 14, "→", 18, MUTED, 400)
    f.text(x1, y0 - 14, f"{atten[-1]:.0f} dB", 18, POWER_RAMP[-1], 700, "end")
    # (b) nonlinearity a per attenuation and the a_ref crossing.
    x0, x1 = 660, W - 30

    def XB(v):
        return x0 + (17 - v) * (x1 - x0) / 14

    def YB(v):
        return y0 + (1.25 - v) * (y1 - y0) / 1.55

    f.rect(x0, YB(1.25), x1 - x0, YB(-0.2) - YB(1.25), "#f2f7f5", rx=0)
    _axis(
        f,
        x0,
        x1,
        y0,
        y1,
        (16, 14, 12, 10, 8, 6, 4),
        (-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2),
        XB,
        YB,
        "drive attenuation (dB) → more power",
        "nonlinearity a",
    )
    f.line(x0, YB(0.2), x1, YB(0.2), ROLE["operator"][1], 2, "7 5")
    f.text(
        x0 + 8,
        YB(0.2) - 9,
        "a_ref = 0.2",
        17,
        ROLE["operator"][1],
        700,
        "start",
        halo=True,
    )
    a = d.a.to_numpy()[:, c]
    f.poly(
        [(XB(u), YB(v)) for u, v in zip(atten, a, strict=True)], MUTED, 2, arrow=False
    )
    for k, (u, v) in enumerate(zip(atten, a, strict=True)):
        f.dot(XB(u), YB(v), 6.5, POWER_RAMP[k], "#fff")
    best = float(d.adrv_best[c])
    f.diamond(XB(best), YB(0.2), 10, ROLE["inline"][1])
    f.text(
        XB(best) + 14,
        YB(0.2) + 30,
        f"selected {best:.2f} dB",
        18,
        ROLE["inline"][1],
        700,
        "start",
        halo=True,
    )
    return f


def fig_power_commit():
    d = _power_result("145485-0-1/*", "drive_fit_commit")
    fit = d.adrv_best_adrv.to_numpy()
    policy = d.adrv_best.to_numpy()
    accepted = (d.flag_adrv.to_numpy() == 0) & (fit < 30)
    raised = accepted & (policy > fit)
    mhz = d.f_chan.to_numpy() / 1e6
    f = Fig(
        "power-commit",
        "Commit of the network 0 drive fit to target 145485: attenuations and amplitudes",
        380,
    )
    y0, y1 = 64, 300
    lo, hi = 440, 920

    def X(v, x0, x1):
        return x0 + (v - lo) * (x1 - x0) / (hi - lo)

    # (a) requested attenuation per tone after the fill and cutoff policy.
    x0, x1 = 70, 520

    def YA(v):
        return y0 + (17 - v) * (y1 - y0) / 13

    _axis(
        f,
        x0,
        x1,
        y0,
        y1,
        (500, 600, 700, 800, 900),
        (4, 8, 12, 16),
        lambda v: X(v, x0, x1),
        YA,
        "tone frequency (MHz)",
        "requested attenuation (dB)",
    )
    groups = [
        (
            accepted & ~raised,
            ROLE["inline"][1],
            f"fit {int((accepted & ~raised).sum())}",
        ),
        (
            raised,
            ROLE["operator"][1],
            f"raised to {policy[raised].min():g} dB {int(raised.sum())}",
        ),
        (
            ~accepted,
            "#8a9aab",
            f"median {policy[~accepted].min():.2f} dB {int((~accepted).sum())}",
        ),
    ]
    lx = x0
    for mask, color, label in groups:
        for u, v in zip(mhz[mask], policy[mask], strict=True):
            f.dot(X(u, x0, x1), YA(v), 3.2, color)
        f.dot(lx + 6, 22, 6, color)
        f.text(lx + 18, 28, label, 17, MUTED, anchor="start")
        lx += 30 + text_width(label, 17)
    # (b) amplitudes: target input (LUT mode) and committed replacement.
    x0, x1 = 680, W - 30

    def YB(v):
        return y0 + (1.05 - v) * (y1 - y0) / 1.05

    _axis(
        f,
        x0,
        x1,
        y0,
        y1,
        (500, 600, 700, 800, 900),
        (0, 0.25, 0.5, 0.75, 1),
        lambda v: X(v, x0, x1),
        YB,
        "tone frequency (MHz)",
        "amplitude coefficient",
    )
    lx = x0
    for values, color, label in [
        (d.amp_tone.to_numpy(), "#8a9aab", "input (LUT)"),
        (d.amp_best.to_numpy(), ROLE["inline"][1], "committed b"),
    ]:
        for u, v in zip(mhz, values, strict=True):
            f.dot(X(u, x0, x1), YB(v), 3.2, color)
        f.dot(lx + 6, 22, 6, color)
        f.text(lx + 18, 28, label, 17, MUTED, anchor="start")
        lx += 40 + text_width(label, 17)
    return f


def fig_power_toneprep():
    f = Fig(
        "power-toneprep",
        "TonePrep carries each probe's amplitude to the tones found near it",
        270,
    )
    inl, acq = ROLE["inline"][1], ROLE["acq"][1]
    base_in, base_out, scale = 110, 236, 80
    f.text(0, base_in - 30, "acquired comb", 19, acq, 700, "start")
    f.text(0, base_in - 6, "input probes", 17, MUTED, anchor="start")
    f.text(0, base_out - 30, "next comb", 19, inl, 700, "start")
    f.text(0, base_out - 6, "prepared tones", 17, MUTED, anchor="start")
    f.line(170, base_in, 760, base_in, RULE, 1.5)
    f.line(170, base_out, 760, base_out, RULE, 1.5)
    probes = [(220, 0.55), (340, 0.9), (470, 0.45), (620, 0.7)]
    tones = [
        (228, 0, "match"),
        (334, 1, "match"),
        (448, 2, "ambiguous"),
        (494, 2, "ambiguous"),
        (640, 3, "match"),
    ]
    for x, h in probes:
        f.rect(x - 9, base_in - h * scale, 18, h * scale, ROLE["acq"][0], acq, rx=2)
    lut = {448: 0.62, 494: 0.58}
    for x, i, kind in tones:
        px, h = probes[i]
        f.line(
            px,
            base_in + 4,
            x,
            base_out - h * scale - 6,
            "#8a9aab",
            1.5,
            "4 4" if kind == "ambiguous" else None,
        )
        f.rect(x - 9, base_out - h * scale, 18, h * scale, ROLE["inline"][0], inl, rx=2)
        if kind == "ambiguous":
            f.rect(
                x - 13,
                base_out - lut[x] * scale,
                26,
                lut[x] * scale,
                "none",
                ROLE["operator"][1],
                rx=2,
                dash=True,
            )
    curve = [
        (x, base_out - (0.75 - 0.0004 * (x - 300)) * scale) for x in range(400, 545, 8)
    ]
    f.poly(curve, ROLE["operator"][1], 2, "3 5", arrow=False)
    f.text(
        560,
        base_out - 0.66 * scale,
        "optional LUT fill k·ℓ(f)",
        17,
        ROLE["operator"][1],
        700,
        "start",
        halo=True,
    )
    f.text(800, 64, "every prepared tone", 19, INK, 700, "start")
    for i, line in enumerate(
        [
            "keeps its probe's amplitude",
            "coefficients scaled to ≤ 1",
            "drive attenuation unchanged",
            "phases: random or from file",
        ]
    ):
        f.text(800, 100 + i * 34, "· " + line, 18, MUTED, anchor="start")
    f.text(760, 266, "schematic", 15, MUTED, anchor="end")
    return f


def fig_power_lifecycle():
    f = Fig(
        "power-lifecycle",
        "Tone amplitudes and drive attenuation through the detector setup scripts",
        440,
    )
    stages = [
        ("10 · init coarse", "VNA: new calibration\ngroup, 1000 tones"),
        ("12 · tune", "sweep, reduce, load;\nTune"),
        ("21 · power setup", "series, fit, commit,\nreload, verify Tune"),
        ("observe", "Tune + science scans;\nretune as needed"),
        ("13 · reinit", "new VNA, refine,\ncommit a saved fit"),
    ]
    rows = [
        (
            "tone amplitudes",
            [
                ("LUT ℓ(f)", "acq"),
                ("LUT ℓ(f)", "acq"),
                ("LUT → committed b", "inline"),
                ("committed b, carried\nby TonePrep", "inline"),
                ("LUT → committed b", "inline"),
            ],
        ),
        (
            "drive attenuation",
            [
                ("A₀ (indexed)", "db"),
                ("A₀", "db"),
                ("A₀ ± 6 dB → A_out", "operator"),
                ("A_out", "db"),
                ("kept → new A_out", "operator"),
            ],
        ),
        (
            "products",
            [
                ("", None),
                ("", None),
                ("drive fit, commit", "ql"),
                ("", None),
                ("commit (pinned fit)", "ql"),
            ],
        ),
    ]
    x0, gap = 170, 14
    w = (W - x0 - gap * (len(stages) - 1)) / len(stages)
    for i, (title, sub) in enumerate(stages):
        x = x0 + i * (w + gap)
        f.rect(
            x,
            0,
            w,
            96,
            "#fff",
            INK if i in (2, 4) else "#8a9aab",
            rx=10,
            sw=2.5 if i in (2, 4) else 1.5,
        )
        f.text(x + w / 2, 30, title, 20, INK, 700)
        f.text(x + w / 2, 58, sub, 16, MUTED)
        if i:
            f.poly([(x - gap + 1, 48), (x - 2, 48)], MUTED, 2)
    y = 124
    for label, cells in rows:
        f.text(0, y + 40, label, 19, INK, 700, "start")
        for i, (text, role) in enumerate(cells):
            if role is None:
                continue
            fill, stroke = ROLE[role]
            x = x0 + i * (w + gap)
            f.rect(x, y, w, 70, fill, stroke, rx=8)
            n = text.count("\n")
            f.text(x + w / 2, y + 42 - n * 11, text, 17, stroke, 700)
        y += 92
    f.text(
        x0,
        424,
        "LUT: Tlaloc evaluates the amplitude LUT at each load.  FILE: loads use the prepared or committed amplitudes.",
        16,
        MUTED,
        anchor="start",
    )
    return f


def fig_power_v3_flow():
    f = Fig(
        "power-v3-flow",
        "v3 detector power setting: dBm targets, prepared tone configuration, applied and reported state",
        284,
    )
    boxes = [
        ("Drive fit", "dBm target\nper detector", "inline"),
        ("TonePrep", "amplitudes, phases,\ngain, attenuation", "inline"),
        ("Tone\nconfiguration", "one table,\none identifier", "db"),
        ("Tlaloc", "validate, apply,\nreport", "acq"),
        ("Acquisition", "applied state\nin metadata", "acq"),
    ]
    gap = 34
    w = (W - gap * (len(boxes) - 1)) / len(boxes)
    for i, (title, sub, role) in enumerate(boxes):
        fill, stroke = ROLE[role]
        x = i * (w + gap)
        f.rect(x, 0, w, 128, fill, stroke, rx=12)
        n = title.count("\n")
        f.text(x + w / 2, 34 - n * 12, title, 21, stroke, 700)
        f.text(x + w / 2, 84, sub, 17, MUTED)
        if i:
            f.poly([(x - gap + 2, 64), (x - 3, 64)], stroke, 2.5)
    cfg_fill, cfg_stroke = ROLE["operator"]
    cw = 2 * w + gap
    f.rect(0, 196, cw, 84, cfg_fill, cfg_stroke, rx=12)
    f.text(cw / 2, 228, "ROACH power-chain config", 20, cfg_stroke, 700)
    f.text(
        cw / 2,
        258,
        "stage gains and attenuations; versioned, stored with results",
        17,
        MUTED,
    )
    for i in (0, 1):
        x = i * (w + gap) + w / 2
        f.poly([(x, 194), (x, 132)], cfg_stroke, 2, "6 5")
    sx = 3 * (w + gap)
    f.rect(sx, 196, W - sx, 84, *ROLE["inline"], rx=12)
    f.text(
        sx + (W - sx) / 2, 228, "SweepCheck readout power", 20, ROLE["inline"][1], 700
    )
    f.text(sx + (W - sx) / 2, 258, "dBm per stage, every sweep", 17, MUTED)
    ax = 4 * (w + gap) + w / 2
    f.poly([(ax, 130), (ax, 192)], ROLE["acq"][1], 2.5)
    f.poly([(cw + 2, 238), (sx - 4, 238)], cfg_stroke, 2, "6 5")
    f.text((cw + sx) / 2, 230, "same model", 16, MUTED, halo=True)
    return f


SEQUENCES = {
    "sweep-cycle": {
        "title": "One sweep, reduce and load cycle",
        "row": 41,
        "lanes": [
            ("ot", "OT script", "operator"),
            ("t", "Tlaloc · per network", "acq"),
            ("db", "ToltecDB", "db"),
            ("w", "reduce.sh → Taca", "inline"),
            ("r", "ROACH", "acq"),
        ],
        "rows": [
            {
                "kind": "msg",
                "a": "ot",
                "b": "t",
                "text": "VnaSweep Cal · TargSweep Cal",
            },
            {"kind": "act", "a": "t", "text": "sweep, close file"},
            {"kind": "msg", "a": "t", "b": "db", "text": "Valid = 1"},
            {"kind": "msg", "a": "ot", "b": "t", "text": "VnaReduce · TargReduce"},
            {"kind": "msg", "a": "t", "b": "w", "text": "reduce.sh, Tlaloc waits"},
            {
                "kind": "act",
                "a": "w",
                "text": "SweepCheck → KidsFind\n→ TonePrep → TlalocOutput",
                "h": 70,
            },
            {
                "kind": "msg",
                "a": "w",
                "b": "t",
                "text": "report installed",
                "dashed": True,
            },
            {"kind": "msg", "a": "ot", "b": "t", "text": "TargLoadFromFile"},
            {"kind": "msg", "a": "t", "b": "r", "text": "read report, upload tones"},
        ],
    },
    "tune-sequence": {
        "title": "Tune Cal inside Tlaloc, with recorded times of 145609",
        "row": 42,
        "lanes": [
            ("ot", "OT script", "operator"),
            ("t", "Tlaloc", "acq"),
            ("w", "reduce.sh → Taca", "inline"),
            ("r", "ROACH", "acq"),
            ("db", "ToltecDB", "db"),
        ],
        "x1": W - 220,
        "spans": (
            "145609",
            [(1, 1, "8.5 s"), (2, 4, "27.5 s"), (5, 5, "8.5 s"), (6, 8, "9.6 s")],
        ),
        "rows": [
            {"kind": "msg", "a": "ot", "b": "t", "text": "Tune Cal"},
            {"kind": "act", "a": "t", "text": "block 0: sweep"},
            {"kind": "msg", "a": "t", "b": "w", "text": "reduce.sh (block 0)"},
            {
                "kind": "msg",
                "a": "w",
                "b": "t",
                "text": "tones + model",
                "dashed": True,
            },
            {"kind": "msg", "a": "t", "b": "r", "text": "targ_load: upload tones"},
            {"kind": "act", "a": "t", "text": "block 1: sweep"},
            {"kind": "msg", "a": "t", "b": "w", "text": "reduce.sh (block 1)"},
            {
                "kind": "msg",
                "a": "w",
                "b": "t",
                "text": "model for the next scan",
                "dashed": True,
            },
            {"kind": "msg", "a": "t", "b": "db", "text": "close file: Valid = 1"},
        ],
    },
    "power-v3-tune": {
        "title": "v3 Tune: the prepared comb and attenuation are applied together between the two sweeps",
        "row": 36,
        "x0": 130,
        "x1": W - 130,
        "lanes": [
            ("t", "Tlaloc (Tune Cal)", "acq"),
            ("w", "reduce.sh → TonePrep", "inline"),
            ("r", "ROACH, attenuator", "acq"),
        ],
        "rows": [
            {"kind": "act", "a": "t", "text": "block 0: sweep"},
            {"kind": "msg", "a": "t", "b": "w", "text": "reduce.sh (block 0)"},
            {
                "kind": "act",
                "a": "w",
                "text": "comb, gain, attenuation for the targets",
                "h": 44,
            },
            {
                "kind": "msg",
                "a": "w",
                "b": "t",
                "text": "tone configuration",
                "dashed": True,
            },
            {"kind": "msg", "a": "t", "b": "r", "text": "apply waveform + attenuation"},
            {
                "kind": "msg",
                "a": "r",
                "b": "t",
                "text": "readback, settle",
                "dashed": True,
            },
            {"kind": "act", "a": "t", "text": "block 1: sweep"},
            {"kind": "msg", "a": "t", "b": "w", "text": "reduce.sh (block 1)"},
            {
                "kind": "msg",
                "a": "w",
                "b": "t",
                "text": "model for the next scan",
                "dashed": True,
            },
        ],
    },
    "ql-sequence": {
        "title": "Quicklook from a valid file to the operator's query",
        "row": 42,
        "lanes": [
            ("t", "Tlaloc", "acq"),
            ("db", "ToltecDB", "db"),
            ("s", "Dagster sensor", "db"),
            ("q", "Quicklook run", "ql"),
            ("api", "QL server", "ql"),
            ("mc", "MC · operator", "operator"),
        ],
        "x0": 90,
        "x1": W - 100,
        "rows": [
            {"kind": "msg", "a": "t", "b": "db", "text": "Valid = 1"},
            {"kind": "msg", "a": "s", "b": "db", "text": "poll, 5 s loop"},
            {"kind": "act", "a": "s", "text": "all interfaces valid"},
            {"kind": "msg", "a": "s", "b": "q", "text": "run request"},
            {"kind": "act", "a": "s", "text": "+ raw ingestion request", "role": "db"},
            {"kind": "act", "a": "q", "text": "wait for inline results (bounded)"},
            {"kind": "act", "a": "q", "text": "collect, plot, summarize"},
            {"kind": "msg", "a": "q", "b": "api", "text": "register dp_quicklook"},
            {"kind": "msg", "a": "mc", "b": "api", "text": "query obsnum"},
            {
                "kind": "msg",
                "a": "api",
                "b": "mc",
                "text": "current version",
                "dashed": True,
            },
        ],
    },
}


def render():
    acqs, tune_offsets, _ = load_acquisitions()
    figs = [
        fig_workflows(),
        fig_night(acqs, tune_offsets),
        fig_pointing(acqs),
        fig_inline_steps(),
        fig_inline_time(),
        fig_ql_time(),
        fig_ql_versions(),
        fig_power_toneprep(),
        fig_power_fit(),
        fig_power_commit(),
        fig_power_lifecycle(),
        fig_power_v3_flow(),
    ]
    for name, spec in SEQUENCES.items():
        kw = {k: spec[k] for k in ("x0", "x1", "row", "spans") if k in spec}
        figs.append(Sequence(name, spec["title"], spec["lanes"], spec["rows"], **kw))
    deck = DECK.read_text()
    for fig in figs:
        pattern = re.compile(
            rf'<svg id="fig-{re.escape(fig.name)}".*?</svg>', re.DOTALL
        )
        match = pattern.search(deck)
        if match is None:
            msg = f'Deck has no <svg id="fig-{fig.name}"> block'
            raise ValueError(msg)
        deck = deck[: match.start()] + fig.svg() + deck[match.end() :]
    DECK.write_text(deck)
    for a in acqs:
        print(
            f"{a.obsnum}-{a.scan} {a.program:9s} {a.start:%H:%M:%S}–{a.end:%H:%M:%S} ({a.end_source})"
        )


if __name__ == "__main__":
    render()
