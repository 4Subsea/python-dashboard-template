"""Page registration, layouts and callbacks, without starting a browser."""

import pytest
from conftest import text_of

import app

EXPECTED_PAGES = {
    "/": "Home",
    "/analytics": "Analytics",
}


def registry():
    import dash

    return {p["relative_path"]: p for p in dash.page_registry.values()}


def test_every_page_is_registered():
    assert set(registry()) == set(EXPECTED_PAGES)


def test_pages_appear_in_the_intended_order():
    import dash

    ordered = sorted(dash.page_registry.values(), key=lambda p: p["order"])
    assert [p["name"] for p in ordered] == list(EXPECTED_PAGES.values())


@pytest.mark.parametrize("path", EXPECTED_PAGES)
def test_page_layout_builds(path):
    layout = registry()[path]["layout"]
    rendered = layout() if callable(layout) else layout
    assert rendered is not None


@pytest.mark.parametrize("path,name", EXPECTED_PAGES.items())
def test_nav_marks_exactly_one_active_tab(path, name):
    links = app.nav_bar(path).children
    active = [text_of(l.children) for l in links if "sidebar-link--active" in l.className]
    assert active == [name]


def component_ids(node, found=None):
    """Every id in a layout tree, so callbacks can be checked against it."""
    found = set() if found is None else found
    if isinstance(node, (list, tuple)):
        for item in node:
            component_ids(item, found)
    elif hasattr(node, "_prop_names"):
        if getattr(node, "id", None) and isinstance(node.id, str):
            found.add(node.id)
        component_ids(getattr(node, "children", None), found)
    return found


CALLBACK_IDS = {
    "/": {"home-sample-grid"},
    "/analytics": {"analytics-category-filter", "analytics-chart"},
}


@pytest.mark.parametrize("path,required", CALLBACK_IDS.items())
def test_every_callback_target_exists_in_its_page(path, required):
    """suppress_callback_exceptions hides typos, so check the ids explicitly."""
    layout = registry()[path]["layout"]
    present = component_ids(layout() if callable(layout) else layout)
    assert required <= present, f"missing from {path}: {sorted(required - present)}"


def test_component_ids_are_unique_within_each_page():
    for path in EXPECTED_PAGES:
        layout = registry()[path]["layout"]
        rendered = layout() if callable(layout) else layout
        ids = []

        def collect(node):
            if isinstance(node, (list, tuple)):
                for item in node:
                    collect(item)
            elif hasattr(node, "_prop_names"):
                if getattr(node, "id", None) and isinstance(node.id, str):
                    ids.append(node.id)
                collect(getattr(node, "children", None))

        collect(rendered)
        assert len(ids) == len(set(ids)), f"duplicate ids on {path}"


# ---------------------------------------------------------------------------
# Callbacks, called directly
# ---------------------------------------------------------------------------


def test_analytics_callback_returns_a_figure_for_each_category():
    from pages.analytics import update_chart

    for category in ("Alpha", "Beta", "Gamma", "Delta"):
        figure = update_chart(category)
        assert figure.data


def test_figures_are_json_serialisable():
    """Dash sends figures over the wire, so they must survive serialisation."""
    import json

    from pages.analytics import update_chart

    figure = update_chart("Alpha")
    json.dumps(figure.to_plotly_json(), default=str)


def test_figures_use_the_4subsea_theme():
    """theme.py only registers its Plotly template as a side effect of being
    imported - regression guard for that import silently going missing."""
    import theme
    from pages.analytics import update_chart

    figure = update_chart("Alpha")
    assert tuple(figure.layout.template.layout.colorway) == tuple(theme.COLORS)


# ---------------------------------------------------------------------------
# The 4insight mock header
# ---------------------------------------------------------------------------


def test_the_mock_header_is_absent_unless_configured(monkeypatch):
    """It must never render on the server, where the real header already exists."""
    monkeypatch.setattr(app, "MOCK_PLATFORM_HEADER", 0)
    assert app.mock_4insight() == ([], [])


def test_the_mock_header_carries_the_logo_and_placeholder_title_when_configured(monkeypatch):
    monkeypatch.setattr(app, "MOCK_PLATFORM_HEADER", 82)
    monkeypatch.setattr(app, "MOCK_PLATFORM_SPACER", 20)
    (bar,), (bottom_bar,) = app.mock_4insight()
    top_row, title = bar.children
    logo, note = top_row.children
    assert logo.src.endswith("4insight_logo.png")
    assert text_of(title) == "Placeholder title"
    assert text_of(note) == "simulated header — not part of the app"
    assert bar.style["height"] == "82px"
    assert bottom_bar.style["height"] == "20px"
    assert text_of(bottom_bar.children) == "simulated spacer — not part of the app"
