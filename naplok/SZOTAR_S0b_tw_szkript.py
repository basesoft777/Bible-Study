"""S0b.2: unfoldingWord Translation Words (tW) lefedettseg-meres a 26 H- es 13
G-token hatokoron (D28). A naplok/SZOTAR_S0b_tw.tsv-t generalta. A tW nyers
kiadasa NEM kerul a repoba (CLAUDE.md); a TW_DIR-et az S0b.2 futtatasakor
letoltott ideiglenes konyvtarra kell allitani (git.door43.org/unfoldingWord/en_tw,
tag v91, commit ff5b3852c27c3a0d01b109e482eb26047dcd20e2)."""
import sys, os, re, glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

TW_DIR = os.environ.get('TW_DIR', r'C:\Users\bases\AppData\Local\Temp\tw_download\en_tw\bible')

H_TOKENS = ("H0127 H0430 H0779 H0922 H1121 H2403 H2416 H2555 H3548 H3678 H4467 "
            "H5303 H5315 H6093 H6975 H7043 H7121 H7451 H7496 H7497 H7585 H7843 "
            "H8004 H8034 H8414 H8415").split()
G_TOKENS = "G0012 G0086 G0282 G0813 G1311 G1941 G1944 G2671 G4151 G5010 G5351 G5356 G5590".split()

strong_re = re.compile(r'\*\*?\s*Strong.?s\s*:\s*(.+)', re.IGNORECASE)
code_re = re.compile(r'[HG]\d{4,6}')

coverage = {t: [] for t in H_TOKENS + G_TOKENS}

for subdir in ('kt', 'other'):
    d = os.path.join(TW_DIR, subdir)
    if not os.path.isdir(d):
        continue
    for fp in glob.glob(os.path.join(d, '*.md')):
        with open(fp, encoding='utf-8') as f:
            text = f.read()
        m = strong_re.search(text)
        if not m:
            continue
        codes = code_re.findall(m.group(1))
        fname = os.path.basename(fp)
        textlen = len(text)
        for tok in H_TOKENS:
            for c in codes:
                if c == tok or (c.startswith(tok) and len(c) == len(tok) + 1):
                    coverage[tok].append((subdir, fname, textlen, c))
                    break
        for tok in G_TOKENS:
            for c in codes:
                if c.startswith(tok) and c[0] == 'G':
                    coverage[tok].append((subdir, fname, textlen, c))
                    break

h_hit = [t for t in H_TOKENS if coverage[t]]
g_hit = [t for t in G_TOKENS if coverage[t]]
print("H: %d/%d -> %s" % (len(h_hit), len(H_TOKENS), ','.join(h_hit)))
print("H hianyzik: %s" % ','.join(t for t in H_TOKENS if not coverage[t]))
print("G: %d/%d -> %s" % (len(g_hit), len(G_TOKENS), ','.join(g_hit)))
print("G hianyzik: %s" % ','.join(t for t in G_TOKENS if not coverage[t]))
