# DIFF_SZUKITES zárójelentés (#113, `claude/diff-szukites`, 2026-10-18)

**Mi változott** (`eszkozok/render_diff_osztalyoz.py`). Mind az öt hely a változás fajtája szerint dönt:
- (1) szerep: a cellához kötött `_szerep_csere`. A régi tábla a `d9b80b37`-es mátrix rögzített kivonata (`REGI_SZEREPMATRIX_D9B80B37`, blob `bce21db8`, DT-F113b). Az F113.10 óta a helyőrző → új érték csak igazolt új oldallal fogadható el.
- (2) licenc: licencszöveg vagy -jelző, illetve bővült lista (`_bovult_lista`, DT-F113a (c)).
- (3) szám: tág darabszám-lista; az igehely, a jelentésszám és a `BDB`/`LSJ N` alak `ismeretlen`.
- (4) LXX: csak előre lépő állapot fogadható el, a `_kanon` nem olvaszt össze állapotokat.
- (5) zárójeles átírás: adatalapú `_atiras_par`.

**Tesztek:** 45 → 73, mind zöld. Minden szűkítéshez van negatív teszt, és ezek a régi kódon elbuknak (mutációs futás). A `:80-82` és a `:84-85` teszt át van írva.

**Mérés:** a kiinduló állapot (F113.1) 0 `ismeretlen` + 44 `felhasznalo_elfogadva`, a záró állapot (`naplok/DIFF_SZUKITES_diff.tsv`) 0 `ismeretlen` + 55 `felhasznalo_elfogadva`. A 11 új sor a DT-F113b szerinti (8 `jelmagyarazat_mondat` és 3 `kezi_2b_lefedettseg_sece`), a `szerep` 208-ról 197-re csökkent. A `lexikon/`, a `generalt_proba/` és a `naplok/SZOTAR_S2_*` bájtra változatlan. `ellenoriz.py`: SÉRTÉS 0; `feladatok.py ellenoriz`: 0 hiba.

**Az 5. lépés választása:** az adatalapú próba, mert a karakter-alapú nem tudná egyszerre elfogadni az `(abussou)` → `(abüsszú)` párt és elutasítani a `(pap)` → `(király)` párt. Ismert gyenge pont: egy x → `atir(x)` alakú csere magyar szónál is átmenne.

**„UBS DNTG → Mounce”:** nem `szerep`, ha a cella szerepéhez a mátrix nem ezt rendeli.

**Egyeztetett eltérés:** két ⛔ volt.
- DT-F113a: a szűkítés szabályai, (a)–(d).
- DT-F113b: a régi tábla forrása a `d9b80b37`, és a 11 sor név szerint elfogadva. Ez felülírja a brief „Nincs benne” listájának elfogadottsor-tilalmát.

A brief öt helyén kívüli blokk szerinti ágak (`_torzscikk_kat`, a `_mezo_kat` `azon` ága, az ellenőr szerint a `_tudomanyos_kategoria` `idezes`/`kolofon`/`lxx` ága is) az N-F113a-ba kerültek.

**Ellenőrzés** (`naplok/ELLENOR_DIFF_SZUKITES.md`): ELTÉRÉS, 1 közepes és 2 alacsony.
- A közepes (helyőrző → bármi = `szerep`) javítva: F113.10.
- Az alacsony fejléc-eltérés javítva.
- Nyitva marad: a 3 `kézi (2/b)` sor egész soros elfogadása a 7. oszlopon kívül más cellacseréket is lefed (H7121: `TBESH` → `BDB 2.c (DT-F42a)`), a felhasználó tisztázására vár.

**N-F09i:** a felhasználó döntése szerint (5d) a menet nem zárja le, csak itt jelzi. A lezárás külön tétel, a merge után.

**A 2. ellenőri eltérés tisztázása (felhasználó, chat, 2026-10-18):** „A 3 sor egész soros elfogadása elfogadható (a többi cellacsere a cellaszabályon is átmenne).” Nincs további kódváltozás.
