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

## Attribúció

Minden felhasználásnál (motívum-cikkben, tanulmányban, jegyzetben) fel kell tüntetni:

> STEPBible-Data (TBESH/TBESG), CC BY 4.0, Tyndale House, Cambridge / STEPBible.org
