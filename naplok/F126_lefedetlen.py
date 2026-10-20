"""F126 (ISTENTISZT001_PROZA) — mellékmérés: a H7121+H8034 kollokáció versei közül
melyik nem szerepel sem az ISTENTISZT-001 előfordulásai, sem a jelöltjei között.

Nem dönt és nem ír táblát: a kimenet az N-tétel (helyőrző) körülírása. A
kollokáció-kimenetet a `lekerdez.py kollokacio H7121 H8034 --naplo F126 --lepes adhoc`
futás mentett fájljából olvassa; a táblákat split('\\t')-tel.

Használat: python naplok/F126_lefedetlen.py <kollokacio_kimenet.txt>
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
MOTIVUM = "ISTENTISZT-001"


def tabla(path):
    fej, ki = None, []
    for s in open(path, encoding="utf-8"):
        s = s.rstrip("\n").rstrip("\r")
        if not s or s.startswith("#"):
            continue
        m = s.split("\t")
        if fej is None:
            fej = m
            continue
        ki.append(dict(zip(fej, m)))
    return ki


def main():
    kimenet = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
    igek = []
    for s in kimenet:
        if s.startswith("#") or s.startswith("proveniencia") or not s.strip():
            continue
        m = re.match(r"^([0-9]?[A-ZÁÉÍÓÖŐÚÜŰa-záéíóöőúüű]+ \d+:\d+)", s.strip())
        if m:
            igek.append(m.group(1))
    prov = next((s for s in kimenet if s.startswith("proveniencia:")), "")
    elo = {r["igehely"] for r in tabla(REPO / "adat" / "elofordulasok.tsv") if r["id"] == MOTIVUM}
    jel = {}
    for r in tabla(REPO / "adat" / "jeloltek.tsv"):
        jel.setdefault(r.get("igehely", ""), set()).add(r.get("id", ""))
    karoli = {}
    for s in open(REPO / "konkordancia" / "Karoli_1908.tsv", encoding="utf-8"):
        m = s.rstrip("\n").rstrip("\r").split("\t")
        if len(m) >= 2:
            karoli[m[0]] = m[1]
    print(f"kollokáció-versek: {len(set(igek))}")
    nincs = []
    for i in sorted(set(igek), key=igek.index):
        if i in elo:
            continue
        hol = jel.get(i)
        if hol and MOTIVUM in hol:
            continue
        nincs.append(i)
        kt = karoli.get(i, "—")
        jelz = "segítségül" if "segítségül" in kt or "segítségűl" in kt else ""
        print(f"{i}\tjelölt más motívumnál: {sorted(hol) if hol else '—'}\t{jelz}\t{kt}")
    print(f"\nsem előfordulás, sem ISTENTISZT-001-jelölt: {len(nincs)}")
    print(f"a kollokáció forrása: {prov}")


if __name__ == "__main__":
    main()
