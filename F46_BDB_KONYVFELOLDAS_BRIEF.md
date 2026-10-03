---
feladat: 46
cim: A BDB rosszul feloldott könyvneveinek felmérése és javítása a forrásban és a fordításokban
kod: BDB_KONYVFELOLDAS
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
ag: claude/bdb-konyvfeloldas
pr: https://github.com/basesoft777/Bible-Study/pull/140
lezarva_osszegzes: "OSHL-forrással felmérve (1032 csere-jelölt), DT-F46 szerint cserélve: forrás 253 token, fordítás 54 token (a Károli-vers Strong-kapun nem igazolt 16 csere visszaállítva); N-F34/N-F34c lezárva, N-F46a nyitott (779 kézi sor), N-F46b nyitott."
ad: a konkordancia/BDB_teljes_unabridged.tsv és az adat/forditasok.tsv BDB-sorainak igehelyei a helyes bibliai könyvre mutatnak (független BDB-forrással és versszám-ellenőrzéssel igazolva); a kétes esetek kézi listán; az N-F34 maradéka és az N-F34c lezárva
kovetkezo: "Te: merge a #140-nel (felhasználó kérte, CI zöld után)"
olvas: [konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/OSHL_lexikalis_index_README.md, adat/licencek.tsv, adat/SEMA.md, eszkozok/bdb_psi_javit.py, eszkozok/forditas_kapuk.py, naplok/F34_M2_maradek.tsv, naplok/BDB_FORDITAS_naplo.md, beerkezo/BDB_KONYVFELOLDASI_AUDIT.md, konkordancia/TAHOT_kivonat.tsv]
ir: [konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, eszkozok/bdb_konyv_javit.py, eszkozok/teszt_bdb_konyv_javit.py, konkordancia/OSHL_BDB_igehelyek.tsv, adat/datasetek.tsv, adat/licencek.tsv, naplok/BDB_KONYVFELOLDAS_csere.tsv, naplok/BDB_KONYVFELOLDAS_kezi.tsv, naplok/BDB_KONYVFELOLDAS_naplo.md, beerkezo/BDB_KONYVFELOLDASI_AUDIT.md]
fugg: [34]
---

# Fxx_BDB_KONYVFELOLDAS_BRIEF.md — A BDB könyvfeloldási hibáinak javítása

*FELADATOK #(a /befogad adja) · Modell: opus · v1 · 2026.10.02 · forrás: `beerkezo/BDB_KONYVFELOLDASI_AUDIT.md` (csonk), a #38 menetében készült*

## 1. Cél

A `konkordancia/BDB_teljes_unabridged.tsv` digitalizálása során a nyomtatott BDB könyvrövidítései helyenként rossz könyvre oldódtak fel. Néhány példa:
- „Gn 41:47” → „Hab 41:47”;
- „Jos 9:9” → „Joel 9:9”;
- „Deut 37:36” = 1Móz 37:36;
- H0413: a Jób-helyek „1 Samuel” alatt;
- a fáraó helyén „Phoenician” (H9005).

A #38 ezeket hűen viszi át a fordításba. Ez a feladat a hibákat **egyszer, teljes körűen** felméri, és gépi cserével javítja a forrásban és a már lefordított sorokban is. Újrafordítás nem kell, csak az igehelyek könyve (és szükség esetén a fejezet:vers) cserélődik.

## 2. Hatókör

**Benne van:**
- minden igehely-hivatkozás könyvfeloldása a teljes BDB-ben (8 090 szócikk);
- az N-F34 maradéka (156 B/R hely, `naplok/F34_M2_maradek.tsv`) és az N-F34c (`Dan c:v` = 5Móz, `Lev 28:17` típus): ezek ebben a menetben zárulnak le;
- a nem leképezett vagy többértelmű könyvalakok feloldása (`Kings`, `Ki`, `Sam`, `Chron`, `Chronicles`, `Samuel`, `Ze`, `Jes`, `Esc`, `De`, `En`);
- a könyvnév helyén álló névhibák, ha a független forrás egyértelműen igazolja őket (pl. „Phoenician” → „Pharaoh”). Ezek külön listára kerülnek, és csak jóváhagyással cserélődnek.

