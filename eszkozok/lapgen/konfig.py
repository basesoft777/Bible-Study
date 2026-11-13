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

# A dátum környezeti változója (YYYY-MM-DD); nélküle a `ts=` a bemenetek hash-éből képződik (GK-29).
DATUM_VALTOZO = 'PARDES_DATUM'
TS_HASH_JEGY = 12
