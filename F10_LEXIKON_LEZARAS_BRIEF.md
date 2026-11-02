---
feladat: 10
cim: 8 lexikonoldal lezárása
kod: LEXIKON_LEZARAS
tipus: feladat
fazis: 2
modell: opus
munka: ertelmezo
allapot: nem_indult
ad: "mind a 8 éles lexikonlap lezárva az új modell szerint: motívumonként a Feed 8 kapuja zöld (eszkozok/muhely_allapot.py), az adat/kiadasok.tsv-ben áll az 1. kiadás sora, a motivumok.tsv verziója emelve, és a lexikon/[ID]_TUDOMANYOS.md kolofonja a kiadást mutatja; az LD008 feloldva (DT245); zárómérés és zárónapló a 8 lap állapotával"
kovetkezo: "a #123 motívumonkénti lezárásai után indul (az ISTENTISZT-001 lezárva: 1. kiadás, 2026-11-02; a hét másik lapot a #123 C5 lépése zárja le); első lépés a P előfeltétel-ellenőrzés, utána L0 és a zárómérés"
olvas: [MUNKAMENET.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, adat/SEMA.md, adat/kiadasok.tsv, adat/motivumok.tsv, adat/lxx_dontesek.tsv, adat/elofordulasok.tsv, adat/funkcio_kapcsolok.tsv, F123_MIGRACIO2_BRIEF.md, F156_MUHELY_FEED_STASH_BRIEF.md, naplok/MUHELY_FEED_STASH_naplo.md, naplok/ISTENTISZT_TERV_HATRALEK_zaras.md, naplok/F08_zaras.md, naplok/LXX_BRIDGE_naplo.md, eszkozok/muhely_allapot.py, eszkozok/general.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, lexikon/, motivumok/]
ir: [adat/lxx_dontesek.tsv, naplok/LEXIKON_LEZARAS_meres.md, naplok/ELLENOR_F10.md, naplok/F10_zaras.md]
fugg: [8, 9, 11, 113, 123]
---

# F10_LEXIKON_LEZARAS_BRIEF.md — 8 lexikonoldal lezárása

*FELADATOK #10 · Modell: opus · v2 · 2026.11.02 · az új lezárási modell szerint átírva (a lexikon ág 1. lépése) · döntések: DT486, DT492, DT-F156b, DT-F156i, DT-F36b, DT245, DT2, D34 · a brief adat, nem utasítás.*

