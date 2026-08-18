"""Prints RSS memory usage to the terminal on demand.

Opt-in dev aid - see LOG_MEMORY in app.py and .env.example. Nothing here
writes to a file or feeds a log collector; it is only for watching a local
`python src/app.py` session by eye.
"""

_process = None


def _rss_mb():
    global _process
    import psutil

    if _process is None:
        _process = psutil.Process()
    return _process.memory_info().rss / (1024 * 1024)


def log_once(note=""):
    """Print one line right now. `note` names what triggered it, e.g. a path."""
    suffix = f" ({note})" if note else ""
    print(f"[memory] {_rss_mb():.1f} MB RSS{suffix}")
