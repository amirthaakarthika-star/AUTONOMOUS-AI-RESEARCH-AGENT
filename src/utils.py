import os
import re
from datetime import datetime


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def extract_queries_from_plan(plan_text: str) -> list[str]:
    queries = []
    for line in plan_text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            queries.append(cleaned[2:].strip())
    return queries[:4]


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def build_timestamped_filename(topic: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{slugify(topic)[:50]}_{timestamp}.md"


def dedupe_sources(results: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for item in results:
        url = item.get("url")
        if url and url not in seen:
            seen.add(url)
            unique.append(
                {
                    "title": item.get("title", "Untitled Source"),
                    "url": url,
                }
            )
    return unique
