#!/usr/bin/env python3

"""Split tweets from stdin into 3 outputs: pre, during, and post game."""

import sys
import datetime

from common import log, read_time

dt = datetime.datetime


class out(object):
    """Stateful output writer."""

    def __init__(self, fn):
        """Set up context-ed writer."""
        self.count = 0
        self.fn = fn

    def __enter__(self):
        """Begin context mgmt of writer."""
        self.fh = open(self.fn, "w")
        log("Open: {}", self.fn)
        return self

    def __exit__(self, *args):
        """All done with writer."""
        self.fh.close()

    def write(self, line):
        """Line writing."""
        self.fh.write(line.strip() + '\n')
        self.count += 1

    def report(self):
        """Report what we've done."""
        log("{:<30s}: {:12,d}", self.fn, self.count)


def main():
    """Entry point."""
    args = sys.argv[1:]
    if len(args) != 1:
        raise ValueError("No file prefix given")
    prefix = args[0]

    prename = prefix + "-pregame.json"
    durname = prefix + "-game.json"
    postname = prefix + "-postgame.json"

    # Kick off was Feb 5, 2017, 5:30pm US Central Time - which is 11:30pm UTC.
    # Note that we also back off 30 minutes. We add 6 hours to get game end
    # (which is 11pm US Central).
    GAME_START = dt(2017, 2, 5, 23, 0, 0, tzinfo=datetime.timezone.utc)
    GAME_END = GAME_START + datetime.timedelta(hours=6)

    log("Starting")
    count = 0

    with out(prename) as pre, out(durname) as dur, out(postname) as post:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue  # don't count blanks

            # Write out to the appropriate file
            time = read_time(line)
            if time < GAME_START:
                chosen = pre
            elif time > GAME_END:
                chosen = post
            else:
                chosen = dur
            chosen.write(line)

            count += 1
            if count % 200000 == 0:
                log("...progress: read {:12,d}", count)

        for i in [pre, dur, post]:
            i.report()

    log("Total Processing: {:,d}", count)


if __name__ == '__main__':
    main()
