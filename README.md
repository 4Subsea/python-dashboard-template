# Python Dashboard Template

A starting point for Plotly Dash dashboards: one theme, one working example
page and one filterable-chart page, a mock-up of 4insight's header for local
layout work, and the process scaffolding (CI, PR template, `CLAUDE.md`
conventions) already wired up.

To start a new project from this template: clone or copy it, replace
`src/assets/sample_data.csv` and the two pages in `src/pages/` with your own,
and update this README and the browser-tab title in `src/app.py`.

## Running it

```bash
python -m venv .venv
.venv\Scripts\activate                # Windows;  source .venv/bin/activate elsewhere
pip install -r requirements-dev.txt   # app, tests and formatter

python src/app.py
```

Requirements are split by purpose: `requirements.txt` is what the dashboard
needs to run, `requirements-dev.txt` adds pytest and black, and
`requirements-notebooks.txt` adds Jupyter for `notebooks/`.

Then open <http://127.0.0.1:8050>. Debug mode is on, so saving a file reloads
the app.

## Configuration

Everything that differs between a laptop, the server and CI comes from the
environment. With no configuration at all the app runs from the repo exactly
as above, so a fresh clone needs no setup.

To change something, copy `.env.example` to `.env` in the repo root and edit
it. `.env.example` documents every variable; `.env` is gitignored, so your
settings stay on your machine. A variable set in the real environment beats
the file, which is how a server or a CI job configures itself without one.

```bash
python src/config.py     # what the app will actually use, without starting it
```

Only two normally change:

| Variable | Laptop | Server |
|---|---|---|
| `DASH_DEBUG` | `true` | **`false`** — the debug console executes Python on the host |
| `DASH_HOST` | `127.0.0.1` | `0.0.0.0`, or nothing outside the machine can reach it |

Setting `DASH_HOST=0.0.0.0` with `DASH_DEBUG=false` is also how you let
colleagues on the office network open your laptop's copy, at
`http://<your-ip>:8050`.

What is *not* configurable, deliberately: domain constants that never change
between machines. Configuration is what differs between where the app runs;
everything else stays in Python, next to the code that uses it.

## Layout

```
src/
├── app.py            Dash shell: side navigation, mock 4insight header
├── config.py         everything that differs between laptop, server and CI
├── theme.py          colours, type scale and the Plotly template
├── pages/
│   ├── home.py       example: an AgGrid over the sample data
│   └── analytics.py  example: a slicer driving a filtered Plotly chart
└── assets/
    ├── css/main.css  page styling, mirrors theme.py as CSS variables
    ├── 4insight_logo.png
    └── sample_data.csv

notebooks/            ad-hoc exploration, outside the running app
tests/                pytest suite
.github/              CI workflow + PR template
.env.example          every setting, documented; copy to .env to override
```

Pages register themselves with `dash.register_page`, and the sidebar is built
from `dash.page_registry` — adding a page means adding one file in `pages/`,
with nothing else to update.

There's no separate `data.py`/`components.py`/`figures.py` layer here — with
two pages and a small sample dataset it would be more indirection than it's
worth. As a real project's pages start repeating the same loading, filtering
or figure-building code, that's the point to pull the shared logic into its
own module.

## Fitting the 4insight frame

Real deployments serve this app inside an iframe on 4insight, under a header
that takes 84px, with 24px of dead space below the frame. Set
`MOCK_PLATFORM_CHROME=84` in `.env` and the app reserves the same space
locally — the bar shows the 4insight logo and a "Placeholder title" standing
in for where 4insight's own header names the dashboard, plus a small dev note
so nobody mistakes the bar for real UI. Two decisions follow from it:

- **No page title in the app.** 4insight's header already names the dashboard.
- **Navigation is a sidebar**, not a row of tabs. Width is the plentiful
  dimension inside the frame; height is not.

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
callback's component IDs actually exist in its page, the mock header, and the
configuration layer — including that `.env.example` documents exactly the
variables `config.py` reads, no more and no fewer.

## Contributing

`CONTRIBUTING.md` holds the definition of done — the checklist every change
ticks before it is merged. It appears automatically on every pull request.

CI runs black, an import check and the full test suite on every push to
`main` and every pull request.

## Conventions

`CLAUDE.md` holds the Dash conventions for this repo — architecture,
callbacks, layout, charts. Read it before adding a page. Format with
`black .` before committing — options come from `pyproject.toml`.
