#!/usr/bin/env python3

"""Read JSON tweets from stdin and write CSV to stdout."""

import sys
import csv

from common import log, json_parse

COLUMNS = [
    "TweetID",         # 64-bit int
    "UserID",          # 64-bit int
    "UserScreenName",  # string
    "UserName",        # string
    "Text",            # string
    "Timestamp",       # string, see ts_to_iso
    "ISOTimestamp",    # string, ts_to_iso
    "FavoriteCount",   # int
    "RetweetCount",    # int
    "Hashtags",        # list
    "Mentions",        # list
    "IsRetweet",       # bool
]


def ts_to_iso(ts):
    """Convert our odd twitter timestamp to an isoformat timestamp."""
    return ts  # todo


def xf_list(lst):
    """Convert list into format for CSV."""
    if not lst:
        return ""
    return "|".join(lst)


def main():
    """Entry point."""
    count = 0
    log("Starting")

    outp = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
    outp.writerow(COLUMNS)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue  # don't count blanks

        # Parse JSON record and perform any field updates
        # Note that some of these updates also function as record checks.
        rec = json_parse(line)
        rec["ISOTimestamp"] = ts_to_iso(rec["Timestamp"])   # Create ISO stamp
        rec["TweetID"] = int(rec["TweetID"])                # handle a big int
        rec["UserID"] = int(rec["UserID"])                  # handle a big int
        rec["FavoriteCount"] = int(rec["FavoriteCount"])    # handle an int
        rec["RetweetCount"] = int(rec["RetweetCount"])      # handle an int
        rec["Hashtags"] = xf_list(rec["Hashtags"])          # handle a list
        rec["Mentions"] = xf_list(rec["Mentions"])          # handle a list

        outp.writerow([rec[c] for c in COLUMNS])
        sys.stdout.write('\n')

        count += 1
        if count % 500000 == 0:
            log("...progress: {:12,d}", count)

    log("Wrote: {:12,d}", count)


if __name__ == '__main__':
    main()
