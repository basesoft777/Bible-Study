# TBESH / TBESG — Translators Brief lexicon of Extended Strongs (Hebrew / Görög)

## Forrás

- **Projekt:** STEPBible-Data (https://github.com/STEPBible/STEPBible-Data)
- **Kiadó:** Tyndale House, Cambridge / STEPBible.org
- **Licenc:** CC BY 4.0
- **Fájlok:**
  - `TBESH.txt` — Lexicons/TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt
  - `TBESG.txt` — Lexicons/TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt
- **Letöltve:** 2026-09-01

## Mi ez a két fájl

- **TBESH** = Translators Brief lexicon of Extended Strongs for **Hebrew**. A rövidített (Abridged) BDB-n alapul (Online Bible kiadása), Tyndale House szerkesztésében, kiterjesztett Strong-számokhoz linkelve (visszafelé kompatibilis az eredeti Strong-számokkal, kiegészítve minden BDB-bejegyzéssel, előtagokkal, utótagokkal, névmási végződésekkel és írásjelekkel).
- **TBESG** = Translators Brief lexicon of Extended Strongs for **Greek**. A javított Abbott-Smith definíciókon alapul; ahol Abbott-Smish nem ad definíciót, ott MiddleLiddell (ML) vagy STEPBible-tudósok pótolják.
- Mindkettő ugyanabból az ökoszisztémából származik, mint a projektben már használt TAHOT/TAGNT (CC BY 4.0), így az attribúciós és licencfeltételek megegyeznek.

## Használati mechanizmus — study-vezérelt, kumulatív

**NEM kell előre feldolgozni a teljes fájlt.** Egy adott motívum vagy tanulmány írásakor, amikor egy konkrét Strong-számra van szükség:

```bash
grep "^H0001" konkordancia/TBESH.txt   # héber tétel
grep "^G1941" konkordancia/TBESG.txt   # görög tétel
```

A találatból csak a releváns sense(ek) kerülnek kiválasztásra és lefordításra, amelyek bekerülnek a study/motívum-cikk szövegébe. Ugyanez az elv, mint ami a `Karoli_Strong_kivonat.tsv`-nél már bevált gyakorlat — a lexikon egésze csak referencia-adatbázisként szolgál, nem kerül tömbösítve feldolgozásra.

## Héber↔görög híd

A héber↔görög kapcsolat **natívan benne van** a TBESG bejegyzéseiben — nem kell külön hídszó-táblát vezetni. Formátumok, amikkel találkozhatunk:

- `[in LXX chiefly for קָרָא ;]` — a görög szó elsődlegesen ezt a héber szót fordítja a Septuagintában
- `[In LXX (for HÉBER-SZÓ, ...; exc. ... for MÁSIK-HÉBER-SZÓ)]` — részletesebb, kivételeket is jelző forma

Ezek a jelölések a definíció szövegének elején, közvetlenül a szó grammatikai adatai után jelennek meg.

## Többsoros Strong-számok — döntést igénylő eset

Egy alap Strong-szám gyakran **több sort** kap. Például `H7121` (קָרָא) négy sort ad:

| Alsor | Gloss |
|---|---|
| `H7121G` | call to/invite/entreat |
| `H7121H` | call by/name |
| `H7121I` | call out/shout/announce |
| `H7121J` | read out/dictated |

Mind a négy alsor **ugyanazt az alap sense-listát ismétli** (1) to call, call out, recite, read, cry out, proclaim... stb.), csak eltérő súlyponti gloss-szal. Ezek tehát nem különböző jelentések, hanem ugyanannak a szónak különböző kontextus-specifikus felhasználási súlypontjai.

**Munkafolyamat-szabály minden TBESH/TBESG-alapú grep-nél:**

