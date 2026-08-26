## File Structure
python-dashboard-template/
├── src/
│   ├── app.py             # Main application file
│   ├── theme.py            # Colours, type scale and the Plotly template
│   ├── assets/            # Static files (CSS, images, sample data)
│   └── pages/             # One module per page, each with dash.register_page
│       ├── home.py
│       └── analytics.py
├── tests/                 # pytest suite
├── notebooks/             # ad-hoc exploration, outside the running app
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # + pytest, black
├── requirements-notebooks.txt  # + Jupyter
├── .env.example           # The mock-header toggle, documented; copy to .env to override
├── .github/                # CI workflow + PR template
├── README.md
├── CONTRIBUTING.md
└── CLAUDE.md              # This file


## General Architecture
- **Global Variables**: Never use global variables to store user-specific state. All mutable state must live in the client browser using `dcc.Store` or URL parameters.
- **Dash Pages**: If Snapshot Engine is used, do not use Dash Pages; use callback routing instead to navigate between views. Otherwise, use `dash.page_registry`, keep all pages in a `pages/` directory, and register each page with `dash.register_page(__name__)`.
- **App IDs**: Prefer descriptive IDs like `"sales-filter-dropdown"` over `"dropdown-1"`. IDs must be unique across the entire app, including all pages.
- **Loading Data**: Load data inside callbacks, not at import time. Avoid `df = pd.read_csv(...)` at module level. Data loaded at startup won't refresh until the process restarts. Fetch or refresh data inside the callback that needs it, or use a layout function (`def serve_layout(): ...`) when the layout must be rebuilt on each page load.
- **Server-side Filtering**: Filter, aggregate, and paginate data in Python before passing it to graphs or `AgGrid`. Only send the rows or points needed for the current view to the client.
- **Pin Dependencies**: Specify minimum or exact versions for `dash`, `plotly`, and component libraries in `requirements.txt` to avoid breaking changes on deploy.

## Callbacks
- **Dataset Size**: Do not pass massive datasets through `dcc.Store` if they can be cached server-side. Use `dcc.Store` only for lightweight state (IDs, UI toggles, query filters) with a maximum of 5MB.
- **Caching**: For large datasets, expensive database queries, heavy computations, or API requests, implement server-side caching using `flask_caching`. Decorate data-fetching operations with the `@cache.memoize()` pattern. Ensure the cache key includes relevant query parameters.
- **Input IDs**: Every `Input`, `Output`, and `State` ID referenced in a callback must be present in the layout when the callback fires. For dynamic or multi-page layouts, set `suppress_callback_exceptions = True`.
- **Prevent Callback Firing**: Apply `prevent_initial_call=True` in callback decorators that should not run on page load (e.g., actions triggered only by a button click).
- **Prevent Unnecessary Updates**: When a callback should leave an output unchanged, return `dash.no_update` instead of re-fetching or re-computing data. Use `raise PreventUpdate` to skip updating the entire callback.
- **Keep Callbacks Focused**: One callback per user interaction when possible. Split large callbacks into smaller, composable ones rather than updating many outputs from a single function.
- **Loading Spinners**: Show a spinner while data is loading to improve perceived performance by wrapping components that may be slow to update with `dcc.Loading`.
- **Background Callbacks**: Use background callbacks for long-running work. For tasks that take more than a few seconds, use `background=True` in the callback decorator, along with the configured manager: `manager=background_callback_manager`.
- **Validate Callback Outputs**: Return strings for `children`, lists of component objects for `children` on containers, dicts for `figure`, and lists of dicts for `AgGrid` `rowData` and `columnDefs`.

## Layout and Styling
- **Custom Style Sheets**: For external stylesheets and CSS files, put core layout styles, layout grids, and structural overrides into custom files inside the `assets/` directory.
- **Theme File**: Use a shared `theme.py` or `theme.js` containing color constants, spacing scales, and font definitions to pass values systematically.
- **Inline Styles**: Use inline Python dictionaries (`style={"marginRight": "10px"}`) only for highly dynamic, runtime-computed values (e.g., styling a component color based on a callback threshold). Avoid static inline styling blocks as much as possible.
- **Code Format**: Run `black` for Python formatting and Prettier for CSS formatting.

