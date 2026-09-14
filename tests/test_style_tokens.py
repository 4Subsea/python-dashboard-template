"""Guards against hardcoded colors/fonts creeping back into src/ instead of
using the foursubsea_design_system tokens (see CLAUDE.md "Layout and
Styling"). A hardcoded value is only allowed when its line carries an
`allow-hardcoded: <reason>` comment, so any exception is a deliberate,
documented one rather than a silent regression.
"""

import pathlib
import re

import pytest

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"

HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGB_FUNC = re.compile(r"\brgba?\([^)]*\)")
ALLOW_MARKER = "allow-hardcoded"


def _css_files():
    return sorted((SRC / "assets" / "css").glob("*.css"))


def _py_files():
    return sorted(p for p in SRC.rglob("*.py") if "__pycache__" not in p.parts)


def _matches(path, pattern):
    hits = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        if pattern.search(line):
            hits.append(f"{path.relative_to(SRC.parent)}:{lineno}: {line.strip()}")
    return hits


@pytest.mark.parametrize("path", _css_files(), ids=lambda p: p.name)
def test_css_has_no_hardcoded_colors(path):
    violations = _matches(path, HEX_COLOR) + _matches(path, RGB_FUNC)
    assert not violations, (
        "Hardcoded color(s) found - use a design-system token (var(--...)) "
        "instead, or mark a deliberate exception with an inline "
        "`allow-hardcoded: <reason>` comment:\n" + "\n".join(violations)
    )


@pytest.mark.parametrize("path", _css_files(), ids=lambda p: p.name)
def test_css_font_family_uses_tokens(path):
    violations = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if ALLOW_MARKER in line:
            continue
        if "font-family" in line and "var(" not in line:
            violations.append(f"{path.name}:{lineno}: {line.strip()}")
    assert not violations, (
        "font-family should reference a design-system font token "
        "(var(--font-...)):\n" + "\n".join(violations)
    )


@pytest.mark.parametrize("path", _py_files(), ids=lambda p: p.relative_to(SRC))
def test_python_has_no_hardcoded_colors(path):
    violations = _matches(path, HEX_COLOR)
    assert not violations, (
        "Hardcoded color(s) found in Python - pull the value from "
        "foursubsea_design_system.theme_4insight (T / FILL / LINE / ...) "
        "instead:\n" + "\n".join(violations)
    )
