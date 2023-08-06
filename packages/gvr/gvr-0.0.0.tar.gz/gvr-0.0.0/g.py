#!/usr/bin/env python

import argparse
import sys

def globals():
    import base64
    import json
    import pprint
    import re

    return {"j":   json,
            "b64": base64,
            "pp":  pprint,
            "re":  re}

def locals():
    return {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="the script to invoke on each input line")
    args = parser.parse_args()

    g = globals()
    l = locals()
    for line in sys.stdin:
        line = line.rstrip('\r\n')
        if not line:
            continue

        src = args.script.replace("$$", line).replace("$", f'"{line}"')
        eval(src, g, l)

if __name__ == '__main__':
    main()