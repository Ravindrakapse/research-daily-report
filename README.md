# research-daily-report

A Claude Code skill for writing daily research progress reports: reading notes plus problem work.
Reports are written in a plain, first-person, human style, have LaTeX equations, are built to a
2-page PDF, are checked against sources and are independently reviewed.

## Install

```bash
git clone https://github.com/Ravindrakapse/research-daily-report ~/.claude/skills/research-daily-report
```

Requirements:
- Python 3
- [tectonic](https://tectonic-typesetting.github.io): `brew install tectonic`
- poppler (`pdftotext`, `pdftoppm`, `pdfinfo`): `brew install poppler`

## Use

In Claude Code, ask for "today's report" or run `/research-daily-report`. The skill:
1. works out what was done today;
2. proposes an outline;
3. writes and builds the report;
4. has it reviewed independently.

Build by hand:

```bash
scripts/build.sh report.md "Project Title" "Subtitle" "Author" "21 September 2026"
scripts/build.sh report.md "Project Title" "Subtitle" "Author" "21 September 2026" tight
```

## Files
- `SKILL.md`: workflow, style rules, and disclosure and framing rules
- `scripts/md2tex.py`: Markdown to LaTeX (math, tables, lists, Greek letters and accents)
- `scripts/build.sh`: md2tex, then tectonic, then prints the page count
