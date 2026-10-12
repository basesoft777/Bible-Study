# MOTIVUM_FORRAS — CI-terv: E28 és E29 (leírás)

*FELADATOK #23 · `F23_MOTIVUM_FORRAS_BRIEF.md` M1/3 · 2026.10.08 · ág: `claude/f23-m1-forrassablon`*

**Csak leírás.** Az implementáció külön ágon megy (D6), a #11 előtt. Ez a fájl a két szabály
szerződését rögzíti: mit vizsgál, mire, milyen szinten, és mi a bukás. Kapcsolódó szabályok:
`adat/SEMA.md` 3/9 (egyirányúság) és 3.10 (szintjelölés, kinyerés), a forrássablon
(`sablonok/9_PaRDeS_motivum_forras_sablon.md`) 1., 2. és 8. pontja.

## 0. A számozás

A következő szabad E-szám a **E28**, utána az **E29**. Mérés:
`scope=eszkozok/ellenorzes/szabalyok.py + .github/workflows/*.yml + a repó md/py/yml fájljai (worktree és konkordancia nélkül) + az összes távoli ág md/py/yml fájlja | forras=manual (grep "\bE2[89]\b", git grep a távoli ágakon) | ts=2026-10-08`:
a `szabalyok.py` az E2–E27 számokat viseli (az E1 az `eszkozok/ellenoriz.py`, a workflow
lépésneve „E2-E27”); E28 vagy E29 sehol nem szerepel. A szám ágon foglalt, nem kiosztott: ha
az implementáló ágig más szabály foglalja, az implementáció a következő szabad számot veszi,
és ezt a fájlt hivatkozással frissíti.

## 1. E28 — az újragenerált nézet bájtazonos a commitolttal

**Mit véd:** a (c) réteget (CLAUDE.md „Rétegek”, SEMA 3/9). Ha egy generált nézet eltér attól,
amit a commit (a)+(b) rétegéből a generátor előállít, akkor vagy kézzel szerkesztették (tilos),
vagy a forrás/adat változott újragenerálás nélkül. A lexikonoldal-sablon Minőségi kapujának
gépi része (DT66 (a): a `Minőségi kapu (lexikon)` sor) és a törzscikk-sablon „Ellenőrzés”
bekezdése ide költözik.

**Hatókör (fájlok):**
- a forrásból generált nézetek: `lexikon/[ID]_TUDOMANYOS.md` és a motívumcikk (a #11 dönti el a
  helyét), **csak a migrált motívumokra** — engedélyezőlista: a migrált ID-k listája (a #11
  vezeti, lépcsőnként bővül). A még nem migrált motívum éles `lexikon/` fájlja befagyasztott
  (DT74 (3)), és a #78 óta a generátor más 2. szakaszt ír, mint ami commitolva van; rá a szabály
  nem fut (különben minden PR bukna).
- a meglévő generált marker-blokkok (`--cel naplo`, `index`, `nyitott`): ezekre ma is van
  törzs-összevetés (`general.py --ellenoriz`), a szabály ezt CI-ba emeli.
- **nem** hatókör: a törzscikk (a #11-ben megszűnik; a próba-törzscikk nulla-diffje nem áll,
  N-F78a), a `generalt_proba/` (verziózott próbakimenet, nem éles nézet).

**Mikor fut:** minden PR-en, ha a változott fájlok között van `adat/*.tsv`, `motivumok/*.md`,
`eszkozok/*general*.py`, `sablonok/9_*.md`, vagy a hatókör valamely generált fájlja.

**Hogyan (a szerződés):**
1. A generátor a PR fej-commitjának munkafájából, ideiglenes könyvtárba (a repón kívül,
   CLAUDE.md `generalt_proba/` szabály) újragenerálja a hatókör fájljait.
2. A dátum rögzített: `PARDES_DATUM` = a commitolt fájl első `GENERÁLT` jelölőjének `ts=`
   értéke (`eszkozok/general.py` `TS`, `eszkozok/nulladiff.sh` D30). A `ts`-mezőt tehát nem
   maszkolja, hanem ugyanarra a napra generál: így a bájtazonosság szó szerint érthető.
3. Összevetés bájtra (UTF-8, sorvég-normalizálás nélkül: a sorvégnek is egyeznie kell; ha a
   repó `.gitattributes`-a sorvéget konvertál, a commitolt blob az összevetés alapja, nem a
   munkafa-fájl).
4. **Eltérés → HIBA.** A jelentés: a fájl, az első eltérő sor száma, mindkét oldal sora, és
   ha a sor egy `GENERÁLT-KEZDET` blokkban áll, a blokk cél-kulcsa.

**Elfogadott eltérés nincs.** Az E28 nem ismer `--csere`-listát: a migráció elfogadott diffje
(pilot-terv 5. szakasz) a régi és az új kimenet *között* értendő, nem a commitolt és az
újragenerált kimenet között. Ha a generátor szándékosan változik, a nézet ugyanabban a PR-ben
újragenerálódik és commitolódik.

**Szint:** HIBA (FAJLSZINTU, mint az E5/E27: a fájl egészére vonatkozik).

**Tesztek (az implementáló ágon):** pozitív — változatlan forrásból generált, commitolt nézet
zöld; negatív — (a) a nézetbe kézzel írt egy szó piros; (b) az `adat/elofordulasok.tsv` egy
`kapcsolodas` mezője változik, a nézet nem: piros; (c) a forrás egy `olvasoi` bekezdése
változik, a nézet nem: piros; (d) nem migrált motívum befagyasztott lapja: nem fut.

