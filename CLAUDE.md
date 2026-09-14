# Bible-Study — belépési pont

PaRDeS-módszerű bibliai motívumkutatás. **A hosszú távú termék egy motívum-indexelt,
kereszthivatkozott motívumlexikon; a tanulmányok ennek előállítási folyamata.**
Ebből következik a rendszer egyetlen fő szabálya: *a kereszthivatkozás adat, a tanulmány
és a lexikon pedig ennek az adatnak a nézete.*

Nyelv: minden fájl, commit-üzenet és válasz **magyarul**.

## Ezt olvasd, ezt ne

**Ne olvasd be egyben** a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`-t (96 KB) —
ez a szabály 2026.09.13-tól **nem érvényes**. A fájl archívum; szakaszonként nyisd meg,
a `Rendszerfejlesztesi_playbook.md` 1. pontjának táblázata szerint. Ugyanígy ne olvasd be
a két changelogot (`PaRDeS_dontesek_CHANGELOG.md`, `motivumlog/PaRDeS_motivumok_CHANGELOG.md`)
és a felfüggesztett SzPA-join dokumentációt, hacsak a feladat nem azokról szól.

| Feladat | Amit megnyitsz |
|---|---|
| bármi | ez a fájl + `NYITOTT_FELADATOK.md` |
| adattábla írása/olvasása | `adat/SEMA.md` |
| tanulmányírás | a megfelelő `sablonok/` fájl + `sablonok/PaRDeS_gyorsreferencia.md` |
| lexikai kutatás | `adat/datasetek.tsv` + `konkordancia/README.md` |
| új dataset, licenc | `Rendszerfejlesztesi_playbook.md` 2. pont |
| rendszer-átalakítás | `ATALAKITASI_TERV.md.md` (fázisok: 6. szakasz) |

## Rétegek — a réteghatár egyetlen kérdés: ki írja?

| Réteg | Hol | Szabály |
|---|---|---|
| **adat** — kanonikus igazságforrás | `adat/*.tsv` | séma szerint; ha itt és egy .md-ben ellentmondás van, **ez az irányadó** |
| **forrás** — kézzel írt | `tematikus_lezart/`, `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `motivumlog/[ID].md` | szabadon szerkeszthető |
| **kimenet** — generált | l. `ATALAKITASI_TERV.md.md` 1.C | **kézzel szerkeszteni tilos**; a forrás javul, és újragenerálódik |

Generált fájl fejlécében gépi jelölés áll (`# GENERÁLT: …`). Ha ilyet látsz, ne írd át.

## Három szabály, amit soha ne sérts

1. **Proveniencia.** Minden lekérdezésből származó állítás mellé a lekérdezés saját
   proveniencia-sora kerül (`scope=… | forras=… | ts=…`). Ha nem futott lekérdezés, az
   érték `manual` — **nem üres, és nem „ellenőrizve"**.
2. **Nincs közvetlen út.** Keresési találatból nem lehet közvetlenül study-táblázat sor.
   Minden jelölt a `adat/jeloltek.tsv`-n megy át, döntéssel és indoklással.
3. **Memória vs. lekérdezés.** Amit nem a repó adata mond, az értelmezés. Hiányt **soha
   ne tölts ki** gyenge vagy asszociatív anyaggal — az üres eredmény elfogadható kimenet,
   és explicit jelölendő.

*Mindhárom megsértésének dokumentált esete van; l. `adat/SEMA.md` 1.5 és 2.4.1.*

## Kutatási menet — a hét lépés

A sorrend maga a védelem a hígulás ellen: **a gerincet mindig le kell vezetni, és a
levezetést dokumentálni kell — akkor is, ha üres az eredmény.**

1. **gerinc-metszet** (közös Strong-halmaz, `adat/grammatikai_strongok.tsv` szűréssel)
2. **szemantikai mező-hipotézis** — az egyetlen *generatív* lépés; a mező-szavak a naplóba kerülnek
3. **teljes ÓSZ/ÚSZ scan** · 4. **kollokáció** (szópár egy versben) · 5. **igealak-ellenőrzés** · 6. **LXX-híd**
7. **nevesített tanító** (web) — önálló menet, saját fájl

Az 1., 3-6. lépés determinisztikus: CLI-ből fut, tehát mindig lefut. Minden
előfordulás-sornak meg kell tudnia nevezni, **melyik gerinc-elemen lóg** (`gerinc_elem`).
Ha nem tudja, a `jeloltek.tsv`-ben marad.

## Új motívum-ID kiosztása — négy kérdés, kötelezően

1. **Mi az azonosság hordozója?** `lexikai` / `formulaikus` / `referenciális` / `fogalmi` /
   `strukturális`
2. **Mi az a minimális jegy, amely nélkül egy igehely NEM tartozik ide?** (negatív kritérium)
3. **Ha egy igehely két motívumhoz is tartozik: különbözik-e a funkciója?** Ha a funkció is
   azonos → egy motívum két néven.
4. **Részhalmaz-e?** Ha B minden előfordulása benne van A-ban → B nem új ID, hanem ↳ alpont.

Plusz a **fölérendelt fogalom** megnevezése: az a tágabb kategória, amely felé a motívum
hígulni fog. Minden új sornál: *csak ezen keresztül tartozik ide?* Ha igen, kizárandó.
**A határt a kizárások rajzolják meg, nem a meghatározás.**

## Adat-tár

`konkordancia/` — 387 MB, 17 dataset; kötelezőségük study-típusonként: `adat/datasetek.tsv`.
Három korlát, amit tudnod kell:

- **`TAHOT_kivonat.tsv` nem teljes**, bár a README annak mondja (hiányzik legalább
  1Móz 32, Zsolt 88/89/140/142, Jóel 3) — minden „teljes körű scan" ennyivel gyengébb.
- **`KJV_/ASV_Strongs`** csak Genezis, Exodus, Példabeszédek.
- **SDBH / SDGNT** (szemantikai domének) **még nincs importálva**.

Nyers adat soha ne kerüljön a fő szál kontextusába — csak kivonat.

**Igehely-formátum:** `1Móz 3:16`, `Mt 24:38`. Három dataset viszont STEPBible-alakot
használ (`Gen.1.1`): `Karoli_kereszthivatkozasok.tsv`, `Karoli_Strong_kivonat.tsv`,
`TIPNR_kivonat.tsv`. Köztük a `konkordancia/Konyv_normalizalo_tabla.tsv` konvertál —
**normalizálás nélkül néma nem-találatot kapsz**, nem hibát.

## Shell — kötelező munkamódszer

**Héber, görög vagy magyar szöveget tartalmazó kódot soha ne futtass inline
`bash -c`-vel. Mindig írd fájlba, és a fájlt futtasd.**

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

## TSV-olvasás — a `csv` modul nem használható ezeken a táblákon

**Az `adat/*.tsv` és a `konkordancia/*.tsv` olvasása `split('\t')`, írása `'\t'.join()`.**
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

Egyik mező sem tartalmaz tabot, tehát a szétvágás egyértelmű. Aki mégis `csv`-t
használna, annak `quoting=csv.QUOTE_NONE, quotechar=None` kell mindkét irányban.
Táblát író szkript írás előtt vesse össze a sorokat az eredetivel, és eltérésnél
álljon meg (minta: `eszkozok/igazolas_migracio.py`).

**Git:** munkaág `main`; commit-üzenet magyarul, tétel-azonosítóval kezdve (`F1.4: …`);
push csak kérésre.

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
