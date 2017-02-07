#!/usr/bin/env python3

"""Remove duplicate tweets from stdin and write to stdout."""

import sys

from common import log, json_parse


class filt(object):
    """Stateful filtering object for the input stream."""

    def __init__(self):
        """Set up filt object."""
        self.seen = set()

    def keep(self, line):
        """Return true if the line should be kept."""
        tid = int(json_parse(line).get('TweetID'))
        if tid in self.seen:
            return False
        self.seen.add(tid)
        return True


def main():
    """Entry point."""
    f = filt()
    count, skipped = 0, 0
    log("Starting")

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue  # don't count blanks

        if not f.keep(line):
            skipped += 1
            continue

        sys.stdout.write(line)
        sys.stdout.write('\n')

        count += 1
        if count % 200000 == 0:
            log("...progress: read {:12,d} skipped {:12,d}", count, skipped)

    log("Skipped: {:12,d}", skipped)
    log("Output:  {:12,d}", count)


if __name__ == '__main__':
    main()
