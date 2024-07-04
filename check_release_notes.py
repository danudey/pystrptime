#!/usr/bin/env python3

import re
import sys
import json

input_data = json.loads(sys.stdin.read())
pr_body = input_data['body']

if result := re.search("(?<=```release-note\n).*?(?=\n```)", pr_body, re.DOTALL):
    release_note = result.group().strip()
    if not release_note:
        print('FAIL: Release note is empty', file=sys.stderr)
        sys.exit(-1)
    if release_note.lower() == "tbd":
        print('FAIL: Release note contains "TBD"', file=sys.stderr)
        sys.exit(-1)
else:
    print('FAIL: No release notes found in PR body', file=sys.stderr)
    sys.exit(-1)

sys.exit(0)