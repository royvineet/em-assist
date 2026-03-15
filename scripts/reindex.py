#!/usr/bin/env python3
"""
Rebuild index.yaml by scanning meetings/, projects/, and files/.

Run this after bulk-adding meetings or files, or when the index is out of sync.

Usage:
    python scripts/reindex.py
"""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
_config = yaml.safe_load((ROOT / "config" / "config.yaml").read_text(encoding="utf-8"))
_storage = _config["storage"]

MEETINGS_DIR = Path(_storage["meetings_dir"]).expanduser()
PROJECTS_DIR = Path(_storage["projects_dir"]).expanduser()
FILES_DIR = Path(_storage["files_dir"]).expanduser()
INDEX_PATH = Path(_storage["index"]).expanduser()

# Meeting filename pattern: YYYY-MM-DD-<type>[-<qualifier>].md
MEETING_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?P<type>[a-z0-9]+)(?:-(?P<qualifier>.+))?$"
)


def index_meetings() -> list[dict]:
    entries = []
    if not MEETINGS_DIR.exists():
        return entries

    for md_file in sorted(MEETINGS_DIR.glob("*.md")):
        m = MEETING_RE.match(md_file.stem)
        if not m:
            continue

        content = md_file.read_text(encoding="utf-8")

        # Extract tags line: "tags: foo, bar"
        tags = []
        tag_match = re.search(r"^tags:\s*(.+)$", content, re.MULTILINE | re.IGNORECASE)
        if tag_match:
            tags = [t.strip() for t in tag_match.group(1).split(",") if t.strip()]

        # Extract project from header block: "- Project: <key>"
        project = ""
        proj_match = re.search(r"^-\s*Project:\s*(.+)$", content, re.MULTILINE)
        if proj_match:
            val = proj_match.group(1).strip()
            if val.lower() not in ("none", "null", ""):
                project = val

        # Extract attendees from header block: "- Attendees: ..."
        attendees = []
        att_match = re.search(r"^-\s*Attendees:\s*(.+)$", content, re.MULTILINE)
        if att_match:
            attendees = [a.strip() for a in att_match.group(1).split(",") if a.strip()]

        # Build summary from first meaningful non-header line after the "---" separator
        summary = ""
        lines = content.splitlines()
        past_header = False
        summary_parts = []
        for line in lines:
            if line.strip() == "---":
                past_header = True
                continue
            if not past_header:
                continue
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.lower().startswith("tags:"):
                clean = re.sub(r"^#{1,6}\s*", "", stripped)
                if clean and clean != "---":
                    summary_parts.append(clean)
                if len(summary_parts) >= 2:
                    break
        summary = " | ".join(summary_parts)

        entries.append({
            "date": m.group("date"),
            "type": m.group("type"),
            "qualifier": m.group("qualifier") or "",
            "filename": md_file.stem,
            "attendees": attendees,
            "project": project,
            "tags": tags,
            "summary": summary,
        })

    return entries


def index_projects() -> list[dict]:
    entries = []
    if not PROJECTS_DIR.exists():
        return entries

    for yaml_file in sorted(PROJECTS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            if not data or "project" not in data:
                continue
            p = data["project"]
            entries.append({
                "key": p.get("key", yaml_file.stem),
                "name": p.get("name", ""),
                "status": p.get("status", ""),
                "summary": p.get("description", "")[:120],
                "tags": [t.lower() for t in p.get("tech_stack", [])],
            })
        except Exception as e:
            print(f"Warning: could not read {yaml_file}: {e}", file=sys.stderr)

    return entries


def index_files() -> list[dict]:
    entries = []
    if not FILES_DIR.exists():
        return entries

    for meta_file in sorted(FILES_DIR.rglob("*.meta.yaml")):
        try:
            meta = yaml.safe_load(meta_file.read_text(encoding="utf-8"))
            if not meta:
                continue
            entries.append({
                "path": meta.get("stored_path", str(meta_file)),
                "category": meta.get("category", ""),
                "subcategory": meta.get("subcategory", ""),
                "summary": meta.get("summary", ""),
                "tags": meta.get("tags", []),
            })
        except Exception as e:
            print(f"Warning: could not read {meta_file}: {e}", file=sys.stderr)

    return entries


def main():
    meetings = index_meetings()
    projects = index_projects()
    files = index_files()

    index = {
        "last_updated": date.today().isoformat(),
        "meetings": meetings,
        "projects": projects,
        "files": files,
    }

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        yaml.dump(index, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )

    print(
        f"Index rebuilt: {len(meetings)} meetings, "
        f"{len(projects)} projects, {len(files)} files."
    )


if __name__ == "__main__":
    main()
