# F4-0 brief — a `csv` modul kiváltása és a stderr-őr egységesítése

*Készítette: chat-menet (Opus 5), 2026-09-14, v6 (v5-ig l. a döntésnaplót; v6: E5 visszavonva, E11 .gitattributes-szal, Tétel B a HEAD-blobhoz mér). Kiindulási állapot: `main` = `origin/main` = `28ae8d4`.*
*Végrehajtás: Claude Code, a repó gyökeréből. A chat-menet nem hajtja végre — ez a brief a bemenete.*

---

## 0. Miért ez az F4 nulladik tétele

Az `ATALAKITASI_TERV.md.md` 446. sora szerint az F4 a **generátorokról** szól
(`general.py`: motívumnapló, index, tematikus study 1. pontja, kereszthivatkozás-naplók).
A generátor a `kapcsolodas` oszlopból dolgozik — abból a mezőből, amelyet a `csv`
olvasás ma **némán megcsonkít**. Ezért a csv-kiváltásnak a generátor megírása *előtt*
kell megtörténnie, különben az F4 elfogadási tesztje („a generált `PaRDeS_motivumok.md`
diffje csak formázási eltérést mutasson") hamis zöldet ad: a hiányzó idézőjelek
formázási eltérésnek látszanak, pedig tartalmiak.

A szabály már ki van mondva (`CLAUDE.md`, „TSV-olvasás" szakasz, `535a695`), de a kód
még nem követi.

---

## 1. Mért kiindulási állapot

Minden szám alatta független méréssel készült a `28ae8d4` munkapéldányán,
nem a korábbi menet jelentéséből átvéve.

### 1.1 A csv-modul jelenléte

| | érték |
|---|---:|
| `eszkozok/*.py` összesen | 24 |
| `csv.*` hívási hely összesen | **49** |
| ebből olvasó (`csv.reader` / `csv.DictReader`) | 39 |
| ebből **író** (`csv.writer` / `csv.DictWriter`) | **10** |
| érintett szkript | 20 |
| ebből író szkript | 8 |

(A 21. érintett fájl, az `igazolas_migracio.py`, csak a docstringjében említi a
`csv`-t — ott a `split('\t')` már helyesen van megírva. Ez a minta-implementáció.)

### 1.2 A tényleges kár a kanonikus táblán

`adat/elofordulasok.tsv`, 201 adatsor, 16 oszlop. A `csv.DictReader` kimenetét
soronként-mezőnként összevetve a `split('\t')` kimenetével:

| | érték |
|---|---:|
| eltérő mező | **79** |
| ebből a `kapcsolodas` oszlopban | **79 (100 %)** |
| egyéb oszlopban | 0 |
| érintett sor | **79** |
| sorszám-torzulás (DictReader vs. nyers) | **0** |
| tabot tartalmazó mező | 0 |

A kár alakja mindenütt ugyanaz: a mezőt nyitó és záró `"` **eltűnik**, a mező
belseje sértetlen. Példa (2. adatsor, `kapcsolodas`):

```
fájlban :  "Sálemben van az ő sátora, és lakóhelye Sionban" — a Sálem=Jeruzsálem…
DictReader: Sálemben van az ő sátora, és lakóhelye Sionban — a Sálem=Jeruzsálem…
```

Ez a `CLAUDE.md` táblázatának „79 mező, 79 soron" állítását **pontosan** igazolja.
Mivel egyetlen mező sem tartalmaz tabot, a `split('\t')` szétvágás egyértelmű.

### 1.3 A stdout/stderr-őr állapota

| | érték |
|---|---:|
| **stdout**-őr megvan | **24 / 24** |
| ebből `sys.stdout.reconfigure(...)` | 16 |
| ebből `sys.stdout = io.TextIOWrapper(...)` | 8 |
| **stderr**-őr megvan | **3 / 24** |
| nem-ASCII szöveget ír a stderr-re, őr nélkül | **3 szkript** |

A három érintett: `lekerdez.py` (8 hívási hely), `kockazat_szures_18_tanulmany.py` (1),
`tahot_karoli_kulcs_generalas.py` (1).

**Ez nem okoz leállást.** A CPython a `sys.stderr`-t alapból `backslashreplace`
hibakezelővel nyitja, tehát kivétel helyett escape-elt kimenet keletkezik.
Mérve, `tűnődő őrült` szövegre:

| konzol-kódlap | a stderr-re kiírt bájtok |
|---|---|
| `cp437` (US alap) | `tűnődő őr\x81lt` — escape-elve |
| `cp852` (magyar DOS) | hibátlan |
| `cp1250` (magyar Windows) | hibátlan |

Következmény tehát olvashatatlan hibaüzenet egy US-kódlapos konzolon —
kozmetikai, de pont a hibaágon üt.

### 1.4 Amit a munkapéldány igazol a `28ae8d4`-ről

| állítás | státusz |
|---|---|
| `main` = `origin/main` = `28ae8d4` | ✅ mindkét ref bájtra azonos |
| ív `cf85aa7` → `bac1f5d` → `535a695` → `28ae8d4` | ✅ a reflog ebben a sorrendben |
| `py_compile` mind a 24 fájlra | ✅ hibátlan |
| a két LXX-letöltő sorvégei megtartva | ✅ 501 ill. 634 CRLF, magányos LF 0 |
| a `stdout` sor a `stderr` fölé, azonos `errors="replace"` | ✅ 429/430 ill. 493/494 |
| D25: `proveniencia` = `scope \| forras \| ts` | ✅ 201/201 sor, `talalat=`/`strong_vart=` maradék: 0 |
| D25: `igazolas` oszlop zárt értékkészlettel | ✅ `TAHOT-igazolt` 138, `nincs` 38, `TAHOT-hatokoron-kivul` 25 |

Egy pontosítás a jelentéshez: a *„mind a 24 futtatható csupasz `python` hívással"*
mondat a **stdout**-ra igaz, és arra teljesen. A stderr-ágon 21 szkript őrizetlen
(l. 1.3) — ezért kerül be a 4. tétel.

---

## 2. Mit kell csinálni

### Tétel E — import-sorrend javítása (3 szkript) — **ELŐFELTÉTEL, mindenki előtt**

*Felvéve v3-ban, 2026-09-14, az E7 baseline-mérés közben derült ki.*

Három szkriptben a stdout-őr **`sys.`-t használ az `import sys` előtt**, tehát
`NameError: name 'sys' is not defined`-del bukik, még mielőtt az argparse
elindulna. Nem a 8 alparancs fagy le külön-külön: a modul be sem töltődik.

| szkript | `import sys` | 1. `sys.`-használat |
|---|---:|---:|
| `lekerdez.py` | 26. sor | **19. sor** |
| `grammatikai_strongok_general.py` | 38. sor | **32. sor** |
| `tahot_lefedettseg_ellenoriz.py` | 17. sor | **13. sor** |

Futtatással igazolva: mind a 24 szkript `--help`-pel indítva, pontosan ez a
három dob `NameError`-t, a többi 21 nem. A `py_compile` ezt **nem fogja meg** —
szintaktikailag hibátlan kód, a hiba futásidejű. A `28ae8d4` jelentésének
„py_compile OK" sora tehát igaz volt, csak nem erre a hibaosztályra vonatkozott.

**A hiba forrása a `CLAUDE.md` szabályszövege**, nem a három fájl: a „Shell —
kötelező munkamódszer" szakasz azt írja, az őr *„a docstringje után, az importok
**előtt**"* kerüljön a fájlba. A repó 21 működő szkriptje viszont az ellenkezőjét
csinálja — ott az őr az importblokk **után** áll (pl. `gate.py`: `import sys` a
25., őr a 27. soron). A `535a695` commit a szabályszöveget követte, és ezzel
törte el a három fájlt.

Ezért a javítás két részből áll, és **együtt** kell menniük:

1. A három fájlban az őr kerüljön az importblokk **alá** — ez a repó tényleges,
   21 fájlon működő konvenciója. Ne az `import sys`-t told feljebb: az
   kettéhasítaná az importblokkot, és a következő szerkesztő visszarendezné.
2. A `CLAUDE.md` „Shell — kötelező munkamódszer" szakaszában az *„importok
   előtt"* javítandó *„importok után"*-ra, a kódmintával együtt. Enélkül a
   következő wrapper-kiterjesztés (a D tétel!) újratermeli a hibát.

Amit a Code-menet nézzen meg és jelentsen: `git log -p -1 535a695 --
eszkozok/lekerdez.py` — ha a `lekerdez.py` a `535a695` 13 szkriptje közt volt,
akkor **a hiba akkor keletkezett, és azóta a `lekerdez.py` egyszer sem futott le**.
Ez jó hír: nem szennyeződött tőle semmilyen korábbi kimenet, csak nem készült.
Ha viszont régebbi, akkor meg kell nézni, mely korábbi menetek hivatkoztak rá.


#### E/2 — a füstteszt módja *(v4, 2026-09-14 — a v3 rossz módszert írt elő)*

**A v3 azt kérte, hogy mind a 24 szkript induljon `--help`-pel. Ez hibás
utasítás volt, és kárt okozott.** Huszonnégyből csak öt szkript használ
`argparse`-t (`gate.py`, `lekerdez.py`, `inline_strong_megjelenito.py`,
`lxx_kivonat_fetch.py`, `lxx_kivonat_fetch_v2.py`) — a maradék tizenkilencnél a
`--help` nem súgót ír, hanem **lefuttatja a teljes szkriptet**. A betöltők pedig
felülírják a kanonikus táblákat: a `f3_1_betoltes.py` a 391-394. sorban négy
`adat/*.tsv`-t ír, a `f3_2_betoltes.py` az 534-536.-ban hármat, a
`merge_karoli_szofaj.py` a 48.-ban a `konkordancia/Karoli_Strong_kivonat.tsv`-t
írja felül helyben, `csv.writer`-rel.

A `if __name__ == "__main__":` őr itt **nem véd**: az csak importáláskor
akadályozza a futást, közvetlen hívásnál nem.

Helyette: **`eszkozok/import_sorrend_ellenoriz.py`** — AST-alapú, a modult be sem
tölti, tehát mellékhatása nincs. Modulszinten összeveti minden név első
olvasását az első kötésével, a függvény- és osztálytörzseket kihagyva. A
`28ae8d4`-en futtatva pontosan a három ismert fájlt adja, téves riasztás nélkül
(az `import csv, sys, os, io, re` alakot is helyesen kezeli, amit a soralapú
grep elnéz).

```
python eszkozok/import_sorrend_ellenoriz.py     # kilépési kód 1, ha van hibás fájl
```

#### E/3 — a félrefutott füstteszt utáni helyreállítás

Ha a `--help`-teszt már lefutott a munkafán, a helyreállítás **ne csak a
szembetűnő fájlokra menjen**. Előbb a teljes kép:

```
git status --porcelain
git diff --stat
```

A várhatóan érintettek: `adat/motivumok.tsv`, `adat/elofordulasok.tsv`,
`adat/jeloltek.tsv`, `adat/kapcsolatok.tsv`, `konkordancia/Karoli_Strong_kivonat.tsv`,
`eszkozok/f3_4_munkalap.tsv`, `sablonok/Kockazat_szures_riport*.md`, és bármi a
`naplok/` alatt, ami nem a szándékos baseline.

Ez **nem kozmetika.** A `f3_1_betoltes.py` az F3.1 kori, beégetett tartalomból
írja újra az `elofordulasok.tsv`-t — az a D25 `igazolas` oszlopa és az F3.4 join
előtti állapot. Ha ez a változat marad a munkafában, az egy csendes
adatregresszió, amit a következő commit visszavinne a `main`-re.

Helyreállítás a **követett** fájlokra (az új, még nem követett baseline-fájlokat
a `checkout` nem bántja):

```
git checkout -- adat/ konkordancia/ sablonok/ eszkozok/f3_4_munkalap.tsv
```

Utána igazold: `git diff --stat` az `adat/`, `konkordancia/` és `sablonok/`
alatt legyen **üres**, és a `git status` már csak a szándékos kódváltozásokat
mutassa.


Commit: `F4.0-elo`, még a kármérés előtt. A javítás után **újra kell futtatni**
az E7 baseline-t — a mai `naplok/F4_0_baseline_lekerdez.txt` csak a NameError-t
tartalmazza, az nem viszonyítási alap.

---

### Tétel A — `csv` kiváltása az olvasókban (39 hely, 18 szkript)

Minden `csv.reader` / `csv.DictReader` helyére nyers szétvágás lép. A javasolt
közös alak (a `gate.py`-ban és a `lekerdez.py`-ban már ma is egy-egy segédfüggvény,
ott egyetlen függvénytörzs cseréje elég):

```python
def read_tsv(path, skip_comments=False):
    """TSV-olvasás a csv modul nélkül — l. CLAUDE.md, „TSV-olvasás".

    A mezők szabad magyar szöveget tartalmaznak idézőjelekkel; a csv modul ezt
    idézés-szintaxisnak veszi, és a kapcsolodas oszlop 79 sorában leszedi a
    határoló " jeleket. Egyetlen mező sem tartalmaz tabot, a szétvágás egyértelmű.
    """
    with open(path, encoding="utf-8") as f:
        sorok = [ln.rstrip("\n").rstrip("\r") for ln in f]
    if skip_comments:
        sorok = [s for s in sorok if not s.startswith("#")]
    sorok = [s for s in sorok if s.strip()]
    fejlec = sorok[0].split("\t")
    ki = []
    for i, s in enumerate(sorok[1:], start=2):
        mezok = s.split("\t")
        if len(mezok) != len(fejlec):
            raise ValueError(
                "%s %d. sor: %d mező a fejléc %d mezője helyett"
                % (path, i, len(mezok), len(fejlec)))
        ki.append(dict(zip(fejlec, mezok)))
    return ki
```

Két megkötés, amit a csere **nem** ronthat el:

1. **A hossz-ellenőrzés kötelező.** A `csv.DictReader` a rövid sort `None`-nal
   tölti fel, a `zip` némán levágja. Ezért van a `raise` — ez a csere egyetlen
   viselkedésbeli szigorítása, és szándékos.
2. **A `#`-kezdetű sorok kezelése marad, ahol ma is van** (`gate.py:45`,
   `lekerdez.py:51`). A `lekerdez.py`-ban két külön olvasó van (`read_tsv` és
   `read_tsv_skip_comments`) — ezek összevonhatók a fenti kapcsolóval, de a
   hívási helyeket akkor át kell nézni.

Ahol a mai kód `csv.reader`-rel listát olvas (nem szótárat), ott a helyettesítés
`s.split("\t")` — a `next(r)` fejléc-átugrás megfelelője a `sorok[1:]`.

### Tétel B — `csv` kiváltása az írókban (10 hely, 8 szkript)

Ez a nagyobb kockázat, mert **irreverzibilis**: a `csv.writer` a `"` jelet
tartalmazó mezőt körülidézi és belül duplázza. A `CLAUDE.md` szerint egyetlen
körút 127 sort változtatna az `elofordulasok.tsv`-n. A `merge_karoli_szofaj.py`
a legveszélyesebb: ugyanazt a `KIVONAT_PATH` fájlt olvassa (26., 37. sor) és
**írja felül helyben** (49. sor).

Helyettesítés:

```python
with open(ut, "w", encoding="utf-8", newline="") as f:
    f.write("\t".join(fejlec) + "\n")
    for sor in sorok:
        assert not any("\t" in str(v) for v in sor), "tab a mezőben: %r" % (sor,)
        f.write("\t".join(str(v) for v in sor) + "\n")
```

Sorvég: `\n`, mert a mai `csv.writer` hívások mind `lineterminator="\n"`-nel
mennek — a csere ne változtasson sorvéget.

**Kötelező: bájt-szintű körút-ellenőrzés — a HEAD-blobhoz, nem a munkafához.**
Minden táblát író szkript vesse össze a kimenetet az eredetivel, és **eltérésnél
álljon meg** (`CLAUDE.md` zárómondata; minta: `eszkozok/igazolas_migracio.py`).

*Javítva v6-ban:* a referencia a `git show HEAD:<fájl>` kimenete legyen, **ne** a
munkafában lévő fájl. Ok: a repó `core.autocrlf=true`-val megy, tehát a munkafa
sorvége checkoutonként változhat, és egy CRLF-es munkapéldány ellen mérve a
körút hamis eltérést — vagy fordítva, hamis egyezést — mutat. A blob a
viszonyítási alap, mert a commit is oda kerül.

### Tétel C — a `konkordancia/` mérése (a B tétel előfeltétele)

A `konkordancia/` 387 MB / 17 dataset — a chat-menet nem tudta megmérni.
**A Code-menet első lépése ez legyen, még a csere előtt:** minden
`konkordancia/*.tsv`-re számold ki, hány mezőn tér el a `csv.reader` kimenete a
`split('\t')` kimenetétől, és melyik oszlopban. Az eredmény menjen a
`naplok/F4_0_csv_karmeres.tsv`-be (`fajl | sorok | oszlopok | eltero_mezo |
eltero_sor | erintett_oszlopok`). Ez adja meg, hogy a csere mit kell helyreállítson
— és ez a B tétel elfogadási alapja.

Ha egy tábla eltérése **0**, azt is írd bele: az a bizonyíték, hogy ott a csere
bájtra semleges.

### Tétel D — stderr-őr egységesítése (21 szkript)

Ugyanoda, ahol a stdout-őr már áll, kerüljön a stderr párja, a fájlban meglévő
alakkal egyezően:

```python
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
```

…illetve a `TextIOWrapper`-es fájlokban a `TextIOWrapper`-es párja. A `CLAUDE.md`
„Shell — kötelező munkamódszer" szakaszának kódmintáját is egészítsd ki a stderr
sorral, különben a szabály és a kód megint szétcsúszik.

---

## 3. Elfogadási kritériumok

Mindegyik **mérés**, nem szemrevételezés. A számokat a Code-menet futtassa és
írja a commit-üzenetbe.

| # | Kritérium | Elvárt |
|---|---|---:|
| E1 | `grep -rn "csv\.\(reader\|DictReader\|writer\|DictWriter\)" eszkozok/*.py` | **0 találat** |
| E2 | `python -m py_compile eszkozok/*.py` | hibátlan |
| E3 | `adat/elofordulasok.tsv`: `kapcsolodas` mezők, amelyek `"`-rel kezdődnek és végződnek | **79** (változatlan) |
| E4 | `git diff --stat` az `adat/` és `konkordancia/` alatt | **üres** — a csere kódot érint, adatot nem |
| ~~E5~~ | ~~`eszkozok/*.py` sorvégei~~ | **visszavonva v6-ban** — `core.autocrlf=true` mellett a munkafa sorvége nem hordoz információt; a blob számít, azt pedig az E4 már őrzi |
| E11 | `adat/*.tsv` és `konkordancia/*.tsv` a munkafában | **LF**, és ezt `.gitattributes` kényszerítse ki (`*.tsv text eol=lf`), ne egyszeri kézi normalizálás |
| E6 | `naplok/F4_0_csv_karmeres.tsv` | létezik, minden `konkordancia/*.tsv`-re van sora |
| E7 | `gate.py` és `lekerdez.py` futtatva, kimenet összevetve a csere előttivel | **tartalmi diff nulla** (csak időbélyeg) — l. lent |
| E8 | stderr-őr `eszkozok/*.py`-ban | **24 / 24** |
| E9 | `python eszkozok/import_sorrend_ellenoriz.py` | **kilépési kód 0** (ma: 1, három fájl) |
| E10 | `git diff --stat` az `adat/`, `konkordancia/`, `sablonok/` alatt az E tétel után | **üres** — a füstteszt mellékhatásai helyreállítva |

**E7 — javítva v5-ben.** A v1-v4 azt írta, a diffnek pontosan 79 mezőt kell
érintenie. Ez hibás elvárás volt: a `CLAUDE.md` maga mondja ki, hogy *„egyik sem
dolgozik ezzel a mezővel"* — a `gate.py` és a `lekerdez.py` nem írja ki a
`kapcsolodas`-t, tehát a helyes eredmény **nulla tartalmi diff**. Az E7 így
regressziós teszt, nem a javítás bizonyítéka.

A javítás bizonyítéka az **E3**: a `csv.DictReader` és a `split('\t')` kimenetét
a mai fájlon összevetve 79 mezőnek kell eltérnie, mind a `kapcsolodas`-ban — ez
mutatja, hogy a régi olvasó tényleg rontott, az új pedig nem.

**Ha az E4 nem üres:** állj meg és jelents. Az azt jelenti, hogy egy író szkript
már a csere előtt is módosított egy táblát, vagy a csere nem bájthű — mindkettő
vizsgálandó, egyik sem elfedendő.

---

## 4. Commit és push

`CLAUDE.md` szerint: munkaág `main`, magyar commit-üzenet, tétel-azonosítóval
kezdve, **tétel-szintű granularitás** — tehát nem egy commit, hanem öt:

```
F4.0-elo: import-sorrend javítása 3 szkriptben + a CLAUDE.md szabályszöveg
F4.0a: a csv-olvasók kiváltása split('\t')-re (39 hely, 18 szkript)
F4.0b: a konkordancia-táblák csv-kármérése
F4.0c: a csv-írók kiváltása '\t'.join()-ra, bájthű körút-ellenőrzéssel
F4.0d: stderr-őr kiterjesztése mind a 24 eszkozok/*.py-ra
```

Sorrend: **E (import-sorrend) → C (kármérés) → A (olvasók) → B (írók) → D (stderr)**.
Az E mindenki előtt, mert nélküle a `lekerdez.py` el sem indul, tehát az E7
baseline nem rögzíthető. A kármérés a csere előtt kell, különben nincs mihez mérni.

Az üzenetet **UTF-8 fájlból** add át (`git commit -F uzenet.txt`), ne `-m`-mel —
`CLAUDE.md` git-szabály, `163e41b`.

**Az öt commit után `git push origin main` — ugyanabban a menetben, nem külön
kérésre várva.** Push előtt `git status` legyen tiszta, és `git log --oneline -5`
kerüljön a jelentésbe.

---

## 5. Amit ez a brief szándékosan nem kér

- **Nem kéri a `tahot_zarojeles_dontesek.py` beégetett Windows-útvonalainak
  javítását** (`REPO + r"\konkordancia\..."`, 41. sor környéke). Valódi hiba, de
  külön tétel — ne keveredjen a csv-cserébe.
- **Nem kéri a generátor (`general.py`) megírását.** Az az F4 tulajdonképpeni
  tartalma, és csak ezután kezdődhet.
- **Nem kéri az `argparse` / `__main__` őrök pótlását.** Tizenegy szkriptnek
  egyik sincs, és ebből hat modulszinten fájlt ír — bármely véletlen hívás
  adatot ír felül. Valódi hiba, de saját tétel; ide most csak a
  `NYITOTT_FELADATOK.md`-be való felvétele tartozik.
- **Nem kéri a `konkordancia/` táblák javítását**, ha a kármérés kárt talál.
  Előbb legyen szám, aztán döntés.

---

## 6. Futtatási rend és modellválasztás

### 6.1 Tételenkénti modelljavaslat

| tétel | a munka jellege | modell | indok |
|---|---|---|---|
| **C** — kármérés | egy mérőszkript megírása, futtatás 387 MB-on, TSV-riport | **Sonnet** | nincs tartalmi ítélet; a nehézség méretbeli, nem értelmezésbeli. A kimenet szám, tehát önellenőrző |
| **A** — olvasók (39 hely, 18 szkript) | sablonos csere, de hívási helyenként más alak (lista vs. szótár, fejléc-átugrás, `#`-sorok) | **Sonnet** | a brief megadja a közös segédfüggvényt; az eltéréseket az E7 diff kimutatja. Opus-ra nincs szükség |
| **B** — írók (10 hely, 8 szkript) | **irreverzibilis**, bájthűség, körút-ellenőrzés, `merge_karoli_szofaj.py` in-place felülírás | **Opus** | itt a hiba nem javítható visszafelé: egy rossz `csv.writer`-csere 127 sort ír át némán a kanonikus táblán |
| **D** — stderr-őr (21 szkript) | pontosan meghatározott beszúrás, sorvég-megtartás | **Sonnet** | mechanikus; az E8 grep egyértelműen zárja |

Egy mondatban: **csak a B kap Opust.** A másik három olyan, ahol a helyesség
mérhető, nem megítélendő — és épp ezért olcsóbb modellen is ellenőrizhető marad.

### 6.2 Menetbeosztás

Három menet, **egymás után** — párhuzamos Code-menet ugyanazon az ágon tilos
(korábbi szinkron-ütközés miatt firm szabály).

| menet | tételek | modell | commit |
|---|---|---|---|
| 1. | **E**, majd C, majd A | Sonnet | `F4.0-elo`, `F4.0b`, `F4.0a` |
| 2. | B | **Opus** | `F4.0c` |
| 3. | D | Sonnet | `F4.0d` |

Miért nem kettő, ahogy a terv írja: a B más modellt kíván, mint a másik három,
és a menethatár az egyetlen hely, ahol modellt lehet váltani. A 2. menet rövid
(10 hívási hely), tehát a három menet együtt sem több tokenben, mint kettő lenne
végig Opuson.

### 6.3 Az 1. menet nyitó promptja

```
Olvasd el az F4_BRIEF.md-t és a CLAUDE.md „TSV-olvasás" szakaszát.
Ebben a menetben az E, a C és az A tétel megy, ebben a sorrendben.

ELŐSZÖR E (brief 2. pont, „Tétel E"):
 - ha a --help-füstteszt már lefutott a munkafán, állítsd helyre a mellékhatásait
   az E/3 pont szerint (git status elemzés, majd célzott git checkout);
 - a három szkriptben az őr az importblokk alá kerül;
 - a CLAUDE.md szabályszövege „importok előtt" -> „importok után";
 - az ellenőrzés az eszkozok/import_sorrend_ellenoriz.py futtatása, NEM a
   --help-es füstteszt (l. E/2 — a 19 argparse nélküli szkript --help-re a
   teljes törzsét lefuttatja és felülírja a kanonikus táblákat).
Commit: F4.0-elo.

UTÁNA, és csak utána, rögzítsd az E7 kiindulási állapotát: futtasd a gate.py-t
és a lekerdez.py-t, és mentsd a kimenetüket a naplok/ alá
(F4_0_baseline_gate.txt, F4_0_baseline_lekerdez.txt). A mai
F4_0_baseline_lekerdez.txt csak a NameError-t tartalmazza — írd felül.

Utána C: a konkordancia/*.tsv kármérése a brief 2.C pontja szerint, kimenet
naplok/F4_0_csv_karmeres.tsv. Commit: F4.0b.

Utána A: a 39 olvasó hívási hely kiváltása a brief 2.A pontjának
segédfüggvényével. Commit: F4.0a.

A commit-üzeneteket UTF-8 fájlból add át (git commit -F). A három commit után
push origin main, ugyanebben a menetben. A jelentésbe kerüljön bele az E1-E5,
az E7 és az E9 mért értéke, és a git log --oneline -5.
```

### 6.4 A 2. menet nyitó promptja *(Opus)*

```
Olvasd el az F4_BRIEF.md-t, a CLAUDE.md „TSV-olvasás" szakaszát, és mintaként
az eszkozok/igazolas_migracio.py docstringjét és I/O-rutinját.

Ebben a menetben csak a B tétel megy: a 10 csv-író hívási hely kiváltása
'\t'.join()-ra, 8 szkriptben.

Kötelező mindegyiknél: írás előtt bájt-szintű körút-ellenőrzés az eredeti
fájllal, és eltérésnél MEGÁLLÁS, nem felülírás. A merge_karoli_szofaj.py a
legveszélyesebb — ugyanazt a KIVONAT_PATH-ot olvassa és írja felül helyben.

A naplok/F4_0_csv_karmeres.tsv (az előző menet kimenete) adja meg, melyik
táblán mit kell a cserének helyreállítania. Ha egy tábla mérése 0 eltérést
mutatott, a cserének ott bájtra semlegesnek kell lennie — ezt igazold is.

Commit: F4.0c, UTF-8 üzenetfájlból, majd push origin main ugyanebben a menetben.
A jelentésbe kerüljön az E4 (git diff --stat az adat/ és konkordancia/ alatt —
üresnek kell lennie) mért eredménye.
```

### 6.5 A 3. menet nyitó promptja

```
Olvasd el az F4_BRIEF.md 2.D pontját.

A stderr-őr kiterjesztése mind a 24 eszkozok/*.py-ra: ahol ma csak stdout-őr
van, kerüljön mellé a stderr párja, a fájlban meglévő alakkal egyezően
(reconfigure mellé reconfigure, TextIOWrapper mellé TextIOWrapper).

Sorvégeket ne változtass: fájlonként ellenőrizd a CRLF/LF arányt a szerkesztés
előtt és után.

Egészítsd ki a CLAUDE.md „Shell — kötelező munkamódszer" szakaszának
kódmintáját is a stderr sorral.

Commit: F4.0d, UTF-8 üzenetfájlból, majd push origin main. A jelentésbe kerüljön
az E8 (stderr-őr 24/24) és az E5 (sorvégek) mért eredménye.
```

### 6.6 A menetek közé

Minden menet után a jelentés jöjjön vissza a chat-menetbe ellenőrzésre,
mielőtt a következő elindul. Az 1. menet E7-diffje a legfontosabb kapu: ha nem
pontosan 79 mező változik, mind a `kapcsolodas` oszlopban, akkor a 2. menet nem
indulhat.


---

## Döntésnapló

| # | Döntés | Indok | Ki döntötte |
|---|---|---|---|
| B1 | Az F4-0 hatóköre a **teljes** csv-mentesítés (20 szkript, 49 hely), nem csak a `gate.py`/`lekerdez.py` | az írók a nagyobb kockázat, és a `CLAUDE.md` 126. szakasza csak így lesz igaz állítás | felhasználó, 2026-09-14 |
| B2 | A stderr-őr az F4-be kerül, külön tételként (D) | ugyanaz a menet amúgy is hozzányúl a `lekerdez.py`-hoz | felhasználó, 2026-09-14 |
| B3 | A `konkordancia/` kármérése **megelőzi** a cserét | csere után már nincs mihez mérni; ez az E4/E7 alapja | chat-menet javaslata |
| B4 | A csere hossz-ellenőrzést vezet be (`raise` rövid sorra) | a `csv.DictReader` némán `None`-nal töltött, a `zip` némán vágott | chat-menet javaslata |
| B5 | Négy külön commit, nem egy | `CLAUDE.md` tétel-szintű granularitás | `CLAUDE.md` |
| B6 | Csak a B tétel fut Opuson; C, A, D Sonneten | a B az egyetlen irreverzibilis tétel; a másik háromnál a helyesség mérhető, nem megítélendő | chat-menet javaslata |
| B7 | Három menet kettő helyett | a modellváltás csak menethatáron lehetséges, és a B más modellt kíván | chat-menet javaslata |
| B8 | Az E7 kiindulási kimenet rögzítése az 1. menet **első** lépése, még a C előtt | a csere után már nincs mihez diffelni | chat-menet javaslata |
| B9 | Új E tétel: az import-sorrend javítása minden más elé kerül, saját `F4.0-elo` committal | a `lekerdez.py` el sem indul, tehát az E7 baseline nem rögzíthető nélküle | chat-menet, 2026-09-14 (Code-menet lelete alapján) |
| B10 | Az őr az importblokk **alá** kerül, nem az `import sys` feljebb | ez a repó 21 működő szkriptjének tényleges konvenciója; a másik irány kettéhasítaná az importblokkot | chat-menet javaslata |
| B11 | A `CLAUDE.md` „importok előtt" szövege ugyanabban a commitban javítandó | a szabályszöveg maga a hiba forrása; enélkül a D tétel újratermelné | chat-menet javaslata |
| B12 | A `--help`-es füstteszt **visszavonva**, helyette AST-alapú `import_sorrend_ellenoriz.py` | 24-ből 19 szkript nem használ argparse-t, a `--help` lefuttatja őket és felülírja a kanonikus táblákat — a v3 utasítása kárt okozott | chat-menet, 2026-09-14 (a Code-menet jelzése után) |
| B13 | A füstteszt mellékhatásait helyre kell állítani, a teljes `git status` alapján, nem csak a szembetűnő fájlokra | a `f3_1_betoltes.py` a D25 és F3.4 előtti állapotra írja vissza az `elofordulasok.tsv`-t — csendes adatregresszió | chat-menet javaslata |
| B14 | Új nyitott tétel: az `argparse`/`__main__` őr nélküli szkriptek | bármely véletlen hívás adatot ír; külön tétel, nem az F4-0 része | chat-menet javaslata; a pontos szám **10 szkript / 8 ír fájlt**, a Code-menet mérése szerint — a brief korábbi 11/6 becslése téves volt |
| B15 | Az E5 újrafogalmazva: a sorvég **fájlonként** változatlan, nem „mind LF" | az 1. menet hét CRLF-fájlt némán LF-re konvertált, mert az E5 szövege ezt megengedte | chat-menet, 2026-09-14 (ellenőrzés után) |
| B16 | Új E11: az `adat/` és `konkordancia/` táblák sorvége LF marad | az `elofordulasok.tsv` az 1. menetben LF-ről CRLF-re váltott; négy olvasó nem strippeli a `\r`-t, egyikük (`f3_4_zaro_ellenoriz.py`) épp ezt a táblát olvassa | chat-menet, 2026-09-14 |
| B17 | E7 elvárása javítva 79-ről nullára | a `gate.py`/`lekerdez.py` nem dolgozik a `kapcsolodas`-szal — a brief v1-v4 rossz értéket írt elő | chat-menet, 2026-09-14 |
| B18 | **E5 visszavonva** | a repó `core.autocrlf=true`-val megy: a munkafa sorvége checkout-műtermék, nem megőrzendő állapot. Az E5 hibás kritérium volt, és fölösleges munkát okozott az utójavításban | chat-menet, 2026-09-14 (a Code-menet `autocrlf` lelete után) |
| B19 | Az E11 `.gitattributes`-szal kényszerítendő (`*.tsv text eol=lf`), nem kézi normalizálással | `autocrlf=true` mellett a kézzel LF-re állított tábla a következő checkoutkor visszaáll CRLF-re, és a négy `\r`-t nem strippelő olvasó némán szennyezett utolsó mezőt lát | chat-menet, 2026-09-14 |
| B20 | Tétel B körút-referenciája a `git show HEAD:<fájl>` blob, nem a munkafa | ugyanezért: a munkafa sorvége nem stabil, a blob igen | chat-menet, 2026-09-14 |

---


---

## Függelék — a 49 hívási hely teljes leltára

Gépi kivonat a `28ae8d4` munkapéldányából. A „célfájl" oszlop a hívást megelőző
legfeljebb 10 sor kontextusából származik; ahol változó- vagy konstansnév áll,
ott a Code-menet nézze meg a definíciót.

| szkript | sor | hívás | célfájl (kontextusból) |
|---|---:|---|---|
| `f3_2_betoltes.py` | 51 | olvas `csv.reader` | `TAHOT_PATH (konstans)` |
| `f3_4_ellenoriz.py` | 25 | olvas `csv.reader` | `Karoli_1908.tsv` |
| `f3_4_ellenoriz.py` | 37 | olvas `csv.DictReader` | `f3_4_dontesek.tsv` |
| `f3_4_elokeszites.py` | 20 | olvas `csv.reader` | `Konyv_normalizalo_tabla.tsv` |
| `f3_4_elokeszites.py` | 38 | olvas `csv.reader` | `Karoli_1908.tsv` |
| `f3_4_elokeszites.py` | 47 | olvas `csv.DictReader` | `Karoli_Strong_kivonat.tsv` |
| `f3_4_elokeszites.py` | 79 | **ÍR** `csv.writer` | `ki (változó)` |
| `f3_4_gorog_ellenoriz.py` | 8 | olvas `csv.DictReader` | `TAGNT_kivonat.tsv` |
| `f3_4_join_potlas.py` | 71 | olvas `csv.DictReader` | `f3_4_dontesek.tsv` |
| `f3_4_join_potlas.py` | 127 | olvas `csv.reader` | `Konyv_normalizalo_tabla.tsv` |
| `f3_4_join_potlas.py` | 145 | olvas `csv.DictReader` | `Strong_szotar.tsv` |
| `f3_4_join_potlas.py` | 182 | olvas `csv.DictReader` | `extra (változó)` |
| `f3_4_munkalap_general.py` | 23 | olvas `csv.reader` | `Karoli_1908.tsv` |
| `f3_4_nema_nemtalalat.py` | 32 | olvas `csv.reader` | `Karoli_1908.tsv` |
| `f3_4_zaro_ellenoriz.py` | 52 | olvas `csv.DictReader` | `ut (változó)` |
| `gate.py` | 47 | olvas `csv.DictReader` | `path (változó)` |
| `grammatikai_strongok_general.py` | 155 | olvas `csv.reader` | `path (változó)` |
| `grammatikai_strongok_general.py` | 232 | **ÍR** `csv.DictWriter` | `?` |
| `inline_strong_megjelenito.py` | 69 | olvas `csv.reader` | `path (változó)` |
| `kockazat_szures_18_tanulmany.py` | 66 | olvas `csv.reader` | `Strong_szotar.tsv` |
| `kockazat_szures_18_tanulmany.py` | 113 | olvas `csv.reader` | `path (változó)` |
| `kockazat_szures_18_tanulmany.py` | 136 | olvas `csv.reader` | `LXX_kivonat_Genezis.tsv` |
| `kockazat_szures_18_tanulmany.py` | 152 | olvas `csv.reader` | `TAGNT_kivonat.tsv` |
| `kockazat_szures_18_tanulmany.py` | 168 | olvas `csv.reader` | `TAHOT_kivonat.tsv` |
| `kockazat_szures_18_tanulmany.py` | 183 | olvas `csv.reader` | `TAGNT_kivonat.tsv` |
| `lekerdez.py` | 44 | olvas `csv.DictReader` | `path (változó)` |
| `lekerdez.py` | 52 | olvas `csv.DictReader` | `path (változó)` |
| `lxx_kivonat_fetch.py` | 87 | olvas `csv.reader` | `NORMALIZO_TABLA (konstans)` |
| `lxx_kivonat_fetch.py` | 113 | olvas `csv.reader` | `path (változó)` |
| `lxx_kivonat_fetch.py` | 141 | olvas `csv.reader` | `path (változó)` |
| `lxx_kivonat_fetch.py` | 189 | olvas `csv.DictReader` | `path (változó)` |
| `lxx_kivonat_fetch.py` | 488 | **ÍR** `csv.writer` | `?` |
| `lxx_kivonat_fetch_v2.py` | 106 | **ÍR** `csv.writer` | `utvonal (változó)` |
| `lxx_kivonat_fetch_v2.py` | 609 | **ÍR** `csv.writer` | `?` |
| `merge_karoli_szofaj.py` | 26 | olvas `csv.reader` | `SZOTAR_PATH (konstans)` |
| `merge_karoli_szofaj.py` | 37 | olvas `csv.reader` | `KIVONAT_PATH (konstans)` |
| `merge_karoli_szofaj.py` | 49 | **ÍR** `csv.writer` | `KIVONAT_PATH (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 72 | olvas `csv.reader` | `NORM_PATH (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 83 | olvas `csv.reader` | `KAROLI_PATH (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 95 | olvas `csv.reader` | `DECISIONS_PATH (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 136 | olvas `csv.reader` | `OLD_TAHOT (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 159 | olvas `csv.reader` | `PHASEA_PATH (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 229 | **ÍR** `csv.writer` | `OUT_MAIN (konstans)` |
| `tahot_karoli_kulcs_generalas.py` | 236 | **ÍR** `csv.writer` | `OUT_OPEN (konstans)` |
| `tahot_lefedettseg_ellenoriz.py` | 44 | olvas `csv.DictReader` | `TAHOT (konstans)` |
| `tahot_zarojeles_dontesek.py` | 41 | olvas `csv.reader` | `NORM_PATH (konstans)` |
| `tahot_zarojeles_dontesek.py` | 52 | olvas `csv.reader` | `KAROLI_PATH (konstans)` |
| `tahot_zarojeles_dontesek.py` | 204 | **ÍR** `csv.writer` | `?` |
| `tahot_zarojeles_phaseA_kivonat.py` | 145 | **ÍR** `csv.writer` | `out_path (változó)` |

---

*A brief a `28ae8d4` munkapéldányának független mérésén alapul; minden szám ebben a menetben futtatott parancsból származik, nem korábbi jelentésből.*

---
