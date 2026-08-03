"""Put src/ on the path so the tests import the app modules the way Dash does."""

import pathlib
import sys

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def text_of(children):
    """Flatten a Dash `children` value (str, component or list) back to text."""
    if children is None:
        return ""
    if isinstance(children, str):
        return children
    if isinstance(children, (list, tuple)):
        return "".join(text_of(c) for c in children)
    return text_of(getattr(children, "children", None))
