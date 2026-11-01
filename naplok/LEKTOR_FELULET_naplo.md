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