**Nincs benne:**
- a BDB lexikai (tartalmi) hibái és a könyvneveken túli OCR-javítás;
- újrafordítás;
- a Thayer hasonló auditja;
- a 11. és 13. kapu logikájának átírása.

## 3. Lépések

### 3.0 Modell-ellenőrzés
Írd ki a saját tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével (`opus`). Eltérésnél ne dolgozz, jelezd, és állj meg.

### 3.1 Előfeltétel
- A #38 állapota `megallt`, és az utolsó adag ága be van olvasztva a `main`-be. Ha a #38 fut, ne indulj, jelezd. A két feladat ugyanazt az `adat/forditasok.tsv`-t írja.
- Új ág a `main`-ből: `claude/bdb-konyvfeloldas`. Az első commit a brief fejlécében `allapot: fut`, az `ag` mező kitöltve.

### 3.2 Független forrás
- Jelölt: az OpenScriptures `HebrewLexicon` repó `BrownDriverBriggs.xml` fájlja, strukturált igehely-hivatkozásokkal. Ugyanebből a repóból már van import: az OSHL (`adat/licencek.tsv`, `tisztazott`, CC BY 4.0, commit `21c9add`). A Strong → BDB-azonosító leképezés a már importált `LexicalIndex.xml`-ből jön.
- Ellenőrizd, hogy a `BrownDriverBriggs.xml` ugyanabban a commitban van-e, és ugyanaz a licenc vonatkozik-e rá (a repó saját licencfájljából, szó szerinti idézettel).
  - **Ha igen:** a licenc tisztázott, nincs megállás. Új `adat/licencek.tsv`-sor az idézettel, és új `adat/datasetek.tsv`-sor.
  - **⛔ Ha nem** (más commit, más licenc, vagy a fájl nincs meg): állj meg, és javasolj másik forrást.
- A nyers XML a gitignore-olt `konkordancia/_nyers/` alá kerül. A repóba csak a szócikkenkénti igehely-kivonat kerül (`konkordancia/OSHL_BDB_igehelyek.tsv`: `strong`, `bdb_id`, `sorszam`, `konyv`, `fejezet`, `vers`), rögzített forrásverzióval.

