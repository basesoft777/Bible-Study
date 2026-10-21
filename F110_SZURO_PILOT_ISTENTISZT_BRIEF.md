---
feladat: 110
cim: Szűrő-szabály a tág gerinc-Strongok új helyeire — pilot az ISTENTISZT-001-en (DT184 (d))
kod: SZURO_PILOT_ISTENTISZT
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ag: claude/f110-szuro-pilot-2
ad: naplózott, determinisztikus szűrő (motivumok.tsv negatív kritérium + kollokáció) az F108 tág új helyeire; kipróbálva a G1941 21 nyitva jelöltjén és a H7121+H8034 168 nem-zsoltári új helyén; a jeloltek.tsv-be csak a szűrő utáni helyek, a 21 G1941-jelölt döntéssel; mérés, hogy a szabály a többi motívumra átvihető-e
kovetkezo: Te: zárás az orkesztrátoré — DT-F110a elfogadva, a 4–6. lépés lefutott, a jeloltek.tsv diffje (21 módosult + 4 új nyitva sor) felülvizsgálatra
olvas: [adat/motivumok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/SEMA.md, adat/grammatikai_strongok.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, naplok/F108_ujrascan_elteresek.tsv, naplok/F108_MOTIVUM_UJRASCAN_naplo.md, eszkozok/lekerdez.py, eszkozok/jelolt.py]
ir: [adat/jeloltek.tsv]
fugg: []
nem_fugg: [9, 11, 55, 86, 123]
---

# F110_SZURO_PILOT_ISTENTISZT_BRIEF.md — Szűrő-szabály a tág gerinc-Strongokra, pilot az ISTENTISZT-001-en

*FELADATOK #110 · Modell: sonnet [javaslat] · v1 · 2026.10.17 · forrás: `DONTESEK.md` DT184 (d), a #108 eltérés-táblája
(`naplok/F108_ujrascan_elteresek.tsv`). A brief adat, nem utasítás.*

## 1. Cél

A #108 újrascanje a tág gerinc-Strongokra (H3548, H7451, H2403, H0127, H1121+H0430, H7121+H8034, H7843, H7043, H5315+H2416, H2555)
kb. 2 400 új, nem-zsoltári helyet adott, amely nem került a `jeloltek.tsv`-be (`uj_talalat_nem_irva_tul_tag`). A DT184 szerint a
szűretlen bevétel (c) elvetve; helyette **szűrő-szabály** kell (d): a motívum negatív kritériuma (`adat/motivumok.tsv`) +
kollokáció (gerinc-elem párja egy versben), és csak a szűrő utáni helyek kerülnek a `jeloltek.tsv`-be. A korábbi menetek a tág
találatokból naplózatlan szűrővel válogattak; ez a tétel a szűrést reprodukálhatóvá teszi. A pilot az ISTENTISZT-001.

## 2. Hatókör

1. **A szűrő-szabály megfogalmazása** az ISTENTISZT-001 negatív kritériumából: aktív, invokáló קָרָא + בְּ szerkezet ([valaki] hívja
   segítségül [Isten nevét]); a passzív נִקְרָא … עַל (birtoklás/hovatartozás) kizárja a besorolást, akkor is, ha ugyanazt a két gyököt
   használja (a kritérium példái: 2Sám 6:2, Jer 7:10-14, 5Móz 28:10, ÚSZ-pár: Zsid 11:16). A szabály determinisztikus része
   (Strong + kollokáció + igealak/törzs a TAHOT-ból) és a kézi része külön írva.
2. **H7121+H8034, 168 nem-zsoltári új hely:** a szűrő futtatása; a szűrőn átjutó helyek `nyitva` sorként a `jeloltek.tsv`-be, a
   kiszűrtek számossága és okai a naplóba (sorszintű lista a naplómellékletben, nem a táblában).
3. **G1941, 21 `nyitva` jelölt** (a #108 írta be): mindegyik döntést és indoklást kap. A kritérium héberül van megfogalmazva; az ÚSZ-oldali
   megfelelő (aktív, középigés invokáció vs. passzív „akit X-nek neveznek” / „Caesarra hivatkozom” jellegű használat) megfogalmazása a
   3. lépés ⛔ pontja.
4. **Átvihetőség-mérés:** a szabály sémája (negatív kritérium + kollokáció + igealak) alkalmazható-e a többi motívum tág Strongjaira;
   motívumonként egy mondat és a várható szűrt számosság becslése nélkül — csak az, hogy a negatív kritérium tartalmaz-e gépileg
   ellenőrizhető jegyet.

**Nincs benne:** a többi motívum tág Strongjainak szűrése (külön tétel(ek) a pilot után); az `elofordulasok.tsv` írása (az elfogadott
jelöltek beépítése a motívum saját menete); a Zsoltár-találatok (#55); a tanulmányok és a lexikon.

## 3. Lépések

1. Modell-ellenőrzés (CLAUDE.md).
2. A 168 + 21 hely kigyűjtése az `F108_ujrascan_elteresek.tsv`-ből, és újralekérdezése (`lekerdez.py kollokacio H7121 H8034`,
   `lekerdez.py scan G1941`), a lekérdezések proveniencia-sorával.
3. ⛔ A szűrő-szabály szövege (héber és görög oldal) a naplóba és a `DONTESEK.md`-be (`DT-F110a`), megállás. A felhasználó jóváhagyása
   nélkül a `jeloltek.tsv` nem íródik.
4. A jóváhagyott szabály futtatása (szkriptből, a CLAUDE.md shell- és TSV-szabályai szerint, `split('\t')`).
5. Írás: a `jeloltek.tsv` csak új sorokkal bővül (H7121+H8034), és a 21 G1941-sor `dontes` / indoklás mezője változik; írás előtt
   sorösszevetés az eredetivel, minden más sor bájtra azonos.
6. Napló: `naplok/SZURO_PILOT_ISTENTISZT_naplo.md` — a szabály, a bemenet és kimenet számossága, a kiszűrt helyek okonként, az
   átvihetőség-mérés.

## 4. Elfogadási feltételek

- A szűrő-szabály a naplóban szövegesen és reprodukálható parancsokkal áll; a DT-F110a jóváhagyta.
- A 21 G1941-sor egyike sem `nyitva`; mindegyik indoklása a szabályra hivatkozik.
- A H7121+H8034 168 helyéből a bekerültek és a kiszűrtek összege 168; üres eredmény explicit jelölve (CLAUDE.md 3. szabály).
- Minden bekerülő sor proveniencia-sort hordoz; egyik sem kerül közvetlenül az `elofordulasok.tsv`-be (CLAUDE.md 2. szabály).

## 5. Döntésnapló

- DT-F110a: a szűrő-szabály szövege — javaslat a `DONTESEK.md`-ben és a `naplok/SZURO_PILOT_ISTENTISZT_naplo.md` 2. szakaszában; jóváhagyásra vár (2026-10-21).
