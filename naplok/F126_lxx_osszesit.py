"""F126 (ISTENTISZT001_PROZA) — N-F55d: a „22 ószövetségi igehely közül 18” újraszámolása.

Bemenet: az `F126_cli_futtat.py` által mentett `lxx-hid` kimenetek (lxx_*.txt) egy
könyvtárban; mindegyik a `lekerdez.py lxx-hid <igehely> --naplo F126 --lepes adhoc`
teljes kimenete, saját proveniencia-sorral. A szkript versenként kiírja, áll-e
G1941 / G2564 / G0994 az LXX-versben, a szóalakot, és az `adat/lxx_dontesek.tsv`
sorát (split('\\t')).

Használat: python naplok/F126_lxx_osszesit.py <cli_kimeneti_konyvtar>
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
FIGYELT = ("G1941", "G2564", "G0994", "G4506", "G4982")


def main():
    d = Path(sys.argv[1])
    dont = {}
    with open(REPO / "adat" / "lxx_dontesek.tsv", encoding="utf-8") as f:
        fej = None
        for s in f:
            s = s.rstrip("\n").rstrip("\r")
            if not s or s.startswith("#"):
                continue
            m = s.split("\t")
            if fej is None:
                fej = m
                continue
            r = dict(zip(fej, m))
            if r.get("heber_strong") == "H7121":  # az id LD-kulcs; motívumoszlop nincs
                dont[r["igehely"]] = r
    g1941 = 0
    n = 0
    for p in sorted(d.glob("lxx_*.txt")):
        sorok = p.read_text(encoding="utf-8").splitlines()
        ige = sorok[0].split("—")[0].replace("# LXX-híd", "").strip()
        lxxv = sorok[1].replace("# LXX-vers:", "").strip() if len(sorok) > 1 else ""
        talal = {}
        for s in sorok[2:]:
            if s.startswith("#") or s.startswith("  ") or s.startswith("proveniencia"):
                continue
            m = s.split("\t")
            if len(m) >= 2 and m[0] in FIGYELT:
                talal.setdefault(m[0], []).append(m[1])
        prov = next((s for s in sorok if s.startswith("proveniencia:")), "")
        van = "G1941" in talal
        if ige != "Zsolt 99:6":
            n += 1
            g1941 += 1 if van else 0
        dsor = dont.get(ige)
        dtxt = (f"{dsor.get('gorog_lemma')} {dsor.get('gorog_strong')} {dsor.get('tipus')}"
                if dsor else "—")
        print(f"{ige}\t{lxxv}\t{talal if talal else 'nincs figyelt G-token'}\t"
              f"lxx_dontesek: {dtxt}\t{prov}")
    print(f"\nÖSSZESEN (Zsolt 99:6 nélkül): {n} ószövetségi hely, ebből G1941 az LXX-versben: {g1941}")


if __name__ == "__main__":
    main()
