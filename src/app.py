"""Dashboard template.

This file is the top level, and contains the sidebar. Each page lives in
pages/ and registers itself with dash.register_page, so adding a page means
adding one file and nothing else.
"""

import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import config

PAGE_TITLE = "Dashboard Template"

# suppress_callback_exceptions: only the current page's components are in the
# DOM, so the other pages' callback targets are absent until you navigate.
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
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

    Off unless MOCK_PLATFORM_CHROME is set - see config.py. Returns the bar and
    the dead space below the iframe, both of which eat into the height a page
    has to work with. "Placeholder title" stands in for the dashboard name
    4insight's real header renders there, below the logo row - matching the
    real header's 44px nav + 38px breadcrumb stack.
    """
    if not config.MOCK_PLATFORM_CHROME:
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
        style={"height": f"{config.MOCK_PLATFORM_CHROME}px"},
    )
    bottom_bar = html.Div(
        className="mock-4insight-bottom-bar",
        style={"height": f"{config.MOCK_PLATFORM_GAP}px"},
    )
    return [bar], [bottom_bar]


_mock_bar, _mock_bottom_bar = mock_4insight()

# No page title on the page itself: 4insight's own header names the dashboard,
# and 34px of heading is 34px not spent on content. It stays as the browser
# tab title, set on the Dash constructor above.
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
    + _mock_bottom_bar
)


@callback(Output("nav-bar", "children"), Input("url", "pathname"))
def highlight_active_tab(pathname):
    """Dash Pages handles the routing; this only marks which tab is current."""
    return nav_bar(pathname)


if __name__ == "__main__":
    # All three come from the environment; see config.py and .env.example.
    # On any shared machine set DASH_DEBUG=false - the debug console executes
    # Python on the host.
    app.run(debug=config.DASH_DEBUG, host=config.DASH_HOST, port=config.DASH_PORT)
