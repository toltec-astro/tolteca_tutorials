"""Build the overview's editable SVG diagrams with explicit slide geometry."""

from html import escape
from pathlib import Path

OUT = Path(__file__).parent / "assets"
INK = "#12283f"
MUTED = "#52677b"
COLORS = {
    "data": ("#e9f1ff", "#316cc5"),
    "compute": ("#e6f5f0", "#008278"),
    "product": ("#f0eafd", "#7653b7"),
    "access": ("#fff2de", "#a45b0b"),
    "neutral": ("#f0f4f8", "#52677b"),
}


class Diagram:
    def __init__(self, name, title, height=490, width=1152):
        self.name = name
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
            f"<title>{escape(title)}</title>",
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#70869a"/></marker></defs>',
        ]

    def text(self, x, y, text, size=25, color=INK, weight=400, anchor="middle"):
        for i, line in enumerate(text.split("\n")):
            self.parts.append(
                f'<text x="{x}" y="{y + i * (size + 8)}" text-anchor="{anchor}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(line)}</text>'
            )

    def box(self, x, y, w, h, title, subtitle="", kind="data", size=27):
        fill, stroke = COLORS[kind]
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
        )
        lines = title.count("\n") + 1
        baseline = (
            y
            + h / 2
            - ((lines - 1) * (size + 8)) / 2
            + size * 0.32
            - (14 if subtitle else 0)
        )
        self.text(x + w / 2, baseline, title, size, stroke, 700)
        if subtitle:
            self.text(x + w / 2, y + h - 21, subtitle, 21, MUTED)

    def area(self, x, y, w, h, title, kind="neutral"):
        fill, stroke = COLORS[kind]
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{fill}" fill-opacity=".35" stroke="{stroke}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="7 6"/>'
        )
        self.text(x + 22, y + 32, title, 21, stroke, 700, "start")

    def arrow(self, points, label="", lx=None, ly=None, dashed=False):
        coords = " ".join(f"{x},{y}" for x, y in points)
        dash = ' stroke-dasharray="7 6"' if dashed else ""
        self.parts.append(
            f'<polyline points="{coords}" fill="none" stroke="#70869a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" marker-end="url(#arrow)"{dash}/>'
        )
        if label:
            self.text(lx, ly, label, 21, MUTED)

    def save(self):
        (OUT / f"{self.name}.svg").write_text("\n".join(self.parts + ["</svg>"]))


d = Diagram("cover", "Acquire, process, publish and explore", 220)
for x, title, subtitle, kind in [
    (0, "Acquire", "files + records", "data"),
    (300, "Process", "blocks + diagnostics", "compute"),
    (600, "Publish", "products + provenance", "product"),
    (900, "Explore", "observer + curator", "access"),
]:
    d.box(x, 40, 240, 125, title, subtitle, kind)
    if x < 900:
        d.arrow([(x + 244, 102), (x + 289, 102)])
d.save()

d = Diagram(
    "lifecycle",
    "Acquisition through processing, publication, inspection and reprocessing",
)
for x, title, subtitle, kind in [
    (0, "Plan", "coverage + time", "access"),
    (235, "Acquire", "files + records", "data"),
    (470, "Process", "reduce + check", "compute"),
    (705, "Publish", "arrays + figures", "product"),
    (940, "Inspect", "quicklook + viewer", "access"),
]:
    d.box(x, 72, 205, 132, title, subtitle, kind)
    if x < 940:
        d.arrow([(x + 207, 138), (x + 225, 138)])
d.box(
    420,
    310,
    465,
    100,
    "Data Product Database",
    "identity · provenance · relationships",
    "product",
)
d.arrow([(337, 204), (337, 360), (409, 360)], "catalog", 280, 290)
d.arrow([(807, 204), (807, 299)], "register", 860, 255)
d.arrow([(885, 360), (1042, 360), (1042, 215)], "discover", 966, 341)
d.arrow(
    [(1042, 72), (1042, 22), (572, 22), (572, 61)],
    "select inputs + configure another run",
    792,
    14,
)
d.text(
    575,
    457,
    "Files and products remain usable through Python and CLI workflows.",
    24,
    MUTED,
)
d.save()

d = Diagram("modes", "Python, CLI and Dagster invoke the same configured workflow")
for x, title, sub in [
    (30, "Python", "analysis + notebooks"),
    (425, "CLI", "manual processing + QA"),
    (820, "Dagster", "sensors + automation"),
]:
    d.box(x, 18, 300, 105, title, sub, "access")
    d.arrow([(x + 150, 125), (x + 150, 168), (576, 168), (576, 197)])
d.box(
    285,
    210,
    582,
    130,
    "Configured application workflow",
    "input selection → steps → publication",
    "compute",
    32,
)
d.box(90, 405, 385, 70, "Artifacts + portable index", kind="product", size=25)
d.box(675, 405, 385, 70, "Optional DB registration", kind="product", size=25)
d.arrow([(440, 340), (440, 371), (282, 371), (282, 395)])
d.arrow([(710, 340), (710, 371), (867, 371), (867, 395)])
d.save()

