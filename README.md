# I-X learning resources

Session metadata and teaching materials are the source of truth; the scripts in
`code/` generate the session indexes and copy published resources into `docs/`.

## Storage recommendation

Keep YAML and one folder per session. This suits a small, Git-managed collection:
changes are reviewable and notebooks stay beside their metadata. A database would
add deployment and backup work without improving the current publishing workflow.
A single large YAML file would make resource ownership and concurrent edits harder.

Use the same metadata format across talks, programming club and technical tutorials.
For new entries, put posters, slides, notebooks and supporting files in the session
folder and reference them explicitly. This removes reliance on asset naming guesses.
Existing talk assets in `docs/assets/` and legacy `repositories` and `content` fields
remain supported, so migration can be gradual. Generated pages should never be
edited directly. Book club pages remain authored Markdown because they currently
contain reading notes rather than session metadata.

## Add a session

Create `<collection>/YYYY-MM-DD-short-description/event.yml`, where collection is
`talks`, `programming-club` or `technical-tutorials`:

```yaml
title: Introduction to graph neural networks
author: Example Speaker
date: 2026-11-12
status: published
resources:
  - label: Notebook
    path: notebook.ipynb
  - label: GitHub repository
    url: https://github.com/example/tutorial
  - label: Slides
    path: slides.pdf
poster: poster.png
```

`title`, `author` and a valid ISO `date` are required for published sessions.
`status` defaults to `published`. Use `status: draft` while details or materials
are incomplete; drafts are excluded from the website. `resources` and `poster`
are optional. A resource has exactly one local `path` or absolute HTTP(S) `url`,
and an optional `label`. Local paths are relative to the session folder and cannot
escape it. Reference any supporting data/images as resources too, preserving their
relative paths so notebooks can find them. Dependencies and the legacy `name`
field may still be stored as metadata; they are not rendered.

The date in YAML determines sorting and display; folder names are stable identifiers.
Changing a folder name changes published resource URLs. All indexes show newest
sessions first. Existing published URLs/files are retained, including the older
Information Bottleneck notebook URL.

## Generate and preview

From the repository root:

```bash
uv sync --project code
bash code/generate.sh --check  # validate all published metadata without writing
bash code/generate.sh         # regenerate all three indexes and copy local resources
uv run --project code mkdocs serve
```

Run generation before previewing or building locally. Read the Docs runs the same
generator automatically before building. To regenerate just one collection:

```bash
uv run --project code code/generate_sessions.py --collection talks
```

The old `generate_talks.py` and `generate_programming.py` commands remain aliases.
Validation collects errors with their source filenames and completes before any
output is written. Generation is deterministic; stale copied assets are deliberately
retained to preserve existing links. Removing an asset from metadata does not delete
its previously published copy.

Run the generator regression tests:

```bash
uv run --project code python -m unittest discover -s code -p 'test_*.py'
```

## Metadata to review

Four technical tutorials with placeholder titles/materials are marked as drafts.
Complete their metadata and switch them to `published` when ready. The Information
Bottleneck folder is dated `2026-04-28`, but its metadata says `2026-04-08`; the
website continues to use the metadata date pending confirmation. Ivan's talk has
no known title and displays “Title to be announced”.
