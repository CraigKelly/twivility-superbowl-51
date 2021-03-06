"""Provide common functions for the processing scripts."""

import sys
import datetime
import inspect

dt = datetime.datetime


def flush():
    """Flush all possible outputs."""
    sys.stdout.flush()
    sys.stderr.flush()


def log(s, *args):
    """Log a message to stderr with optional formatting."""
    if args:
        s = s.format(*args)
    pre = inspect.getfile(sys._getframe(1)) + ": "
    sys.stderr.write(pre + s + '\n')
    flush()


# Special: we try and use ujson but fall back to ujson
try:
    import ujson as json
except:
    log("Could not import ujson: will use the slower std json")
    import json


json_parse = json.loads


def read_time(ts):
    """Convert the twivility timestamp string into a datetime object."""
    # ts is in format 'Mon Feb 06 18:00:37 +0000 2017'
    return dt.strptime(ts, "%a %b %d %H:%M:%S %z %Y")
