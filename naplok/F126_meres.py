"""F126 (ISTENTISZT001_PROZA) — a felmérés adatállításainak újramérése a 32 előfordulásra.

Csak olvas. A TSV-ket `split('\\t')`-tel olvassa (CLAUDE.md: a `csv` modul ezeken a
táblákon adatot ront). Kimenet: stdout, összefüggésenként, a végén saját
proveniencia-sorral. A felmérés számai itt kiindulópontok, nem források.

Források:
  adat/elofordulasok.tsv (id=ISTENTISZT-001: a 32 igehely, funkció, BDB-jelentés)
  adat/kapcsolatok.tsv (id=ISTENTISZT-001)
  adat/lxx_dontesek.tsv (id=ISTENTISZT-001)
  adat/grammatikai_strongok.tsv (a tartalmi szó szűrője)
  konkordancia/TAHOT_kivonat.tsv (ÓSZ-tokenek, Károli-vers kulcs)
  konkordancia/TAGNT_kivonat.tsv (ÚSZ-tokenek, `Kritikai kiadás` mező)
  konkordancia/Karoli_1908.tsv (Károli-szöveg)
  konkordancia/BSB_Strongs.tsv + Konyv_normalizalo_tabla.tsv (BSB angol szó)

Használat: python naplok/F126_meres.py
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = Path(__file__).resolve().parent.parent
MOTIVUM = "ISTENTISZT-001"


def sorok(path):
    """Fejléces TSV: (fejléc, sorlista dict-ként); a '#' kezdetű sorokat átugorja."""
    fej = None
    ki = []
    with open(path, encoding="utf-8") as f:
        for s in f:
            s = s.rstrip("\n").rstrip("\r")
            if not s or s.startswith("#"):
                continue
            mezok = s.split("\t")
            if fej is None:
                fej = mezok
                continue
            ki.append(dict(zip(fej, mezok)))
    return fej, ki


def strong_norm(s):
    s = s.strip()
    if len(s) >= 2 and s[0] in "HG" and s[1:].isdigit():
        return s[0] + s[1:].zfill(4)
    return s


# --- alapadatok -------------------------------------------------------------
_, elo = sorok(REPO / "adat" / "elofordulasok.tsv")
elo = [r for r in elo if r.get("id") == MOTIVUM]
IGEK = [r["igehely"] for r in elo]
OSZ = [r["igehely"] for r in elo if r["strong"].startswith("H")]
USZ = [r["igehely"] for r in elo if r["strong"].startswith("G")]

_, gram = sorok(REPO / "adat" / "grammatikai_strongok.tsv")
GRAM = {strong_norm(r["strong"]) for r in gram}


def tokenek(fajl, igek):
    ki = {i: [] for i in igek}
    with open(fajl, encoding="utf-8") as f:
        fej = None
        for s in f:
            s = s.rstrip("\n").rstrip("\r")
            if not s or s.startswith("#"):
                continue
            m = s.split("\t")
            if fej is None:
                fej = m
                continue
            if m[0] in ki:
                ki[m[0]].append(dict(zip(fej, m)))
    return ki


TOK = tokenek(REPO / "konkordancia" / "TAHOT_kivonat.tsv", OSZ)
TOK.update(tokenek(REPO / "konkordancia" / "TAGNT_kivonat.tsv", USZ))


def strongok(ige):
    return [strong_norm(t["Strong-szám"]) for t in TOK[ige]]


KAROLI = {}
with open(REPO / "konkordancia" / "Karoli_1908.tsv", encoding="utf-8") as f:
    for s in f:
        m = s.rstrip("\n").rstrip("\r").split("\t")
        if len(m) >= 2 and m[0] in IGEK:
            KAROLI[m[0]] = m[1]


def hol(strong, igek=None):
    igek = igek or IGEK
    return [i for i in igek if strong in strongok(i)]


def tartalmi(ige):
    return {s for s in strongok(ige) if s not in GRAM and not s.startswith("H9")}


def kiir(cim, ertek):
    print(f"{cim}\t{ertek}")


print(f"# 32 előfordulás? n={len(IGEK)} (ÓSZ {len(OSZ)}, ÚSZ {len(USZ)})")
hiany = [i for i in IGEK if not TOK[i]]
print(f"# tokennélküli igehely: {hiany if hiany else 'nincs'}")
print()

# --- 1. Hívás és felelet ----------------------------------------------------
print("## 1. Hívás és felelet")
kiir("H6030 (felel) a 32 közül", hol("H6030"))
kiir("H0784 (tűz) a 32 közül", hol("H0784"))
for i in ["1Kir 18:24", "1Kir 18:25", "1Kir 18:26", "Zak 13:9"]:
    kiir(f"Károli {i}", KAROLI.get(i, "—"))
for i in ["1Kir 18:24", "1Kir 18:25", "1Kir 18:26"]:
    kiir(f"H1168 (Baál) {i}", "H1168" in strongok(i))
kiir("H4196 (oltár) 1Kir 18:24–26", hol("H4196", ["1Kir 18:24", "1Kir 18:25", "1Kir 18:26"]))
print()

# --- 2. Hívás és megmenekülés -----------------------------------------------
print("## 2. Hívás és megmenekülés")
kiir("H4422 (megmenekül) a 32 közül", hol("H4422"))
kiir("G4982 (megment) a 32 közül", hol("G4982"))
kiir("Károli Zsolt 116:4", KAROLI.get("Zsolt 116:4"))
kiir("Károli Jóel 2:32", KAROLI.get("Jóel 2:32"))
kiir("Zsolt 116:4 tartalmi Strongok", sorted(tartalmi("Zsolt 116:4")))
kiir("Jóel 2:32 tartalmi Strongok", sorted(tartalmi("Jóel 2:32")))
print()

# --- Zsolt 116:13 (nincs-e új anyag) -----------------------------------------
print("## Zsolt 116:13")
kiir("Károli", KAROLI.get("Zsolt 116:13"))
kiir("tartalmi Strongok", sorted(tartalmi("Zsolt 116:13")))
for s in sorted(tartalmi("Zsolt 116:13")):
    kiir(f"  {s} a 32 közül", hol(s))
print()

# --- 6. Ismerni és nem ismerni ----------------------------------------------
print("## 6. Ismerni és nem ismerni")
kiir("H3045 (ismer) a 32 közül", hol("H3045"))
kiir("H1471 (pogányok/nemzetek) a 32 közül", hol("H1471"))
kiir("H5971 (nép) a 32 közül", hol("H5971"))
kiir("H3816 (nemzet) a 32 közül", hol("H3816"))
kiir("H4940 (nemzetség) a 32 közül", hol("H4940"))
kiir("H4467 (ország) a 32 közül", hol("H4467"))
for i in ["1Krón 16:8", "Zsolt 105:1", "Ézs 12:4", "Zsolt 79:6", "Jer 10:25", "Sof 3:9"]:
    kiir(f"Károli {i}", KAROLI.get(i))
print()

# --- 7. Liturgikus hármas ----------------------------------------------------
print("## 7. A liturgikus hármas")
kiir("H3034 (hálát ad) a 32 közül", hol("H3034"))
a, b, c = (tartalmi(x) for x in ["1Krón 16:8", "Zsolt 105:1", "Ézs 12:4"])
kiir("1Krón 16:8 tartalmi", sorted(a))
kiir("Zsolt 105:1 tartalmi", sorted(b))
kiir("Ézs 12:4 tartalmi", sorted(c))
kiir("1Krón 16:8 ∩ Zsolt 105:1", f"{sorted(a & b)} | {len(a & b)}/{len(a | b)}")
kiir("1Krón 16:8 ∩ Ézs 12:4", f"{sorted(a & c)} | {len(a & c)}/{len(a | c)}")
kiir("Zsolt 105:1 ∩ Ézs 12:4", f"{sorted(b & c)} | {len(b & c)}/{len(b | c)}")
print()

# --- 8. Két oltár ------------------------------------------------------------
print("## 8. Két oltár")
kiir("H4196 (oltár) a 32 közül", hol("H4196"))
kiir("H1129 (épít) a 32 közül", hol("H1129"))
print()

# --- 9. Mindenki, aki --------------------------------------------------------
print("## 9. „Mindenki, aki”")
kiir("H3605 (mind) a 32 közül", hol("H3605"))
kiir("G3956 (mind) a 32 közül", hol("G3956"))
for i in ["ApCsel 9:14", "ApCsel 9:21", "Róm 10:12", "1Kor 1:2", "Jóel 2:32", "Sof 3:9"]:
    kiir(f"Károli {i}", KAROLI.get(i))
for i in hol("G3956"):
    al = [t["Ragozott alak"] for t in TOK[i] if strong_norm(t["Strong-szám"]) == "G3956"]
    kiir(f"  G3956 alak {i}", al)
kiir("G1672 (görög) a 32 közül", hol("G1672"))
kiir("G2453 (zsidó) a 32 közül", hol("G2453"))
kiir("G3686 (név) ApCsel 9:21-ben", "G3686" in strongok("ApCsel 9:21"))
print()

# --- 10. A kívülálló ---------------------------------------------------------
print("## 10. A kívülálló elvárása")
r = next(x for x in elo if x["igehely"] == "2Kir 5:11")
kiir("funkcio", r["funkcio"])
kiir("kapcsolodas", r["kapcsolodas"])
kiir("Károli", KAROLI.get("2Kir 5:11"))
print()

# --- 11. Négy forrás ---------------------------------------------------------
print("## 11. Négy forrás a határeseteken")
norm = {}
_, nt = sorok(REPO / "konkordancia" / "Konyv_normalizalo_tabla.tsv")
for x in nt:
    norm[x["STEPBible-rövidítés"]] = x["Magyar rövidítés"]
BSB = {}
with open(REPO / "konkordancia" / "BSB_Strongs.tsv", encoding="utf-8") as f:
    fej = None
    for s in f:
        m = s.rstrip("\n").rstrip("\r").split("\t")
        if fej is None:
            fej = m
            continue
        if len(m) < 4 or strong_norm(m[2]) != "H7121":
            continue
        k, fe, v = m[0].split(".")
        hu = f"{norm.get(k, k)} {fe}:{v}"
        if hu in OSZ:
            BSB.setdefault(hu, []).append(m[3])
_, lxxd = sorok(REPO / "adat" / "lxx_dontesek.tsv")
lxxd = {x.get("igehely"): x for x in lxxd if x.get("igehely") in OSZ and x.get("heber_strong") == "H7121"}  # id: LD-kulcs
for i in OSZ:
    r = next(x for x in elo if x["igehely"] == i)
    kiir(f"{i}", f"BDB {r['lexikon_szotar']} {r['jelentes_szam']} | BSB H7121: {BSB.get(i, ['—'])} | "
                 f"Károli-szó: {r['karoli_szo']} | lxx_dontesek: {'sor van' if i in lxxd else '—'}")
print("# lxx_dontesek sorai:")
for i, x in lxxd.items():
    print("  " + " | ".join(f"{k}={v}" for k, v in x.items() if k in ("id", "igehely", "lxx_igehely", "gorog_lemma", "gorog_strong", "tipus")))
print()

# --- 12. Róm 10:14 -----------------------------------------------------------
print("## 12. Hit, hirdetés, hívás — Róm 10:14")
for t in TOK["Róm 10:14"]:
    print(f"  {t['Strong-szám']}\t{t['Ragozott alak']}\t{t['Kritikai kiadás']}")
_, kap = sorok(REPO / "adat" / "kapcsolatok.tsv")
for x in kap:
    if x["id"] == MOTIVUM and "Róm 10:14" in (x["forras_igehely"], x["cel_igehely"]):
        kiir("kapcsolat", f"{x['forras_igehely']} → {x['cel_igehely']} | {x['tipus']} | {x['bizonyossag']}")
print()

# --- a 8 meg nem nevezett hely kapcsolatai -----------------------------------
print("## A 8 hely kapcsolatai (kapcsolatok.tsv)")
NYOLC = ["1Kir 18:25", "1Kir 18:26", "1Krón 16:8", "Zsolt 105:1", "Zsolt 116:4",
         "Zsolt 116:13", "ApCsel 9:21", "Róm 10:14"]
for i in NYOLC:
    k = [f"{x['forras_igehely']}→{x['cel_igehely']} ({x['tipus']}, {x['bizonyossag']})"
         for x in kap if x["id"] == MOTIVUM and i in (x["forras_igehely"], x["cel_igehely"])]
    r = next(x for x in elo if x["igehely"] == i)
    kiir(i, f"funkcio={r['funkcio']} | kapcsolatok={k}")
print()

ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
print(f"proveniencia: scope=adat/elofordulasok.tsv (id={MOTIVUM}, n={len(IGEK)}) | "
      f"forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+Karoli_1908.tsv+BSB_Strongs.tsv+"
      f"kapcsolatok.tsv+lxx_dontesek.tsv+grammatikai_strongok.tsv (naplok/F126_meres.py, split('\\t')) | ts={ts}")
