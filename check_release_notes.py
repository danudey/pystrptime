#!/usr/bin/env python3

import os
import re
import sys
import json

import github

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

github_data = json.load(open(GITHUB_EVENT_PATH))

gh = github.Github()

repo_name = os.getenv("GH_REPO")
pr_number = github_data['number']

repo = gh.get_repo(repo_name)
pr = repo.get_pull(pr_number)

release_note_label = repo.get_label("release-note-required")

if release_note_label in pr.labels:
    if result := re.search("(?<=```release-note\n).*?(?=\n```)", pr.body, re.DOTALL):
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
else:
    print('INFO: no release note required', file=sys.stderr)

sys.exit(0)