"""lapgen.konfig — a generátor küszöbei, szűrő-halmazai és kiadási azonosítói egy helyen.

Ide nevesített konstans kerül, teszttel (`tesztek/teszt_konfig.py`). Látható mondat nem áll itt:
az a sablontáblában van; a mondatban álló szám innen jön, formázott sablonparaméterként.
"""

# A generált blokkok jelölőjében álló célnév. A termék célneve `lexikon`; az új generátor a 218a
# alatt `--cel lexikon2` néven hívható, de a lapon a végleges célnevet írja (a jelölőket más eszközök
# is olvassák, és a regresszió bájtra mér).
CEL_NEV = 'lexikon'
GENERATOR_JELOLO = 'general.py --cel ' + CEL_NEV

# A nézetek fájlnév-utótagjai.
NEZET_TUDOMANYOS = 'TUDOMANYOS'
NEZET_KIZARASOK = 'KIZARASOK'

# Az olvasási napló fájlja a lap mellett (`<ID>_olvasasi_naplo.tsv`): a regresszió bemenet-hash őre olvassa.
NAPLO_FAJLNEV = '%s_olvasasi_naplo.tsv'
NAPLO_OSZLOPOK = ('b_id', 'utvonal', 'sha256')

# A dátum környezeti változója (YYYY-MM-DD); nélküle a `ts=` a bemenetek hash-éből képződik (GK-29).
DATUM_VALTOZO = 'PARDES_DATUM'
TS_HASH_JEGY = 12

# --- 2. Előfordulások: az összegző mondat küszöbei --------------------------------------------------------------
SULYPONT_KUSZOB = 0.40      # egy könyvben a helyek legalább ekkora hányada: a motívum súlypontja
SZOVETSEG_KUSZOB = 0.20     # ennél kisebb arányú szövetség: „főként ószövetségi / újszövetségi”
BIZONYTALAN_KUSZOB = 0.67   # a magas megbízhatóságú helyek aránya ez alatt: „sok a bizonytalan azonosítás”

KOZOS_PROVENIENCIA_KUSZOB = 2   # ennyi jegyzetben álló proveniencia-hármas kap közös jelet (‹E1› …)

# --- Döntési út és a kizárások melléklete ----------------------------------------------------------------------
CSOPORT_PELDA_DB = 5            # a csoportos ok alatt ennyi példavers áll a Károli-szöveggel
KIZARASOK_NYITVA_HATAR = 10     # a melléklet verslistája ennyi versig nyitva áll, fölötte lenyíló

# --- Döntések, amelyeknek a dátuma a lapon áll (a szám nem) -----------------------------------------------------
DONTES_JELENTES_FUNKCIO = 'DT272'   # a „Jelentés (a szó)” és a „Funkció (a motívumban)” oszlop szétválasztása
DONTES_UBS_SZONEZET = 'DT393'       # az UBS-jelentés cellája: rövid glossza, a teljes szócikk a szónézetben

# --- UBS-jelentés: a fordítástábla kulcsai ---------------------------------------------------------------------
SZOTAR_UBS_DNTG = 'UBS_DNTG'
SZOTAR_UBS_DBH = 'UBS_DBH'
UBS_GLOSSZA_MEZO = 'glosszak_hu'
NINCS_JELENTESSZAM = '—'            # a fordítástábla kulcsában a jelentésszám nélküli szócikk jele
