"""Dashboard template.

This file is the top level, and contains the sidebar. Each page lives in
pages/ and registers itself with dash.register_page, so adding a page means
adding one file - plus updating EXPECTED_PAGES/CALLBACK_IDS in
tests/test_app.py, which is the one thing that doesn't update itself.
"""

import os
import pathlib

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, dcc, html
from dotenv import load_dotenv

import theme  # registers the "4subsea" Plotly template

PAGE_TITLE = "Dashboard Template"

# Read environment variables from .env in the repo root, if present
load_dotenv(pathlib.Path(__file__).resolve().parents[1] / ".env", override=False)

# Load environemnt variables into globals
DASH_DEBUG = os.getenv("DASH_DEBUG", "true").strip().lower() == "true"
MOCK_PLATFORM_HEADER = int(os.getenv("MOCK_PLATFORM_HEADER", "0") or 0)
MOCK_PLATFORM_SPACER = int(os.getenv("MOCK_PLATFORM_SPACER", "20") or 20)

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,  # Set true for multi-page apps to avoid raising exceptions.
    title=PAGE_TITLE,
)


def nav_bar(pathname):
    """
    Side navigation, built from the page registry so it never needs editing.
    """
    pages = sorted(dash.page_registry.values(), key=lambda p: p.get("order", 0))
    return html.Div(
        [
            dcc.Link(
                page["name"],
                href=page["relative_path"],
                className="sidebar-link"
                + (" sidebar-link--active" if page["relative_path"] == pathname else ""),
            )
            for page in pages
        ],
        className="sidebar-links",
    )


def mock_4insight():
    """A stand-in for 4insight's header, so local screens match the real thing.

    Off unless MOCK_PLATFORM_HEADER is set - see .env.example. Returns the bar
    and the dead space below the iframe, both of which eat into the height a
    page has to work with. "Placeholder title" stands in for the dashboard
    name 4insight's real header renders there, below the logo row - matching
    the real header's 44px nav + 38px breadcrumb stack.
    """
    if not MOCK_PLATFORM_HEADER:
        return [], []
    bar = html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src=app.get_asset_url("4insight_logo.png"),
                        className="mock-4insight-logo",
                        alt="4insight",
                    ),
                    html.Span(
                        "simulated header — not part of the app",
                        className="mock-4insight-note",
                    ),
                ],
                className="mock-4insight-top",
            ),
            html.Span("Placeholder title", className="mock-4insight-title"),
        ],
        className="mock-4insight",
        style={"height": f"{MOCK_PLATFORM_HEADER}px"},
    )
    bottom_bar = html.Div(
        html.Span(
            "simulated spacer — not part of the app",
            className="mock-4insight-bottom-note",
        ),
        className="mock-4insight-bottom-bar",
        style={"height": f"{MOCK_PLATFORM_SPACER}px"},
    )
    return [bar], [bottom_bar]


_mock_bar, _mock_bottom_bar = mock_4insight()
_mock_top_height = MOCK_PLATFORM_HEADER if MOCK_PLATFORM_HEADER else 0
_mock_bottom_height = MOCK_PLATFORM_SPACER if MOCK_PLATFORM_HEADER else 0

# App layout
app.layout = html.Div(
    _mock_bar
    + [
        dcc.Location(id="url"),
        html.Div(
            [
                html.Div(id="nav-bar", className="sidebar"),
                html.Div(dash.page_container, className="content"),
            ],
            className="shell",
        ),
    ]
    + _mock_bottom_bar,
    className="app-root",
    style={
        "--mock-top-height": f"{_mock_top_height}px",
        "--mock-bottom-height": f"{_mock_bottom_height}px",
    },
)


@callback(Output("nav-bar", "children"), Input("url", "pathname"))
def highlight_active_tab(pathname):
    """Function to highlight the active tab in the sidebar based on the current URL path."""
    return nav_bar(pathname)


if __name__ == "__main__":
    # Run the app. Set DASH_DEBUG in .env to toggle debug mode.
    app.run(debug=DASH_DEBUG, port = 8051)
