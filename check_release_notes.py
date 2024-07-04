#!/usr/bin/env python3

import os
import re
import sys
import json

import github

def get_env(env_name):
    value = os.getenv(env_name)
    # print(f"ENV {env_name} = {value}", file=sys.stdout)
    return value

def fail(message):
    with open(GITHUB_RESULT_PATH, "a+") as output_file:
        output_file.write(message + "\n")
    # print(f'FAIL: {message}', file=sys.stderr)
    print(f'::error::{message}')

def info(message):
    with open(GITHUB_RESULT_PATH, "a+") as output_file:
        output_file.write(message + "\n")
    # print(f'INFO: {message}', file=sys.stderr)
    print(f'::notice::{message}')


GITHUB_EVENT_PATH = get_env("GITHUB_EVENT_PATH")
GITHUB_RESULT_PATH = get_env("GITHUB_STEP_SUMMARY")

github_data = json.load(open(GITHUB_EVENT_PATH))

gh = github.Github()

repo_name = get_env("GITHUB_REPOSITORY")
pr_number = github_data['number']

repo = gh.get_repo(repo_name)
pr = repo.get_pull(pr_number)

release_note_label = repo.get_label("release-note-required")

if release_note_label in pr.labels:
    if result := re.search("(?<=```release-note\n).*?(?=\n```)", pr.body, re.DOTALL):
        release_note = result.group().strip()
        if not release_note:
            fail('Release note is empty')
            sys.exit(-1)
        if release_note.lower() == "tbd":
            fail('Release note contains "TBD"')
            sys.exit(-1)
    else:
        fail('No release notes found in PR body')
        sys.exit(-1)
else:
    info('No release note required')

sys.exit(0)