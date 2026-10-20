"""F126 (ISTENTISZT001_PROZA) — a mérés CLI-lekérdezései egy futásban.

A `lekerdez.py` parancsait `--naplo F126 --lepes adhoc` kapcsolóval futtatja
(a proveniencia-sorok a `naplok/F126_lekerdezesek.tsv`-be kerülnek, nem az
`adat/auditok.tsv`-be, DT103), a teljes kimenetet pedig a megadott könyvtárba
írja lekérdezésenként egy fájlba (a repón kívül, munkapéldány).

Használat: python naplok/F126_cli_futtat.py <kimeneti_konyvtar>
"""
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent

# A 22 ószövetségi előfordulás (lxx-hid, N-F55d) + a Zsolt 99:6 külön soron.
OSZ = ["1Móz 4:26", "1Móz 12:8", "1Móz 13:4", "1Móz 21:33", "1Móz 26:25",
       "2Móz 33:19", "2Móz 34:5", "1Kir 18:24", "1Kir 18:25", "1Kir 18:26",
       "2Kir 5:11", "1Krón 16:8", "Zsolt 79:6", "Zsolt 105:1", "Zsolt 116:4",
       "Zsolt 116:13", "Zsolt 116:17", "Ézs 12:4", "Jer 10:25", "Jóel 2:32",
       "Sof 3:9", "Zak 13:9", "Zsolt 99:6"]

# Károli-szöveg: a 8 meg nem nevezett hely és a bekezdések partnerhelyei.
KAROLI = ["1Kir 18:24", "1Kir 18:25", "1Kir 18:26", "Zak 13:9",
          "Zsolt 116:4", "Zsolt 116:13", "Jóel 2:32", "ApCsel 2:21", "Róm 10:13",
          "1Krón 16:8", "Zsolt 105:1", "Ézs 12:4", "Zsolt 79:6", "Jer 10:25", "Sof 3:9",
          "1Móz 12:8", "1Móz 13:4", "1Móz 26:25",
          "ApCsel 9:14", "ApCsel 9:21", "Róm 10:12", "1Kor 1:2",
          "2Kir 5:11", "Róm 10:14", "2Móz 33:19", "2Móz 34:5"]

# Kollokációk a gerinc-igével (H7121) — a kísérő szavak teljes-ÓSZ képe.
KOLL = [("H7121", "H6030"), ("H7121", "H0784"), ("H7121", "H4422"),
        ("H7121", "H3045"), ("H7121", "H3034"), ("H7121", "H4196"),
        ("H7121", "H3605"), ("H7121", "H1471")]

# Teljes scan a G4982-re és a G3956-ra nem kell (túl gyakori); a G1941-re igen.
SCAN = [("G1941", None)]


def fut(args, kimenet: Path):
    cmd = [sys.executable, str(REPO / "eszkozok" / "lekerdez.py"),
           "--naplo", "F126", "--lepes", "adhoc"] + args
    p = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True,
                       encoding="utf-8")
    kimenet.write_text(p.stdout + ("\n# STDERR\n" + p.stderr if p.stderr else ""),
                       encoding="utf-8")
    utolso = [s for s in p.stdout.splitlines() if s.startswith("proveniencia:")]
    print(f"{' '.join(args)}\t{p.returncode}\t{utolso[-1] if utolso else '(nincs proveniencia-sor)'}")


def main():
    ki = Path(sys.argv[1])
    ki.mkdir(parents=True, exist_ok=True)
    for ige in OSZ:
        fut(["lxx-hid", ige], ki / f"lxx_{ige.replace(' ', '_').replace(':', '_')}.txt")
    for ige in KAROLI:
        fut(["karoli", ige], ki / f"karoli_{ige.replace(' ', '_').replace(':', '_')}.txt")
    for a, b in KOLL:
        fut(["kollokacio", a, b], ki / f"koll_{a}_{b}.txt")
    for s, szak in SCAN:
        fut(["scan", s] + (["--szakasz", szak] if szak else []), ki / f"scan_{s}.txt")


if __name__ == "__main__":
    main()
