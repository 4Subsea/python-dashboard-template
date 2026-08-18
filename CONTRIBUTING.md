# Contributing

## Definition of done

Every change ticks all of these before it is merged. The list lives in the pull request template (.github/pull_request_template.md) so that the PR request is pre-populated at creation. 


- [ ] **`pytest` passes** (CI checks this)
- [ ] **`black` is clean**  (CI checks this)
- [ ] **Every threshold, unit and label comes from a named constant**, not a
      literal. If a number decides a colour or a pass/fail, it is defined once
      and read by the chart, the conditional formatting and the caption alike.
- [ ] **Anything machine-specific goes in `.env.example`**, not hardcoded —
      unless it's a deliberate simplification, documented where it deviates
      (see README's Configuration section for this template's own exception).
      Domain constants are not machine-specific either way.
- [ ] **Every page opened and looked at** after the change. Layout and rendering
      faults do not appear in a diff or in a test run.
- [ ] **At least one displayed number spot-checked** against the source.
- [ ] **`CLAUDE.md` updated** if the change establishes a new convention, and
      **`README.md`** if it changes how to run, refresh or deploy anything.


## Conventions

`CLAUDE.md` holds the Dash conventions for this repo — architecture, callbacks,
layout, charts. Read it before your first change.

The 4Subsea PBI style guide governs all colours, typography and figure
conventions: <https://miro.com/app/board/uXjVHbD9HV0=/>. Note that the theme 
was translated by claude on 2026-07-30 and an update will require manual 
triggering. 

If a change deliberately deviates from `CLAUDE.md`, document it: one place (the
README is a good default), a comment at the line that deviates naming the
rule, and why.

## Continuous integration

`.github/workflows/ci.yml` runs on every push to `main` and every pull request:

1. `black --check --diff .` — formatting
2. `pytest` — the full suite

Options live in `pyproject.toml`, so the commands below behave identically for
you, for your editor and for CI. Do not pass `--line-length` by hand; if the
config and the flag ever disagree you will reformat the whole repo.

`.pre-commit-config.yaml` runs black locally on the same files, so installing
the hooks (see "Running things" below) catches most formatting issues before
they ever reach CI.

## Running things

```bash
pip install -r requirements-dev.txt        # app + tests + formatter
pip install -r requirements-notebooks.txt  # adds Jupyter for notebooks/

# optional but recommended: auto-format staged files with black on commit
pre-commit install --hook-type pre-commit
# optional: run black check before push as well
pre-commit install --hook-type pre-push

cp .env.example .env                       # optional; defaults work as-is

python src/app.py                          # the app, on :5050
pytest                                     # the tests
black .                                    # format
pre-commit run --all-files                 # run configured hooks manually
```
