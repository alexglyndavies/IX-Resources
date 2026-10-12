"""Validate session metadata and generate MkDocs pages from source collections."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from html import escape
from pathlib import Path
from shutil import copy2
from urllib.parse import quote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
COLLECTIONS = {
    "talks": "List of Talks",
    "programming-club": "Programming Club",
    "technical-tutorials": "Technical Tutorials",
}


@dataclass
class Resource:
    label: str
    url: str
    source: Path | None = None
    destination: Path | None = None


@dataclass
class Event:
    title: str
    author: str
    date: date
    resources: list[Resource]
    poster: Resource | None = None


def local_resource(root: Path, collection: str, folder: Path, value: str, label: str) -> Resource:
    source = (folder / value).resolve()
    if not source.is_relative_to(folder.resolve()):
        raise ValueError("local resources must stay inside the event folder")
    if not source.is_file():
        raise ValueError(f"missing local resource: {source}")
    relative = Path(folder.name) / source.relative_to(folder.resolve())
    destination = root / "docs" / "sessions" / collection / relative
    return Resource(label, quote(relative.as_posix(), safe="/"), source, destination)


def text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def read_event(path: Path, collection: str, root: Path = ROOT) -> Event | None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("expected a YAML mapping")
    status = data.get("status", "published")
    if status not in ("published", "draft"):
        raise ValueError("status must be published or draft")
    if status == "draft":
        return None
    title = text(data.get("title"), "title")
    author = text(data.get("author"), "author")
    try:
        event_date = date.fromisoformat(str(data.get("date")))
    except ValueError as exc:
        raise ValueError("date must be a valid YYYY-MM-DD date") from exc
    if title in ("...", "None"):
        title = "Title to be announced"
    resources = data.get("resources")
    if resources is None:
        legacy = data.get("repositories")
        resources = [] if legacy is None else [legacy]
        if data.get("content"):
            content = data["content"]
            if not isinstance(content, dict):
                raise ValueError("content must be a mapping")
            resources.append({"path": content.get("file"), "label": "Slides"})
    if not isinstance(resources, list):
        raise ValueError("resources must be a list")
    parsed = []
    for resource in resources:
        if not isinstance(resource, dict):
            raise ValueError("each resource must be a mapping")
        location = resource.get("location")
        if location is not None and location not in ("local", "github", "colab"):
            raise ValueError(f"unsupported resource location: {location}")
        local = resource.get("path") or (resource.get("name") if location == "local" else None)
        url = resource.get("url")
        if bool(local) == bool(url):
            raise ValueError("each resource needs exactly one path or URL")
        label = text(resource.get("label", {"github": "GitHub repository", "colab": "Open in Colab"}.get(location, "Notebook" if str(local).endswith(".ipynb") else "Download")), "resource label")
        if local:
            # Existing talk slides have already been published under docs/assets.
            legacy_slide = root / "docs" / "assets" / "slides" / f"{path.parent.name}.pdf"
            if "content" in data and not (path.parent / local).is_file() and legacy_slide.is_file():
                parsed.append(Resource(label, f"../../assets/slides/{quote(legacy_slide.name)}"))
            else:
                parsed.append(local_resource(root, collection, path.parent, text(local, "path"), label))
        else:
            url = text(url, "URL")
            parts = urlsplit(url)
            if parts.scheme not in ("http", "https") or not parts.netloc:
                raise ValueError("resource URL must be an absolute HTTP(S) URL")
            parsed.append(Resource(label, quote(url, safe=":/?&=%#+@,;~")))
    poster = None
    if data.get("poster"):
        poster = local_resource(root, collection, path.parent, text(data["poster"], "poster"), "Poster")
    elif collection == "talks":
        for suffix in ("png", "jpg", "jpeg"):
            candidate = root / "docs" / "assets" / "posters" / f"{path.parent.name}.{suffix}"
            if candidate.is_file():
                poster = Resource("Poster", f"../../assets/posters/{quote(candidate.name)}")
                break
    return Event(title, author, event_date, parsed, poster)


def cell(value: str) -> str:
    return escape(value).replace("|", "&#124;").replace("\n", " ").replace("\r", " ").replace("[", "&#91;").replace("]", "&#93;")


def link(label: str, url: str) -> str:
    return f"[{cell(label)}]({url})"


def render(collection: str, events: list[Event]) -> str:
    lines = ["<!-- Generated by code/generate_sessions.py; edit source event.yml files. -->", "", f"# {COLLECTIONS[collection]}", ""]
    if any(event.poster for event in events):
        lines.extend(['<div class="poster-grid" markdown="1">', ''])
        for event in events:
            if event.poster:
                img = f"![{cell(f'Poster for {event.title} by {event.author}')}]({event.poster.url})"
                if event.resources:
                    img = f"[{img}]({event.resources[0].url})"
                lines.extend([img, ""])
        lines.extend(["</div>", ""])
    lines.extend(["| Date | Title | Author | Resources |", "|---|---|---|---|"])
    for event in events:
        title = link(event.title, event.resources[0].url) if event.resources else cell(event.title)
        resources = " · ".join(link(resource.label, resource.url) for resource in event.resources) or "—"
        lines.append(f"| {event.date} | {title} | {cell(event.author)} | {resources} |")
    return "\n".join(lines) + "\n"


def generate(root: Path = ROOT, collections: list[str] | None = None, check: bool = False) -> None:
    pages = {}
    errors = []
    for collection in collections or list(COLLECTIONS):
        paths = sorted((root / collection).glob("*/event.yml"))
        if not paths:
            errors.append(f"{collection}: no event.yml files found")
        events = []
        for path in paths:
            try:
                event = read_event(path, collection, root)
                if event:
                    events.append(event)
            except (ValueError, TypeError, yaml.YAMLError) as exc:
                errors.append(f"{path.relative_to(root)}: {exc}")
        events.sort(key=lambda event: (event.date, event.title), reverse=True)
        pages[collection] = events
    if errors:
        raise ValueError("Invalid session metadata:\n" + "\n".join(errors))
    for collection, events in pages.items():
        if not check:
            for event in events:
                for resource in [*event.resources, event.poster]:
                    if resource and resource.source:
                        resource.destination.parent.mkdir(parents=True, exist_ok=True)
                        copy2(resource.source, resource.destination)
            output = root / "docs" / "sessions" / collection / "index.md"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(render(collection, events), encoding="utf-8")
        print(f'{collection}: {len(events)} published sessions {"validated" if check else "generated"}')


def main(collections: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without writing files")
    parser.add_argument("--collection", action="append", choices=COLLECTIONS)
    args = parser.parse_args()
    try:
        generate(collections=collections or args.collection, check=args.check)
    except ValueError as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
