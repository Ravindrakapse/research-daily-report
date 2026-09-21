---
name: research-daily-report
description: Write a daily research progress report (reading notes + problem work) in a plain, human, first-person style, with LaTeX equations, built to a 2-page PDF via md2tex + tectonic, verified against sources and independently reviewed. Use when the user asks for "today's report", "report for today", a daily log/update for a manager, or reading notes on a paper.
---

# Research daily report

A daily report a researcher sends to their manager: what they read, what they
worked on, what comes next. It must read as written by the researcher, be
factually traceable, and reveal only as much as the researcher wants to reveal.

## Workflow (always in this order)

1. **Find out what was actually done today. Never invent activity.**
   - Check the working folders for files added or changed since the last report
     (`find . -newermt "<last report date>"`), new papers in `papers/`, and new code
     or data.
   - Read the previous report's "Next" section. Today's report should continue it.
   - If it is still unclear what the day went into, ask one short question with
     2–4 options. Do not write up work that may not have happened.
2. **Propose the outline before writing.** List the sections, the points and
   equations each will carry, and what will be **held back**. Wait for approval
   or edits. When the user asks "first tell me what you will put", reply with
   the outline only.
3. **Read the sources.** Use `pdftotext -layout` on the paper and read the
   sections being reported. Read the code and data files behind any numbers.
   If a cited paper's PDF is not available, say so to the user and keep the
   claims general. Never attribute to a paper something it does not contain.
4. **Write the Markdown**, following the style rules below.
5. **Build.** Run `scripts/build.sh report.md "<Project title>" "<Subtitle>" "<Author>" "<D Month YYYY>"`.
   Render the pages to PNG (`pdftoppm -r 60 -png`) and look at them. Check that
   equations render, tables are real tables, and no characters were dropped.
6. **Independent review.** Spawn a subagent that has read-only access to the
   report and its sources. Have it check every number, equation, citation and
   attribution, and flag overclaims and wording that reads as self-correction.
   Apply the fixes.
7. **Fit to length.** The default is 2 pages. If it spills, first cut secondary
   sentences, then pass `tight` to build.sh. Never drop a correction to save space.
8. **Save** the PDF and the `.md` next to earlier reports, named
   `<Project Title> <Author> <DD Mon>.pdf`, and tell the user what went in and
   what was held back.

## Style rules

**Voice**
- Write in the first person as the researcher: "I worked through", "What caught
  my attention", "I have not finished it".
- State uncertainty plainly: "I did not properly follow", "I do not yet know
  whether". A named gap reads more human than a confident summary.
- Vary paragraph length. Some points get one sentence, some get a paragraph.
- Use bold only as a lead-in label at the start of a paragraph or bullet.
- No emoji. Avoid em-dash chains. No "delve", "crucial", "comprehensive",
  "seamless", "leverage", "In conclusion". No self-grading filler such as
  "all criteria met" or "successfully completed".
- Explain technical ideas in plain words first, then give the equation.

**Structure of a daily report**
- **Reading: <paper short name> (in progress / continued / finished)**
  - Open with the full citation: authors, "Title", venue, vol., pages, year.
  - Say which sections were read today and which are still ahead.
  - Give the points taken, each as a bold lead-in and 2–4 sentences, with an
    equation where the paper has one.
  - End with **why this matters for <the problem>**: a concrete link, not a
    generic one.
- **<Problem ID>: <what was done>**
  - Give a one-line reminder of the problem, and the core condition as an
    equation.
  - Cover what was done today and the results the user approved for release.
  - Put what is still in progress under a neutral heading.
- **Next**: 2–3 concrete steps. They become the next report's starting point.

**Equations**
- Every equation is LaTeX: inline `$...$`, display `$$...$$` on its own lines.
- Use the source paper's own notation and symbols, e.g. $D_f$, $\vartheta$,
  $\omega_{\mathrm{ref}}$.
- If a symbol clashes with another section, rename it, e.g. $k_{ps}$ vs $k_p$.
- State every hypothesis a theorem needs, e.g. "each member open-loop stable,
  $G_j \in \mathcal{RH}_\infty$".

**Accuracy**
- Every number must trace to a data file or the paper. Round consistently.
- Keep compared quantities separate: say which error is compared against which
  margin.
- A boundary case is a boundary witness, not a counterexample. Match claim
  strength to what was shown.
- Describe methods as the code runs them, not as a draft paper describes them.

## Disclosure and framing rules

- **Hold back headline results until the deliverable** unless the user says
  otherwise. Describe the setup and method, and say results are being
  consolidated: "Full results, plots and the write-up will come in the
  deliverable." If the user allows "some results", release the smallest
  illustrative set and keep the headline numbers back.
- **Verification work is framed as routine**: "Verifying the simulations",
  "What was verified", "Planned extensions". Never "checking my own work",
  "errors I found", "needs another pass before it is final", or anything that
  implies earlier reports were wrong.
- When something in an earlier report turns out to be wrong, fix that earlier
  report file and tell the user. Do not confess it in today's report.
- Do not mention who asked for the report or why, internal meta-documents, or
  tooling (LLMs, agents).
- Credit prior work correctly. When a result is standard, say it is standard
  and say what is being added.

## Build notes

- `scripts/md2tex.py` is a small Markdown→LaTeX converter. It handles:
  - headings, paragraphs, bullets and numbered lists
  - pipe tables, rendered with booktabs; `|` inside `$...$` is safe
  - `$...$` and `$$...$$` math passed through as-is
  - bold, italic, code and links
  - Greek letters, accents and dashes mapped to LaTeX

  The page setup is 11pt Times, 0.6in margins and tight section spacing.
- `tectonic` (Homebrew) compiles in one pass and fetches packages on demand.
- If the scratchpad is wiped, the scripts here are the durable copy.
