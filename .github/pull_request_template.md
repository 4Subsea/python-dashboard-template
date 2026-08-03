## What changed

<!-- One or two sentences. What does this do that the previous version did not? -->

## Why

<!-- The problem, or the request. Link an issue if there is one. -->

## Definition of done

CI covers the first two. The rest are yours — tick them because you did them,
not because they were already ticked. See `CONTRIBUTING.md` for why each is here.

- [ ] `pytest` passes
- [ ] `black` is clean
- [ ] Every threshold, unit and label comes from a named constant, not a literal
- [ ] Anything machine-specific is in `config.py` and `.env.example`, not in a module
- [ ] Malformed input fails loudly — if this touches data loading, a missing file
      or a shifted spreadsheet raises with a message naming the file
- [ ] Every page opened and looked at after the change
- [ ] At least one displayed number spot-checked against the source
- [ ] `CLAUDE.md` updated if this establishes a new convention, `README.md` if it
      changes how to run, refresh or deploy anything

## Anything the reviewer should look at closely

<!-- Deliberate deviations, judgement calls, things you were unsure about.
     If a number or a threshold changed, say which and what it was before. -->
