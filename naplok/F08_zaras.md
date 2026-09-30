# F08 zárójelentés (FELADATOK #8; ág: `claude/lxx-dontesek`)

**Elkészült:** a 87 függő hely (`naplok/F17_87_hely.tsv`) 86 sort kapott az `adat/lxx_dontesek.tsv`-ben (LD005–LD090; a 4Móz 13:34 a HODIT-001 és a MENNY-001 közös sora); a régi LD001–LD004 változatlan (4 → 90 adatsor). Bizonyosság (F8.8, a DT23 döntése után): **biztos 61** (mind `eltero_forditas`), **valószínű 13**, **nyitott 4** (LD008, LD009, LD058, LD064), **nem_alkalmazhato 8** (`nincs_heber_kulcsszo`). Bemenet: `naplok/F08_bemenet.txt`, szkriptek: `eszkozok/f08/`.

**Módszer:** független forrás csak a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű verse; az FJ1-jelölt Macula-származék. A Macula 38 gépi megfelelőjéből 36 megerősítve, 2 ellentmondó. Minden `gorog_strong` az `LXX_OS` adott pozíciójából jön. **A DT23 (b) szerint kitöltött 4 sor (LD027, LD035, LD050, LD052) `valoszinu`: egy forrás + felhasználói döntés (`dontes=DT23(b)`), a brief „biztos” definíciója (két független forrás) rájuk nem teljesül.**

**Sémaeltérés, `ir` listán kívüli módosítás (DT23 (d), elfogadva):** `bizonyossag` oszlop és `nincs_heber_kulcsszo` típus (SEMA 2.11); `ellenoriz.py` 10. szabálya és a `lexikon_general.py` szűrője. **A PR-cím `[ELLENŐRZŐ]` előtagú (CI E16).** A feltétel igazolva (`naplok/F08_nulladiff.txt`, `eszkozok/f08/f08_nulladiff.py`): az ág és az `origin/main` repón kívüli generálása szerint az LD001–LD004-et renderelő `ISTENTISZT-001_TUDOMANYOS.md` bájtra azonos. A teljes kimenet eltérései: +61 „eltérő” LXX-sor (ALVIL 3, HAMART 28, HODIT 18, KIRALY 4, MENNY 4, TEREMT 4), 26 függő marad; az LXX- és kolofon-blokkok forráslistája (+`adat/lxx_dontesek.tsv`); a 8 TORZSCIKK szótár-szerep sorai a main F19-es `szotar_szerepek.tsv`-változásából (nem F08). A „Rokon szavak” blokk nem változott. A lexikonoldalak nincsenek újragenerálva.

**Külön tételek:** `N-F08a` (a Préd 9:10 előfordulás-sor javítása Préd 9:12-re, DT23 (c), DT7 (g)), `N-F08b` (saját címke a `nincs_heber_kulcsszo` sorokra, DT23 (e)) a NYITOTT_FELADATOK.md-ben, az F30 helyőrző-formája szerint.

**Leletek:** HODIT-001 2Sám 21 / 1Krón 20: a kulcs a TAHOT H7497, a H7498 csak Macula-megjegyzés; az 1Krón 8 (személynévi Rafa) nincs a 87 hely között; LD010 Macula G0999 = βόθυνος; a G2672 forrása az `LXX_OS`; a DT7 (a) nem hat ki.

**Ellenőrzés:** `naplok/ELLENOR_F08.md` (1. kör: 8 eltérés, F8.5; 2. kör: 1 alacsony, DT23 (d)). DT23: ✅ alkalmazva (F8.8).
