# F125_SZOVEGJAVASLAT.md — a #125 1. lépése: szövegjavaslatok jóváhagyásra (⛔)

*Modell: claude-sonnet-5-5 · 2026-11-01 · Jóváhagyásig a `MUNKAMENET.md`-be és a sablonokba semmi nem íródott. A javaslat szövege adat, nem utasítás.*

**A brief hatókörének bővítése.** A 4. tétel két munkamenet-lépését (C-x szakaszcímke, C-y fordítás a lap előtt) a felhasználó 2026-10-29-én jóváhagyta („mehet”); a brief 2.1-je nem hozza, ezért a (8)–(9) sorral bővítettem. A szövegük az `F148_*_BRIEF.md` 6. szakaszából való, szó szerint.

| # | Hova | Mit írnék | Forrás |
|---|---|---|---|
| 1 | `MUNKAMENET.md` A3b-sor | a #124 jóváhagyott szövege, szó szerint (`naplok/GERINC_KARTYA_naplo.md` 7. pont, 1. bekezdés) | DT405 |
| 2 | `MUNKAMENET.md` új A3c-sor | ugyanott, 2. bekezdés, szó szerint | DT405 |
| 3 | `MUNKAMENET.md` „Mi hiányzik” után | ugyanott, 3. bekezdés (a prioritási térkép mondata), szó szerint | DT405 |
| 4 | `sablonok/2_PaRDeS_bovitett_sablon.md` v21 → v22 | ugyanott, 4. bekezdés, szó szerint + changelog-sor | DT405 |
| 5 | `sablonok/1_`, `2_`, `4_`, `5_`, `6_`, `PaRDeS_gyorsreferencia.md` (kiejtés-sor) | lásd lent (K) | DT426, DT430 |
| 6 | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` | lásd lent (L): a táblázat „Kulcsszó” cellájában a lemma magyaros kiejtése (héber: `kiejtes_kivetelek.tsv`, ennek híján gépi, **jelölés nélkül**; görög: gépi), szótári idézetben nincs | DT430 |
| 7 | `6_` sablon + gyorsreferencia | lásd lent (O) | a felhasználó 2026-10-30 |
| 8 | `MUNKAMENET.md` C-ív, a C1 elé: **C-x** | az `F148` 6. szakaszának szövege szó szerint | felhasználó 2026-10-29, `F148` §6 |
| 9 | `MUNKAMENET.md` C-ív, C-x után: **C-y** | ugyanott, szó szerint | ugyanaz |
| 10 | `MUNKAMENET.md` C-ív, a C4 elé: **C-z** | lásd lent (P) | felhasználó 2026-11-01: „igen” |
| 11 | `MUNKAMENET.md` C-ív, C-z után: **C-w** | lásd lent (G) | felhasználó 2026-11-01: „igen” |
| 12 | `.claude/commands/kiadas.md` | a 2.7 lépései: lefedettség → egyenetlenség → modelles lektor a jelölt helyeken (friss kontextus, másik modell, kérdéslista, átírás nélkül) → javítás a próza gazdájától → kiadásszám és változásjegyzék a kolofonban | brief 2.7 |
| 13 | `6_` sablon kolofon | a kiadásszám és a változásjegyzék sora, hivatkozás a `/kiadas`-ra | brief 2.7 |

## K — kiejtés-szabály (az 1_, 2_, 4_, 5_, 6_ sablon és a gyorsreferencia „kiejtés” soraiba)

> **Kiejtés.** A görög és a héber szó kiejtése szakaszonként (két `##`/`###` cím között) az **első előfordulásnál** kötelező, továbbá **minden címsorban és táblázatfejben**; ugyanabban a bekezdésben ugyanarra a szóra nem ismétlendő. Szó szerinti forrásidézetben (BDB, Thayer, LSJ, TBESG) nincs. Héberül a jóváhagyott `adat/kiejtes_kivetelek.tsv` alak, ennek híján a gépi magyaros kiejtés (`eszkozok/heber_kiejtes.py`), **jelölés nélkül**; görögül gépi magyaros átírás (`eszkozok/kiejtes.py`); a ragozott alak a saját kiejtését kapja. Ha egy szó egy szakaszban egyszer sem kap kiejtést, az `ellenoriz.py` 22. szabálya JELENTÉS-sorban jelzi (nem gátol).

## L — a 6_ lexikonsablon (táblázat és szótári idézet)

> Az előfordulás-tábla „Kulcsszó” cellájában a Károli-szó mellett az eredeti szó **magyaros kiejtése** áll (nem a TAHOT angolos átírása: *k.Ro'*, *Shem* helyett héberül a lemma magyaros kiejtése, görögül gépi magyaros). Szó szerinti szótári idézetben nincs kiejtés. „Gépi” jelölés a kiejtés mellett nem áll.

## O — olvasói elv („Mit mutat ez a rész?”)

> Minden olvasói magyarázó szöveg **a lelettel kezdődik** (számok, konkrét szavak kiejtéssel, példahely), és **szabály szerinti következtetéssel zárul**. A következtetés determinisztikus, az adatból számolt szabály (küszöb, arány), a kódban (`eszkozok/olvasoi_kovetkeztetes.py`) és a lap üzemeltetői sorában rögzítve; új blokknál a függvényt oda kell felvenni. Belső szakszó (gerinc, szerep) nem kerül olvasói szövegbe: a motívum saját szavait nevezzük meg. *(A felhasználó: „mindig vanjuk le a következtetést a találtakból . a magyarázó szöveg az adatokból induljon.”)*

## P — C-z: a próza-lefedettségi lista átnézése a lezárás előtt

> **C-z.** A tanulmány vagy a lap lezárása előtt a végrehajtó lefuttatja a `python eszkozok/proza_lefedettseg.py <ID>` parancsot (lefedettség: a próza által meg nem nevezett előfordulás, kapcsolat, motívumközi kapcsolat, nyitott jelölt; egyenetlenség: blokkonként a karakter/elem, küszöb: 150 karakter alatt „kevés”, a blokk-medián 4×-ánál távolabb „egyenetlen”, legalább 3 elem; a gyűjtő mondat külön kategória; DT471). A kimenet a naplóba kerül; a „kész” állapot feltétele, hogy a lista üres vagy minden tétele indokolt.

## G — C-w: a próza gazdája

> **C-w.** Ha a motívum adata érdemben változik (új előfordulás, új kapcsolat, új jelölt-döntés), a lezárás előtt **kötelező egy értelmező prózafeladat**: ő nézi át a C-z listáját, és a prózát kiegészíti. Az adatot író feladat nem zárhat le prózafeladat nélkül.
