import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# az okok szerinti bontas ujraolvasasa (KK1-bol)
ok_szamlalo = Counter()
with open("naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 5:
            continue
        ok_szamlalo[parts[4]] += 1

mert_osszesen = sum(ok_szamlalo.values())
megoldodna = ok_szamlalo.get("H1_importer_kezi_none_fallthrough", 0) + ok_szamlalo.get("H2_karoli_mt_szamozas", 0)
nem_oldodik = ok_szamlalo.get("H3_egyeb_karoli_sajatossag", 0) + ok_szamlalo.get("H5_valodi_verstartalmi_elteres", 0)

print("=== Hatasbecsles: a KK2-tervezet (G4-javitas) alkalmazasa eseten ===")
print(f"Mert szamozas_elteres LXX-vers (a 38 nem-Zsoltar konyvben): {mert_osszesen}")
print(f"  -> megoldodna (H1+H2, az importer-javitas kezelné): {megoldodna} ({100*megoldodna/mert_osszesen:.1f}%)")
print(f"  -> tovabbra sem oldodik meg (H3 EGYIK_SEM + H5 valodi LXX-elteres): {nem_oldodik} ({100*nem_oldodik/mert_osszesen:.1f}%)")

# a teljes 1015-re (39 konyv, Zsoltarokkal egyutt) aranyositva becsult ertek
teljes_1015_becsult = round(1015 * megoldodna / mert_osszesen)
print(f"\nA teljes 1015 LXX-versre aranyositva becsult megoldodo szam: ~{teljes_1015_becsult} ({100*megoldodna/mert_osszesen:.1f}%)")
print("(A Zsoltarok 63 fejezete/kb. 30 erintett verse nincs kulon mérve -- "
      "sajat cim-eltolas-logikaja van, a becsles csak aranyositas, nem kulon szamitas.)")

# a 15 lexikon-sor becsult uj allapota
print("\n=== A lexikon 15 sora - becsult uj allapot (csak elorejelzes, generalast NEM futtatunk) ===")
sorok = []
with open("naplok/KAROLI_KK1_15sor.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 2:
            continue
        igehely, ok = parts[0], parts[1]
        if ok in ("H1", "H2"):
            uj_allapot = "megoldodna (uj Karoli-igehely szuletik)"
        elif ok == "H4":
            uj_allapot = "VALTOZATLAN marad ebben a menetben (generator-oldali, G6: csak javaslat)"
        else:
            uj_allapot = "VALTOZATLAN marad (H3: kezi egyeztetes kell / H5: valodi elteres)"
        sorok.append((igehely, ok, uj_allapot))
        print(f"  {igehely} ({ok}): {uj_allapot}")

megoldodo_sorok = sum(1 for _, ok, _ in sorok if ok in ("H1", "H2"))
print(f"\nOsszesen {megoldodo_sorok}/15 lexikon-sor oldodna meg kozvetlenul a G4-importer-javitastol.")
print("A H4 (4 sor, Jozsue) kulon generator-oldali javitast igenyel (G6, kesobbi menet).")

print("\n=== Elorejelzes a lexikon 'Egyezes' bontasara (123/87/3/5/1 -- csak a 8 TUDOMANYOS oldalon) ===")
print("  egyezo: 123 -> ~130 (7 uj sor a H1+H2-bol)")
print("  szamozas_elteres: 15 -> ~8 (3 H3 + 4 H4 + 1 H5 marad)")
print("  a tobbi (kutatoi azonositas fuggoben 87, elterő 3, nincs LXX_OS-konyv 5, LXX-minusz 1): valtozatlan")
print("  MEGJEGYZES: ez elorejelzes, a tenyleges szam csak a KK5 (lexikon ujragenerálás) utan derul ki (KK6).")