d = Diagram(
    "hierarchy", "An observation contains acquisitions, interfaces and KIDs blocks"
)
d.box(0, 20, 270, 110, "Observation", "master + obsnum", "data")
d.box(0, 212, 270, 110, "Acquisition", "+ subobsnum + scannum", "data")
d.arrow([(135, 130), (135, 202)], "one → many", 217, 178)
d.area(330, 0, 820, 385, "INTERFACE FILES", "data")
d.box(365, 70, 225, 85, "KIDs readout", kind="data", size=26)
d.box(635, 70, 225, 85, "Telescope", kind="data", size=26)
d.box(900, 70, 215, 85, "HWPR", kind="data", size=26)
d.arrow([(270, 267), (305, 267), (305, 112), (353, 112)])
d.arrow([(478, 155), (478, 204)])
d.box(365, 215, 225, 118, "Block 0", "sweep", "compute")
d.box(635, 215, 225, 118, "Block 1", "sweep", "compute")
d.arrow([(478, 177), (747, 177), (747, 204)])
d.text(1007, 262, "…", 54, MUTED)
d.text(
    370,
    440,
    "Each KIDs block is an independent processing scope.",
    27,
    INK,
    700,
    "start",
)
d.save()

d = Diagram("blocks", "Sweep and timestream processing on one selected KIDs block")
d.box(0, 171, 235, 130, "Raw I / Q", "one block · all channels", "data")
d.box(325, 46, 290, 125, "SweepReduce", "step means + uncertainty", "compute")
d.box(325, 291, 290, 125, "TimestreamReduce", "time-ordered I / Q", "compute")
d.arrow([(235, 236), (277, 236), (277, 108), (314, 108)])
d.arrow([(277, 236), (277, 353), (314, 353)])
d.box(725, 46, 400, 125, "SweepCheck", "flags · despiking · D21", "compute")
d.box(725, 291, 400, 125, "PSD analysis", "channel + common spectra", "compute")
d.arrow([(615, 108), (714, 108)])
d.arrow([(615, 353), (714, 353)])
d.text(925, 218, "Configurable analyses", 23, MUTED)
d.text(
    575, 475, "Results stay with the block in an xarray DataTree → Zarr.", 26, INK, 700
)
d.save()

d = Diagram(
    "operations",
    "Telescope acquisition triggers independent ingestion and quicklook workflows; MC reads registered feedback",
)
d.box(0, 100, 240, 110, "Telescope", "ToltecDB + raw files", "data", 28)
d.box(300, 100, 225, 110, "Dagster", "readiness sensor", "access", 28)
d.arrow([(240, 155), (289, 155)])
d.box(610, 30, 260, 90, "Raw ingestion", kind="compute", size=27)
d.box(610, 190, 260, 100, "KIDs quicklook", "reduce · check · plot", "compute", 27)
d.arrow([(525, 155), (565, 155), (565, 75), (599, 75)])
d.arrow([(565, 155), (565, 240), (599, 240)])
d.text(563, 54, "records", 19, MUTED)
d.text(558, 285, "files ready", 19, MUTED)
d.box(945, 100, 200, 170, "Register\nfeedback", "DPDB + artifacts", "product", 27)
d.arrow([(870, 75), (908, 75), (908, 140), (934, 140)])
d.arrow([(870, 240), (934, 240)])
d.text(740, 159, "Independent workflows", 22, MUTED)
d.box(0, 365, 275, 95, "Telescope MC", "observer display", "access", 28)
d.box(520, 350, 350, 115, "Quicklook HTTP API", "tolteca_web · FastAPI", "access", 27)
d.arrow([(275, 388), (509, 388)], "obsnum / ObsSpec", 392, 370)
d.arrow([(520, 435), (286, 435)], "state + image URLs", 395, 470)
d.arrow([(1045, 270), (1045, 407), (882, 407)], "query + read", 950, 334)
d.save()

d = Diagram(
    "products",
    "A published run stores data, configuration and step records; tags select runs",
)
d.area(0, 5, 635, 465, "PUBLISHED RUN", "product")
d.box(28, 65, 280, 105, "Zarr datasets", "interfaces → blocks", "data", 26)
d.box(328, 65, 280, 105, "Figures + index", "portable output", "product", 26)
d.box(28, 200, 580, 95, "Resolved workflow configuration", kind="neutral", size=27)
d.box(
    28,
    319,
    580,
    118,
    "Step records + analysis settings",
    "inputs · run UID · software / runtime info",
    "neutral",
    26,
)
d.area(695, 5, 455, 465, "PRODUCT DATABASE", "product")
d.box(732, 65, 380, 85, "Version group", kind="product")
d.box(732, 212, 170, 85, "Run A", kind="product")
d.box(942, 212, 170, 85, "Run B", kind="product")
d.arrow([(832, 150), (832, 200)])
d.arrow([(1017, 150), (1017, 200)])
d.box(932, 363, 190, 70, "main", kind="access")
d.arrow([(1027, 363), (1027, 307)], "selects", 1080, 335)
d.text(818, 391, "other runs\nremain available", 21, MUTED)
d.save()

