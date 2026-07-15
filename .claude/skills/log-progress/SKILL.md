---
name: log-progress
description: Use when the user wants to commit and push their OpenAI Agents SDK learning progress to GitHub (e.g. "log my progress", "commit and push", "update the journal and push"). Appends a new dated entry to README.md documenting what changed and pushes to origin — never rewrites or deletes prior entries.
version: 0.1.0
---

# Log Progress

Commits the day's work and appends a new dated entry to the README's Progress Log — building on top of history, never overwriting it.

## Core rule

**Never edit, reword, reorder, or delete any existing entry under `## Progress Log`.** Only ever insert one new entry. If today's date already has an entry (re-running this skill same day), extend that existing entry with new bullet points instead of creating a duplicate section — still don't remove anything already written.

## Steps

1. **See what changed.**
   - `git status` and `git diff` (plus `git diff --staged` if anything's already staged) to see unstaged/staged work.
   - `git log -5 --oneline` to see recent commit history for context on what's already been logged.

2. **Understand the change, not just the diff.** Skim the actual files that changed (new scripts, edited scripts) to understand *what was learned or built*, not just line-level diffs. Pull from the current conversation's context too if it explains the "why" behind the change (e.g. a design decision, a bug that was fixed, a concept that was learned).

3. **Always check for a recent screenshot — don't wait to be told.** Search `~/Desktop` for an image file modified recently (e.g. `find ~/Desktop -maxdepth 1 -iname "*.png" -mmin -30`). If one exists from around this session's activity, copy it into `assets/` (descriptive filename, e.g. `assets/<topic>_run.png`) and embed it in the entry with a markdown image tag and a short caption. This applies every time this skill runs, not just when the user explicitly attaches or mentions a screenshot.

4. **Draft the entry.** Date header: `### YYYY-MM-DD` (use today's actual date). Under it, one subsection per distinct concept/milestone touched this session (`#### <Concept Name> — path/to/script.py`), each covering all four of:
   - **Concept:** 1-3 sentences on what the concept/technique actually is.
   - **Why it matters:** why this matters in a real/production AI system, not just "because the SDK has it."
   - **Example use cases:** 2 concrete scenarios beyond the toy example just built.
   - **What I built:** the real code written for it (a snippet, not the whole file) plus any non-obvious decisions, bugs found and fixed, or dependency notes — specifics (function/file names, concrete numbers) beat vague summaries like "made progress."
   - If there's a natural "what's next" thread, keep a `**Next up:**` line like prior entries.
   - Match the voice/format of existing entries in README.md — read a couple of them first. If a session only extends one existing concept's script further, extend that concept's subsection rather than making a new one.

5. **Insert the entry.**
   - Read the current `README.md`.
   - Insert the new dated section directly under the `## Progress Log` heading, **above** all existing dated entries (newest-first order).
   - Do not touch anything else in the file.

6. **Stage and commit.**
   - `git add` the specific changed/new files (never `git add -A`/`.` blindly — check `git status` output first and confirm nothing unexpected like `.env` is included; `.gitignore` should already exclude `.venv`/`.env`).
   - Commit message: short, describes the actual change (e.g. `Add cost analysis formatting + interactive input to first agent`), not "update README."

7. **Push.**
   - Push to `origin` on the current branch (`main`).
   - If `origin` isn't configured yet, ask the user for the remote URL rather than guessing.
   - If the push is rejected (remote has commits this branch doesn't), stop and surface that to the user — do not force-push.

8. **Confirm.** Tell the user what was committed/pushed in 1-2 sentences — don't dump the full diff back at them.
