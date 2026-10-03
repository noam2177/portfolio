"""Register a project so the next session can continue it. One id, one row.

One command writes the portfolio row, the tracker block, and the file-bus
folder the work wave reads. A second call refreshes the same id.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "projects.json"
FIELDS = ("id", "title", "kind", "path", "url", "stage", "next", "updated")
_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{0,62}$")
_BLOCKED = ("sagole", "octave", "secure_data_939", "real_inputs")


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


def assert_admissible(row: dict) -> None:
    project_id = str(row.get("id") or "")
    if not _ID.match(project_id):
        raise ValueError("bad_id")
    blob = " ".join(str(row.get(key) or "") for key in ("id", "path", "title", "url")).lower()
    if any(token in blob for token in _BLOCKED):
        raise ValueError("project_not_admissible")


def tracker_block(row: dict) -> str:
    project_id = str(row.get("id") or "")
    title = str(row.get("title") or project_id)
    stage = str(row.get("stage") or "נרשם")
    nxt = str(row.get("next") or "להמשיך מהנתיב")
    path = str(row.get("path") or "")
    return (
        f"<!-- project:{project_id} -->\n"
        f"## {title} · `{project_id}`\n\n"
        f"- שלב: {stage}\n"
        f"- הבא: {nxt}\n"
        f"- נתיב: `{path}`\n"
        f"<!-- /project:{project_id} -->\n"
    )


def upsert_tracker(text: str, row: dict) -> str:
    """Replace the marked block for this id, or append one."""
    project_id = str(row.get("id") or "")
    block = tracker_block(row)
    pattern = re.compile(
        rf"<!-- project:{re.escape(project_id)} -->.*?<!-- /project:{re.escape(project_id)} -->\n?",
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(lambda _match: block, text, count=1)
    base = text if text.endswith("\n") else text + "\n"
    return base + "\n" + block


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _agent_for(row: dict) -> str:
    path = str(row.get("path") or "").lower()
    if "principal-architect-hub" in path:
        return "chief_architect"
    return "personal_projects_agent"


def sync_file_bus(row: dict, projects: Path) -> None:
    """Create the continuation folder and registry row. Refresh the open next step."""
    project_id = str(row["id"])
    folder = projects / project_id
    folder.mkdir(parents=True, exist_ok=True)
    title = str(row.get("title") or project_id)
    agent = _agent_for(row)
    nxt = str(row.get("next") or "להמשיך מהנתיב")
    knowledge = folder / "PROJECT_KNOWLEDGE.md"
    if not knowledge.is_file():
        knowledge.write_text(
            "\n".join(
                [
                    f"# Project knowledge — {project_id}",
                    "",
                    f"Assigned agent: `{agent}`",
                    "Pipeline: `portfolio_continue`",
                    f"Created_utc: {_utc()}",
                    "",
                    "## Specs",
                    f"- Product: {title}",
                    f"- Path: {row.get('path') or ''}",
                    f"- Stage: {row.get('stage') or ''}",
                    "",
                    "## Progress",
                    f"- Next: {nxt}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    checklist_path = folder / "OPERATIONAL_CHECKLIST.json"
    if checklist_path.is_file():
        checklist = json.loads(checklist_path.read_text(encoding="utf-8"))
        if not isinstance(checklist, dict):
            checklist = {}
    else:
        checklist = {
            "schema_version": 1,
            "project_id": project_id,
            "title": title,
            "assigned_agent": agent,
            "pipeline": "portfolio_continue",
            "gates": [
                {"id": "registered", "title": "נרשם במאגר הפרויקטים", "done": True, "auto": True},
                {"id": "continue_next", "title": nxt, "done": False, "halt": True},
            ],
        }
    gates = checklist.get("gates")
    if isinstance(gates, list):
        for gate in gates:
            if isinstance(gate, dict) and gate.get("id") == "continue_next" and not gate.get("done"):
                gate["title"] = nxt
    checklist["title"] = title
    checklist["assigned_agent"] = agent
    checklist_path.write_text(json.dumps(checklist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (folder / "NEXT_STEPS.md").write_text(f"# Next steps\n\n{nxt}\n", encoding="utf-8")
    registry_path = projects / "PROJECT_REGISTRY.json"
    if registry_path.is_file():
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    else:
        data = {"schema_version": 1, "projects": []}
    rows = data.get("projects") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        rows = []
    found = False
    for existing in rows:
        if isinstance(existing, dict) and existing.get("project_id") == project_id:
            existing["title"] = title
            existing["assigned_agent"] = agent
            existing["pipeline"] = str(existing.get("pipeline") or "portfolio_continue")
            existing["updated_utc"] = _utc()
            found = True
            break
    if not found:
        rows.append(
            {
                "project_id": project_id,
                "title": title,
                "assigned_agent": agent,
                "pipeline": "portfolio_continue",
                "updated_utc": _utc(),
            }
        )
    registry_path.write_text(
        json.dumps({"schema_version": 1, "projects": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def local_projects_dir() -> Path | None:
    candidate = Path.home() / "Documents" / "form939-local-sandbox" / "file_bus" / "projects"
    if candidate.is_dir():
        return candidate
    return None


def continue_locally(row: dict) -> None:
    """Mirror the row into the sandbox tracker and file bus when they exist."""
    projects = local_projects_dir()
    if projects is None:
        return
    tracker = projects / "PROJECT_TRACKER.md"
    if tracker.is_file():
        tracker.write_text(upsert_tracker(tracker.read_text(encoding="utf-8"), row), encoding="utf-8")
    sync_file_bus(row, projects)


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
    row = {
        "id": args.id,
        "title": args.title or args.id,
        "kind": args.kind,
        "path": args.path,
        "url": args.url,
        "stage": args.stage,
        "next": args.next,
        "updated": args.updated,
    }
    assert_admissible(row)
    rows = upsert(row)
    save(rows)
    (ROOT / "PROJECTS.md").write_text(render(rows), encoding="utf-8")
    continue_locally(row)
    print(args.id)


if __name__ == "__main__":
    main()
