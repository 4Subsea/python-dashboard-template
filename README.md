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
needs to run, `requirements-dev.txt` adds pytest and black, and
`requirements-notebooks.txt` adds Jupyter for `notebooks/`.

Then open <http://127.0.0.1:8050>. Debug mode is on, so saving a file reloads
the app.

## Configuration

There isn't much. Two variables come from `.env` (copy `.env.example` and
edit it; `.env` is gitignored):

- `DASH_DEBUG` - the one setting with a security consequence, so it stays
  configurable rather than hardcoded. Keep it `true` on your own laptop for
  hot reloading; set it `false` on anything anyone else can reach - the debug
  console executes Python on the host.
- `MOCK_PLATFORM_CHROME` (and `MOCK_PLATFORM_GAP`) - see "Fitting the
  4insight frame" below. A personal, not-committed toggle rather than a
  machine-specific setting.

Host and port aren't configurable - `app.run(debug=DASH_DEBUG)` uses Dash's
own defaults (`127.0.0.1:8050`). 

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
```

Pages register themselves with `dash.register_page`, and the sidebar is built
from `dash.page_registry` — adding a page means adding one file in `pages/`,
with nothing else to update.


## Fitting the 4insight frame

Real deployments serve this app inside an iframe on 4insight, under a header
that takes 82 px, with 20 px of dead space below the frame. Set
`MOCK_PLATFORM_CHROME=82` in `.env` and the app reserves the same space
locally — the bar shows the 4insight logo and a "Placeholder title" standing
in for where 4insight's own header names the dashboard, plus a small dev note
so nobody mistakes the bar for real UI. 

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
callback's component IDs actually exist in its page, and the mock header
(absent by default, carries the logo and placeholder title when configured).

## Contributing

`CONTRIBUTING.md` holds the definition of done — the checklist every change
ticks before it is merged. It appears automatically on every pull request.

CI runs black and the full test suite on every push to `main` and every pull
request.

## Conventions

`CLAUDE.md` holds the Dash conventions for this repo — architecture,
callbacks, layout, charts. Read it before adding a page. Format with
`black .` before committing — options come from `pyproject.toml`.
