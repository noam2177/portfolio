"""Register a project so the next session can continue it. One id, one row."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "projects.json"
FIELDS = ("id", "title", "kind", "path", "url", "stage", "next", "updated")


def load(path: Path = REGISTRY) -> list[dict]:
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("projects") if isinstance(data, dict) else None
    return [row for row in rows if isinstance(row, dict)] if isinstance(rows, list) else []


def save(rows: list[dict], path: Path = REGISTRY) -> None:
    path.write_text(
        json.dumps({"projects": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def upsert(row: dict, rows: list[dict] | None = None) -> list[dict]:
    """Insert a new id or refresh the same id. Does not add a second row."""
    current = list(rows if rows is not None else load())
    incoming = {key: str(row.get(key) or "") for key in FIELDS}
    if not incoming["id"]:
        raise ValueError("id is required")
    for index, old in enumerate(current):
        if old.get("id") == incoming["id"]:
            current[index] = incoming
            return current
    current.append(incoming)
    return current


def render(rows: list[dict]) -> str:
    lines = ["# מאגר פרויקטים", "", "| id | שם | שלב | הבא |", "| --- | --- | --- | --- |"]
    for row in rows:
        lines.append(
            f"| {row.get('id', '')} | {row.get('title', '')} | {row.get('stage', '')} | {row.get('next', '')} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Add or refresh one project in the registry.")
    parser.add_argument("id", nargs="?", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--kind", default="tool")
    parser.add_argument("--path", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--stage", default="")
    parser.add_argument("--next", default="")
    parser.add_argument("--updated", default="")
    args = parser.parse_args()
    if not args.id:
        print(render(load()))
        return
    rows = upsert(
        {
            "id": args.id,
            "title": args.title or args.id,
            "kind": args.kind,
            "path": args.path,
            "url": args.url,
            "stage": args.stage,
            "next": args.next,
            "updated": args.updated,
        }
    )
    save(rows)
    (ROOT / "PROJECTS.md").write_text(render(rows), encoding="utf-8")
    print(args.id)


if __name__ == "__main__":
    main()
