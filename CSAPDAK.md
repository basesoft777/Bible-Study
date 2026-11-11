# Csapdák — a CLAUDE.md szabályainak indoklása és részletei

*A `CLAUDE.md` minden kérésben betöltődik, ezért ott csak a szabály áll, egy-két sorban. Az indoklás, a mért kár és a részletek itt vannak (F189, 2026-11-11). A szabály helye továbbra is a `CLAUDE.md`. Ha a kettő eltér, a `CLAUDE.md` az irányadó. Ezt a fájlt akkor nyisd meg, ha a szabály oka vagy a részlete kell.*

## Shell — miért fájlból fut a héber/görög/magyar kód

*Szabály: `CLAUDE.md` „Shell”.*

Ok: a transzliterációk aposztrófjai (*Pi'él*, *Nif'ál*, *Hif'íl*, *bené ha-elohim*)
**törik a shell idézőjelezését**. A hiba nem a kódban jelenik meg, hanem parse-hibaként
(`unexpected EOF while looking for matching`), tehát a szkript **el sem indul** — és ha
egy `&&`-lánc közepén áll, a lánc korábbi tagjai már lefutottak. Ugyanez vonatkozik a
heredocra is: az idézett határoló (`<<'EOF'`) sem véd meg minden esetben.

```bash
# HELYES: fájlba írás, majd futtatás
python eszkozok/valami.py
```

Ez a magyar kimenetre is áll: `PYTHONIOENCODING=utf-8` nélkül a Windows-konzol
`cp1250` kódlapja `UnicodeEncodeError`-t dob a héber és görög karakterekre.

Ezt ne a hívóra bízd: minden `eszkozok/*.py` a docstringje után, az importok után
ráteszi magára a wrappert —

```python
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
```

— így a szkript csupasz `python eszkozok/valami.py` hívásra is helyes. A
`PYTHONIOENCODING` ezután tartalék, nem előfeltétel.

(Az őr az importblokk *után* álljon, ne előtte — ha az `import sys` a wrapper
alatt van, a wrapper `sys.`-használata `NameError`-ral bukik, mielőtt bármi
lefutna. Dokumentált eset: `lekerdez.py`, `grammatikai_strongok_general.py`,
`tahot_lefedettseg_ellenoriz.py`, l. `F4_BRIEF.md` „Tétel E".)

## Az olvasó-szerver tesztjei

*Szabály: `CLAUDE.md` „Shell”.*

Az olvasó-szerver tesztjei (`eszkozok/olvaso_szerver/teszt_*.py`) csak `python eszkozok/teszt_futtat.py` hívással futnak (Windowsról és WSL-ből is, `--gyors`: a lassú `teszt_szintek.py` nélkül): a WSL venv-jét és a WSL-natív `~/pardes/pardes.db`-t választja, kiírja, melyik adatbázist nyitotta meg, és figyelmeztet, ha az a `/mnt/c` alatt van; `PARDES_DB` nélküli kézi futtatás a `/mnt/c`-ről 45+ perc (#100, DT160).

## TSV-olvasás — miért nem használható a `csv` modul

*Szabály: `CLAUDE.md` „TSV-olvasás”.*

A `csv.reader` / `csv.DictReader` / `csv.writer` ezeken a fájlokon adatot ront, mert a
mezők szabad magyar szöveget tartalmaznak idézőjelekkel, a `csv` pedig ezt
idézés-szintaxisnak veszi. Két külön kár, és külön is jelentkeznek:

| | Mit csinál | Mért hatás az `elofordulasok.tsv`-n |
|---|---|---|
| **olvasás** (`csv.reader`) | az idézőjellel kezdődő mezőről leszedi az idézőjeleket | **79 mező, 79 soron** — mind a `kapcsolodas` oszlopban |
| **írás** (`csv.writer`) | a `"` jelet tartalmazó mezőt körülidézi és belül duplázza | **127 sor** változna egyetlen körúttól |

Az olvasási kár akkor is megtörténik, ha a szkript nem ír vissza semmit — a `gate.py`
és a `lekerdez.py` ma is megcsonkított `kapcsolodas`-értéket lát. Ez eddig nem
számított, mert egyik sem dolgozik ezzel a mezővel; **a generátornak viszont számítani
fog**: a `kapcsolodas` idézőjelei határolják el a szó szerinti igeidézetet a
magyarázattól, és 79 igehelynél némán eltűnnének a generált motívumnaplóból.

*Miért ez a legveszélyesebb a három csapda közül:* a shell-hibánál a szkript el sem
indul, a `cp1250`-nél a kimenet dobja el magát — itt viszont **minden hibátlanul
lefut**, és a kár csendben a kanonikus táblában marad. A hiba nem ott jelentkezik,
ahol keletkezik.

Egyik mező sem tartalmaz tabot, tehát a szétvágás egyértelmű.

## A TAHOT-kivonat mért állapota (F85)

*Szabály: `CLAUDE.md` „Adat-tár”.*

**`TAHOT_kivonat.tsv`: a mért állapot (F85, 2026.10.09).** Fejezet-szinten nincs hiány (`eszkozok/tahot_lefedettseg_ellenoriz.py`): a Zsolt 88/89/140/142-t, az 1Móz 32-t és a Jóel 3-at az F2 pótolta (2026.09.14), a Jób 41-et az F84 (332 sor, `naplok/F84_jelentes.md`); a Jób 40:1–5 nem hiányzik. Az `Igehely` kulcs az F85.6 óta (versszintű átkulcsolás, 337 vers, 6 330 sor) maga a **Károli-vers**, amelynek a héber szövegét a sor hordozza: a korábbi eltolások (Jób 40 +5, fejezethatáron és fejezeten belül Préd 2, Hós 2/12, Ézs 9, Dán 4, Én 6, 2Móz 36, 4Móz 30, Péld 12, …) megszűntek (`naplok/F85_jelentes.md`, `naplok/F85_igazolas.md`). A versszintű kulcs-összevetés (Károli-vers ↔ TAHOT-kulcs, teljes ÓSZ: 23 204 kulcs, 0 Károli-vers nélküli TAHOT-kulcs, 0 TAHOT-sor nélküli ÓSZ-Károli-vers) naplózva: `naplok/F85_kulcsosszevetes.md`. Két tudnivaló: ahol a Károli két TAHOT-verset egy versbe vont (9 hely), mindkét vers a közös Károli-kulcson áll (a vershatár: `f22/versosszevonas.tsv`); a fájlsorrend nem Károli-sorrend (áthelyezett blokkok), ezért kulcs szerint olvass.

## Git — miért fájlból megy a commit-üzenet, és miért tétel-szintű

*Szabály: `CLAUDE.md` „Git”.*

A granularitás **tétel-szintű, nem fázis-szintű**: az `F3` nem egy commit, hanem `F3.0:`,
`F3.1:`, `F3.2:` … külön-külön. Ok: a piszkozatot termelő lépéseknél a commit a validálás
visszapontja, és a `git log --oneline` csak így marad olvasható.

Az üzenet **mindig UTF-8 fájlból megy, soha nem inline `-m`-mel**:

```bash
git -c i18n.commitEncoding=UTF-8 commit -F commit_uzenet.txt
```

Két ok. Egy: a Windows-konzol `cp1250` kódlapja az inline `-m` ékezeteit elnyelheti —
ugyanaz a kockázat, amit a fenti shell-szakasz a szkriptekre rögzít. Kettő, és ez a
fontosabb: a fájlba írt üzenet szem előtt van íráskor, tehát az ékezetek kitétele nem
múlik a gépelési kényelmen. Az ékezetlen üzenet ugyanis nem kozmetikai kérdés — kiüti a
`GitHub_feltoltesi_workflow.md`-ben rögzített célt, a `git log --grep` tartalmi
kereshetőségét: a `--grep="betöltés"` nem találja meg a „betoltes"-t.
