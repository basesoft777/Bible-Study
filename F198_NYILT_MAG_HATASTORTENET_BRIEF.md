---
feladat: 198
cim: A nyílt mag bővítése a hatástörténet (visszhang-réteg) adatával — a HAMART-001 1. kiadása előtt
kod: NYILT_MAG_HATASTORTENET
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ag: claude/brave-allen-7b2eb6
ad: négy új nyílt tábla (visszhang_megfelelok, visszhang_tanuk, vitatott_forrasok, sblgnt_apparatus) forrásonkénti licenccel, kódkönyvvel, angol párral, OLVASSEL/README-szakasszal és ellenőrző összeggel; a Chain Lineage-tanúk kiszűrve; a nyílt mag kapuja 0 BUKÁS, a lap érintetlen
kovetkezo: "Te: a draft PR áttekintése; a két nyitott licenc-kérdés (DT778, DT779) eldöntése; merge a HAMART-001 /kiadas-a előtt"
munka: folyamat
olvas: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/nyilt_mag_angol.py, adat/visszhang_megfelelok.tsv, adat/visszhang_tanuk.tsv, adat/vitatott_forrasok.tsv, adat/licencek.tsv, adat/nyilt_kodkonyv.tsv, adat/nyilt_angol.tsv, konkordancia/SBLGNT_apparatus.tsv]
ir: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py, adat/nyilt_kodkonyv.tsv, adat/nyilt_angol.tsv, nyilt_mag/, naplok/F198_jelentes.md, naplok/ELLENOR_F198.md, dontesek/uj/brave-allen-7b2eb6.md, nyitott/uj/brave-allen-7b2eb6.md, F198_NYILT_MAG_HATASTORTENET_BRIEF.md]
fugg: [162, 170, 176, 183, 191]
---

# F198_NYILT_MAG_HATASTORTENET_BRIEF.md — A nyílt mag és a hatástörténet

*FELADATOK #198 · Modell: sonnet · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, szó szerint).** A javaslat: „egy kis, külön PR a #183 merge-e után és a HAMART /kiadas-a előtt. Csak a nyílt mag exportálóját érinti, a lapot nem. Így az 1. kiadás nyílt magja már a hatástörténettel együtt megy ki. Rendben?” A válasz: „rendben”. A Chain Lineage-ről: „ez most így marad”, vagyis a Chain Lineage-tanú nem kerül be.

## Cél és hatókör

A #690-nel (#183) bekerült visszhang-adat (Targum, Vulgata, LXX-híd, az ÚSZ-apparátus, az egyházatyai és rabbinikus tanúk, a Glossa Ordinaria, a vitatott pontok szakirodalma) a nyílt magba is kerüljön, forrásonként a licenccel. **A lexikonlap nem változik** (E28 0), a generátor (`lexikon_general.py`) és a kinyerők (`eszkozok/visszhang/`) érintetlenek.

## Teendő

1. **Exportáló** (`nyilt_mag_export.py`): négy új tábla az `adat/` forrástáblákból, csak a **második kéz által ellenőrzött** sorokból (üres `ellenorzes`: nem exportálódik, mint a lapon sem): `visszhang_megfelelok.tsv` (`targum`, `vulgata`, `lxx`; a `bdb` kimarad, DT778), `visszhang_tanuk.tsv` (`hcf`, `sefaria`, `glossa`; a `chain_lineage` **kiszűrve**), `vitatott_forrasok.tsv` (csak bibliográfiai adat; az `osszefoglalo` nincs, DT779), `sblgnt_apparatus.tsv` (az apparátus-jegyzetek a motívumok igehelyeire).
2. **Licenc**: minden sor `forras_megnevezes` és `forras_licenc` oszlopot kap a `licencek.tsv` szerint; a `forrasok_es_licencek.tsv`-ben a használt források „forrás” szerepűek lesznek; az SBLGNT kötelező megjelölése és a Sefaria „CC BY” megnevezése az OLVASSEL/README-ben.
3. **Kódkönyv** (`adat/nyilt_kodkonyv.tsv`), **angol pár** (`adat/nyilt_angol.tsv`, a meglévő eszközzel), **OLVASSEL/README-bekezdés**, **ellenőrző összeg** (az export adja).
4. **Kapu** (`nyilt_mag_kapu.py`): az új fájlok kötelezők; a Chain Lineage-tanú **nem szerepelhet** (új ellenőrzés); a forrásonkénti arány-kapu a mai szabály szerint.
5. **Tesztek**, jelentés (`naplok/F198_jelentes.md`), egy független ellenőrzés, legfeljebb egy javítókör, draft PR.

## Garanciák

- G1: a diff csak a fenti `ir` fájlokat érinti.
- G2: a nyílt mag kapuja (E35) 0 BUKÁS; az olvasói kapu és E28 változatlanul 0.
- G3: a hiány nem tölthető ki; a hiány-sor (nincs lektorált forrás) kimondott hiány marad.
- G4: TSV-olvasás `split('\t')`; UTF-8 wrapper.
- ⛔ A merge a felhasználóé.
