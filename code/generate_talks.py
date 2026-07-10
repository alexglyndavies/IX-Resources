from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

TALKS_DIR = ROOT / "talks"
POSTERS_DIR = ROOT / "docs" / "assets" / "posters"
SLIDES_DIR = ROOT / "docs" / "assets" / "slides"
OUTPUT_FILE = ROOT / "docs" / "sessions" / "talks" / "index.md"


def read_event(event_file: Path) -> dict:
    """Read and validate an event.yml file."""
    with event_file.open(encoding="utf-8") as file:
        event = yaml.safe_load(file)

    required_fields = {"name", "title", "date", "author"}
    missing_fields = required_fields - event.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"{event_file} is missing fields: {missing}")

    # PyYAML may parse an ISO date as a datetime.date object.
    event["date"] = str(event["date"])
    event["directory"] = event_file.parent.name

    return event


def find_poster(event: dict) -> Path | None:
    """Find the poster associated with an event."""
    directory_name = event["directory"]

    candidates = [
        POSTERS_DIR / f"{directory_name}.png",
        POSTERS_DIR / f"{directory_name}.jpg",
        POSTERS_DIR / f"{directory_name}.jpeg",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def find_slides(event: dict) -> Path | None:
    """Find the published slides associated with an event."""
    directory_name = event["directory"]
    short_name = directory_name.split("-", maxsplit=3)[-1].lower()

    candidates = [
        # Preferred descriptive name, e.g. 2026-06-11-Farbod.pdf
        SLIDES_DIR / f"{directory_name}.pdf",

        # Short name used in the current assets, e.g. farbod.pdf
        SLIDES_DIR / f"{short_name}.pdf",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def asset_link(asset: Path) -> str:
    """
    Return a link from docs/sessions/talks/index.md to an asset under
    docs/assets/.
    """
    relative_path = asset.relative_to(ROOT / "docs")
    return f"../../{relative_path.as_posix()}"


def poster_html(event: dict, number: int) -> str | None:
    """Generate one poster-grid item."""
    poster = find_poster(event)

    if poster is None:
        return None

    poster_url = asset_link(poster)
    slides = find_slides(event)

    image = (
        f'    <img src="{poster_url}" '
        f'alt="Poster for {event["title"]} by {event["author"]}">'
    )

    if slides is None:
        return image

    slides_url = asset_link(slides)

    return (
        f'    <a href="{slides_url}">\n'
        f"    {image.strip()}\n"
        f"    </a>"
    )


def talk_table_row(event: dict) -> str:
    """Generate one Markdown table row."""
    title = event["title"]
    slides = find_slides(event)

    if slides is not None:
        title = f"[{title}]({asset_link(slides)})"

    return f'| {event["date"]} | {title} | {event["author"]} |'


def generate_page(events: list[dict]) -> str:
    """Generate the complete talks index page."""
    lines = [
        "# Posters",
        "",
        '<div class="poster-grid">',
    ]

    poster_number = 1

    for event in events:
        html = poster_html(event, poster_number)

        if html is not None:
            lines.append(html)
            poster_number += 1

    lines.extend(
        [
            "</div>",
            "",
            "",
            "# List of Talks",
            "",
            "| Date | Talk | Speaker |",
            "|---|---|---|",
        ]
    )

    lines.extend(talk_table_row(event) for event in events)
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    event_files = sorted(TALKS_DIR.glob("*/event.yml"))

    if not event_files:
        raise FileNotFoundError(f"No event.yml files found in {TALKS_DIR}")

    events = [read_event(event_file) for event_file in event_files]
    events.sort(key=lambda event: (event["date"], event["author"]))

    content = generate_page(events)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(content, encoding="utf-8")

    print(f"Generated {OUTPUT_FILE}")
    print(f"Talks: {len(events)}")
    print(f"Posters: {sum(find_poster(event) is not None for event in events)}")


if __name__ == "__main__":
    main()
