# research-daily-report

A [Claude Code](https://claude.com/claude-code) skill for writing daily research progress reports:
reading notes plus problem work. Reports are written in a plain, first-person, human style, have
LaTeX equations, are built to a 2-page PDF, are checked against sources, and are independently
reviewed before you send them.

---

## Who this is for

Researchers who send a short daily update to a manager or supervisor, covering what they read,
what they worked on, and what comes next. The update should read like they wrote it and hold up
if someone checks the numbers.

---

## 1. Prerequisites

| Tool | Why | Install (macOS) | Install (Linux) |
|---|---|---|---|
| Claude Code | runs the skill | see [docs](https://docs.claude.com/en/docs/claude-code) | same |
| Python 3 | Markdown → LaTeX | usually preinstalled | `sudo apt install python3` |
| tectonic | compiles LaTeX to PDF in one pass | `brew install tectonic` | `curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net \| sh` |
| poppler | `pdftotext`, `pdftoppm`, `pdfinfo` | `brew install poppler` | `sudo apt install poppler-utils` |

Check:

```bash
python3 --version && tectonic --version && pdftotext -v
```

---

## 2. Install

Pick **one** of the following.

**For yourself, available in every project (recommended):**

```bash
git clone https://github.com/Ravindrakapse/research-daily-report ~/.claude/skills/research-daily-report
```

**For one project, shared with your team through that project's repo:**

```bash
cd your-project
git clone https://github.com/Ravindrakapse/research-daily-report .claude/skills/research-daily-report
```

Restart Claude Code, or start a new session. The skill then shows up in the skill list.

> If you get "repository not found", the repo is private. Ask the owner to add you as a
> collaborator.

---

## 3. Use

In Claude Code, in the folder where your research lives, either type:

```
/research-daily-report
```

or just ask in plain words:

```
create today's report
```

```
write today's report: I read sections 3-4 of the paper in papers/, and ran the sweep in sim/
```

What happens next:

1. **Claude works out what you did today.** It looks at files changed since your last report and
   at that report's "Next" section. If it is still unclear, it asks you one short question. It
   will not make up work.
2. **Claude proposes an outline.** You get the sections, the points and equations it plans to
   include, and what it will **hold back**. Approve it or edit it, for example "don't mention X"
   or "add some results for Y".
3. **Claude writes and builds the PDF**, then renders the pages and checks them.
4. **Claude runs an independent review.** A separate agent checks every number, equation and
   citation against your sources, and the fixes are applied.
5. **Claude saves the report** as `<Project Title> <Your Name> <DD Mon>.pdf` (plus the `.md`)
   next to your earlier reports.

### Useful things to say

| You say | Effect |
|---|---|
| "first tell me what you will put" | outline only, nothing is written yet |
| "don't put all the info for X" | results for X held back and described as in progress |
| "you can mention some results for X" | a small illustrative set released; headline numbers stay back |
| "make it 2 pages only" | trims secondary sentences, then tightens spacing |
| "it's ok if it exceeds 2 pages" | no length limit |
| "I added the paper, check" | re-reads the PDF and fixes anything in earlier reports that the paper contradicts |

### Tips

- Keep papers in a `papers/` folder and reports in one folder, for example `reading_notes/`.
  Claude uses the previous report to continue the story.
- Tell Claude your **project title** and **name** once, for the report header and file name.
- If Claude cites a paper whose PDF it does not have, it tells you so. Add the PDF and say "check".

---

## 4. Build by hand (optional)

The build script works without Claude:

```bash
~/.claude/skills/research-daily-report/scripts/build.sh report.md \
  "Project Title" "Subtitle" "Your Name" "21 September 2026"

# tighter margins and line spacing, when a report spills by a few lines
~/.claude/skills/research-daily-report/scripts/build.sh report.md \
  "Project Title" "Subtitle" "Your Name" "21 September 2026" tight
```

The Markdown supports:
- headings (`##`, `###`), paragraphs, `-` bullets and `1.` lists
- `**bold**`, `*italic*`, `` `code` `` and `[links](url)`
- inline math `$...$` and display math `$$...$$` on their own lines
- pipe tables, with `|` inside `$...$` handled correctly
- Greek letters and accented names, e.g. ω, Δ, Dörfler, Verbič

---

## 5. Customise

- **Style, structure, disclosure rules:** edit `SKILL.md`.
- **Page layout** (margins, font, spacing): edit the `PRE` block at the top of
  `scripts/md2tex.py`.
- **Default length:** change "The default is 2 pages" in `SKILL.md`.

## 6. Update and uninstall

```bash
cd ~/.claude/skills/research-daily-report && git pull   # update
rm -rf ~/.claude/skills/research-daily-report           # uninstall
```

---

## Files

- `SKILL.md`: workflow, style rules, and disclosure and framing rules; this is what Claude reads
- `scripts/md2tex.py`: Markdown to LaTeX converter
- `scripts/build.sh`: md2tex, then tectonic, then prints the page count