## Charts and Components
- **Graphing Library**: Use `plotly.express` for charts first—it is simpler and covers most use cases. Switch to `plotly.graph_objects` only when you need fine-grained control.
- **Component Libraries**: Prioritize component libraries in this order: Dash Core Components combined with Dash HTML Components, then Dash Mantine Components, then Dash Bootstrap Components if required. Try to minimize the number of libraries required. 
- **Data Tables**: Do not use `dash.datatable`; use `dash.AgGrid` instead.
- **AgGrid Configs**: When instantiating `dag.AgGrid`, always set the following properties:
  - `dashGridOptions={"theme": "themeBalham", "animateRows": True, "pagination": True, "paginationPageSize": 10}`
  - `columnSize="responsiveSizeToFit"`
  - `defaultColDef={"filter": True, "sortable": True}`

## Fullscreen Toggle Pattern
A reusable "expand to fullscreen" button for any chart inside a `.visual` box. No Dash callback is needed — it's pure CSS + one small JS file in `assets/`, so it automatically applies to any current or future chart that follows the markup pattern below.

**Why it's built this way (read this before changing it):** the naive version — toggle a `position: fixed` class and call `Plotly.Plots.resize(gd)` — breaks in two ways that are easy to reintroduce by accident:
1. Outside fullscreen, a plot's container normally has no explicit height (it's sized *by* the plot, not the other way round). Asking Plotly to "resize to fit its container" on exit is therefore circular — the container has no size to resize to, and the chart doesn't shrink back.
2. `dcc.Loading` wraps the graph in one or two extra `<div>`s whose class names aren't part of the public Dash API. Trying to cascade a height down through them with CSS percentages (`height: 100%` chained through unknown wrapper divs) silently breaks and leaves the chart stuck at a stale pixel size — which, in a flex row with the default `align-items: stretch`, then drags the *other* column's box height along with it.

The fix: give the chart's own wrapper (`.graph-wrap`, not the Plotly div itself) an explicit, always-defined height in both states (fixed px normally, flex-filled in fullscreen), then measure that wrapper directly in JS and set the chart's exact pixel size via `Plotly.relayout(gd, {width, height, autosize: false})`. This never depends on the unknown internal `dcc.Loading` DOM structure.

**Markup** — wrap every chart to make fullscreen-able like this:
```python
html.Div(
    [
        html.Button(
            "⛶",
            className="fullscreen-toggle-btn",
            title="Toggle full screen",
            **{"aria-label": "Toggle full screen"},
        ),
        html.Div("Chart Title", className="visual-title"),
        html.Div(
            dcc.Loading(dcc.Graph(id="my-chart")),
            className="graph-wrap",
        ),
    ],
    className="visual",
)
```
If several charts sit side by side in a flex row, add `"alignItems": "flex-start"` to that row's `style` dict — a safety net so one chart's sizing hiccup can never stretch its neighbor.

The CSS lives in `assets/css/main.css` (the `.visual`, `.fullscreen-toggle-btn`, `.visual--fullscreen`, `.graph-wrap` and `body.fullscreen-active` rules) and the JS lives in `assets/fullscreen.js`. Both are already in the template and apply automatically — no per-page wiring needed beyond the markup above.

**Rules when reusing this:**
- Always wrap the chart in `.graph-wrap` — never put `fullscreen-toggle-btn` next to a bare `dcc.Graph`/`dcc.Loading` without it; the JS measures `.graph-wrap`, not the Plotly div, so skipping it breaks the resize.
- Don't try to make the chart's height cascade through CSS percentages past `.graph-wrap` — that's the exact thing that broke before. Let the JS set the Plotly size explicitly.
- Only one visual can be fullscreen at a time by design (`enterFullscreen` clears any other `.visual--fullscreen` first); don't remove that if adding more charts.

## Avoid Hallucinations
- Never use `app.run_server`; only use `app.run`
- Never use obsolete patterns like `app.validation_layout`. Modern Dash handles dynamic layouts smoothly; just use `suppress_callback_exceptions=True` on app initialization if building dynamic layouts.
- Never import `dash.dependencies` items individually (from `dash.dependencies import Input`). Always use the modern syntax: `from dash import Input, Output, State, callback, clientside_callback, no_update, ALL, MATCH`.
- Never write blocking `time.sleep` loops inside a callback in production contexts; use `dcc.Interval` for asynchronous long-polling or integrate an external task queue (like Celery/Redis) if handling long-running computations.
- Never assign to callback `Input` values or mutate callback arguments in place.
- Never use `dash_table.DataTable`; use `dash.AgGrid()` instead.
- Never put secrets, API keys, or credentials in layout code or `dcc.Store`. Use environment variables and server-side logic only.