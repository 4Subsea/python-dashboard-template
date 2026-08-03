"""Configuration: defaults, overrides, and the errors for bad values.

Every test reloads config with a controlled environment and with .env reading
disabled, so the suite behaves the same on a machine that has a .env and on
one that does not - including CI.
"""

import importlib
import pathlib
import re

import dotenv
import pytest

import config

ROOT = pathlib.Path(config.__file__).resolve().parents[1]
EXAMPLE = ROOT / ".env.example"

# Every name config reads from the environment.
ENV_VARS = [
    "DASH_DEBUG",
    "DASH_HOST",
    "DASH_PORT",
    "MOCK_PLATFORM_CHROME",
    "MOCK_PLATFORM_GAP",
]


@pytest.fixture
def load(monkeypatch):
    """Reload config with a given environment and no .env, then restore it."""

    def loader(**env):
        monkeypatch.setattr(dotenv, "load_dotenv", lambda *a, **k: False)
        for name in ENV_VARS:
            monkeypatch.delenv(name, raising=False)
        for name, value in env.items():
            monkeypatch.setenv(name, value)
        return importlib.reload(config)

    yield loader
    monkeypatch.undo()
    importlib.reload(config)


# ---------------------------------------------------------------------------
# Defaults - a fresh clone with no .env must run exactly as before
# ---------------------------------------------------------------------------


def test_serving_defaults_are_the_safe_local_ones(load):
    cfg = load()
    assert cfg.DASH_HOST == "127.0.0.1", "must not be reachable off-machine by default"
    assert cfg.DASH_PORT == 8050


# ---------------------------------------------------------------------------
# Booleans, ports and paths people get wrong
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["true", "True", "TRUE"])
def test_debug_can_be_switched_on(load, text):
    assert load(DASH_DEBUG=text).DASH_DEBUG is True


@pytest.mark.parametrize("text", ["false", "False", "no", "0", "flase"])
def test_anything_other_than_true_is_off(load, text):
    """The one setting with a security consequence, so a typo fails safe."""
    assert load(DASH_DEBUG=text).DASH_DEBUG is False


def test_port_is_parsed_as_a_number(load):
    assert load(DASH_PORT="9000").DASH_PORT == 9000


def test_a_blank_port_falls_back_to_the_default(load):
    assert load(DASH_PORT="").DASH_PORT == 8050


# ---------------------------------------------------------------------------
# The 4insight header stand-in
# ---------------------------------------------------------------------------


def test_the_platform_mock_is_off_unless_asked_for(load):
    """It must never reach the server, where the real header already exists."""
    assert load().MOCK_PLATFORM_CHROME == 0


def test_the_platform_mock_takes_a_height(load):
    assert load(MOCK_PLATFORM_CHROME="84").MOCK_PLATFORM_CHROME == 84


# ---------------------------------------------------------------------------
# The example file is the documentation, so keep it honest
# ---------------------------------------------------------------------------


def documented_variables():
    """Names in .env.example, whether commented out or not."""
    text = EXAMPLE.read_text(encoding="utf-8")
    return set(re.findall(r"^#?\s*([A-Z][A-Z0-9_]+)=", text, flags=re.MULTILINE))


def variables_config_reads():
    """Names read via os.getenv() in config.py."""
    source = pathlib.Path(config.__file__).read_text(encoding="utf-8")
    return set(re.findall(r'os\.getenv\(\s*"([A-Z][A-Z0-9_]+)"', source))


def test_every_variable_config_reads_is_documented():
    assert variables_config_reads() - documented_variables() == set()


def test_the_example_documents_nothing_that_does_not_exist():
    """A renamed variable leaves a line that looks like it works but does not."""
    assert documented_variables() - variables_config_reads() == set()


def test_the_list_in_this_file_matches_config():
    """So the `load` fixture keeps isolating every variable as they are added."""
    assert set(ENV_VARS) == variables_config_reads()


def test_env_is_gitignored():
    """It holds machine-specific paths today and a password on the next app."""
    lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    patterns = [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]
    assert ".env" in patterns
    assert ".env.example" not in patterns, "the example is the documentation; commit it"
