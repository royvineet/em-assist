# EM-Assist

A plain-file personal assistant for software engineering managers, powered by an AI coding assistant (GitHub Copilot, Claude Code, or similar).

EM-Assist helps you manage:
- Team 1:1s and meeting notes
- Action items and delegated follow-ups
- Project milestones, risks, and stakeholders
- Calendar events and scheduling
- Hiring pipeline and interview notes
- Team performance and growth tracking
- Free-time planning against personal goals

---

## How it works

All data lives as plain YAML and Markdown files outside this repo (default: `~/Documents/em-assist/`). The repo contains only tooling, scripts, and AI instructions. Data is never committed here.

The AI assistant reads `CLAUDE.md` / `.github/copilot-instructions.md` to understand how to navigate and update your data. You talk to it in natural language; it reads and writes the right files.

---

## Setup

### 1. Clone the repo

```bash
git clone <repo-url> em-assist
cd em-assist
```

### 2. Set up Python environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3. Scaffold the data directory

```bash
.venv/bin/python scripts/init-data.py
```

This creates `~/Documents/em-assist/` (or the path in `config/config.yaml`) with template files for every profile, a sample project, and empty action/event lists. **Existing files are never overwritten**, so it is safe to re-run.

Then open each file and fill in your details:

| File | What to fill in |
|------|-----------------|
| `profiles/manager.md` | Your name, timezone, schedule, focus areas |
| `profiles/directives.md` | Protected time blocks, hard constraints |
| `profiles/team/` | Rename `example-person.md`; add one file per direct report |
| `projects/` | Rename or delete `example-project.yaml`; add real projects |
| `actions.yaml` | Replace the setup placeholders with real actions |
| `events.yaml` | Add your recurring meetings |
| `profiles/calendar.md` | Holidays and team leave periods |

### 4. Run startup

```bash
bash scripts/startup.sh
```

Run this at the start of every AI session. It rebuilds the search index and (when configured) syncs data from a remote source.

---

## Daily use

Open this repo in your AI assistant and start talking:

```
"What's on today?"
"Add a 1:1 with Priya on Friday at 11am"
"Ravi mentioned the infra ticket is blocked — add an action for me to follow up"
"I have 30 minutes free, I'm in shallow mode"
"What did we decide in the last retro?"
"How is Priya tracking against her growth goals?"
```

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/init-data.py` | **First-time setup**: scaffold all template data files |
| `scripts/startup.sh` | Session startup: rebuild index, (future) sync data |
| `scripts/new-meeting.py <type> [qualifier]` | Scaffold a new meeting note from template |
| `scripts/reindex.py` | Rebuild `index.yaml` from all data files |
| `scripts/ingest.py <file>` | Extract text from a file for ingestion |

---

## Data layout

```
~/Documents/em-assist/
├── index.yaml            # search index
├── actions.yaml          # action items
├── events.yaml           # calendar events
├── projects/<key>.yaml   # one file per project
├── meetings/             # meeting notes (Markdown)
├── profiles/             # manager + team context files
└── files/                # ingested documents, reports, notes
```

See `CLAUDE.md` for full schema documentation.

---

## AI assistant instructions

- **GitHub Copilot**: `.github/copilot-instructions.md` is auto-loaded by GitHub Copilot.
- **Claude Code**: `CLAUDE.md` is auto-loaded by Claude Code.

Keep `.github/copilot-instructions.md` and `CLAUDE.md` aligned when workflows or data schemas change.

---

## Data sync

Data sync is not configured by default. To enable it, edit `scripts/startup.sh` and add your sync command (git remote, rclone, rsync, etc.). The placeholder is clearly marked in the script.
