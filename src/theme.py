"""4Subsea theme: colours, typography and the Plotly template.

Translated from the 4Subsea PBI style guide
https://miro.com/app/board/uXjVHbD9HV0=/ on 2026-07-30.

Importing this module registers the template as Plotly's default, so any figure
built afterwards picks it up without asking. Everything that needs a brand
colour should import it from here rather than hardcoding a hex value.

Notes on what the template cannot cover
---------------------------------------
- Visual borders (1px, 4px corners, border grey 1) are page chrome, not figure
  chrome - they live in assets/css/main.css, which mirrors these constants as
  CSS custom properties.
- The guide's sizes are PowerPoint/PBI points, used here as Plotly font sizes,
  which are pixels. SCALE below converts between the two; keep it in step with
  the --size-* variables in main.css.
"""

import plotly.graph_objects as go
import plotly.io as pio

# ── UI colours ────────────────────────────────────────────────────────────────
BORDER_GREY_1 = "#e6e6e6"
BORDER_GREY_2 = "#d2d3ce"
LIGHT_GREY = "#f8f9fa"
GREY = "#a8a9a5"
DARK_GREY = "#7e7f7c"
DARK_BLUE = "#012b5d"
TURQUOISE = "#00a0b0"
BODY_TEXT = "#002023"

UI_COLORS = {
    "border_grey_1": BORDER_GREY_1,
    "border_grey_2": BORDER_GREY_2,
    "light_grey": LIGHT_GREY,
    "grey": GREY,
    "dark_grey": DARK_GREY,
    "dark_blue": DARK_BLUE,
    "turquoise": TURQUOISE,
    "body_text": BODY_TEXT,
}

# ── Data colours — the guide says to use them in this order ───────────────────
COLORS = [
    "#012b5d",  # Dark blue
    "#00a0b0",  # Turquoise
    "#f3776f",  # Red
    "#feb272",  # Orange
    "#a8a9a5",  # Border grey 2 / grey
    "#87d8f8",  # Light blue
    "#bdf4eb",  # Mint
    "#8e00b0",  # Purple
    "#716fb3",  # Muted purple
    "#95b000",  # Olive
]

# ── Typography ────────────────────────────────────────────────────────────────
# Guide sizes are in points; SCALE converts them to pixel sizes.
# Raise or lower this one number to scale every font in every figure.
SCALE = 1.6

FONT_FAMILY = "Trebuchet MS, Arial, sans-serif"

BODY_SIZE = round(10 * SCALE)  # body text, legend entries, category labels
TITLE_SIZE = round(12 * SCALE)  # visual title
AXIS_TITLE_SIZE = round(9 * SCALE)  # axis title
AXIS_VALUE_SIZE = round(8 * SCALE)  # axis values / scales
TABLE_HEADER_SIZE = round(9 * SCALE)  # mirrored by --size-table-head in main.css

# ── Grid ──────────────────────────────────────────────────────────────────────
GRID_COLOR = BORDER_GREY_1


def rgba(hex_color, alpha):
    """'#012b5d' -> 'rgba(1,43,93,alpha)'"""
    r, g, b = (int(hex_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def make_template() -> go.layout.Template:
    axis = dict(
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks="",
        # Axis title: size 9, dark grey
        title=dict(font=dict(size=AXIS_TITLE_SIZE, color=DARK_GREY)),
        # Axis values / scales: size 8, grey
        tickfont=dict(size=AXIS_VALUE_SIZE, color=GREY),
        exponentformat="power",
        showexponent="all",
    )

    return go.layout.Template(
        layout=go.Layout(
            # Body text: Trebuchet MS, size 10, body text colour
            font=dict(family=FONT_FAMILY, size=BODY_SIZE, color=BODY_TEXT),
            # Visual title: size 12, grey, left aligned
            title=dict(
                font=dict(family=FONT_FAMILY, size=TITLE_SIZE, color=GREY),
                x=0,
                xanchor="left",
                xref="paper",
            ),
            colorway=COLORS,
            # No fixed width - visuals stretch to the width of their container
            width=None,
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=60, r=20, t=48, b=48),
            xaxis=axis,
            yaxis=axis,
            # Legend entries: size 10, body text. The guide notes a legend title
            # is usually not needed, so it is off by default. Legends sit in a
            # vertical block to the right, as in the guide's scatter example.
            legend=dict(
                title=dict(text=""),
                x=1.02,
                y=1.0,
                xanchor="left",
                yanchor="top",
                orientation="v",
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                font=dict(size=BODY_SIZE, color=BODY_TEXT),
            ),
            # Zoom/pan controls, top right by default. main.css gives the bar a
            # border so it reads as chrome rather than data.
            modebar=dict(
                orientation="h",
                bgcolor="rgba(255,255,255,0.85)",
                color=GREY,
                activecolor=TURQUOISE,
            ),
            colorscale=dict(sequential=[[0, "#bdf4eb"], [0.5, TURQUOISE], [1, DARK_BLUE]]),
        ),
        data=dict(
            scatter=[go.Scatter(line=dict(width=2), marker=dict(size=6))],
            scattergl=[go.Scattergl(line=dict(width=2), marker=dict(size=6))],
            bar=[go.Bar(marker=dict(line=dict(width=0)))],
        ),
    )


def register_theme(set_as_default: bool = True) -> None:
    """Register the 4Subsea template with Plotly."""
    pio.templates["4subsea"] = make_template()
    if set_as_default:
        pio.templates.default = "4subsea"


# Register theme on import so that themes are available after import wihout needing to call register_theme()
register_theme()
