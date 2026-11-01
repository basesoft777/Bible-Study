# LEKTOR_FELULET_naplo.md — F157 (#157) végrehajtási napló

*Modell-ellenőrzés: kért `sonnet`, tényleges `claude-sonnet-5-5` — egyezik.*

## 0. Ellenőrzés (2026-11-01)

- **DT-F157a–c** a brief 6. szakaszában eldöntve (egy felület; tároló: artifact-adatbázis; beolvasás kérésre) — átvéve.
- **db capability:** az `artifact-capabilities` szolgáltatás a fiók élő jogosultság-listáján a `db`-t kínálja (`artifact`, `assets`,
  `comments`, `db`, `downloads`, … ; runtime contract 0.2.96). A publikálás utáni működési próba eredménye lent (M1).
- **Tartalék:** a felület a db hiányában (`claude.use("db") === null`, vagy elutasított írás) a válaszokat a lapon tartja
  (kényelmi `localStorage`), és másolható összesítő sort ad; ez a tartalék a db mellett is ott van.

## M0 — kérdés-séma és generátor

- `eszkozok/lektor_kerdesek.py` (+ `eszkozok/teszt_lektor_kerdesek.py`, 8 teszt): a `naplok/HATAR_<ID>.md` Gépi rész K/N pontjaiból
  és a Modelles rész K pontjaiból `naplok/LEKTOR_<ID>.tsv`. A „Felhasználói besorolás” K-sorai a `valasz` mezőbe, az `allapot`
  `megvalaszolva`-ra kerülnek (DT-F151c, szó szerint); a már kitöltött `valasz`/`allapot`/`atvezetes` megmarad.
- `LEKTOR_ISTENTISZT-001.tsv`: 5 kérdés (K1–K5, mind a #151 felhasználói besorolásával); `LEKTOR_HAMART-001.tsv`: 0 kérdés (gépi
  rész 0 kérdés, modelles rész „nem futott”) — üres eredmény, jelölve, nem hiba.
- A CRLF-es forrásfájl (Windows) kezelve; a `hely` a kérdés első `jeloltek.tsv:<sor>` hivatkozásának igehelye.

## M1 — felület és artifact

- `eszkozok/lektor_felulet/sablon.html` + `epit.py`: a `naplok/LEKTOR_*.tsv` kérdéseiből építi az oldalt (csak kérdés-mezők és a
  repóban már rögzített döntés; a felhasználó artifact-beli válasza soha nem kerül az oldalba). Gombok: Elfogadom / Elvetem /
  Visszakérdezek / Saját szöveg; szűrő forrás, motívum, állapot szerint; egy hasáb, 48 px-es gombok (telefon); „lapnézet” link.
- Artifact (privát, `db` capability): https://claude.ai/artifact/GqczbTiP918WHpRVnzxZZv — a válaszok a `valaszok/<kerdes_id>`
  dokumentumokban; tartalék: kényelmi `localStorage` + másolható `LEKTOR-VALASZ | <kerdes_id> | <típus> | <szöveg>` összesítő.
- **Működési próba (db):** a `valaszok` gyűjtemény `ArtifactData` `list`-je a publikálás után üres (nem töltöttem fel), `as_level: view`
  szerint is üres. Amit nem tudtam kipróbálni: a gombok és az írás a böngészőben, telefonon (⛔ a felhasználó próbája, brief 2. lépés).
- Az artifact „lapnézet” linkje az arany lap nézetére mutat (1d9WcUQDkSLgEwopYXtFKq); horgony-ugrás nincs, a `hely` a kártyán áll.

## M2 — `proza_javaslat` kérdés-típus (orkesztrátor-kérés, felhasználó: „mehet”)

- Felhasználói felvetés: a lektor ne csak a meglévő próza hibáit találja meg, hanem olvasás közben is kérdezhessen: „az adatból ez
  következik, de a lap nem mondja ki — legyen róla mondat?”.
- Séma: új `forras` érték `proza_javaslat` (`FORRASOK`); `proza_javaslat_sor()` kötelezően kér adatsort (`fájl:sor`) és az adat saját
  proveniencia-sorát; a kérdés csak kérdez, mondatot nem javasol. Válaszlehetőségek: legyen mondat; nem kell; később.
- Felület: ennél a típusnál a gombok „Legyen mondat / Nem kell / Visszakérdezek / Saját szöveg”.
- A lektor prózát NEM ír (DT-F32b). Az „igen” a forrásfájl prózai feladata (`/befogad`-dal, jóváhagyással); a mondatot a próza írója
  írja az egészet olvasva. Az `eszkozok/lektor_kerdesek.py` ehhez nem generál sort: a forrás (a lektor-futás) a #125 után jön.
- **Függő:** a brief 3.1/3.4 szakasza és a `DONTESEK.md` DT-F157 helyőrző az `ir` listán kívül esik; írásuk jóváhagyásra vár.
