---
feladat: 143
cim: A KIRALY-001 lexikonoldalainak újragenerálása a G0813 → G0540 javítás után (N-F132a)
kod: KIRALY_LEXIKON_UJRAGEN
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: a lexikon/KIRALY-001_TUDOMANYOS.md és _TORZSCIKK.md a javított Strong-mezővel (G5010+G0540+G0282) újragenerálva, a G0813 (ἄτακτος) nélkül; a diff mérve és indokolva; az N-F132a lezárva
kovetkezo: "Te: /kovetkezo — M0: szárazfutás a repón kívülre, ⛔ az éles írás előtt"
olvas: [adat/elofordulasok.tsv, adat/forditasok.tsv, adat/res_forras.tsv, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/torzscikk_general.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, tematikus_lezart/Melkizedek_tematikus.md, tematikus_lezart/naplok/Melkizedek_tematikus_kereszthivatkozas_naplo.md, "tematikus_lezart/KIRALY-001*", "tematikus_lezart/naplok/KIRALY-001*", RENDER_BRIEF.md, F36_LEXIKON_UJRAGEN_BRIEF.md, F132_THAYER_SZAKASZ_BRIEF.md]
ir: [lexikon/KIRALY-001_TUDOMANYOS.md, lexikon/KIRALY-001_TORZSCIKK.md]
fugg: []
nem_fugg: [27, 38, 123, 131]
---

# Fnn_KIRALY_LEXIKON_UJRAGEN_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

*FELADATOK #nn · Modell: sonnet · v0 (tervezet) · 2026.10.25 · készítette: a #132 javítókörének orkesztrátora a felhasználó kérésére
(„A”, chat, 2026-10-25); befogadás: `/befogad`, a felhasználó jóváhagyásával.*

## 1. Cél

Az N-F132a (`NYITOTT_FELADATOK.md`) lezárása. Az F132.19 (DT-F132l (a)) az `adat/elofordulasok.tsv` KIRALY-001 / Zsid 7:1-28
sorában a `G5010+G0813+G0282` Strong-mezőt `G5010+G0540+G0282`-re javította. A G0813 (ἄτακτος) a Zsid 7:1-28-ban nem fordul elő,
egyetlen helye az 1Thessz 5:14; a Zsid 7:3 *ἀπάτωρ* szava a G0540. A generált nézet (`lexikon/KIRALY-001_TUDOMANYOS.md`,
`_TORZSCIKK.md`) ma is a régi mezőt és egy „G0813 — ἄτακτος” alszakaszt mutat, vagyis a kanonikus adat és a nézet elvált
(CLAUDE.md: a kimenet kézzel nem szerkeszthető, a forrás javul, és újragenerálódik).

Mért állapot (`naplok/ELLENOR_F132_3.md`, a #132 záró újraellenőrzése; a futáskor újramérendő):

- `KIRALY-001_TORZSCIKK.md`: G0813 a 16., 203., 204. és 314. sorban; G0540 csak kulcsszóként (202. sor).
- `KIRALY-001_TUDOMANYOS.md`: G0813 a 78. sorban (a `strong` mező és az UBS-érték) és a 204. sorban (`### G0813 — ἄτακτος`).
- G0540 alszakasz egyik oldalon sincs; hogy az újragenerálás létrehozza-e, a futás mutatja meg.
- Az E28 csak az ISTENTISZT-001-et nézi (`eszkozok/ellenorzes/e28_migralt_nezetek.tsv`), ezért a CI ezt az elválást nem jelzi.

## 2. Hatókör

**Benne van:** a két KIRALY-001 lexikonoldal újragenerálása a meglévő generátorral (`eszkozok/general.py --cel lexikon` és
`--cel torzscikk`, `--id KIRALY-001`); szárazfutás, diffmérés, éles írás a ⛔ jóváhagyás után; az N-F132a lezárása.

**Nincs benne:** más motívum lexikonoldala; a generátor vagy bármely adattábla módosítása; a G0540 szótári tartalmának
(fordítás, Thayer-szakasz) pótlása — ha a G0540-nek nincs fordítása, az hiányként a naplóba kerül, nem tölti ki semmi
(CLAUDE.md 3. szabály); a #36 (a teljes `lexikon/` újragenerálása).

**Nyitott kérdés a befogadáskor / M0-ban:** a #36 `kovetkezo` mezője szerint az éles lexikon újragenerálása a DT74 (3) alapján
„befagyasztva a #11 1. lépcsőjéig”. Ha a szárazfutás diffje a G0813/G0540 sorokon túl is változást mutat (a generátor vagy a
többi adat drift-je), az éles írás a DT74 (3) hatálya alá eshet: ezt az M0 ⛔ pontja dönti el, a felhasználó.

## 3. Lépések (⛔ a kötelező megállások)

0. **Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév vs. `modell: sonnet`; eltérésnél nincs munka.
1. **M0 — szárazfutás a repón kívülre** (`--kimenet <scratchpad>/…`, `--ir` nélkül; CLAUDE.md: a `--kimenet` próbák ideiglenes
   könyvtárba, a repón kívülre): `general.py --cel lexikon --id KIRALY-001` és `--cel torzscikk --id KIRALY-001`, majd `diff` az
   éles fájlokkal. A naplóba: a változott sorok száma és osztályozása — (i) a G0813 → G0540 javításból eredő; (ii) egyéb
   (drift). Proveniencia-sorral.
2. **⛔ Döntés** (`DONTESEK.md`, helyőrző `DT-F<nn>`): ha csak (i) változik → javaslat: éles írás; ha (ii) is van → opciók:
   (a) éles írás mindennel együtt (DT74 (3) alóli kivétel); (b) a feladat megáll, az N-F132a a #36-ba / #11-be olvad; (c) más.
   A döntés a felhasználóé.
3. **Éles írás** a döntés szerint (`--ir`), utána `general.py --cel lexikon --id KIRALY-001 --ellenoriz` nem jelez.
4. **Mz:** Grep `G0813` a `lexikon/KIRALY-001_*` fájlokon → 0; a G0540 megjelenése (alszakasz vagy hiányjelölés) a naplóba;
   `git diff --stat` csak a két `ir`-fájlt mutatja; `python eszkozok/ellenoriz.py` SÉRTÉS 0; `python eszkozok/feladatok.py ellenoriz`
   0 hiba; az N-F132a a `NYITOTT_FELADATOK.md` Lezárva szakaszába.

## 4. Elfogadási feltételek

1. A két KIRALY-001 lexikonoldalon a G0813 nem szerepel; a Strong-mező `G5010+G0540+G0282`.
2. A diff minden sora osztályozva ((i)/(ii)), és a (ii) sorok a ⛔ döntés szerint kerültek (vagy nem kerültek) élesbe.
3. Más fájl nem változott (a közös koordinációs fájlok és a saját napló kivételével, `BRIEF_SABLON.md`).
4. Hiány explicit (pl. a G0540 fordításának hiánya), nem kitöltve.

## 5. Döntésnapló

| Azonosító | Kérdés | Állapot |
|---|---|---|
| DT-F132l | a G0813 → G0540 csere | eldöntve: (a) (felhasználó, 2026-10-25) |
| (M0 ⛔) | az éles írás és a DT74 (3) | nyitott |