### 3.3 Összevetés szócikkenként
- `eszkozok/bdb_konyv_javit.py`, az `eszkozok/bdb_psi_javit.py` (#34) mintájára. A két forrás igehely-listáját illeszti szócikkenként, sorrend és fejezet:vers alapján (könyvnév nélkül is).
- Ahol a könyv eltér, az csere-jelölt. Kimenet: `naplok/BDB_KONYVFELOLDAS_csere.tsv` (`strong`, `pozicio`, `forras_alak`, `fuggetlen_alak`, `javasolt_karoli_alak`, `hibatipus`, `bizonyossag`).

### 3.4 Igazolás
Minden csere-jelöltre:
- **Versszám-ellenőrzés:** létezik-e a javasolt fejezet és vers (MT-számozás, TAHOT). Lehetetlen igehely nem kerülhet cserébe.
- **Strong-próba:** a javasolt helyen szerepel-e a szócikk Strong-száma (TAHOT, ±1 vers).
- **Bizonyosság:**
  - `magas`: a független forrás egyezik, a vers létezik, a Strong-próba sikeres;
  - `kozepes`: két feltétel teljesül;
  - `kezi`: a többi. Ezek a `naplok/BDB_KONYVFELOLDAS_kezi.tsv`-be kerülnek, a forrás és a független alak szövegkörnyezetével.

### 3.5 Jelentés és ⛔ megállás a csere előtt
- A naplóban (`naplok/BDB_KONYVFELOLDAS_naplo.md`) hibatípusonként (ψ-maradék, más könyv érvényes fejezettel, fejezet-túllépés, vers-túllépés, összeolvadt alak, névhiba) és bizonyossági szintenként darabszám; az érintett szócikkek száma a forrásban és a fordításokban; 10 jellemző példa.
- **⛔ Állj meg:** a felhasználó jóváhagyja a csere-táblát. Az alapjavaslat: a `magas` szintű sorok gépi cserével, a `kozepes` és a `kezi` szintűek a felhasználó döntése szerint. A brief állapota `dontesre_var`, a tétel a `DONTESEK.md`-be kerül (helyőrző: DT-Fxx).

### 3.6 Gépi csere (a jóváhagyás után)
- Mezőkulcsos, pozícióhoz kötött csere, mint a #34-ben, mindkét táblán:
  - a `konkordancia/BDB_teljes_unabridged.tsv`-ben a forrásalak;
  - az `adat/forditasok.tsv` érintett BDB-soraiban a Károli-alak, a `forras_hash` frissítésével (DT-F34c (1) szerint).
- `kezi` állapotú sor csak külön jóváhagyással cserélhető.
- Utána a 11. és a 13. kapu fusson le az összes fordított soron, és az `ellenoriz.py` adjon 0 SÉRTÉS-t.
- A 13. kapu forráshiba-jelzéseinek száma előtte és utána is kerüljön a naplóba (az M0-ban 109 szócikk volt).

### 3.7 Lezárás
- A `beerkezo/BDB_KONYVFELOLDASI_AUDIT.md` csonk archiválva: „befogadva: #xx”.
- Az N-F34 és az N-F34c lezárása a `NYITOTT_FELADATOK.md`-ben.
- Futtasd a `fuggetlen-ellenor` ügynököt. A jelentése a `naplok/ELLENOR_BDB_KONYVFELOLDAS.md` fájlba kerüljön, commitolva.
- Push, majd draft PR a `main`-be. A záró összefoglaló első sora a PR linkje és a CI állapota. Utána: a cserék száma táblánként, a kézi listán maradt sorok száma, és a 13. kapu jelzéseinek száma előtte és utána.

## 4. Elfogadási feltételek

- Minden csere igazolt: a vers létezik, a sor szerepel a csere-táblán, és a felhasználó jóváhagyta.
- A forrásban és a fordításban ugyanaz a hely ugyanarra a könyvre mutat.
- A 13. kapu jelzései csökkentek. Ami megmaradt, az a kézi listán szerepel indoklással.
- Az `ellenoriz.py` 0 SÉRTÉS-t ad, a tesztek átmennek.
- A szövegtartalom nem változott, csak az igehely-hivatkozások.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett |
|---|---|---|---|
| D1 | Egy menet, egy ⛔ megállással a csere előtt | kevesebb lépés (a felhasználó kérése); a licencmegállás csak akkor kell, ha az OSHL-licenc nem terjed ki a BDB-XML-re | két menet |
| D2 | Független forrás: OpenScriptures `BrownDriverBriggs.xml` | ugyanaz a repó, mint a már tisztázott OSHL; strukturált igehelyek | kézi összevetés nyomtatott BDB-vel |
| D3 | Az N-F34 maradéka és az N-F34c ebben a menetben zárul | egy forrásjavítás, ugyanaz a mechanizmus | külön feladat |
| D4 | Javítás a forrásban és a fordításban is, újrafordítás nélkül | a #38 hűen viszi a forráshibát; a csere elég | újrafordítás |
| D5 | A #38 két adagja közötti megállásnál fut | kölcsönös kizárás az `adat/forditasok.tsv` miatt; minél korábban, annál kevesebb cserélendő fordított sor | a #38 végén |
| D6 | Modell: opus | a kétes esetek előkészítése nyelvi ítéletet kér | sonnet |

<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Első lépésként írd ki a saját tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével (`opus`). Ha eltér, ne dolgozz, jelezd, és állj meg. Ha egyezik: olvasd be a csatolt briefet, és hajtsd végre a 3. szakasz lépéseit. Minden lépés után commit és push a `claude/bdb-konyvfeloldas` ágra. A 3.5 ⛔ pontnál állj meg.
<!-- /KOZVETLEN_FUTTATAS -->