**Kapcsolat a meglévő szabályokhoz:** az E27 a `GENERÁLT-VÉGE` jelölők épségét nézi, az E28 a
blokk tartalmát; az E5 tartalomveszteség-őre a generált fájlra nem fut, az E28 viszont csak
arra. A `general.py --ellenoriz` csak a marker-blokk törzsét veti össze (a markert és a kézi
szakaszt nem); a forrásból generált nézetnek nincs kézi szakasza, ezért ott a teljes fájl
az összevetés tárgya.

## 2. E29 — a nyilvános kimenetben nulla `belso` jelölés és nulla `【NAPLO`

**Mit véd:** a D36 build-kihagyását (SEMA 3.10.4): a `belso` blokk a nyilvános nézetből
kimarad, nem elrejtődik. Előképe a törzscikk-sablon „Ellenőrzés” bekezdése (`GENERÁLT` 0,
`【NAPLO` 0, `proveniencia:` 0, …).

**Hatókör (fájlok):** a nyilvános nézetek — az `olvasoi` és az `apparatus` mélységű kimenetek:
a migrált motívumok `lexikon/[ID]_TUDOMANYOS.md` lapja és motívumcikke, valamint az olvasói
build (#25/#76) kimenete, amikor elkészül. **Nem** hatókör: a `belso` (szerkesztői) nézet, a
`motivumok/*.md` forrás (ott a `【NAPLO` kötelező hely), a `naplok/`, a `generalt_proba/`.

**Mit keres (mind nulla kell legyen):**

| Minta | Miért tilos a nyilvános kimenetben |
|---|---|
| `【NAPLO` | mindig `belso` (SEMA 3.10.3) |
| `SZINT-KEZDET: belso`, `SZINT-VÉGE: belso`, és a #64 ideiglenes `SZINT: belso` alakja (`ADAT-NÉZET` jelölőben is) | `belso` blokk jelölője: ha a jelölő kijutott, a blokk is |
| `SZINT-KEZDET`, `SZINT-VÉGE` (bármely értékkel) | csak-forrásbeli jelölő (SEMA 3.10.4) |
| `INAKTÍV:`, `JELÖLT:`, `ADAT-HIV:`, `ADAT-ÉRTÉK:`, `FORRÁSRÉTEG` | csak-forrásbeli jelölő |
| az `olvasoi` nézetben ezen felül: `GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`, `RÉS-KEZDET`, `RÉS-VÉGE`, `proveniencia:` | az olvasói nézet a jelölőket és a proveniencia-sorokat sem viszi (törzscikk-sablon „Amit a törzscikk kihagy”) |

**Hogyan:** szöveges keresés a hatókör fájljain (kódkerítésen belül is: a nyilvános kimenetben
kódblokkban sem állhat `【NAPLO`). A minta-lista egy konstans a szabálykódban, a SEMA 3.10.4
jelölő-listájával egyezően; ha a SEMA bővül, a konstans is (az E25 mintájára hivatkozva).

**Bukás:** bármely találat **HIBA**; a jelentés a fájl, a sor, a minta.

**Szint:** HIBA (soronkénti találat).

**Tesztek:** pozitív — `apparatus` nézet `【NAPLO` nélkül zöld; negatív — (a) egy `【NAPLO`
a lapon piros; (b) `<!-- SZINT-KEZDET: belso -->` a lapon piros; (c) `INAKTÍV:` jelölő a lapon
piros; (d) ugyanez a `motivumok/*.md` forrásban: nem fut (nem hatókör).

**Mért kiindulás:** a mai éles `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 14, a
`lexikon/HAMART-001_TUDOMANYOS.md` 3 `【NAPLO`-t tartalmaz; a #78 próbalapja
(`generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md`) szintén 14-et
(`scope=a három fájl | forras=manual (szkript, „【NAPLO” előfordulás-számlálás) | ts=2026-10-08`).
A mai lapok tehát az E29-en elbuknának; ezért fut a szabály csak a migrált motívumokon (az E28
engedélyezőlistáján), és ezért elfogadott diff-kategória a migrációban a `belso`-kihagyás
(pilot-terv 5. szakasz, D3). *[javaslat: DT84 (10) — a lexikonoldal `apparatus` mélységű
nyilvános nézet-e; ha igen, a 14 + 3 `【NAPLO` a migrált lapról kimarad.]*

## 3. Ami a két szabályon kívül marad (a #11 briefjének)

- A meglévő tanulmány-szabályok (E6, E20) a `tematikus_lezart/` tematikus tanulmányokra
  szólnak; a migráció után a forrás a `motivumok/[ID].md`. Hogy a forrásra milyen szakasz-
  szabály fut (pl. az L1 gépi része: minden aktív szakasz jelen van vagy `INAKTÍV`), a #11
  és a sablon véglegesítése (#12) után dől el; itt nincs E-szám foglalva rá.
- A CI E11 kivezetése a #11 dolga (`F11_MIGRACIO_BRIEF.md` `ad` mezője).
- Az arany-készlet CI-része (DT78 (22)): az ISTENTISZT-001 és a HAMART-001 regressziós
  futtatása (pilot-terv 3. és 4. szakasz) külön ágon, a D6 szerint; az E28 erre építhet, de nem
  azonos vele (az E28 a commitolt nézetet nézi, az arany-készlet a generátor-változás hatását).
