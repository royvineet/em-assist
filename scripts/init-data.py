#!/usr/bin/env python3
"""
Scaffold the EM-Assist data directory with template files.

Safe to re-run: existing files are never overwritten.
Run once after cloning the repo to get a working data directory.

Usage:
    python scripts/init-data.py [--data-dir PATH]

Options:
    --data-dir PATH   Override the data directory from config/config.yaml
    --force           Overwrite existing files (use with caution)
"""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
_config = yaml.safe_load((ROOT / "config" / "config.yaml").read_text(encoding="utf-8"))
_storage = _config["storage"]

DEFAULT_DATA_DIR = Path(_storage["index"]).expanduser().parent

TODAY = date.today().isoformat()
NEXT_MONDAY = (date.today() + timedelta(days=(7 - date.today().weekday()))).isoformat()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        print(f"  skip  {path.relative_to(path.parent.parent.parent.parent) if path.parts[-4:] else path}  (already exists)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    action = "overwrite" if path.exists() else "create"
    print(f"  {action}  {path}")


# ---------------------------------------------------------------------------
# Template content
# ---------------------------------------------------------------------------

INDEX_YAML = f"""\
last_updated: "{TODAY}"

meetings: []

projects: []

files: []
"""

ACTIONS_YAML = f"""\
# Action items — all tasks and follow-ups tracked by the manager.
# See CLAUDE.md for full field documentation.

actions:
  - id: 1
    title: "Fill in manager profile"
    description: "Complete profiles/manager.md with your name, management style, and schedule."
    status: pending
    priority: high
    due_date: null
    owner: "me"
    project: null
    context: "shallow"
    source_meeting: null
    tags: [setup]
    created_at: "{TODAY}"
    updated_at: "{TODAY}"

  - id: 2
    title: "Add team member profiles"
    description: "Create one profiles/team/<name>.md file per direct report."
    status: pending
    priority: high
    due_date: null
    owner: "me"
    project: null
    context: "shallow"
    source_meeting: null
    tags: [setup]
    created_at: "{TODAY}"
    updated_at: "{TODAY}"
"""

EVENTS_YAML = f"""\
# Calendar events — recurring and one-off meetings.
# See CLAUDE.md for full field documentation.

events:
  - id: 1
    title: "Weekly Team Standup"
    meeting_type: standup
    description: "Daily standup — update as needed."
    start: "{NEXT_MONDAY} 10:00"
    end: "{NEXT_MONDAY} 10:15"
    location: ""
    recurring: weekly
    attendees: []          # fill in profile keys from profiles/team/
    project: null
    notes_file: null
    tags: [standup]
    created_at: "{TODAY}"
"""

DIRECTIVES_MD = """\
# Directives

Hard rules and constraints that override default EM-Assist behavior.
Read this before any scheduling, prioritisation, or suggestion decision.

---

## Working hours & protected time
- No meetings before 09:00 or after 18:00.
- [ TODO ] Add any deep-work focus blocks here, e.g. "Tuesday 09:00–12:00 is focus time."

## Communication preferences
- Async-first; synchronous only for unblocking or relationship work.
- [ TODO ] Add any channel or response-time preferences.

## Team norms
- [ TODO ] e.g. On-call rotation: do not schedule planning on on-call handoff days.

## Current overrides
- None.
  # Add temporary rules here, e.g. "Freeze non-critical actions until Q2 OKRs are signed off."
"""

MANAGER_MD = """\
# Manager Profile

## Identity
- Name:          [ YOUR NAME ]
- Title:         Engineering Manager
- Team:          [ TEAM NAME ]
- Organisation:  [ ORG / COMPANY ]
- Manager:       [ YOUR MANAGER'S NAME ]
- Start date:    [ YYYY-MM-DD ]

## Management style
- [ Describe your approach in a few bullets, e.g. servant-leader, outcome-focused, etc. ]

## Schedule & calendar preferences
- Timezone:      [ e.g. America/New_York ]
- Work days:     Monday – Friday
- Core hours:    09:00 – 18:00
- Deep-work blocks:
    - [ e.g. Tuesday 09:00–12:00 ]
- Travel / commute days:
    - [ e.g. Tuesday and Thursday in-office ]

## Current focus areas
- [ What are you personally most focused on this quarter? ]

## Goals & development
- See profiles/goals.md for OKRs and personal goals.
"""

CALENDAR_MD = """\
# Calendar

## Public / company holidays
| Date       | Name                  | Applies to |
|------------|-----------------------|------------|
| [ YYYY-MM-DD ] | [ Holiday name ]  | all        |

## Team member leave
| Name | From | To | Type | Notes |
|------|------|----|------|-------|
| [ name ] | [ YYYY-MM-DD ] | [ YYYY-MM-DD ] | planned leave | |

## Blackout periods
| From | To | Reason |
|------|----|--------|
| [ YYYY-MM-DD ] | [ YYYY-MM-DD ] | [ e.g. Company all-hands ] |
"""

GOALS_MD = """\
# Goals

## Team OKRs — [ QUARTER, e.g. Q2 2026 ]

### Objective 1: [ Title ]
- KR1: [ Measurable key result ]  — status: on-track | at-risk | done
- KR2: [ Measurable key result ]  — status: on-track | at-risk | done

### Objective 2: [ Title ]
- KR1: [ Measurable key result ]  — status: on-track | at-risk | done

---

## Manager Personal Goals — [ QUARTER ]

- [ Goal 1 ]: [ Description and success criteria ]
- [ Goal 2 ]: [ Description and success criteria ]
"""

WORK_TYPES_MD = """\
# Work Types

Reference table used for free-time matching.
This is NOT the active action list — see actions.yaml for that.

| Work type              | Duration  | Energy     | Context           | Related goal |
|------------------------|-----------|------------|-------------------|--------------|
| 1:1 prep               | 15 min    | low        | anywhere          | team health  |
| Async code review      | 30 min    | medium     | deep-work         | eng quality  |
| Write growth doc       | 45 min    | high       | deep-work         | people dev   |
| OKR planning draft     | 45 min    | high       | deep-work         | strategy     |
| Reply to stakeholders  | 15 min    | low        | shallow / async   | stakeholders |
| Interview debrief note | 20 min    | medium     | anywhere          | hiring       |
| Read RFC / design doc  | 30 min    | medium     | deep-work         | eng quality  |
| Cross-team follow-up   | 20 min    | low        | async             | stakeholders |
| Update project status  | 15 min    | low        | anywhere          | strategy     |
| Retro patterns write-up| 30 min    | medium     | deep-work         | team health  |
"""

ENVIRONMENT_MD = """\
# Environment

## Offices & locations
| Location | Address / description |
|----------|-----------------------|
| HQ       | [ address ]           |
| Home     | remote                |

## Conference rooms
| Room | Location | Capacity | Notes |
|------|----------|----------|-------|
| [ Room A ] | [ floor/building ] | 6 | AV-equipped |

## Commute times
| From   | To  | Duration | Mode   |
|--------|-----|----------|--------|
| Home   | HQ  | [ N min ] | [ e.g. subway ] |

## Team timezones
| Name | Timezone | Overlap with manager |
|------|----------|----------------------|
| [ name ] | [ e.g. US/Pacific ] | [ e.g. 09:00–14:00 ET ] |
"""

SAMPLE_TEAM_MD = """\
# [ Full Name ]

## Role
- Title:             [ e.g. Senior Software Engineer ]
- Team:              [ team name ]
- Start date:        [ YYYY-MM-DD ]
- Employment type:   full-time   # full-time | contractor | intern

## Contact
- Email:    [ email ]
- Slack:    [ @handle ]
- Timezone: [ e.g. America/Los_Angeles ]

## Skills & strengths
- [ e.g. Distributed systems design ]
- [ e.g. Strong communicator ]

## Growth areas
- [ e.g. Project estimation ]
- [ e.g. Cross-team influence ]

## Current assignment
- Project:          [ project key ]
- Role on project:  [ e.g. tech lead ]
- Current focus:    [ e.g. implementing event consumer in Go ]

## 1:1 cadence
- Frequency:          weekly   # weekly | biweekly
- Day/time:           [ e.g. Tuesday 11:00 ]
- Notes file pattern: meetings/YYYY-MM-DD-1on1-[ name-slug ].md

## Performance
- Current cycle:          [ e.g. H1 2026 ]
- Rating (last cycle):    Meets   # Exceeds | Meets | Below | N/A
- Promotion track:        not currently   # not currently | eligible next cycle | nominated
- Key strengths observed: [ bullet ]
- Development areas:      [ bullet ]
- PIP or concern:         no   # no | monitoring | PIP

## Availability
- On leave:           no
- Next planned leave: [ YYYY-MM-DD or "none" ]
- On-call:            no

## Context notes
- [ Personal context, preferences, or sensitivities shared in 1:1 ]
"""

SAMPLE_PROJECT_YAML = f"""\
project:
  key: "example-project"
  name: "Example Project"
  status: planning          # planning | active | on-hold | shipped | cancelled
  description: "Replace this with a real description of the project."

  team:
    - name: [ name-slug ]   # must match profiles/team/<name>.md stem
      role: tech-lead
    - name: [ name-slug ]
      role: backend-engineer

  tech_stack: []            # e.g. [Go, Kafka, React, PostgreSQL]

  milestones:
    - id: M1
      title: "[ Milestone title ]"
      due_date: "[ YYYY-MM-DD ]"
      status: pending       # pending | done | at-risk | missed
      notes: ""

  risks: []

  stakeholders:
    - name: "[ Name ]"
      role: "[ e.g. Product Manager ]"
      contact: ""

  links: []

  created_at: "{TODAY}"
  updated_at: "{TODAY}"
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help="Override the data directory (default: from config/config.yaml)")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite existing files")
    args = parser.parse_args()

    data_dir: Path = args.data_dir.expanduser()
    force: bool = args.force

    print(f"Data directory: {data_dir}")
    if force:
        print("  --force: existing files will be overwritten")
    print()

    # Create directory tree
    dirs = [
        data_dir,
        data_dir / "meetings",
        data_dir / "projects",
        data_dir / "profiles" / "team",
        data_dir / "files" / "documents",
        data_dir / "files" / "reports",
        data_dir / "files" / "notes",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Root data files
    files: list[tuple[Path, str]] = [
        (data_dir / "index.yaml",   INDEX_YAML),
        (data_dir / "actions.yaml", ACTIONS_YAML),
        (data_dir / "events.yaml",  EVENTS_YAML),
    ]

    # Profiles
    profiles = [
        (data_dir / "profiles" / "directives.md",  DIRECTIVES_MD),
        (data_dir / "profiles" / "manager.md",     MANAGER_MD),
        (data_dir / "profiles" / "calendar.md",    CALENDAR_MD),
        (data_dir / "profiles" / "goals.md",       GOALS_MD),
        (data_dir / "profiles" / "work-types.md",  WORK_TYPES_MD),
        (data_dir / "profiles" / "environment.md", ENVIRONMENT_MD),
        (data_dir / "profiles" / "team" / "example-person.md", SAMPLE_TEAM_MD),
    ]

    # Sample project
    projects = [
        (data_dir / "projects" / "example-project.yaml", SAMPLE_PROJECT_YAML),
    ]

    print("Root data files:")
    for path, content in files:
        write_file(path, content, force)

    print("\nProfiles:")
    for path, content in profiles:
        write_file(path, content, force)

    print("\nSample project:")
    for path, content in projects:
        write_file(path, content, force)

    print(f"""
Done. Next steps:
  1. Edit profiles/manager.md       — fill in your name, timezone, schedule
  2. Edit profiles/directives.md    — add protected time blocks and hard rules
  3. Edit profiles/team/            — rename example-person.md; add one file per direct report
  4. Edit projects/                 — rename or delete example-project.yaml; add real projects
  5. Edit actions.yaml              — replace setup actions with real ones
  6. Edit events.yaml               — add your recurring meetings
  7. Edit profiles/calendar.md      — add holidays and leave periods
  8. Run: python scripts/reindex.py — rebuild the index

  Tip: delete profiles/team/example-person.md and projects/example-project.yaml
       once you have real data in place.
""")


if __name__ == "__main__":
    main()