d = Diagram(
    "lineage",
    "Interface calibration references produce acquisition links and calibration groups",
)
d.area(
    25, 10, 1102, 325, "ONE CALIBRATION GROUP · ILLUSTRATIVE RELATIONSHIPS", "product"
)
d.box(60, 95, 210, 130, "VNA A", kind="data")
d.box(350, 60, 245, 95, "Tune C", kind="compute")
d.box(350, 210, 245, 95, "VNA B", kind="data")
d.box(805, 60, 270, 95, "Timestream D", kind="compute")
d.arrow([(350, 108), (282, 152)], "toltec0", 302, 90)
d.arrow([(472, 155), (472, 199)], "toltec1", 536, 187)
d.arrow([(805, 108), (606, 108)], "calibration", 700, 91)
d.text(817, 252, "An acquisition can use\nmultiple calibrations.", 25, INK)
d.box(25, 393, 315, 82, "Per-interface references", kind="data", size=25)
d.box(420, 393, 310, 82, "Acquisition links", kind="product", size=25)
d.box(810, 393, 315, 82, "Connected groups", kind="product", size=25)
d.arrow([(340, 434), (409, 434)])
d.arrow([(730, 434), (799, 434)])
d.save()

d = Diagram(
    "sites",
    "Independent Taco, transferred and Unity inventories combine into a unified inventory",
)
for y, title, sub in [
    (5, "Taco live", "site processing"),
    (170, "Taco copy on Unity", "transferred artifacts"),
    (335, "Unity native", "archive reprocessing"),
]:
    d.box(0, y, 305, 128, title, sub, "data", 26)
    d.box(350, y, 225, 128, "Own inventory", "DB + artifact tree", "product", 25)
    d.arrow([(305, y + 64), (339, y + 64)])
    d.arrow([(575, y + 64), (630, y + 64), (630, 234), (685, 234)])
d.box(
    695,
    168,
    430,
    130,
    "Unified inventory",
    "merge records · retain locations",
    "product",
    30,
)
d.box(745, 372, 330, 92, "Web viewer", kind="access", size=30)
d.arrow([(910, 298), (910, 361)], "query", 964, 341)
d.text(910, 76, "Independent sources", 26, INK, 700)
d.text(910, 111, "Local and remote artifact access", 22, MUTED)
d.save()

d = Diagram(
    "helpdesk",
    "Task guidance, source-grounded human assistance and independent agent access",
)
d.box(0, 30, 330, 120, "Authored sources", "package guides + tutorials", "data", 30)
d.box(420, 30, 310, 120, "Workflow guidance", "science / operations", "access", 27)
d.arrow([(330, 90), (409, 90)])
d.box(820, 30, 330, 120, "People", "FAQ + source documents", "access", 30)
d.arrow([(730, 90), (809, 90)])
d.box(420, 250, 310, 130, "AI provider API", "retrieved source passages", "compute", 29)
d.box(820, 250, 330, 130, "Draft + citations", "TolTEC AI Assistant", "access", 29)
d.arrow([(575, 150), (575, 239)], "optional", 640, 201)
d.arrow([(730, 315), (809, 315)])
d.box(0, 250, 330, 130, "Software assistants", "offline · HTTP · MCP", "product", 27)
d.arrow([(165, 150), (165, 239)], "authored text", 250, 201)
d.text(575, 455, "Guides remain available independently of AI inference.", 27, INK, 700)
d.save()

d = Diagram(
    "execution", "Service processes submit and supervise Slurm workers sharing storage"
)
d.area(0, 5, 450, 333, "SERVICE CONTAINER", "access")
d.box(
    25,
    64,
    395,
    92,
    "Dagster + code locations",
    "sensors · partitions · run supervision",
    "access",
    26,
)
d.box(25, 196, 395, 90, "Web + APIs + PostgreSQL", kind="access", size=25)
d.area(685, 5, 465, 333, "SLURM COMPUTE NODES", "compute")
d.box(
    715,
    64,
    405,
    92,
    "Workflow worker",
    "same Python / CLI implementation",
    "compute",
    27,
)
d.box(715, 196, 405, 90, "Interactive QA allocation", kind="compute", size=26)
d.arrow([(450, 110), (674, 110)], "submit", 562, 90)
d.arrow([(685, 168), (461, 168)], "state + logs", 562, 195)
d.box(
    150,
    400,
    850,
    80,
    "Shared /nese/ · inputs, products, execution records",
    kind="data",
    size=27,
)
d.arrow([(225, 333), (225, 390)])
d.arrow([(917, 333), (917, 390)])
d.text(565, 281, "Policies select\nresources + limits", 22, MUTED)
d.save()
