import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

"""
KARB_KB3_nullaz.py -- a konkordancia/Karoli_Strong_kivonat.tsv 26 nullazatlan
sorat lattatja el a SEMA.md 1.2 szerinti alakkal (H/G betu + NEGYJEGYU szam,
pl. H430 -> H0430; osszetett tokeneknel `+` valasztja el oket, minden token
kulon padolva).

Minta: naplok/FORRAS_K6_nullaz.py (a pad() fuggveny logikaja onnan van).
Csak a "Strong-szam" oszlop valtozhat -- semmi mas mezo, sor vagy sorrend
nem modosulhat. TSV-olvasas/iras kizarolag split('\\t') / '\\t'.join()
(CLAUDE.md).
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UT = os.path.join(ROOT, "konkordancia", "Karoli_Strong_kivonat.tsv")
RIPORT = os.path.join(ROOT, "naplok", "KARB_KB3_nullazas.tsv")

TOKEN_RE = re.compile(r"^([HG])(\d+)$")


def pad_token(tok):
    m = TOKEN_RE.match(tok)
    if not m:
        return tok, False
    letter, digits = m.groups()
    if len(digits) == 4:
        return tok, False
    return "%s%04d" % (letter, int(digits)), True


def pad_strong_mezo(mezo):
    reszek = mezo.split("+")
    uj_reszek = []
    valtozott = False
    for r in reszek:
        uj, v = pad_token(r)
        uj_reszek.append(uj)
        valtozott = valtozott or v
    return "+".join(uj_reszek), valtozott


def main():
    with open(UT, encoding="utf-8") as f:
        sorok = f.readlines()

    header = sorok[0].rstrip("\r\n").split("\t")
    idx = header.index("Strong-szám")
    idx_igehely = header.index("Igehely")

    valtozasok = []  # (igehely, regi, uj)
    uj_sorok = [sorok[0]]
    for sor in sorok[1:]:
        veg = "\r\n" if sor.endswith("\r\n") else ("\n" if sor.endswith("\n") else "")
        mezok = sor.rstrip("\r\n").split("\t")
        regi_ertek = mezok[idx]
        uj_ertek, valtozott = pad_strong_mezo(regi_ertek)
        if valtozott:
            valtozasok.append((mezok[idx_igehely], regi_ertek, uj_ertek))
            mezok[idx] = uj_ertek
        uj_sorok.append("\t".join(mezok) + veg)

    with open(UT, "w", encoding="utf-8", newline="") as f:
        f.writelines(uj_sorok)

    with open(RIPORT, "w", encoding="utf-8", newline="\n") as f:
        f.write("igehely\tregi\tuj\n")
        for igehely, regi, uj in valtozasok:
            f.write("%s\t%s\t%s\n" % (igehely, regi, uj))

    print("Modositott sorok: %d" % len(valtozasok))
    print("Riport: %s" % RIPORT)


if __name__ == "__main__":
    main()
