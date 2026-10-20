"""F126 (ISTENTISZT001_PROZA) — 5. lépés: a jóváhagyott v2 bekezdések beírása a forrásba.

A `naplok/F126_szovegjavaslat.md` (v2, a felhasználó jóváhagyta 2026-10-20) kódblokkjait
szó szerint, változtatás nélkül szúrja be a `motivumok/ISTENTISZT-001.md` három pontjára.
Blokkok: A0–A4 (A pont), B0, B2–B7 (B pont; a B1 elhagyva), C1 (C pont).
Minden horgonynak pontosan egyszer kell előfordulnia, különben megáll.

Használat: python naplok/F126_beiras.py
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
JAV = REPO / "naplok" / "F126_szovegjavaslat.md"
FORRAS = REPO / "motivumok" / "ISTENTISZT-001.md"


def blokkok():
    s = JAV.read_text(encoding="utf-8").replace("\r\n", "\n")
    ki = {}
    for m in re.finditer(r"^### (?!~~)([ABC]\d) ", s, re.M):
        kod = m.group(1)
        k = s.index("```markdown\n", m.end())
        v = s.index("\n```", k + 12)
        ki[kod] = s[k + len("```markdown\n"):v].strip("\n")
    return ki


def beszur(szoveg, horgony, uj, utana=True):
    if szoveg.count(horgony) != 1:
        sys.exit(f"HIBA: a horgony {szoveg.count(horgony)}× fordul elő: {horgony[:60]!r}")
    i = szoveg.index(horgony) + (len(horgony) if utana else 0)
    return szoveg[:i] + uj + szoveg[i:]


def main():
    b = blokkok()
    A = ["A0", "A1", "A2", "A3", "A4"]
    B = ["B0", "B2", "B3", "B4", "B5", "B6", "B7"]
    C = ["C1"]
    for k in A + B + C:
        if k not in b:
            sys.exit(f"HIBA: hiányzó blokk {k}")
    if "B1" in b:
        sys.exit("HIBA: a B1 nem lehet a beírandók között")
    raw = FORRAS.read_bytes()
    crlf = b"\r\n" in raw
    s = raw.decode("utf-8").replace("\r\n", "\n")
    eredeti = s

    hA = "teológiai kijelentést is hordoz Isten természetéről.\n"
    s = beszur(s, hA, "\n" + "\n\n".join(b[k] for k in A) + "\n")
    hB = "állapotot tükrözi, a study-frissítés így teljesült.】\n"
    s = beszur(s, hB, "\n" + "\n\n".join(b[k] for k in B) + "\n")
    hC = "ezt a párt a kutatás a BDB-idézet alapján találta meg, nem önálló kereséssel.\n"
    s = beszur(s, hC, "\n" + "\n\n".join(b[k] for k in C) + "\n")

    # ellenőrzés: az eredeti szöveg minden sora sorrendben megmaradt
    it = iter(s.split("\n"))
    for sor in eredeti.split("\n"):
        if not any(sor == x for x in it):
            sys.exit(f"HIBA: eredeti sor elveszett: {sor[:60]!r}")
    # a rés-határok között vannak-e
    for kod, nyit, zar in (("A/B", "<!-- RÉS-KEZDET: ertelmezes -->", "<!-- RÉS-VÉGE: ertelmezes -->"),
                           ("C", "<!-- RÉS-KEZDET: modszertan -->", "<!-- RÉS-VÉGE: modszertan -->")):
        n, z = s.index(nyit), s.index(zar)
        for k in (A + B if kod == "A/B" else C):
            p = s.index(b[k])
            if not (n < p < z):
                sys.exit(f"HIBA: a {k} blokk a résen kívül van")
    out = s.replace("\n", "\r\n") if crlf else s
    FORRAS.write_bytes(out.encode("utf-8"))
    print(f"ok: {len(A + B + C)} blokk beírva; sorok {len(eredeti.splitlines())} -> {len(s.splitlines())}")


if __name__ == "__main__":
    main()
