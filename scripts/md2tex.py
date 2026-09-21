import sys, re

src, dst, title, subtitle, author, date = sys.argv[1:7]
md = open(src).read()

PRE = r"""\documentclass[11pt]{article}
\usepackage[top=0.6in,bottom=0.6in,left=0.7in,right=0.7in]{geometry}
\usepackage{times}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{microtype}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
\setlength{\parindent}{0pt}
\setlength{\parskip}{2.5pt}
\titleformat{\section}{\normalfont\large\bfseries}{}{0pt}{}
\titlespacing*{\section}{0pt}{7pt}{2pt}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{6pt}{2pt}
\linespread{0.97}\selectfont
\pagestyle{plain}
\begin{document}
\begin{center}
{\Large\bfseries TITLE}\\[4pt]
{\normalsize SUBTITLE}\\[6pt]
{\normalsize AUTHOR \quad\textbullet\quad DATE}
\end{center}
\vspace{2pt}
"""

def esc(s):
    raw, stash = [], []
    def keep_raw(m):
        raw.append(m.group(1)); return "\x05%d\x05" % (len(raw) - 1)
    def keep(m):
        stash.append(m.group(1)); return "\x00%d\x00" % (len(stash) - 1)
    s = re.sub(r'\$([^$\n]+)\$', keep_raw, s)
    s = re.sub(r'`([^`]+)`', keep, s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: "\x01%s\x02%s\x03" % (m.group(1), m.group(2)), s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")]:
        s = s.replace(a, b)
    s = re.sub(r'"([^"\n]+)"', r"``\1''", s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'\\emph{\1}', s)
    s = re.sub(r'\x01(.*?)\x02(.*?)\x03', lambda m: r'\href{%s}{%s}' % (m.group(2), m.group(1)), s)
    for u, tex in [("ω", r"$\omega$"), ("Δ", r"$\Delta$"), ("ρ", r"$\rho$"), ("σ", r"$\sigma$"),
                   ("α", r"$\alpha$"), ("β", r"$\beta$"), ("±", r"$\pm$"), ("×", r"$\times$"),
                   ("≤", r"$\le$"), ("≥", r"$\ge$"), ("→", r"$\to$"), ("−", "-"), ("—", "---"), ("–", "--"),
                   ("Á", r"\'{A}"), ("á", r"\'{a}"), ("é", r"\'{e}"), ("è", r"\`{e}"),
                   ("č", r"\v{c}"), ("ö", r'\"{o}'), ("ü", r'\"{u}'), ("ř", r"\v{r}"), ("š", r"\v{s}")]:
        s = s.replace(u, tex)
    s = re.sub(r'\x00(\d+)\x00',
               lambda m: r'\texttt{%s}' % stash[int(m.group(1))].replace("_", r"\_").replace("&", r"\&")
               .replace("%", r"\%").replace("#", r"\#").replace("$", r"\$"), s)
    s = re.sub(r'\x05(\d+)\x05', lambda m: "$" + raw[int(m.group(1))] + "$", s)
    return s

out, lines, i, mode = [], md.split("\n"), 0, None
while i < len(lines):
    st = lines[i].strip()
    if not st:
        if mode:
            out.append(r"\end{%s}" % mode); mode = None
        i += 1; continue
    if st.startswith("$$"):
        if mode:
            out.append(r"\end{%s}" % mode); mode = None
        buf = [st]
        while not (buf[-1].endswith("$$") and (len(buf) > 1 or len(st) > 4)):
            i += 1; buf.append(lines[i].strip())
        body = " ".join(buf).strip()[2:-2].strip()
        out.append("\\[\n" + body + "\n\\]")
        i += 1; continue
    m = re.match(r'^(#{1,3})\s+(.*)', st)
    if m:
        if mode:
            out.append(r"\end{%s}" % mode); mode = None
        out.append("\\%s{%s}" % ({1: "section", 2: "section", 3: "subsection"}[len(m.group(1))], esc(m.group(2))))
        i += 1; continue
    if st.startswith("|"):
        if mode:
            out.append(r"\end{%s}" % mode); mode = None
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rows.append(lines[i].strip()); i += 1
        def cells(r):
            r = r.strip().strip("|"); c, cur, inm = [], "", False
            for ch in r:
                if ch == "$": inm = not inm
                if ch == "|" and not inm:
                    c.append(cur.strip()); cur = ""
                else:
                    cur += ch
            c.append(cur.strip()); return c
        body = [cells(r) for r in rows if not re.match(r'^\|[\s:|-]+\|$', r)]
        n = len(body[0])
        tb = ["\\begin{center}\\small", "\\begin{tabular}{l" + "c" * (n - 1) + "}", "\\toprule"]
        for k, r in enumerate(body):
            tb.append(" & ".join(esc(x) for x in r) + r" \\")
            if k == 0: tb.append("\\midrule")
        tb += ["\\bottomrule", "\\end{tabular}", "\\end{center}"]
        out.append("\n".join(tb)); continue
    if st == "---":
        if mode:
            out.append(r"\end{%s}" % mode); mode = None
        out.append(r"\vspace{3pt}\hrule\vspace{3pt}"); i += 1; continue
    m = re.match(r'^[-*]\s+(.*)', st)
    if m:
        if mode != "itemize":
            if mode: out.append(r"\end{%s}" % mode)
            out.append(r"\begin{itemize}\setlength\itemsep{1pt}\setlength\parskip{0pt}"); mode = "itemize"
        out.append(r"\item " + esc(m.group(1))); i += 1; continue
    m = re.match(r'^\d+\.\s+(.*)', st)
    if m:
        if mode != "enumerate":
            if mode: out.append(r"\end{%s}" % mode)
            out.append(r"\begin{enumerate}\setlength\itemsep{1pt}\setlength\parskip{0pt}"); mode = "enumerate"
        out.append(r"\item " + esc(m.group(1))); i += 1; continue
    if mode:
        out.append(r"\end{%s}" % mode); mode = None
    para = [st]; i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3}\s|[-*]\s|\d+\.\s|---$|\$\$|\|)', lines[i].strip()):
        para.append(lines[i].strip()); i += 1
    out.append(esc(" ".join(para)))
if mode:
    out.append(r"\end{%s}" % mode)

head = PRE.replace("SUBTITLE", subtitle).replace("TITLE", title).replace("AUTHOR", author).replace("DATE", date)
open(dst, "w").write(head + "\n\n".join(out) + "\n\\end{document}\n")
