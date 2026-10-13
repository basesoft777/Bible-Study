---
feladat: 89
cim: Licenc-rendezés — a projekt saját adata minden jog fenntartva, táblaszintű licenc a pardes.db-ben (DT116, DT113)
kod: LICENC_RENDEZES
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: dontesre_var
ag: claude/f89-licenc-rendezes
ad: jogfenntartó LICENSE a repó gyökerében (a saját adat és a próza minden jog fenntartva, a harmadik fél adata a licencek.tsv szerint); a licencek.tsv projekt_adat sora tisztazott, új sorok a karoli_strong/* és karoli_variancia számára, a projekt_adat-on múló sorok újraértékelve; a sqlite_epit.py SZARMAZTATOTT_LICENC cseréje és táblaszintű licenc (tabla_licenc), a méret újramérve (a #86 N-F86b bemenete)
kovetkezo: "Te: DT-F89b (M2: a lexikon teljes újragenerálása elfogadható-e ebben a feladatban); M1, M3, M4 kész (F89.2–F89.5), utána fuggetlen-ellenor és zárás"
olvas: [DONTESEK.md, NYITOTT_FELADATOK.md, adat/SEMA.md, adat/licencek.tsv, adat/datasetek.tsv, eszkozok/sqlite_epit.py, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/igazolas_migracio.py, naplok/SQLITE_EPIT_meres.md, Rendszerfejlesztesi_playbook.md]
ir: [LICENSE, adat/licencek.tsv, adat/SEMA.md, eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, naplok/SQLITE_EPIT_meres.md, NYITOTT_FELADATOK.md, lexikon/]
fugg: [79]
---

# F89_LICENC_RENDEZES_BRIEF.md — a projekt saját adatának jogai és a táblaszintű licenc

*FELADATOK #89 · Modell: sonnet · v2 · 2026.10.12 · a v1-et (DT112, CC BY 4.0) a DT116 váltja fel · döntés: DT116, DT113 · forrás: `NYITOTT_FELADATOK.md` N-F79a, `adat/licencek.tsv` (`projekt_adat`), `adat/SEMA.md` 2.19, `naplok/SQLITE_EPIT_meres.md`*

## 1. Cél

A felhasználó döntése (DT116, a DT112 helyett): a projekt **saját adatrétege**
(`adat/*.tsv`, `adat/karoli_strong/*`, `adat/karoli_variancia.tsv`, a `pardes.db` saját táblái)
**minden jog fenntartva**, akárcsak a **próza** (tanulmányok, lexikon, motívumcikkek). Az
adatbázis a felhasználó saját strongozására épül. Ma a `licencek.tsv` `projekt_adat` sora
`tisztazatlan` („a repó saját licence nincs rögzítve”), és ez a sor tart `tisztazatlan`-ban több
származtatott sort is. A harmadik fél adata a saját sora szerint marad.

A második döntés (DT113): a `pardes.db` a licencet **táblaszinten** tárolja, nem soronként (a
`licenc_*` oszlopok a mérés szerint kb. 250 MB-ot tesznek ki a 845 MB-ból).

A javaslattevő nem jogász; a kereskedelmi kiadás előtt a DT-M6 szerint jogász néz rá. A
jogászi kérdéslistán (DT116): a modell által előállított, a felhasználó által irányított és
ellenőrzött párosítás szerzői jogi védelme.

## 2. Hatókör

**Benne van**

- **`LICENSE`** a repó gyökerében, rövid jogfenntartó nyilatkozat: a jogtulajdonos neve és az
  év (M0 ⛔, D1), „minden jog fenntartva” a saját adatra és a prózára, fájlkörönként; a
  harmadik fél adatára utalás a `adat/licencek.tsv`-re (az ott álló licencek és kötelező
  megjelölések érvényesek, a jogfenntartás azokra nem terjed ki). Jogi értelmezést nem tartalmaz.
- **`adat/licencek.tsv`:**
  - a `projekt_adat` sor: `licenc` = minden jog fenntartva, `forras_hely` = `LICENSE` + DT116,
    `allapot` = `tisztazott`, `share_alike` = `nem`, `kereskedelmi` és `cimke` az M0 ⛔ szerint
    (D2, D3), a `megjegyzes`-ben a DT-F24 halasztás lezárása és a DT112 felülírása;
  - új sorok: `Karoli_Strong_parok`, `Karoli_Strong_szavak` (a `datasetek.tsv` azonosítói) és
    `karoli_variancia`: a saját rész minden jog fenntartva, a forrásaik (Károli 1908 közkincs,
    TAHOT/TAGNT CC BY 4.0) a megjegyzésben, a kötelező megjelölés a STEPBible-szöveggel;
  - újraértékelés: a `projekt_adat`-on múló `tisztazatlan` sorok (`Karoli_Strong_kivonat`,
    `LXX_versszintu_parok`, `Karoli_versmegfeleltetes`); ahol a többi összetevő igazolt, a sor
    `tisztazott` lesz, ahol nem, a sor marad, és a megjegyzés megnevezi, min múlik.
- **`adat/SEMA.md` 2.19:** a 3. szabály (a `projekt_adat` nyitott) helyére a DT116: a saját adat
  jogainak forrása a jogtulajdonos döntése, a `LICENSE`-ban rögzítve (ez a `forras_hely`); a
  `cimke` zárt készlete és a `projekt-adat` kivétel a D2 szerint módosul.
- **`eszkozok/sqlite_epit.py`:**
  - a `SZARMAZTATOTT_LICENC` a fenti új sorokra mutat (`token_par`, `token_karoli`,
    `frazis_pozicio`, `karoli_variancia`);
  - **táblaszintű licenc (DT113):** egy `tabla_licenc(tabla, licenc_allapot, kereskedelmi,
    licenc_dataset, cimke)` tábla; a `licenc_allapot`, `kereskedelmi`, `licenc_dataset` oszlop
    kikerül a táblákból (az FTS `UNINDEXED` licenc-oszlopai is); a „legszigorúbb érték” szabály
    (DT109 (2c)) változatlan, csak a tárolás helye változik;
  - az F79 G6-ja átfogalmazva: minden épített táblának pontosan egy `tabla_licenc`-sora van;
    licencsor nélkül a tábla továbbra sem épül be;
  - a CC BY-SA (`sdbh_domenek`, SDGNT, UBS, LSJ, tW) és az MCGED tábla `tabla_licenc`-sora
    megkülönböztethető a saját, zárt tábláktól (a `licenc_dataset` és a `cimke` alapján), hogy
    egy későbbi zárt csomag (#86) szűrni tudja őket (DT116).
- **`eszkozok/teszt_sqlite_epit.py`:** a licenc-tesztek a `tabla_licenc`-re.
- **A generált lexikon** (`lexikon/`): ha a `projekt_adat` címkéje változik (D2), a
  `lexikon_general.py` a prózai és a saját adatblokkokra az új címkét teszi; a lexikon a
  generátorral újragenerálódik (`python eszkozok/general.py --cel lexikon`), kézzel nem írható.
  A `lexikon_general.py` nem változik: a címkét a táblából olvassa (SEMA 2.19, N9).
- Teljes újraépítés és mérés a `naplok/SQLITE_EPIT_meres.md`-ben: méret előtte/utána, a
  `tabla_licenc` tartalma, a `tisztazatlan` és a CC BY-SA/NC táblák listája.
- `NYITOTT_FELADATOK.md`: az N-F79a lezárása a DT-F89a-ra hivatkozva.

**Nincs benne**

- a jogi vélemény, a kereskedelmi kiadás és a #86 csomagja (csak a mérés a bemenete);
- a repó nyilvánossága (N-F23c; a `karoli_strong/*` ma nyilvánosan olvasható — nem ez a feladat
  dönt róla);
- a többi `tisztazatlan` harmadik fél sor (KJV, LXX_kivonat, lexikonok_nyers, …): nem a
  `projekt_adat`-on múlnak;
- a `.gitignore`, a `pardes.db` terjesztése (#76);
- a TIPNR (#88), a nem létező Károli-versek (DT114), a ki nem épített táblák (DT115).

## 3. Lépések

- **M0 — felmérés (csak olvas).** (1) Minden `licencek.tsv`-sor, amely a `projekt_adat`-on
  múlik (a `licenc` vagy a `megjegyzes` mezőben), és mi lenne az állapota a DT116 után;
  (2) minden kódhely, amely a `projekt_adat` kulcsot, a `cimke` értékét vagy a `licenc_*`
  oszlopokat olvassa (`grep`: generátorok, `lekerdez.py`, `ellenoriz.py`, CI), és hogy a
  címkeváltás mely generált fájlokat érinti; (3) a `LICENSE` tervezete. ⛔ **A felhasználónak:**
  D1 (a `LICENSE` szövege és a jogtulajdonos neve), D2 (a címke), D3 (a `kereskedelmi` érték).
- **M1 — `LICENSE`, `licencek.tsv`, SEMA 2.19** (`F89.1:` …): a jóváhagyott szöveg; a TSV
  írása `split('\t')`/`'\t'.join()`, írás előtt soronkénti összevetés az eredetivel (minta:
  `eszkozok/igazolas_migracio.py`); csak a megnevezett sorok változnak.
- **M2 — a lexikon újragenerálása**, ha a D2 címkét vált: a generált diff csak a címkesorokat
  érinti.
- **M3 — táblaszintű licenc az építőben**, kis mintán; tesztek.
- **M4 — teljes újraépítés és mérés.**
- **Zárás.** `fuggetlen-ellenor`; `python eszkozok/feladatok.py ellenoriz` 0; ha a lexikon
  újragenerálódott: `python eszkozok/general.py --cel lexikon --ellenoriz` 0; fejléc `lezarva`,
  `lezarva_osszegzes`; draft PR.

## 4. Elfogadási feltételek

- **G1** A `licencek.tsv` diffje csak a megnevezett sorokat érinti; a többi sor bájtra azonos
  (soronkénti összevetés a naplóban); a TSV-ket `csv` modul nem írja.
- **G2** A `projekt_adat` sor `tisztazott`, `forras_hely`-e a `LICENSE`-ra és a DT-F89a-ra
  mutat; az új sorok minden mezője kitöltött (a `kotelezo_megjeloles` szó szerint, ahol a forrás
  megad ilyet).
- **G3** Sem a saját adat, sem a próza nem kap szabad licenc-jelölést (CC BY vagy más) a generált
  nézetekben; a lexikon-generátor futása és egy prózai, egy saját adat- és egy harmadik fél
  blokk címkéje a naplóban.
- **G4** A `pardes.db`-ben egyik táblának sincs `licenc_allapot`/`kereskedelmi`/`licenc_dataset`
  oszlopa; minden táblának pontosan egy `tabla_licenc`-sora van; a legszigorúbb-érték szabály
  teszttel igazolva (egy származtatott tábla a legszigorúbb forrása értékét kapja); a CC BY-SA és
  az MCGED tábla a `tabla_licenc`-ből szűrhető.
- **G5** A mért méret előtte/utána a `naplok/SQLITE_EPIT_meres.md`-ben, proveniencia-sorral;
  a `tisztazatlan` és a CC BY-SA/NC táblák listája név szerint.
- **G6** Az építés determinisztikus (két futás táblánkénti hash-e azonos); minden teszt zöld.

## 5. Döntésnapló

| Tétel | Kérdés | Javaslat | Állapot |
|---|---|---|---|
| DT112 | A projekt saját adatának licence (CC BY 4.0) | — | felülírva a DT-F89a-val (felhasználó, 2026.10.12) |
| DT116 | A projekt saját adatának jogai | minden jog fenntartva (adat és próza); a harmadik fél adata a saját sora szerint; a CC BY-SA és az MCGED nem kerülhet zárt csomagba | eldöntve (felhasználó, 2026.10.12) |
| DT113 | Licenc soronként vagy táblánként | táblaszintű (`tabla_licenc`), a DT-F89a-val egy menetben | eldöntve (felhasználó, 2026.10.12) |
| D1 | A `LICENSE` szövege és a jogtulajdonos neve (Demeter Tamás, 2026; kapcsolat nincs kiírva) | rövid jogfenntartó nyilatkozat fájlkörönként, a harmadik fél adatára a `licencek.tsv`-re utalva; a név a felhasználótól | eldöntve a javaslat szerint (felhasználó, 2026.10.13; DT-F89a) |
| D2 | A címke | új zárt `cimke`-érték: `minden jog fenntartva` (SEMA 2.19); a `projekt-adat` kivétel megszűnik | eldöntve a javaslat szerint (felhasználó, 2026.10.13; DT-F89a) |
| D3 | A `projekt_adat` `kereskedelmi` értéke | `igen` — a jogtulajdonos maga kereskedelmileg felhasználhatja (DT-F86a); harmadik félnek a `LICENSE` nem ad jogot. `nem` esetén a „legszigorúbb érték” szabály minden saját származtatott táblát `nem`-re vinne, és a #86 csomagja nem épülhetne rájuk | eldöntve a javaslat szerint (felhasználó, 2026.10.13; DT-F89a) |
