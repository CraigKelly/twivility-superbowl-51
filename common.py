"""Provide common functions for the processing scripts."""

import sys


def flush():
    """Flush all possible outputs."""
    sys.stdout.flush()
    sys.stderr.flush()


def log(s, *args):
    """Log a message to stderr with optional formatting."""
    if args:
        s = s.format(*args)
    sys.stderr.write(s + '\n')
    flush()


# Special: we try and use ujson but fall back to ujson
try:
    import ujson as json
except:
    log("Could not import ujson: will use the slower std json")
    import json


json_parse = json.loads
