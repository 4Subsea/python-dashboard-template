# Python Dashboard Template

A starting point for Plotly Dash dashboards: one theme, one working example
page and one filterable-chart page, a mock-up of 4insight's header for local
layout work, and the process scaffolding (CI, PR template, `CLAUDE.md`
conventions) set up.

To start a new project from this template: clone or copy it, replace
`src/assets/sample_data.csv` and the two pages in `src/pages/` with your own,
and update this README and the browser-tab title in `src/app.py`.

## Running it

```bash
python -m venv .venv
.venv\Scripts\activate                
pip install -r requirements-dev.txt   # app, tests and formatter

python src/app.py
```

Requirements are split by purpose: `requirements.txt` is what the dashboard
needs to run, `requirements-dev.txt` adds pytest, black and pre-commit, and
`requirements-notebooks.txt` adds Jupyter for `notebooks/`.

Then open <http://127.0.0.1:8050>. Debug mode is on, so saving a file reloads
the app.

Optional but recommended: `pre-commit install --hook-type pre-commit` runs
black on staged files automatically, so formatting issues are caught before
they reach CI at all. See `CONTRIBUTING.md` for the full set of hooks.

## Configuration

There isn't much. Two variables come from `.env` (copy `.env.example` and
edit it; `.env` is gitignored):

- `DASH_DEBUG` - the only setting with a security consequence: its debug console can run arbitrary Python for anyone who reaches it. Keep it `true` 
  on your own laptop for hot reloading; set it `false` on anything anyone else can reach.
- `MOCK_PLATFORM_HEADER` (and `MOCK_PLATFORM_SPACER`) - see "Fitting the
  4insight frame" below. 

`app.run(debug=DASH_DEBUG)` uses Dash's own defaults (`127.0.0.1:8050`). 

## Layout

```
src/
├── app.py            Dash shell: side navigation, mock 4insight header
├── theme.py          colours, type scale and the Plotly template
├── pages/
│   ├── home.py       example: an AgGrid over the sample data
│   └── analytics.py  example: a slicer driving a filtered Plotly chart
└── assets/
    ├── css/main.css  page styling, mirrors theme.py as CSS variables
    ├── 4insight_logo.png
    └── sample_data.csv

notebooks/            any notebooks used for exploration, sandboxing. Outside the running app.
tests/                pytest suite
.github/              CI workflow + PR template
.env.example          Example .env file; copy to .env to override
.pre-commit-config.yaml   optional local git hooks; see CONTRIBUTING.md
```

Pages register themselves with `dash.register_page`, and the sidebar is built
from `dash.page_registry` — adding a page means adding one file in `pages/`.
The one thing that doesn't update itself: `EXPECTED_PAGES`/`CALLBACK_IDS` at
the top of `tests/test_app.py`, a small hand-written spec of what pages
should exist and what their callbacks target. Add your page there too, or
`pytest` will (correctly) tell you the registered pages don't match what the
suite expects.


## Fitting the 4insight frame

Real deployments serve this app inside an iframe on 4insight, under a header
that takes 82 px, with 20 px of dead space below the frame. Set
`MOCK_PLATFORM_HEADER=82` in `.env` and the app reserves the same space
locally — the top bar shows the 4insight logo and a "Placeholder title"
standing in for where 4insight's own header names the dashboard, and the
bottom bar stands in for the dead space below it. Both carry a small dev
note so nobody mistakes them for real UI.

Both bars are fixed-position overlays (`main.css`'s `.mock-4insight`/
`.mock-4insight-bottom-bar`), not part of the normal page flow. `app.py` sets
their heights as `--mock-top-height`/`--mock-bottom-height` CSS custom
properties on the page root, and `.shell` pads itself by those same
variables — that's what actually reserves the space so page content doesn't
render underneath the bars.

## Memory logging

Set `LOG_MEMORY=true` in `.env` to print the app's RSS memory usage to the
terminal every time you click a page link. It's a dev aid only, off by
default.

## Styling / theming

Colours, fonts and spacing live in two places that must be kept in step:

- `src/theme.py` — the single source of truth as Python constants
  (`UI_COLORS`, `COLORS`, font sizes). Importing it registers a Plotly
  template as the default, so any figure built anywhere in the app picks up
  the palette and typography automatically — no chart-by-chart styling.
- `src/assets/css/main.css` — the same palette and type scale as CSS custom
  properties, used for page chrome, the sidebar, the mock header, and AgGrid's
  theme variables (AgGrid isn't a Plotly figure, so it reads the CSS
  variables rather than `theme.py` directly).

If you change `theme.py`'s `SCALE` or a size constant, change the matching
`--size-*` variable in `main.css` too — nothing enforces this automatically.

## Sample data

`src/assets/sample_data.csv` is a small, generic dataset (category, region,
date, value, target) used by both example pages, loaded with
`pandas.read_csv` inside each page's layout function / callback — never at
import time, so it's read fresh on every page load. Swap it for your real
data source once you have one.

## Tests

```bash
pytest
```

Covers page registration, that each page's layout builds, that every
callback's component IDs actually exist in its page, the mock header (absent
by default, carries the logo, placeholder title and spacer note when
configured), and that the analytics chart actually renders through the
"4subsea" Plotly theme rather than silently falling back to Plotly's default.

## Contributing

`CONTRIBUTING.md` holds the definition of done — the checklist every change
ticks before it is merged. It appears automatically on every pull request.

CI runs black and the full test suite on every push to `main` and every pull
request.

## Conventions

`CLAUDE.md` holds the Dash conventions for this repo — architecture,
callbacks, layout, charts. Read it before adding a page. Format with
`black .` before committing — options come from `pyproject.toml`.
