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

---

# 3. kör (csak az F8.8 commit, 3965bc2) — eredmény: ELTÉRÉS 6 tétel

*A `fuggetlen-ellenor` jelentésének összefoglalója; az orkesztrátor mentette.*

**Rendben:** a 4 átsorolt sor (LD027, LD035, LD050, LD052) `valoszinu`, a Strong és a pozíció a `konkordancia/LXX_OS`-sel egyezik, a proveniencia `dontes=DT23(b)`-t tartalmaz; a nyitott sorok LD008, LD009, LD058, LD064; darabszám 61 / 13 / 4 / 8 (86 sor); az LD001–LD004 változatlan (csak az üres `bizonyossag` mező); az N-F08a és N-F08b megvan és helyes; a H7497/H7498 átfogalmazás a 6 soron helyes (TAHOT: 2Sám 21:16/18/20/22, 1Krón 20:4/6/8 → H7497), az 1Krón 8 nincs a 87 helyben; nincs adatcsökkenés.

**Eltérések:**
1. **(1f)** az LD027, LD035, LD052 `valoszinu`, de a SEMA 2.11 és a brief szerint a `valoszinu` „egy forrás, ellentmondás nélkül”; a források ellentmondanak.
2. **(1g)** a 3 sor `forras=` mezőjéből kikerült a `Macula_heber`.
3. **(4b)** a DT23 idézetében szerepel a „(nulla-diff vagy CI igazolja)” zárójel.
4. a `f08_nulladiff.py` soronként hasonlít, de a dokumentumok „bájtra azonos”-t állítanak.
5. elavult „a DT23 döntéséig” szöveg a SEMA 2.11-ben és a `lexikon_general.py`-ban.
6. hiányzó `stderr`-őr a `f08_dt_dontes.py`-ban és a `f08_nulladiff.py`-ban, használatlan `S = None`.

# 4. kör (de1bbd0 merge + e2745d2 F8.10) — eredmény: ELTÉRÉS 4 tétel

**A 3. kör 6 tételének feloldása:**

| # | tétel | állapot |
|---|---|---|
| 1 (1f) | `valoszinu` + SEMA 2.11 definíció | feloldva, OK (a SEMA „vagy ellentmondásos források, felhasználói döntéssel feloldva (`feloldas=` kötelező)”); a brief-eltérést l. a 4. kör 1. tételét |
| 2 (1g) | `forras=` Macula + LXX_OS, `feloldas=DT23` | feloldva, OK (LD027, LD035, LD052) |
| 3 (4b) | a DT23 idézet zárójeles része | feloldva, OK (marad, kiegészítve: „teljesült: nulladiff a main-nel összefésülve, `naplok/F08_nulladiff.txt`”) |
| 4 | „bájtra” → „soronként azonos” | feloldva, OK (zárás, DT23, brief, `F08_nulladiff.txt`, `f08_nulladiff.py`) |
| 5 | elavult „a DT23 döntéséig” | feloldva, OK (SEMA 2.11, `lexikon_general.py`) |
| 6 | `stderr`-őr, `S = None` | feloldva, OK |

A merge (de1bbd0) csak a `DONTESEK.md` konfliktusát oldotta fel, a DT19 és a DT23 is megmaradt. A 10. szabály új ága statikusan nem ad téves SÉRTÉST (a 13 `valoszinu` sorból csak az LD027/LD035/LD052 forrása tartalmaz Macula + LXX_OS-t). Az `lxx_dontesek.tsv` diffje az e2745d2-ben pontosan 3 sor, az LD001–LD004 és a 90 adatsor változatlan. A `F08_nulladiff.txt` a merge-elt állapotot mutatja (172 diff-sor; ISTENTISZT-001_TUDOMANYOS −0/+0; 8 törzscikk −0/+0).

**Új eltérések és feloldásuk (a felhasználó jóváhagyásával, F8.11, 5a82d7f):**
1. *(közepes)* a SEMA `valoszinu`-bővítése eltért a brief 3. lépésétől (ott az ellentmondás `nyitott`) → a brief 3. lépése a SEMA-hoz igazítva (v2): ellentmondó források felhasználói döntés nélkül `nyitott`, döntéssel (`feloldas=` kitöltve) `valoszinu`; a döntésnapló F08-3 sora és a DT23 (b) mondata igazodik.
2. *(alacsony)* az F10 csonk-brief törzsének „Következő lépés” sora a régi szöveg maradt → szó szerint egyezik a fejléc `kovetkezo` mezőjével.
3. *(alacsony)* az F08 brief „merge-re kész (ellenőrizve)” jelölése a 4. kör előtt került be → utólag nem átírva; a `naplok/F08_zaras.md` egy mondatban rögzíti, hogy a jelölés a 4. kör előtt került be, és a 4. kör igazolta.
4. *(alacsony)* a SEMA az LD050 forrását „csak LXX_OS”-nek írta → pontosítva: a két független forrás közül csak az LXX_OS, LD050: LXX_OS + Karoli_versmegfeleltetes.

**Megjegyzés (nem eltérés, kezelve):** a `f08_dt_sor.py` újrafuttatása felülírta volna a DT23 döntését → az F8.11 őrt tett bele (DT23 sor esetén 2-es kilépési kód, nem ír), a fejlécben „egyszeri, DT23 után letiltva”.

**Nem ellenőrizhető az ellenőr szerepével:** `ellenoriz.py`, `feladatok.py ellenoriz`, generátor-futás, Macula-lekérdezés, CI-jelentés (a CI mindkét check SUCCESS volt az e2745d2-n).