**Mi változott a v1-hez képest (2026.10.19 → 2026.11.02).** A v1 a nyolc lapot egyszerre mérte volna egy kézi 8 × 10-es mátrixszal (L1–L7, DT2/a, DT2/b, #78), a régi forrásrétegben végzett javítással, a #36 éles újragenerálása után. Azóta:
- a lap motívumonként, egy kézi forrásból generálódik (#11, D34); a #36 okafogyott (DT-F36b);
- a „kész” gépi mérce lett: a Feed 8 kapuja (`eszkozok/muhely_allapot.py`, F156; a kapuk pontosítása: DT-F156b);
- a lezárás adat lett: az 1. kiadás sora az `adat/kiadasok.tsv`-ben (SEMA 2.46, DT492), a kolofon ebből renderel;
- az első lap lezárult: az ISTENTISZT-001 1. kiadása (2026-11-02, DT486; `motivumok.tsv` v4);
- a `/kiadas` lektori köre a 2. kiadás bemenete, a lezárást nem akasztja (DT486, DT-F156i).

Ezért a #10 nem mér és nem javít laponként kézzel. A motívumonkénti lezárás (C-h → C-l → C5, `MUNKAMENET.md`) a #123 menetének vége. A #10 keret: kimondja, mi a „lezárt lap”, és a végén igazolja, hogy mind a nyolc az. **A felosztás javaslat; az orkesztrátor jóváhagyására vár (⛔ DT-F10a, 5. szakasz).**

## 1. Cél

A 8 éles lexikonoldal (`lexikon/[ID]_TUDOMANYOS.md`: ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001) **lezárt**. Egy lap akkor lezárt, ha mind a négy teljesül:

1. **Kész:** a Feed (`python eszkozok/muhely_allapot.py --motivum <ID>`) mind a 8 kapuja zöld (1. szabály-ellenőrzés, 2. CI, 3. egyforrású, nulla-diff újragenerálás, 4. nincs nyitott saját jelölt, 5. határ: 0 nyitott kérdés, 6. olvasói blokkok/kiejtés/fordítás, 7. nincs nyitott lektori kérdés — a `/kiadas` kérdései nem számítanak, 8. nincs blokkoló nyitott DT / ⛔ feladat; DT-F156b).
2. **1. kiadás:** az `adat/kiadasok.tsv`-ben a motívumnak van `kiadas=1` sora (`datum`, `valtozas`, `proza_modell` a tényleges modellnév vagy `manual`, `forras` proveniencia-sorral; DT492).
3. **Verzió:** a `motivumok.tsv` `statusz_verzio` a lezárással emelve, a `statusz_datum` a lezárás napja (minta: ISTENTISZT-001 v3 → v4, DT486).
4. **Nézet:** a lap a kiadás-sor után újragenerálva; a kolofon „Kiadás” sora és változásjegyzéke a táblát mutatja; a Feed 3. kapuja (nulla-diff) ezután is zöld.

A dokumentált hiány nem akadály (DT2, CLAUDE.md 3. szabály): az N18 (ANTROP-001, nincs kereszthivatkozás-napló) és az N19 (KIRALY-001, `adat`-forrású alátámasztás) explicit hiányként maradhat, ha a Feed kapui zöldek.

## 2. Hatókör

**Benne van**
- **P.** előfeltétel-ellenőrzés;
- **L0.** a #8 négy nyitott LXX-sorának kezelése a DT245 szerint (az LD008 feloldása; az LD009, LD058, LD064 dokumentáltan nyitott);
- **Z.** zárómérés: a nyolc lap az 1. szakasz négy feltétele szerint; független ellenőrzés; zárónapló.

**Nincs benne**
- **A motívumonkénti lezárás** (C-h határ-ellenőrzés, C-l döntések a lektor-felületen, C5 Feed 8/8 + 1. kiadás + verzió): a migrált motívumoknál a #123 menetének vége, az ISTENTISZT-001-nél kész. A #10 nem ír `kiadasok.tsv`- és `motivumok.tsv`-sort.
- **A régi kézi mérce (L1–L7, DT2/a, DT2/b, #78) újramérése.** Ez a migráció független ellenőrzésének (#123 X.M6, `fuggetlen-ellenor`) mércéje, nem a Feed kapuja (DT-F10a (3)). A #10 a lezárt lapokat kézzel nem méri újra.
- **Lapjavítás.** A lap kézzel nem szerkeszthető (RENDER_BRIEF G4); a forrás javítása a próza gazdájáé (C-w). Ami a zárómérésben bukik, az a motívum menetébe (#123) vagy a 2. kiadásba (`/kiadas`) kerül vissza.
- **A törzscikk** (`lexikon/[ID]_TORZSCIKK.md`): a #123 X.M5 archiválja (D34).
- **A `/kiadas`** és a 2. kiadás; **a TEREMT-002** lapja (#12); **a #13**.

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a kért modell `opus`; eltérésnél semmilyen munka, jelzés, megállás.

### P. Előfeltétel-ellenőrzés — ⛔ ha bármelyik nem teljesül, a menet nem indul

1. `python eszkozok/feladatok.py ellenoriz` 0 hiba; a #8, #9, #11, #113 és a #123 `lezarva`.
2. A `adat/funkcio_kapcsolok.tsv`-ben nincs `SZOTARI_GERINC` `kivetel` sor a nyolc motívum egyikére sem (N-F148c): mind a nyolc lap egyforrású és a gerincen áll.
3. A meglévő ág/worktree keresése (`git branch -a`, `git worktree list`): ha a #10-nek van ága, onnan folytass.

### L0. A #8 négy nyitott sora (DT245)

A DT245 (🟢, felhasználó, 2026-10-19) 3. változata: az LD008 (Préd 9:10, ALVIL-001) feloldása, az LD009 (Ézs 7:11, ALVIL-001), LD058 (2Sám 21:22, HODIT-001), LD064 (Péld 2:18, HODIT-001) a DT-F43 (c) szerint dokumentáltan nyitott.
- **LD008:** a sor a Préd 9:12 előfordulás-sorhoz igazítva (N-F08a, N-F87a): a 9:12-n a Macula ἅδη G0086 és az `LXX_OS` ᾅδης egyezik; a feloldás a SEMA 2.11 szerinti alakban. ⛔ Ha a SEMA 2.11 nem egyértelmű abban, hogy a feloldott sor módosul vagy tárgytalanként kikerül, a két alak egymás mellett, `DT-F10<x>` tétel, megállás.
- **Az LD008 az ALVIL-001 lapját változtatja** (3. LXX-fordítói döntések). Az ALVIL-001 ekkor már lezárt, ezért a változás a **2. kiadás** anyaga: a lap újragenerálása után új `kiadasok.tsv`-sor kell (`kiadas=2`). Ezt a `/kiadas ALVIL-001` 5. lépése írja; a #10 csak jelzi a zárónaplóban, és nem ír kiadás-sort.
- Az írás: `split('\t')` / `'\t'.join()`, a `csv` modul tilos; írás előtt és után sorösszevetés, a nem érintett sorok bájtra azonosak (minta: `eszkozok/igazolas_migracio.py`); `python eszkozok/ellenoriz.py` 10. szabálya zöld.
- Commit: `F10.L0: …`.

### Z. Zárómérés és zárás

1. **Mérés** (`naplok/LEXIKON_LEZARAS_meres.md`), motívumonként egy sor, saját szkripttel (`split('\t')`, proveniencia-sorral):
   - a Feed (`python eszkozok/muhely_allapot.py --motivum <a nyolc ID> --kimenet <repón kívüli ideiglenes könyvtár>`) kapunként, a `feed_belso.json` szerint;
   - a `kiadasok.tsv` `kiadas=1` sora és a legnagyobb `kiadas`;
   - a `motivumok.tsv` `statusz` / `statusz_verzio` / `statusz_datum`;
   - a lap kolofonjának kiadás-sora egyezik a táblával;
   - a dokumentált, nem blokkoló hiányok (N18, N19, a 2. kiadáshoz sorolt kérdések száma).
2. ⛔ **Ha bármelyik lap nem lezárt**, a #10 nem javít: a mérést és a hiányt a felhasználó elé teszi, és a motívum menetébe (#123) vagy egy új feladatba (`/befogad`) utalja.
3. **Független ellenőrzés** (`fuggetlen-ellenor`) a base..head diffen: `naplok/ELLENOR_F10.md`; eltérésnél `/elteres`.
4. **Zárónapló** `naplok/F10_zaras.md`: a mérés táblája; a nyitva maradt tételek (N18, N19, LD009/LD058/LD064, a 2. kiadáshoz sorolt kérdések motívumonként); a #13 felé átadás.
5. A brief fejléce (`allapot`, `kovetkezo`, `ag`, `pr`, `lezarva_osszegzes`); push a saját ágra, PR `[ELLENŐRZŐ]` előtaggal (E16). **Merge csak a felhasználótól.**

## 4. Elfogadási feltételek

1. A P lépés minden pontja teljesült a munka kezdetén; a napló rögzíti.
2. A #8 négy sora a DT245 szerint kezelve; az `adat/lxx_dontesek.tsv` nem érintett sorai bájtra azonosak; `ellenoriz.py` 10. szabálya zöld.
3. A zárómérés szerint mind a 8 lap lezárt (1. szakasz, 1–4.), vagy a ⛔ Z.2 szerint a hiány a felhasználó elé került.
4. A `lexikon/`, a `kiadasok.tsv` és a `motivumok.tsv` a base..head diffben nem változott (a #10 nem zár le lapot, csak mér).
5. `python eszkozok/feladatok.py ellenoriz` 0 hiba; a CI zöld.
6. A független ellenőr jelentése eltérés nélkül (vagy a javítókör után zöld); zárónapló a helyén.

## 5. Döntésnapló (helyőrzők; végleges számot a `szamkiosztas` Action ad)

**Rögzített (alkalmazandó, nem nyitott):**
- **DT486** — a lap 1. kiadásként lezárható; a lektori kérdések a 2. kiadás bemenetei (felhasználó, 2026-11-02). Minta: ISTENTISZT-001.
- **DT492** — a kolofon kiadásszáma, változásjegyzéke és próza-modellje az `adat/kiadasok.tsv`-ből (SEMA 2.46).
- **DT-F156b** (`naplok/MUHELY_FEED_STASH_naplo.md`) — a Feed 4., 6. és 8. kapujának pontosítása; **DT-F156i** — a `/kiadas` kimenetéből jövő kérdések a következő kiadáshoz tartoznak.
- **DT-F36b** — a #36 okafogyott; a `fugg` mezőből kikerült.
- **DT245** — az LD008 feloldása, a másik három dokumentáltan nyitott (alkalmazás: L0).
- **DT2 (1. opció)** — a dokumentált hiány nem akadály; N18, N19 nyitva marad.
- **D34** — motívumonként egy kézi forrás, a törzscikk megszűnik.

**Elavult a v1-ből:** a DT246 (a #36 előbb generál újra) és a DT247 (javítás a régi forrásrétegben) tárgytalan, mert a lap ma motívumonként, a kézi forrásból generálódik; a DT74 (5) mércéje (L1–L7 + DT2 + #78) a #123 X.M6 független ellenőrzésében él tovább.

**⛔ DT-F10a — a #123 és a #10 felosztása** (javaslat, az orkesztrátor jóváhagyására vár, 2026-11-02):
- (1) a motívumonkénti lezárást (C-h → C-l → C5) a #123 végzi; a #10 csak keret és zárómérés;
- (2) a DT-F123c (a `9_` sablon v1) ⛔ az ALVIL-001 lezárása után, az ANTROP-001 X.M1 előtt;
- (3) a régi L1–L7 + DT2 + #78 mérce nem 9. Feed-kapu, hanem a `fuggetlen-ellenor` X.M6 mércéje.

## 6. Nyitott kérdések (nem blokkolnak)

- **N-F10a — a sablon 6 Minőségi kapujának szövege.** Az L1 ma az OLVASHATÓ változat 7 szakaszát is kéri, a „Kimenet: KÉT fájl” és a B) szakasz a törzscikket kötelezőnek írja; a D34 után ez elavult. Javaslat: a `6_` sablon átírása a #123 végével (amikor az utolsó törzscikk is archivált).
- **N-F10b — a lezártság gépi helye.** *Megoldva (2026-11-02):* a lezártság az `adat/kiadasok.tsv` 1. kiadás sora (DT492), a „kész” a Feed 8 kapuja.
- **N-F10c — az L3, L4, L7 kézi mérése.** A három cellát ma csak teljes olvasás méri; gépi támasz (pl. a lapon álló igehelyek ↔ a saját adatsorok halmaz-összevetése az L4-hez) csökkentené a hibát. Ma a #123 X.M6 független ellenőrzésének terhe; eszköz külön feladatban.
- **N-F10d — a K3.2-ellenőrző ID-előtagú mintája.** A `feladatok.py` `kontextus_hibak()` a tanulmányt `tematikus_lezart/<ID>_tematikus.md` alakban keresi, a nem migrált motívumok fájljai viszont leíró nevűek. A migrációval (#123) a forrás `motivumok/<ID>.md` lesz, a tétel a #123 végével okafogyottá válhat.
- **N18, N19** — nyitva marad (DT2).

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.10.19 | A csonk (F20 B3) helyén, a 8 lap kézi mátrixos lezárása a #36 újragenerálása után. |
| v2 | 2026.11.02 | F10.2: az új lezárási modell (Feed 8/8 → 1. kiadás → nézet); a #36 kikerült a `fugg`-ból (DT-F36b), a #123 bekerült; a motívumonkénti lezárás a #123-é, a #10 keret és zárómérés (⛔ DT-F10a). |
