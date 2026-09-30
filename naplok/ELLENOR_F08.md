# ELLENŐR — F08_LXX_DONTESEK_BRIEF.md · 5b18263..7bd04f3 (claude/lxx-dontesek)

*1. kör. A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette fájlba (az ellenőrnek nincs író eszköze). Eredmény: **ELTÉRÉS: 8 tétel**.*

## Rendben

- Lefedettség: 87 hely, `adat/lxx_dontesek.tsv:7-92`, LD005–LD090 hézag nélkül (a 4Móz 13:34 HODIT+MENNY közös sor).
- LD001–LD004 bájtra azonos (csak üres `bizonyossag` mező került be); az `adat/` sorai nem csökkentek, az `adat/elofordulasok.tsv` érintetlen.
- Törölt sorok (14): fejléc és oszlopbővítés miatti átírások, tartalmi törlés 0.
- Bontási napló (4 → 90 adatsor, DT3 1% fölött): `naplok/F08_bemenet.txt`, proveniencia `#n`.
- Nyitottak igazolva: 1Móz 8:21 (LD027), Mik 6:12 (LD035), valamint Préd 9:10/9:12, Ézs 7:11, 2Sám 21:22, Péld 2:18.
- Valószínű és biztos minta (24 hely) egyezik a `lekerdez.py lxx-hid` és a Macula (F17) értékeivel.
- Proveniencia-sor mind a 86 új soron; az értelmezések jelölve (LD063, LD079).
- Préd 9:10 MT-számozás igazolva; A2, F08-1, F08-2 rendben. A3–A6, E12–E15 nem alkalmazható / 0 találat.

## Eltérések (súlyosság szerint)

1. **LD052 (5Móz 2:20)** `biztos`, pedig a Macula (`κατῴκουν`) ellentmond az LXX-versnek (`ραφαιν`); a Mik 6:12-vel azonos eset ott nyitott lett. A szabály nem egységes.
2. **LD050 (4Móz 13:34)** a döntés nem a munkalap-kulcsszóra (második נְפִלִים, LXX-minusz, a Macula `’’`) vonatkozik, mégis `biztos`; két egyező forrás nincs.
3. **LD030 `G2672`** (és LD027 megjegyzése): az `LXX_OS` és a Macula Strongja üres (`lxx-hid "1Móz 12:3"`), az érték nem a repó adatából jön. A megjegyzés „az LXX_OS (2672) egyezik” nem igazolt. Proveniencia-sértés (CLAUDE.md 1., 3. szabály).
4. **8 `nincs_heber_kulcsszo` sor `biztos`-ként**: a tárgytalanság igaz, de a brief „két független forrás egyezik” skálája nem értelmezhető (nincs LXX-forrás). A „biztos 71” ebből 8-cal felfújt, az érdemi biztos LXX-döntés 63.
5. **E16 CI-hiba**: a PR érinti az ellenőrzőt (`eszkozok/ellenoriz.py`), a cím nem `[ELLENŐRZŐ]` előtagú. A módosítás a brief `ir` listáján kívül esik (SEMA 2.11, `ellenoriz.py` 10. szabály, `lexikon_general.py`), a DT23 (d) elfogadása előtt commitolva. A `lexikon_general.py` változása a „Rokon szavak” blokkot is érinti (`:709-717`), nem csak a 3. (LXX) blokkot.
6. **DT23 (f) H7498**: a TAHOT H7497-et ad (2Sám 21:16/18/20/22, 1Krón 20:4/6/8), a H7498 csak Macula-állítás (`scan H7498` → csak 1Krón 8:2, 8:37). A tétel ezt tényként közli.
7. **DT23 hiányzó tételek**: LD050, LD052 ellentmondása; LD010 G0999/βόθυνος (csak a zárásban); az E16 hiba; a Zsolt 76:3 / 88:11 `igehely_karoli` egy verses elcsúszása az `LXX_OS`-ben (a generátor `lxx_os_karoli_index`-e ettől hibás LXX-igehelyet adhat).
8. **DT23 (a) javaslat**: a 9 valószínű sor biztosra állítása ütközik a brief 3. lépésének definíciójával (két független forrás); a tétel ezt nem mondja ki. (alacsony)

## Nem ellenőrizhető (az ellenőr eszközkészletével)

- `ellenoriz.py` (E1) „RENDBEN 11, SÉRTÉS 0”, `feladatok.py ellenoriz`, a „64 lexikonsor eltérő” generátor-futás, CI-jelentés egyezése. *(Az orkesztrátor a 2. körben futtatja.)*

## Ellenőrző parancs (E2–E15)

`python eszkozok/ellenorzes/futtat.py --valtozott <11 fájl> --diff-alap 5b18263 --diff-fej HEAD` → E2–E8, E10–E15: 0; E9: 2 JELENTES (`adat/SEMA.md:235-236`, változatlan sorok); **E16: HIBA** (PR-cím nélkül futtatva).

---

# 2. kör (head 87980ca) — eredmény: ELTÉRÉS 1 tétel (alacsony), tisztázva

*A `fuggetlen-ellenor` 2. körös jelentésének összefoglalója; az orkesztrátor mentette.*

- **Megoldva (saját lekérdezéssel igazolva):** 1. LD052 `nyitott` (Macula-felcserélés valódi), 2. LD050 `nyitott`, 4. `nem_alkalmazhato` egységes (SEMA 2.11, `ellenoriz.py` 10. szabály, generátor-szűrő; 61 biztos / 9 valószínű / 8 nyitott / 8 nem_alkalmazhato), 6. DT23 (f) H7497/H7498, 7. DT23 kiegészítése, 8. DT23 (a). Bontási napló, ⛔ (adatsor-csökkenés: nincs), A1, A2, A6 rendben.
- **1. kör téves riasztásai:** a 3. pont (G2672): a Strong a `konkordancia/LXX_OS/genesis.tsv`-ben van (12:3 10. pozíció, 8:21 18. pozíció), az `lxx-hid` az `LXX_kivonat`-ot olvassa; az érték a repó adatából jön, a proveniencia a helyes datasetet nevezi. Szúrópróba 13 sor egyezik. A 7. pont Zsolt 76:3/88:11 része: nincs elcsúszás (`igehely_karoli` = MT = Károli, a KJV-mező eggyel kisebb).
- **Nyitott (alacsony):** az `adat/SEMA.md`, `eszkozok/ellenoriz.py`, `eszkozok/lexikon_general.py` módosítása a brief `ir` listáján kívül esik, a DT23 (d) elfogadása előtt commitolva. A felhasználó dönt (DT23 (d)). Az E16 csak `[ELLENŐRZŐ]` előtagú PR-címmel zöld; a PR címe ezt viseli.
- **Nem ellenőrizhető az ellenőr szerepével, az orkesztrátor futtatta:** lásd alább.
- `python eszkozok/ellenoriz.py`: RENDBEN 11, SÉRTÉS 0, KÉZI 2, JELENTÉS 3; `python eszkozok/feladatok.py ellenoriz`: 50 brief, 0 hiba (orkesztrátor, head 87980ca).
