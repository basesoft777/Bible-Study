---
feladat: 89
cim: Licenc-rendezés — a projekt saját adata CC BY 4.0, táblaszintű licenc a pardes.db-ben (DT112, DT113)
kod: LICENC_RENDEZES
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: nem_indult
ad: LICENSE-DATA (saját adat CC BY 4.0, próza minden jog fenntartva); a licencek.tsv projekt_adat sora tisztazott, új sorok a karoli_strong/* és karoli_variancia számára, a projekt_adat-on múló sorok újraértékelve; a sqlite_epit.py SZARMAZTATOTT_LICENC cseréje és táblaszintű licenc (tabla_licenc), a méret újramérve (a #86 N-F86b bemenete)
kovetkezo: "M0 felmérés (csak olvas); ⛔ a próza-címke (D1) és a LICENSE-DATA szövege (D2) a felhasználónak"
olvas: [DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, eszkozok/sqlite_epit.py, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/igazolas_migracio.py, naplok/SQLITE_EPIT_meres.md, Rendszerfejlesztesi_playbook.md]
ir: [LICENSE-DATA, adat/licencek.tsv, adat/SEMA.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, naplok/SQLITE_EPIT_meres.md, NYITOTT_FELADATOK.md, eszkozok/lexikon_general.py, lexikon/]
fugg: [79]
---

# F89_LICENC_RENDEZES_BRIEF.md — a projekt saját adatának licence és a táblaszintű licenc

*FELADATOK #89 · Modell: sonnet · v1 · 2026.10.12 · a csonk-briefet váltja fel · döntés: DT112, DT113 · forrás: `NYITOTT_FELADATOK.md` N-F79a, `adat/licencek.tsv` (`projekt_adat`), `adat/SEMA.md` 2.19, `naplok/SQLITE_EPIT_meres.md`*

## 1. Cél

A felhasználó döntése (DT112): a projekt **saját adatrétege** (`adat/*.tsv`, `adat/karoli_strong/*`,
`adat/karoli_variancia.tsv`, a `pardes.db`) **CC BY 4.0** licenc alatt áll; a **próza**
(tanulmányok, lexikon, motívumcikkek) külön réteg, **minden jog fenntartva**; a repóba
`LICENSE-DATA` kerül. Ma a `licencek.tsv` `projekt_adat` sora `tisztazatlan` („a repó saját
licence nincs rögzítve”), és ez a sor tart `tisztazatlan`-ban több származtatott sort is. A
második döntés (DT113): a `pardes.db` a licencet **táblaszinten** tárolja, nem soronként (a
`licenc_*` oszlopok a mérés szerint kb. 250 MB-ot tesznek ki a 845 MB-ból).

A javaslattevő nem jogász; a kereskedelmi kiadás előtt a DT-M6 szerint jogász néz rá. Ez a
feladat a nem kereskedelmi első kiadás (DT-M6) alapját rakja le.

## 2. Hatókör

**Benne van**

- **`LICENSE-DATA`** a repó gyökerében: mire vonatkozik a CC BY 4.0 (a saját adatréteg
  fájlkörei név szerint), mire nem (a próza: minden jog fenntartva; harmadik fél adata: a
  `adat/licencek.tsv` saját sora szerint), a kötelező megjelölés szövege, a licenc hivatalos
  URL-je. A fájl rövid, jogi értelmezést nem tartalmaz.
- **`adat/licencek.tsv`:**
  - a `projekt_adat` sor: `licenc` = CC BY 4.0, `forras_hely` = `LICENSE-DATA` + DT112,
    `allapot` = `tisztazott`, `cimke` = `CC BY 4.0`, `kereskedelmi` = `igen`, `share_alike` =
    `nem`, a `megjegyzes`-ben a DT-F24 halasztás lezárása;
  - új sorok: `Karoli_Strong_parok`, `Karoli_Strong_szavak` (a `datasetek.tsv` azonosítói) és
    `karoli_variancia`; a licencük a forrásaikból (Károli 1908 közkincs, TAHOT/TAGNT CC BY 4.0,
    projekt-adat CC BY 4.0), a kötelező megjelölés a STEPBible-szöveggel;
  - újraértékelés: a `projekt_adat`-on múló `tisztazatlan` sorok (`Karoli_Strong_kivonat`,
    `LXX_versszintu_parok`, `Karoli_versmegfeleltetes`); ahol a többi összetevő igazolt, a sor
    `tisztazott` lesz, ahol nem, a sor marad, és a megjegyzés megnevezi, min múlik.
- **`adat/SEMA.md` 2.19:** a 3. szabály (a `projekt_adat` nyitott) helyére a DT112: a saját adat
  licencének forrása a jogtulajdonos döntése, a `LICENSE-DATA`-ban rögzítve (ez a `forras_hely`);
  a `cimke` szabály kivétele (`projekt-adat`) a próza-kérdés (M0 ⛔) szerint módosul.
- **`eszkozok/sqlite_epit.py`:**
  - a `SZARMAZTATOTT_LICENC` a fenti új sorokra mutat (`token_par`, `token_karoli`,
    `frazis_pozicio`, `karoli_variancia`);
  - **táblaszintű licenc (DT113):** egy `tabla_licenc(tabla, licenc_allapot, kereskedelmi,
    licenc_dataset, cimke)` tábla; a `licenc_allapot`, `kereskedelmi`, `licenc_dataset` oszlop
    kikerül a táblákból (az FTS `UNINDEXED` licenc-oszlopai is); a „legszigorúbb érték” szabály
    (DT109 (2c)) változatlan, csak a tárolás helye változik;
  - az F79 G6-ja átfogalmazva: minden épített táblának pontosan egy `tabla_licenc`-sora van;
    licencsor nélkül a tábla továbbra sem épül be.
- **`eszkozok/teszt_sqlite_epit.py`:** a licenc-tesztek a `tabla_licenc`-re.
- Teljes újraépítés és mérés a `naplok/SQLITE_EPIT_meres.md`-ben: méret előtte/utána, a
  `tabla_licenc` tartalma, a `tisztazatlan` táblák listája.
- `NYITOTT_FELADATOK.md`: az N-F79a lezárása a DT112-re hivatkozva.

**Feltételesen benne (az M0 ⛔ döntése szerint)**

- **A próza címkéje.** A `eszkozok/lexikon_general.py` ma a lexikon prózai blokkjaira
  (`tartalom`, `jelmagyarazat`; 338., 370. sor) a `projekt_adat` sor címkéjét teszi. Ha a
  `projekt_adat` címkéje `CC BY 4.0` lesz, a generált lexikon a prózát is CC BY 4.0-nak
  jelölné, ami ellentmond a DT112-nek. A javaslat: külön `projekt_proza` sor (minden jog
  fenntartva; új `cimke`-érték a SEMA 2.19 zárt készletében), a prózai blokkok erre a kulcsra
  váltanak, a lexikon a generátorral újragenerálódik (`python eszkozok/general.py --cel lexikon`).
  Ehhez az `eszkozok/lexikon_general.py` és a generált `lexikon/` is az `ir`-be kerül.

**Nincs benne**

- a jogi vélemény, a kereskedelmi kiadás és a #86 csomagja (csak a mérés a bemenete);
- a többi `tisztazatlan` harmadik fél sor (KJV, LXX_kivonat, lexikonok_nyers, …): nem a
  `projekt_adat`-on múlnak;
- a `.gitignore`, a `pardes.db` terjesztése (#76);
- a TIPNR (#88), a nem létező Károli-versek (DT114), a ki nem épített táblák (DT115).

## 3. Lépések

- **M0 — felmérés (csak olvas).** (1) Minden `licencek.tsv`-sor, amely a `projekt_adat`-on
  múlik (a `licenc` vagy a `megjegyzes` mezőben), és mi lenne az állapota a DT112 után; (2) minden
  kódhely, amely a `projekt_adat` kulcsot vagy a `licenc_*` oszlopokat olvassa (`grep`: generátorok,
  `lekerdez.py`, `ellenoriz.py`, CI); (3) a próza-címke kérdése a fenti javaslattal; (4) a
  `LICENSE-DATA` tervezete. ⛔ **A (1)–(4) a felhasználónak**: a próza-címke (külön sor vagy
  más megoldás) és a `LICENSE-DATA` szövege jóváhagyásra vár.
- **M1 — `LICENSE-DATA`, `licencek.tsv`, SEMA 2.19** (`F89.1:` …): a jóváhagyott szöveg; a TSV
  írása `split('\t')`/`'\t'.join()`, írás előtt soronkénti összevetés az eredetivel (minta:
  `eszkozok/igazolas_migracio.py`); csak a megnevezett sorok változnak.
- **M2 — a próza-címke** (ha az M0 ⛔ így dönt): `lexikon_general.py`, újragenerálás, a generált
  diff csak a címkesorokat érinti.
- **M3 — táblaszintű licenc az építőben**, kis mintán; tesztek.
- **M4 — teljes újraépítés és mérés.**
- **Zárás.** `fuggetlen-ellenor`; `python eszkozok/feladatok.py ellenoriz` 0; ha a lexikon
  újragenerálódott: `python eszkozok/general.py --cel lexikon --ellenoriz` 0; fejléc `lezarva`,
  `lezarva_osszegzes`; draft PR.

## 4. Elfogadási feltételek

- **G1** A `licencek.tsv` diffje csak a megnevezett sorokat érinti; a többi sor bájtra azonos
  (soronkénti összevetés a naplóban); a TSV-ket `csv` modul nem írja.
- **G2** A `projekt_adat` sor `tisztazott`, `forras_hely`-e a `LICENSE-DATA`-ra és a DT112-re
  mutat; az új sorok minden mezője kitöltött (a `kotelezo_megjeloles` szó szerint, ahol a forrás
  megad ilyet).
- **G3** A generált nézetekben a próza nem kap CC BY 4.0 jelölést (a lexikon-generátor futása
  és egy prózai blokk címkéje a naplóban); ha az M0 ⛔ másként dönt, az ott rögzített feltétel.
- **G4** A `pardes.db`-ben egyik táblának sincs `licenc_allapot`/`kereskedelmi`/`licenc_dataset`
  oszlopa; minden táblának pontosan egy `tabla_licenc`-sora van; a legszigorúbb-érték szabály
  teszttel igazolva (egy származtatott tábla a legszigorúbb forrása értékét kapja).
- **G5** A mért méret előtte/utána a `naplok/SQLITE_EPIT_meres.md`-ben, proveniencia-sorral;
  a `tisztazatlan` táblák listája név szerint.
- **G6** Az építés determinisztikus (két futás táblánkénti hash-e azonos); minden teszt zöld.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| DT112 | A projekt saját adatának licence | adat CC BY 4.0, próza minden jog fenntartva, `LICENSE-DATA` | eldöntve (felhasználó, 2026.10.12) |
| DT113 | Licenc soronként vagy táblánként | táblaszintű (`tabla_licenc`), a DT112-vel egy menetben | eldöntve (felhasználó, 2026.10.12) |
| D1 | A próza címkéje a generált lexikonban | külön `projekt_proza` sor, a prózai blokkok erre váltanak | javaslat (M0 ⛔) |
| D2 | A `LICENSE-DATA` szövege | rövid, fájlkörönként; jogi értelmezés nélkül | javaslat (M0 ⛔) |
