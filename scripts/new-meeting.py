#!/usr/bin/env python3
"""
Scaffold a new meeting note file with the correct typed template.

Usage:
    python scripts/new-meeting.py <type> [qualifier]

Types: standup | 1on1 | retro | planning | review | cross-team | interview | other

Examples:
    python scripts/new-meeting.py standup
    python scripts/new-meeting.py 1on1 priya-sharma
    python scripts/new-meeting.py retro sprint-43
    python scripts/new-meeting.py planning sprint-44
    python scripts/new-meeting.py interview backend-candidate
"""

import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
_config = yaml.safe_load((ROOT / "config" / "config.yaml").read_text(encoding="utf-8"))
MEETINGS_DIR = Path(_config["storage"]["meetings_dir"]).expanduser()

TEMPLATES = {
    "standup": """\
# Standup — {date}

- Date: {datetime}
- Type: standup
- Attendees:
- Project:
- Duration: 15

---

## Updates

| Person | Yesterday | Today | Blockers |
|--------|-----------|-------|----------|
| | | | |

## Blockers & Follow-ups

- [ ] [Owner]: [action] — [by when]

---
tags: standup
""",

    "1on1": """\
# 1:1 — {qualifier_title} — {date}

- Date: {datetime}
- Type: 1on1
- Attendees: {qualifier_title},
- Project: none
- Duration: 30

---

## How are they doing?



## Their agenda

-

## Manager agenda

-

## Project / work update



## Career & growth



## Action items

- [ ] [Owner]: [action] [by date]

## Private notes



---
tags: 1on1{qualifier_tag}
""",

    "retro": """\
# Retro — {qualifier_title} — {date}

- Date: {datetime}
- Type: retro
- Attendees:
- Project:
- Duration: 60

---

## What went well

-

## What didn't go well

-

## Puzzles / questions

-

## Action items

- [ ] [Owner]: [action] [by date]

## Patterns (manager's view)



---
tags: retro{qualifier_tag}
""",

    "planning": """\
# Planning — {qualifier_title} — {date}

- Date: {datetime}
- Type: planning
- Attendees:
- Project:
- Duration: 90

---

## Sprint goal



## Capacity

| Person | Available days | Notes |
|--------|----------------|-------|
| | | |

## Committed stories / tickets

| Ticket | Title | Owner | Points |
|--------|-------|-------|--------|
| | | | |

## Risks flagged

-

## Action items

- [ ] [Owner]: [action]

---
tags: planning{qualifier_tag}
""",

    "review": """\
# Sprint Review — {qualifier_title} — {date}

- Date: {datetime}
- Type: review
- Attendees:
- Project:
- Duration: 45

---

## Demo'd

-

## Accepted

-

## Not accepted / carried over

-

## Stakeholder feedback

-

## Action items

- [ ] [Owner]: [action]

---
tags: review{qualifier_tag}
""",

    "cross-team": """\
# Cross-team Sync — {date}

- Date: {datetime}
- Type: cross-team
- Attendees:
- Project:
- Duration: 30

---

## Context



## Discussion

-

## Decisions made

-

## Action items

- [ ] [Owner / team]: [action] [by date]

## Follow-up needed from us

-

---
tags: cross-team
""",

    "interview": """\
# Interview — {qualifier_title} — {date}

- Date: {datetime}
- Type: interview
- Attendees:
- Project: none
- Duration: 45

---

## Candidate

- Name:
- Role applied:
- Interview round:
- Recruiter:

## Areas assessed

| Area | Signal | Notes |
|------|--------|-------|
| System design | | |
| Coding | | |
| Communication | | |
| Culture fit | | |

## Overall impression



## Recommendation

[ ] Strong hire  [ ] Hire  [ ] No hire  [ ] Strong no hire

## Specific feedback for debrief

-

---
tags: interview, hiring{qualifier_tag}
""",

    "other": """\
# Meeting — {date}

- Date: {datetime}
- Type: other
- Attendees:
- Project:
- Duration:

---

## Agenda / context



## Discussion



## Decisions made

-

## Action items

- [ ] [Owner]: [action] [by date]

---
tags:
""",
}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    meeting_type = sys.argv[1].lower()
    qualifier = sys.argv[2].lower().replace(" ", "-") if len(sys.argv) > 2 else ""

    if meeting_type not in TEMPLATES:
        valid = ", ".join(TEMPLATES.keys())
        print(f"Unknown type '{meeting_type}'. Valid types: {valid}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    datetime_str = now.strftime("%Y-%m-%d %H:%M")

    stem = f"{date_str}-{meeting_type}"
    if qualifier:
        stem += f"-{qualifier}"

    qualifier_title = qualifier.replace("-", " ").title() if qualifier else ""
    qualifier_tag = f", {qualifier}" if qualifier else ""

    content = TEMPLATES[meeting_type].format(
        date=date_str,
        datetime=datetime_str,
        qualifier_title=qualifier_title,
        qualifier_tag=qualifier_tag,
    )

    MEETINGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = MEETINGS_DIR / f"{stem}.md"

    if out_path.exists():
        print(f"File already exists: {out_path}", file=sys.stderr)
        sys.exit(1)

    out_path.write_text(content, encoding="utf-8")
    print(f"Created: {out_path}")


if __name__ == "__main__":
    main()