- `grep "^H####"` (vagy `^G####`) **minden alsort visszaad**, nem csak egyet.
- A study/motívum-cikk szerzőjének **explicit döntenie kell**, hogy a teljes alsor-készletet nézi-e át, vagy csak az első/"fő" sort használja.
- Ezt a döntést a study/cikk szövegében **rögzíteni kell**, ha BDB-árnyalat-jelölést használ, hogy két különböző tanulmány ne alkalmazzon következetlenül eltérő gyakorlatot ugyanarra a Strong-számra.

A chat-felületen futott TBESH-pilot (`TBESH_pilot_atmeneti_adatbazis.tsv`, 2026.08.31) az első alsort használta minden esetben (`grep -m1`) — ez egy működő, de **nem az egyetlen lehetséges konvenció**. Ha a mechanizmus véglegesül, ezt a választást explicit meg kell erősíteni vagy felülbírálni.

## Fájlformátum

Mindkét fájl tab-elválasztott (`\t`), UTF-8 kódolású szöveges fájl. A tényleges lexikon-adatok **nem a fájl elején kezdődnek**:

- `TBESH.txt`: a bevezető/dokumentációs sorok után az első valódi tétel (`H0001`) az **55. sorban** kezdődik.
- `TBESG.txt`: a bevezető sorok (és egy beágyazott név-jelölési példa, ld. "Herod") után az első valódi tétel (`G0001`) a **91. sorban** kezdődik.
- Mindkét fájl végén (`TBESH.txt` kb. a 11700+ sortól, `TBESG.txt` a G-tételek után) magyarázó lábjegyzet-blokk található az oszlopok jelentéséről és a rövidítésekről.

### Oszlopok sorrendje (8 mező, tab-elválasztva)

| # | Mező | Leírás | Példa (H0001) |
|---|------|--------|----------------|
| 1 | Strong-szám (bázis) | Az alap Strong-szám, amire a `grep "^H####"` / `grep "^G####"` illeszkedik | `H0001` |
| 2 | Kiterjesztett Strong-azonosító + kapcsolat típusa | Az adott értelemhez tartozó kiterjesztett kód, és ha van, a kapcsolat leírása (pl. `= a Part of`, `= a Name of`, `= combination of`, `= in Aramaic of`) | `H0001G =` |
| 3 | Hivatkozott/kapcsolt kiterjesztett kód(ok) | Az elsődleges vagy kapcsolódó kiterjesztett Strong-kód(ok); összetett bejegyzéseknél több kód is szerepelhet | `H0001G` |
| 4 | Eredeti szó (héber/görög írásmóddal) | A szó az eredeti nyelven | `אָב` |
| 5 | Átírás (transliteráció) | Latin betűs kiejtés-közelítő forma | `av` |
| 6 | Morfológiai kód | `Nyelv:Típus-Nem-Extra` formátum (Nyelv: A=arám, H=héber, G=görög, N=név; Típus: N=főnév, V=ige, A=melléknév stb.) | `H:N-M` |
| 7 | Gloss (rövid jelentés) | Egy-két szavas alapjelentés | `father` |
| 8 | Teljes definíció | A BDB (héber) vagy Abbott-Smith/MiddleLiddell (görög) alapú, számozott értelmezés-lista, HTML-szerű jelölésekkel (`<br>`, `<BR>`, `<i>...</i>`, `<b>...</b>`, `<ref='...'>`) | `1) father of an individual<br>2) of God...` |

### Formátum-eltérések és sajátosságok

