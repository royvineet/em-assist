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

The AI assistant reads `CLAUDE.md` / `copilot-instructions.md` to understand how to navigate and update your data. You talk to it in natural language; it reads and writes the right files.

---

## Setup

### 1. Clone the repo

```bash
git clone <repo-url> em-assist
cd em-assist
```

### 2. Create the data directory

```bash
mkdir -p ~/Documents/em-assist/{projects,meetings,files/{documents,reports,notes},profiles/team}
```

### 3. Set up Python environment

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 4. Initialise your profiles

Create the following files in `~/Documents/em-assist/profiles/`:

| File | Purpose |
|------|---------|
| `directives.md` | Hard rules — read by the AI before every decision |
| `manager.md` | Your identity, style, calendar preferences |
| `calendar.md` | Public holidays, company holidays, team leave |
| `environment.md` | Offices, conf rooms, team timezones |
| `goals.md` | Team OKRs + your personal manager goals |
| `work-types.md` | EM work-type reference (duration, energy, context) |

See `CLAUDE.md` for the schema and example content for each file.

### 5. Run startup

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

- **GitHub Copilot**: `copilot-instructions.md` is auto-loaded by Copilot in VS Code.
- **Claude Code**: `CLAUDE.md` is auto-loaded by Claude Code.

Both files are kept in sync — they contain identical instructions.

---

## Data sync

Data sync is not configured by default. To enable it, edit `scripts/startup.sh` and add your sync command (git remote, rclone, rsync, etc.). The placeholder is clearly marked in the script.
