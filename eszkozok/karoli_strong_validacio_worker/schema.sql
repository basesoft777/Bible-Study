-- F175.V21 — a validációs D1 adatbázis sémája (DT-F175vp). Betöltés: a letétben készülő d1_betoltes.sql
-- (eszkozok/karoli_strong_validacio_d1.py) ezt a sémát is tartalmazza; itt a repóban, titok és tétel nélkül.
--   ellenor  — ellenőrönként a token SHA-256-ja (a token maga nem), a szerep és az oldal minta-azonosítója;
--   tetel    — a tétel kész JSON-ja (az ellenőrző oldal formájában), a letétből;
--   kiosztas — melyik ellenőr melyik tételt kapja;
--   naplo    — append-only napló: minden mentés egy sor (UPDATE és DELETE tiltva);
--   utolso   — nézet: ellenőrönként és tételenként az utolsó érvényes válasz (a kliens ideje, majd a napló sorszáma szerint).
CREATE TABLE IF NOT EXISTS ellenor (
  id TEXT PRIMARY KEY,
  szerep TEXT NOT NULL CHECK (szerep IN ('kulso', 'masodik', 'proba')),
  token_sha256 TEXT NOT NULL UNIQUE,
  minta_hash TEXT NOT NULL,
  tetelszam INTEGER NOT NULL,
  kesz_ido TEXT
);
CREATE TABLE IF NOT EXISTS tetel (
  id TEXT PRIMARY KEY,
  adat TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS kiosztas (
  ellenor TEXT NOT NULL REFERENCES ellenor(id),
  tetel TEXT NOT NULL REFERENCES tetel(id),
  PRIMARY KEY (ellenor, tetel)
);
CREATE TABLE IF NOT EXISTS naplo (
  n INTEGER PRIMARY KEY AUTOINCREMENT,
  ellenor TEXT NOT NULL REFERENCES ellenor(id),
  tetel TEXT,
  esemeny TEXT NOT NULL CHECK (esemeny IN ('valasz', 'kesz')),
  valasz TEXT,
  kliens_ido TEXT,
  szerver_ido TEXT NOT NULL,
  kliens_azon TEXT NOT NULL,
  UNIQUE (ellenor, kliens_azon)
);
CREATE INDEX IF NOT EXISTS naplo_ellenor_tetel ON naplo (ellenor, tetel);
CREATE TRIGGER IF NOT EXISTS naplo_nincs_modositas BEFORE UPDATE ON naplo
BEGIN SELECT RAISE(ABORT, 'a naplo append-only'); END;
CREATE TRIGGER IF NOT EXISTS naplo_nincs_torles BEFORE DELETE ON naplo
BEGIN SELECT RAISE(ABORT, 'a naplo append-only'); END;
CREATE VIEW IF NOT EXISTS utolso AS
SELECT ellenor, tetel, valasz, kliens_ido, szerver_ido, n FROM (
  SELECT ellenor, tetel, valasz, kliens_ido, szerver_ido, n,
         ROW_NUMBER() OVER (PARTITION BY ellenor, tetel ORDER BY kliens_ido DESC, n DESC) AS rn
  FROM naplo WHERE esemeny = 'valasz'
) WHERE rn = 1;
