from pathlib import Path
from shutil import copy2

import yaml


ROOT = Path(__file__).resolve().parents[1]

EVENTS_DIR = ROOT / "programming-club"
OUTPUT_DIR = ROOT / "docs" / "sessions" / "programming-club"
OUTPUT_FILE = OUTPUT_DIR / "index.md"


def read_event(event_file: Path) -> dict:
    """Read and validate a programming-club event."""
    with event_file.open(encoding="utf-8") as file:
        event = yaml.safe_load(file)

    required_fields = {
        "name",
        "title",
        "date",
        "author",
        "repositories",
    }

    missing_fields = required_fields - event.keys()

    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"{event_file} is missing fields: {missing}")

    repository = event["repositories"]

    if "location" not in repository or "name" not in repository:
        raise ValueError(
            f"{event_file}: repositories must contain location and name"
        )

    if repository["location"] in ("github", "colab") and "url" not in repository:
        raise ValueError(
            f"{event_file}: External repositories must include a URL"
        )

    event["date"] = str(event["date"])
    event["directory"] = event_file.parent.name
    event["source_directory"] = event_file.parent

    return event


def copy_local_resource(event: dict) -> Path:
    """
    Copy a local notebook or resource into the MkDocs documentation tree.

    Returns its path relative to the programming-club index.
    """
    repository = event["repositories"]
    source = event["source_directory"] / repository["name"]

    if not source.exists():
        raise FileNotFoundError(
            f"Local resource does not exist: {source}"
        )

    destination_directory = OUTPUT_DIR / event["directory"]
    destination_directory.mkdir(parents=True, exist_ok=True)

    destination = destination_directory / source.name
    copy2(source, destination)

    return Path(event["directory"]) / source.name


def resource_details(event: dict) -> tuple[str, str]:
    """
    Return the URL and display label for an event resource.
    """
    repository = event["repositories"]
    location = repository["location"].lower()

    if location == "local":
        relative_path = copy_local_resource(event)

        if relative_path.suffix == ".ipynb":
            label = "Notebook"
        else:
            label = repository["name"]

        return relative_path.as_posix(), label

    if location == "github":
        return repository["url"], "GitHub repository"

    if location == "colab":
        return None, None

    raise ValueError(
        f'{event["directory"]}: unsupported repository location '
        f'"{repository["location"]}"'
    )


def table_row(event: dict) -> str:
    """Generate one Markdown table row."""

    repository = event["repositories"]
    location = repository["location"].lower()

    if location == "colab":
        url = repository["url"]
        linked_resource = f"<a href=\"{repository["url"]}\"> <img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/>"
    else:
        url, resource_label = resource_details(event)
        linked_resource = f"[{resource_label}]({url})"

    linked_title = f'[{event["title"]}]({url})'

    return (
        f'| {event["date"]} '
        f'| {linked_title} '
        f'| {event["author"]} '
        f'| {linked_resource} |'
    )


def generate_page(events: list[dict]) -> str:
    """Generate the complete Programming Club index."""
    lines = [
        "# Programming Club",
        "",
        "Practical programming sessions covering data analysis, "
        "machine learning and scientific computing.",
        "",
        "| Date | Title | Author | Repositories / notebooks |",
        "|---|---|---|---|",
    ]

    lines.extend(table_row(event) for event in events)
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    event_files = sorted(EVENTS_DIR.glob("*/event.yml"))

    if not event_files:
        raise FileNotFoundError(
            f"No event.yml files found in {EVENTS_DIR}"
        )

    events = [read_event(event_file) for event_file in event_files]
    events.sort(key=lambda event: (event["date"], event["title"]))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(generate_page(events), encoding="utf-8")

    local_count = sum(
        event["repositories"]["location"].lower() == "local"
        for event in events
    )

    print(f"Generated {OUTPUT_FILE}")
    print(f"Events: {len(events)}")
    print(f"Local resources copied: {local_count}")


if __name__ == "__main__":
    main()
