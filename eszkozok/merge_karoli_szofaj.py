#!/usr/bin/env python3
"""Egyszeri script: Karoli_Strong_kivonat.tsv bovitese Szofaj + Gyok/Szarmaztatas oszlopokkal, Strong_szotar.tsv alapjan."""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import re

SZOTAR_PATH = "konkordancia/Strong_szotar.tsv"
KIVONAT_PATH = "konkordancia/Karoli_Strong_kivonat.tsv"


def tsv_sor(mezok):
    """Egy TSV-sor a csv modul nelkul — l. CLAUDE.md, „TSV-olvasas".

    A modul iroja a " jelet tartalmazo mezot korulidezi es belul duplazza,
    tehat a korutja nem bajthu. Sorveg '\\n', mint a kivaltott hivas
    lineterminator erteke.
    """
    ki = []
    for m in mezok:
        m = "" if m is None else str(m)
        if "\t" in m or "\n" in m or "\r" in m:
            raise ValueError("elvalaszto a mezoben: %r" % (m,))
        ki.append(m)
    return "\t".join(ki) + "\n"


def normalize(strong):
    """H430 -> H0430, H7225 -> H7225, G26 -> G0026 (4 szamjegyre padolva)."""
    m = re.match(r"^([HG])(\d+)([A-Za-z]*)$", strong)
    if not m:
        return strong
    letter, digits, suffix = m.groups()
    return f"{letter}{int(digits):04d}{suffix}"

lookup = {}
with open(SZOTAR_PATH, encoding="utf-8") as f:
    szotar_sorok = [ln.rstrip("\n").rstrip("\r") for ln in f if ln.strip()]
for s in szotar_sorok[1:]:
    row = s.split("\t")
    if not row:
        continue
    strong = row[0]
    szofaj = row[3] if len(row) > 3 else ""
    gyok = row[4] if len(row) > 4 else ""
    lookup[strong] = (szofaj, gyok)

with open(KIVONAT_PATH, encoding="utf-8", newline="") as f:
    eredeti_nyers = f.read()
kivonat_sorok = [s.rstrip("\r") for s in eredeti_nyers.split("\n")]
rows = [s.split("\t") for s in kivonat_sorok if s.strip()]

fejlec_hossz = len(rows[0])
for i, row in enumerate(rows[1:], start=2):
    if len(row) != fejlec_hossz:
        raise SystemExit(
            "MEGALLAS: %s %d. sor: %d mezo a fejlec %d mezoje helyett. Nem irtam semmit."
            % (KIVONAT_PATH, i, len(row), fejlec_hossz))

out_rows = [rows[0] + ["Szófaj", "Gyök/Származtatás"]]
for row in rows[1:]:
    if not row:
        continue
    strong = row[1]
    szofaj, gyok = lookup.get(normalize(strong), ("", ""))
    out_rows.append(row + [szofaj, gyok])

kimenet = "".join(tsv_sor(r) for r in out_rows)

# --- bajt-szintu korut-ellenorzes, IRAS ELOTT (CLAUDE.md zaromondata) ---
# A szkript ugyanazt a fajlt olvassa es irja felul helyben, tehat egy nem bajthu
# iro itt visszavonhatatlanul rontana. A kimenetbol a ket hozzafuzott oszlopot
# levagva pontosan az eredeti fajlt kell visszakapni — kulonben MEGALLAS.
# (A referencia-blobhoz merest l. eszkozok/f4_0c_korut_ellenoriz.py.)
_vissza = "".join(tsv_sor(r[:-2]) for r in out_rows)
_varht = "".join(s + "\n" for s in kivonat_sorok if s.strip())
if _vissza != _varht:
    raise SystemExit(
        "MEGALLAS: a korut nem bajthu — a kimenetbol a ket uj oszlopot levagva "
        "nem az eredeti %s jon vissza. Nem irtam semmit." % KIVONAT_PATH)
if len([s for s in kivonat_sorok if not s.strip()]) > (1 if eredeti_nyers.endswith("\n") else 0):
    raise SystemExit(
        "MEGALLAS: %s ures sort tartalmaz, amit az iras eldobna. Nem irtam semmit."
        % KIVONAT_PATH)

with open(KIVONAT_PATH, "w", encoding="utf-8", newline="") as f:
    f.write(kimenet)

print(f"Sorok: {len(out_rows)-1}, ebbol Strong_szotar-adattal ellatva: {sum(1 for r in out_rows[1:] if r[6])}")