- **Több sor egy Strong-számhoz:** egy alap Strong-szám (1. mező) több sort is kaphat, ha a szónak több különálló értelme/kiterjesztett kódja van (pl. `H0001` → `H0001G`, `H0001H`, `H0001I` külön sorokban, tulajdonnévi és köznévi jelentésekkel).
- **Összetett hivatkozások:** a 3. mezőben előfordulnak vesszővel elválasztott több kód (`H2438H, ` — záró vessző+szóköz maradvánnyal), illetve zárójeles összetételek (`H0022G (H0001I+H1391)`).
- **Névtételek (Person/Place):** tulajdonnevek esetén (`N:N-M-P` stb.) a 8. mező genealógiai/történeti jegyzeteket, kereszthivatkozásokat (más néven említett alakok) és névetimológiát (`§ Abigail = "my father is joy"`) is tartalmaz, nem csak szótári definíciót.
- **Nincs explicit oszlopfejléc-sor** a tétel-blokk tetején — az oszlopok jelentése csak a fájl végén lévő szöveges magyarázatban van dokumentálva.
- **TBESG appendix-tartalom:** a TBESG fájl elején (a 91. sor előtt) egy beágyazott, eltérő oszlopszámú példa-blokk található (személyek/helynevek jelölési konvenciójának bemutatására, pl. "Herod" család) — ez nem tartozik a fő G-tétel-listához, és `grep "^G####"` nem érinti.
- **Nyelvtani elemek (TBESH vége felé, H9000+ tartomány):** ragok, névmási végződések, írásjelek önálló "Strong-számként" (pl. `H9020`–`H9049`) — ezek nem szótári tételek, hanem morfológiai komponensek.

## `TBESH_konszolidalt.tsv` — a TBESH.txt és a TBESH.lexicon uniója (SZOTAR_BRIEF.md S4)

**Generált** (`eszkozok/tbesh_konszolidalt_import.py`, kézzel nem szerkesztendő):
**unió, nem csere** — egyik forrás sem váltja ki a másikat, mert szócikkenként
hol az egyik, hol a másik bővebb (§0 0.5 mérés). Fejléc: `strong alap_strong
lemma atirat pos_kod rovid_glosszak teljes_szoveg forras txt_hossz
lexicon_hossz`.

- `strong` — a STEP-forrás saját kulcsa; **betű-utótaggal is lehet** (pl.
  `H7121a`), ha a forrás egy Strong-számot több alszócikkre/
  mikro-jelentésre bont (l. lent, F05/D-UT1). A kulcs önmagában NEM mindig
  a 4-jegyű alapszám.
- `alap_strong` — a 4-jegyű Strong-szám, betű-utótag nélkül. Ha az
  alapszámhoz több sor is tartozik (egy alaptétel + N alszócikk), a
  downstream kód **ezen** az oszlopon keresztül illesszen, ha alapszám
  szerint keres — nem a `strong` oszlopon, aminek nem minden alapszámhoz
  van pontos (utótag nélküli) megfelelője.
- `teljes_szoveg` / `forras` — a `TBESH.txt` (az adott **kulcs** — alapszám
  vagy egy adott betű-utótag — összes alsorának dedupikált,
  HTML-mentesített definíciója) és a `konkordancia/lexikonok_nyers/
  TBESH.lexicon` (SQLite, egyetlen konszolidált HTML-bejegyzés ugyanerre a
  kulcsra) közül a **hosszabb tisztított szöveg** — `forras` jelzi, melyik
  (`txt` / `lexicon` / `egyenlo`, ha a különbség ≤5%).
- `rovid_glosszak` — csak a `.txt`-ben elérhető: az adott kulcs összes
  alsorának rövid glosszája (7. mező), pontosvesszővel összefűzve — ez a
  szócikk mikro-jelentéseinek listája, amit a `.lexicon` nem tartalmaz
  külön.
- `lemma` / `atirat` / `pos_kod` — a `.txt` 4./5./6. mezője; ha a szó csak a
  `.lexicon`-ban szerepel, ezek üresek (a `.lexicon` nem tartja külön ezeket
  a mezőket).

