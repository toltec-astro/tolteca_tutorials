"""Build the astronomer's handbook independently of software API references."""

project = "TolTEC Data Handbook"
author = "TolTEC team"
copyright = "2026, TolTEC team"
version = release = "Draft · 2026-10-26"
extensions = ["myst_parser"]
source_suffix = {".md": "markdown"}
# Editorial evidence and probes sit beside the book but are not chapters.
exclude_patterns = ["evidence", "probes"]
html_theme = "sphinx_book_theme"
html_title = project
html_theme_options = {
    "show_navbar_depth": 2,
    "extra_footer": '<a href="../../">Return to the portal</a>',
    "announcement": "Draft for review · 26 October 2026 · TolTECA v3",
}
myst_heading_anchors = 3