**Betű-utótagos kulcsok (F05, D-UT1, 2026.09.29 — javítás egy független
ellenőrzés nyomán):** mindkét forrás egy Strong-számot időnként több,
betű-utótagos alszócikkre bont (pl. `H1121` "ben" a `TBESH.txt`-ben
KIZÁRÓLAG `H1121a`/`H1121b` alakban létezik, sima `H1121` sosem — a szó
"gyermek/fiú" és "kinsfolk" jelentése két külön alszócikk). A korábbi
szigorú `^H\d{4}$` szűrő ezeket a kulcsokat egyáltalán nem ismerte fel
Strong-kulcsként, és **szó nélkül eldobta** — 1424 nyers `.txt`-sor és a
megfelelő `.lexicon`-bejegyzések vesztek el így, összesen **542 Strong-szám
`.txt`-oldali tartalma** (ezek alapszáma máig is csak a `.lexicon`-ból
adatosított, `forras=lexicon`), köztük **5 motívum-tokené** (`H1121`,
`H2403`, `H2416`, `H7451`, `H7497`). A javítás: a szűrő (`STRONG_H_RE`)
mostantól elfogadja az opcionális egybetűs utótagot is, a betű-utótagos
kulcs **saját sorként marad meg** (nem olvad össze az alapszámmal — a
tartalom nem egyesíthető félreértés nélkül), az `alap_strong` oszlop köti
vissza az alapszámhoz. Ellenőrizve: mind az 1424 nyers `.txt`-sor
importálódik, és mind az 542 érintett alapszámnál elérhető a `.txt`-tartalom
(a saját, betű-utótagos sorában).

**Kiszűrve: a `H9xxx` tartomány.** A `TBESH.txt` saját fejléce szerint az
Extended Strongs a "prefixes, suffixes, personal pronoun endings and
punctuation" jelölésére is `H9xxx`-kódokat használ — ugyanaz a konvenció,
mint az `adat/grammatikai_strongok.tsv` `H9xxx`-szűrése (SEMA 2.7.2) —,
ezek nem szótári tételek.

**Normalizálva, nem kiszűrve: a nem nullával töltött kulcsok.** A
`TBESH.lexicon` egy részét (pl. `H9`, `H90`, `H900`, `H122`) nem 4 jegyű,
nullával nem töltött alakban tárolja — ezek **valódi** Strong-kulcsok
(pl. `H9` tartalma szó szerint egyezik a `TBESH.txt` `H0009` sorával), nem
a forrás saját prefix-indexei, ahogy egy korábbi mérés feltételezte
(l. `naplok/S1_TBESH_kiszurt_elemzes.md`). A szűrés előtt egy
`normalizal()` lépés `zfill(4)`-gyel 4 jegyre tölti a csak-számjegyekből
álló nyers kulcsot (`H122` → `H0122`), így ezek is bekerülnek a táblába,
és a `konszolidal()` hossz-alapú forrásválasztásába is — 35 korábban
teljesen hiányzó Strong-szám mentődött meg ezzel, és 509 már meglévő sor
tartalma frissült `txt`-ről `lexicon`-ra (mert korábban a lexikon-változat
sosem jutott be az összehasonlításba).

Mért értékek (2026.09.29, a `H9xxx`-kizárás, a nullával-töltés
normalizálása és a betű-utótag-javítás után): **9 838 sor** (1 csak
`.txt`, 542 csak `.lexicon`, 3 404 mindkettő + `.txt` bővebb, 5 783
mindkettő + `.lexicon` bővebb, 108 kb. egyenlő). A D28 hatókörébe tartozó
26 motívum-token **alapszám-sorára** (a betű-utótagos alszócikkeket nem
számolva) a bontás: **8 `txt`, 16 `lexicon`, 2 `egyenlo`** (eltér a §0 0.5
24-tokenes, kézi mérésétől, és a korábban itt közölt 11/13/2 számtól is —
ez utóbbi elavult volt, l. `naplok/ELLENOR_SZOTAR_S1.md`; ez a szám a
jelenlegi, teljes körű, automatizált mérés).

## Attribúció

Minden felhasználásnál (motívum-cikkben, tanulmányban, jegyzetben) fel kell tüntetni:

> STEPBible-Data (TBESH/TBESG), CC BY 4.0, Tyndale House, Cambridge / STEPBible.org
