# 9. PaRDeS motívum-forrás sablon (`motivumok/[ID].md`)

**Állapot: tervezet, a #12 pilotja véglegesíti.**

*v0 — 2026.10.08 (F23 M1/1, `F23_MOTIVUM_FORRAS_BRIEF.md`). Döntések: D34 (B út: motívumonként egy kézi forrás), D36 (három mélységi szint, a `belso` buildkor kimarad), D37 + DT66 (c) (aktiválás), DT28 (egyirányúság), DT66 (a)–(b) (szakasz-besorolás, `naplok/MOTIVUM_FORRAS_lekepezes.tsv`), DT68 (1)–(2) (a próza helye, a mérce), DT74 (1), (5) (a #78 váza mint aranyminta), DT76 (9) (13–14. szerep). Bemenet: a #64 mérése (`naplok/TEREMT002_PROZA_PROBA_meres.md` 3. szakasz), a #78 mérése (`naplok/F78_meres.md`). A `javaslat` jelölésű pontokról a `DONTESEK.md` DT-F23a tétele dönt; amíg nem dőlt el, a pont nem kötelező.*

**Kimenet nyelve:** magyar

---

## 0. Mire szolgál ez a sablon

A `motivumok/[ID].md` a motívum **egyetlen kézi forrása** (D34). Összefüggő érvelés, amelyben jelölők állnak; a generátor ezekből a jelölőkből nyer ki adatot, és ezekből állítja össze a nézeteket. **Nem adatséma, amelybe prózamezők vannak beszúrva** (F32 KONTEXTUS K1/2): a sablon szakaszsorrendet és jelölőket ad, mezőhatárt nem. Az értelmező próza egy kézben, egy modellel készül, és aki belenyúl, az egészet olvassa (KONTEXTUS K1).

A forrásból generált nézetek (kimenet, kézzel nem szerkeszthetők):

| Nézet | Mélység | Mi lesz belőle |
|---|---|---|
| motívumcikk (a tematikus tanulmány utódja) | `apparatus` | a forrás összes aktív szakasza + az `ADAT-NÉZET` helyére generált táblák |
| lexikonoldal (`lexikon/[ID]_TUDOMANYOS.md`) | `apparatus` | a lexikonoldal-sablon (`6_…`) szakaszai; a kézi rések a forrás `RÉS` jelölői közül |
| olvasói nézet (a törzscikk utódja, #25/#76) | `olvasoi` | csak az `olvasoi` blokkok és a nyilvános generált táblák |
| szerkesztői nézet | `belso` | minden, a `【NAPLO】` blokkokkal együtt; nem nyilvános |

A törzscikk (`8_PaRDeS_torzscikk_sablon.md`) a #11-ben megszűnik (D34); csak-törzscikk tartalom nincs (`naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv`).

## 1. Három réteg, egy irány (DT28)

A forrás a (b) réteg. Az adat két irányban mozog, és csak ebben a kettőben:

- **(b) → (a) kinyerés:** a forrás kinyerő jelölőiből a generátor jelölt-sort ír (`adat/jeloltek.tsv`), `manual` provenienciával; a sorról ember dönt (`adat/SEMA.md` 3/2, 3.10).
- **(a) → (c) generálás:** a nézetek az adatból és a forrásból generálódnak.

**(a) → (b) út nincs.** A generátor a forrásba nem ír; egyetlen jelölő sem jelent visszaírást; az adatból a forrásba semmi nem kerül vissza. Generált jelölő (`GENERÁLT-KEZDET`, `GENERÁLT`, `ÜRES-BLOKK`, `ÜRES-NYELV`) a forrásban tilos: ha ott áll, az visszaírás-gyanú (`naplok/MOTIVUM_FORRAS_pilot_terv.md` 7. szakasz).

## 2. Mélységi szintek

Három szint: `olvasoi` ⊂ `apparatus` ⊂ `belso` (a nézet a saját szintjét és az alatta lévőket mutatja: az `apparatus` nézet az `olvasoi` blokkokat is). A szabály teljes leírása: `adat/SEMA.md` 3.10.

- **A szakasz alapszintje** a 4. pont táblázatában áll; ehhez a forrásban jelölő nem kell.
- **Eltérés** a szakaszon belül blokkszintű jelölőpárral: `<!-- SZINT-KEZDET: belso -->` … `<!-- SZINT-VÉGE: belso -->`. A pár csak mélyebb szintre válthat (pl. `olvasoi` szakaszon belül `apparatus` vagy `belso` blokk), és nem nyúlhat át `##` címsoron. *[javaslat: a jelölő alakja és a hatókör-szabály, DT-F23a (1); a #64 ideiglenes `<!-- SZINT: x -->` alakja a következő jelölőig tartott, és a hatóköre nem volt kimondva (#64 mérés 3. szakasz, 2. tanulság).]*
- **A `【NAPLO: …】` mindig `belso`,** bármilyen szintű szakaszban áll (DT66 (a) 1. kivétel). Jelölő nem kell hozzá: a `【NAPLO` maga a jelölő.

## 3. Aktiválás

A szakasz aktiválási feltétele a 4. pont táblázatában áll. Inaktív szakasz **üres címmel nem áll a forrásban**; a helyén egy sor: `<!-- INAKTÍV: [szakasz] — a feltétel nem áll fenn: [ok] -->`. A generált nézet az inaktív szakaszt kihagyja.

**A tematikus szakaszok (3., 5., és a lexikonoldal 6. Értelmezés rése) aktiválása (D37, DT66 (c)):**

> aktív, ha `COUNT(DISTINCT fo_elofordulas) ≥ 3` (⭐ küszöb, SEMA 2.2.3) **VAGY** a motívum `statusz` mezője `publikálható` vagy `véglegesített` (`adat/motivumok.tsv`).

A második ág a DT66 (c) „van lezárt tematikus forrás” feltételének B-beli alakja: a migráció után a lezártság a `statusz` mezőben áll, nem egy `tematikus_lezart/` fájl létezésében. A küszöb a tanulmány *indítására* szól, nem a meglévő szakaszokra; a `fo_elofordulas` adatot nem bővítjük (DT66 (c)). *Mért állapot (2026.10.08):* a 9 motívumból 8 `publikálható` (köztük a küszöb alatti KIRALY-001, MENNY-001, HODIT-001: 1-1 csoport), a TEREMT-002 `feldolgozás alatt`, 3 csoporttal; mind a kilenc aktív (`scope=adat/motivumok.tsv+adat/elofordulasok.tsv | forras=manual (szkript, split('\t')) | ts=2026-10-08`).

**Értelmezői aktiválás.** A „⚠️ Vitatott pontok” és a „4. Kapcsolódás a kutatási sablonhoz” feltétele értelmezői ítélet, gépi feltétel nélkül (#64 mérés 5. szakasz, 1–2. pont). Az inaktív állapot ilyenkor a „nincs adat” tényt rögzíti, nem a „nincs vonatkozás” tényt; az `INAKTÍV` sor ezt kimondja. *[javaslat: DT-F23a (6)]*

## 4. Szakaszok, sorrendben

Oszlopok: **réteg** = a szakasz célrétege a B szerkezetben (`naplok/MOTIVUM_FORRAS_lekepezes.tsv` `B_helye`; `kezi_forras` = a forrásban próza, `adat` = táblából generált, `generalt` = adatból vagy a forrásból generált); **szint** = alapszint; **aktiválás**; **jelölő** = ami a forrásban a szakasz helyén áll.

| # | Szakasz | Réteg | Szint | Aktiválás | Jelölő a forrásban |
|---|---|---|---|---|---|
| F | Forrásréteg-fejléc | `generalt` (cím, ID a `motivumok.tsv`-ből) | `belso` | mindig | `<!-- FORRÁSRÉTEG … -->`; a fejléc-proveniencia `【NAPLO】` (DT66 (a) 3.) |
| K | Kivonat | `kezi_forras` | `olvasoi` | mindig | `RÉS: kivonat` |
| 0 | Forrás-összegyűjtés a meglévő anyagból | `adat` (folyamat-nyom → `auditok.tsv` / `jeloltek.tsv` `forras_kereses`) | `belso` | feltételes: örökölt motívum, van előzményanyag | natívnál `INAKTÍV`; örököltnél `ADAT-NÉZET` |
| 1.P | Friss keresés, P1–P7 | `adat` (proveniencia → `auditok.tsv`, jelölt → `jeloltek.tsv`); a P2 indoklása `kezi_forras` | `belso` | mindig | a P2 próza; a P1, P3–P6 eredménye proveniencia-lábjegyzettel |
| 1.T | Előfordulások — 7 oszlopos tábla | `adat` (`elofordulasok.tsv`, a `jeloltek.tsv`-n át) | `apparatus` | mindig | `ADAT-NÉZET` (`--cel study`) |
| 1.L | Logikai kötőszó szerinti bontás | `kezi_forras` | `apparatus` (a tudatos kihagyás jelölése `belso`) | feltételes: van igehely-tartományú előfordulás-sor | próza vagy `INAKTÍV` |
| 2 | Eredeti nyelvi összevetés | `kezi_forras` (a szótári idézet `adat`: `lexikon_hivatkozasok.tsv`) | `apparatus` | mindig | próza + `ADAT-HIV` a szótári sorra |
| 2.S | Szótári háttér — szerepmátrix | `generalt` (5. pont) | `apparatus` | mindig | `ADAT-NÉZET` (`--cel lexikon#…#szocikkek`) |
| 2/b | Kiegészítő szótári adatok | `adat` (`lexikon_hivatkozasok.tsv`, SEMA 2.5) | `apparatus` | feltételes: van a generált blokkon túli szótári anyag | nincs kézi blokk; a kísérő mondatok a „Miért fontos” résbe |
| 2.M | Miért fontos ez a lelet | `kezi_forras` | `apparatus` | feltételes: többforrásos szerep-blokk | `RÉS: miert_fontos` |
| 3 | PaRDeS: Peshat, Remez, Drash, Sod | `kezi_forras` | `olvasoi` | tematikus (3. pont) | `RÉS: ertelmezes` |
| 3.V | ⚠️ Vitatott pontok | `kezi_forras` | `olvasoi` | értelmezői: tudományosan vitatott | próza vagy `INAKTÍV` |
| 3.U | Új felismerés | `kezi_forras` (a 3. szakasz része) | `olvasoi` | feltételes: van ilyen | próza a 3. szakaszon belül |
| 4 | Kapcsolódás a kutatási sablonhoz | `kezi_forras` | `apparatus` | értelmezői: van pünkösdi/karizmatikus szakirodalmi vonatkozás | próza vagy `INAKTÍV` |
| 5 | Alkalmazás és tanítványság | `kezi_forras` | `olvasoi` | tematikus (3. pont) | próza |
| 5.T | Nevesített tanítói egyezés | `kezi_forras` (hivatkozó mondat a 7. lépés saját fájljára, beemelés nélkül; DT66 (a) 2.) | `olvasoi` | feltételes: lefutott a 7. lépés | hivatkozó mondat vagy `INAKTÍV` |
| 6 | Napló-frissítés (státusz) | `adat` (`motivumok.tsv` `statusz`) | `belso` | mindig | `ADAT-NÉZET` (`--cel naplo`) |
| 7.K | Kereszthivatkozások + Minősítés | `adat` (`jeloltek.tsv` `dontes` + `indoklas`, SEMA 2.4) | `apparatus` | mindig | `ADAT-NÉZET`; a kétpontos modellbe nem férő tárgyalás kézi próza |
| 7.A | Kapcsolatok + Alátámasztás | `adat` (`kapcsolatok.tsv`; az indoklás oszlopa séma-kérdés) | `apparatus` | feltételes: van `kapcsolatok.tsv` sor | `ADAT-NÉZET`; a kétpontos modellbe nem férő eset kézi próza |
| 7.M | Módszertan — ellenőrzési rétegek | `adat` (`auditok.tsv`) | `belso` | mindig | `ADAT-NÉZET` |
| 7.N | Nyitott kérdések | `kezi_forras` tételenként (l. alább) | `apparatus` | feltételes: van nyitott tétel | `RÉS: modszertan` (csak a tartalmi tételek) |
| 7.Q | Minőségi kapu, verzió-címke | `adat` (`motivumok.tsv` `sablon_verzio`; a kapu-eredmény helye séma-kérdés) | `belso` | mindig | `ADAT-NÉZET` |
| P | Proveniencia-sorok | `kezi_forras` (a lábjegyzetek gyűjtőhelye) | `belso` | mindig, ha van lábjegyzet | lábjegyzet-definíciók |

**A 7.N tételenkénti besorolása** (DT66 (a) 4.; a lekepezes `7. Nyitott kérdések` sora): a *tartalmi* nyitott kérdés (értelmezési, exegetikai) `kezi_forras`, `apparatus`, a 7.N-ben marad; a *séma-korlát* (a tábla nem tudja ábrázolni) és az *adatállapot* (forrás hiányzik, bekötés hiányzik) nem a motívum érvelése: N-tétel a `NYITOTT_FELADATOK.md`-ben (a `/befogad` útján), a forrásban legfeljebb `【NAPLO】` mutató; a *lezárt* tétel (áthúzott) a migrációban archívum. *[javaslat: DT-F23a (5); az ISTENTISZT-001 öt tételére alkalmazva: pilot-terv 4.4]*

**Két új szakasz a tematikus sablonhoz képest** (#64 mérés 3. szakasz, 4. tanulság: a tematikus sablonból hiányzott): a **7.N Nyitott kérdések** (a lexikonoldal `modszertan` résének kézi része) és a **P Proveniencia-sorok** (lábjegyzet-alak, az ISTENTISZT-001 és a TEREMT-002 mintája). *[javaslat: DT-F23a (4)]*

**Ami nem szakasz** (`sablonszabaly`, DT66 (b)): a „Mikor használandó”, a terminológiai és formai szabályok, a konfliktuskezelés, a Lezárási checklist, a licenc, a fájlnév-konvenció, a lexikonoldal Minőségi kapuja (a CI veszi át: `naplok/MOTIVUM_FORRAS_ci_terv.md`), a megszűnt kimenetek (OLVASHATÓ, KÉT fájl, törzscikk). Ezek a 6–8. pontba kerültek, vagy megszűnnek.

**Örökölt motívum `motivumok/[ID].md` blokkjai** (ma a napló archív másolatai): a Tematikus áttekintés, a Kulcsszó-index és a Lezárt tanulmányok indexe `generalt` (a #11-ben archívum); a ⭐-bekezdés száma és igehely-listája `generalt`, értelmező mondatai a Kivonat/3. szakasz anyaga; a „Kulcsszavak részletesen” igehely-listája és státusza `adat`, a maradék értelmező szöveg a Kivonat/3. szakasz anyaga (lekepezes, `szetvalasztando`).

## 5. A szótári szakasz (2.S) — a szerepmátrix szerint

A szótári háttér **generált**: a forrás nem tartalmazza, csak a helyét jelöli (`ADAT-NÉZET`). A váz a #78 aranymintája (`generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md`, 2. szakasz; `naplok/F78_meres.md` 9–11., 14.):

- **Sorrend:** nyelvenként (görög, héber), azon belül az `adat/szotar_szerepek.tsv` `sorrend` mezője szerint (1–10); a mindkét nyelven azonos (szerep, forrás, állapot) sorok (12–14.) egyszer, a „Nyelvfüggetlen szerepek” alatt; a végén a „Rokon szavak”. A 11. sorszám nincs kiosztva (SEMA 2.13).
- **Állapot → blokk** (ATALAKITASI 13.3, DT80, DT82):
  - `adatosítva` + van sor → a forrás(ok) blokkja;
  - `adatosítva`, de a tartalom máshol él → hivatkozás („l. 2/b”, „l. 3. szakasz”, „l. 1. szakasz UBS-oszlop”), nem üres blokk;
  - `adatosítva`, de a tokenhez nincs sor → jelölt üres blokk `adatosítva, nincs bekötve` állapottal, mutató a #9-re;
  - `nincs adatosítva` / `javaslat` → **explicit üres blokk**: `<!-- ÜRES-BLOKK: [szerep] | [állapot] -->` + látható zárójeles sor; részadat (TWOT-szám, kiejtés-lemma) esetén a sor kimondja, hogy csak részadat áll;
  - `nincs forrás` → nincs blokk;
  - token nélküli nyelv → `<!-- ÜRES-NYELV: [nyelv] | nincs Strong-token -->`.
- **13. Károli-megfelelők (+ SZPA)** és **14. Rejtett / hamis párhuzam:** `javaslat` állapotú szerepek (DT-M4, DT76 (9)); amíg a #22 nem teljes, explicit üres blokk.

A 26 sor (13 szerep × 2 nyelv) a forrásban **nem** ismétlődik; az alábbi váz csak azt mutatja, hova mutat a forrás kézi anyaga:

```
### Görög szavak / ### Héber szavak
#### 1. Alapjelentés             ← generált (TBESG / TBESH)
#### 2. Mélységi szócikk         ← generált (Thayer / BDB)
#### 3. Teológiai szócikk        ← üres blokk (nincs adatosítva); héber: TWOT-szám részadat
#### 4. Jelentésszerkezet        ← generált (SDGNT / SDBH domén)
#### 5. Tömör jelentés           ← görög: generált vagy hivatkozás; héber: üres blokk
#### 6. LXX-híd                  ← hivatkozás a lexikonoldal 3. szakaszára
#### 7. Megfelelők               ← ma „l. 2/b”; a B-ben a 2/b adata (lexikon_hivatkozasok) tölti
#### 8. Nyelvi háttér            ← görög: LSJ vagy hivatkozás; héber: üres blokk
#### 9. Versenkénti jelentés     ← görög: hivatkozás az 1. szakaszra; héber: üres blokk
#### 10. Kiejtés                 ← részadat + üres blokk
### Nyelvfüggetlen szerepek
#### 12. Tematikus index          ← üres blokk (javaslat)
#### 13. Károli-megfelelők (+ SZPA) ← üres blokk (javaslat)
#### 14. Rejtett / hamis párhuzam  ← üres blokk (javaslat)
### Rokon szavak
```

**Mit ír a forrás a szótári részhez:** csak értelmezést, a 2. szakaszban (Eredeti nyelvi összevetés) és a 2.M-ben (Miért fontos). Szótári idézetet a próza nem másol be: az `ADAT-HIV` jelölővel a `lexikon_hivatkozasok.tsv` sorára mutat (6. pont). Kitöltetlen szerepet a próza nem pótol (CLAUDE.md 3. szabály): az üres blokk a generált nézetben látszik, és ez elfogadott kimenet. A 2/b kézi blokk a B-ben megszűnik: a szó szerinti kivonatai a `lexikon_hivatkozasok.tsv`-be kerülnek (a #9 vagy a #11 adatútján, a jelölt-folyamaton át), és a szerepmátrix 5., 7. és 8. blokkját töltik; a kísérő mondatai a Miért fontos résbe.

## 6. Jelölők — mit nyer ki belőlük a generátor

Minden jelölő HTML-megjegyzés, saját sorban (kivéve a `【NAPLO】` és a lábjegyzet). **Szerkezeti** jelölőből a generátor semmit nem nyer ki; **kinyerő** jelölőből jelölt-sort ír; **ellenőrző** jelölőből semmit nem ír, csak összevet. A kinyerés részletes szabálya (kulcs, ütközés, proveniencia): `adat/SEMA.md` 3.10.5.

| Jelölő | Alak | Fajta | Mit nyer ki a generátor | Melyik táblába |
|---|---|---|---|---|
| Forrásréteg | `<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->` | szerkezeti | semmit | — |
| Szint | `<!-- SZINT-KEZDET: [szint] -->` … `<!-- SZINT-VÉGE: [szint] -->` | szerkezeti (szűrő) | semmit; a nézet mélysége szerint szűr | — |
| Napló | `【NAPLO: …】` | szerkezeti (mindig `belso`) | semmit (DT66 (a) 1.: az `adat` alternatíva elvetve) | — |
| Inaktív | `<!-- INAKTÍV: [szakasz] — [ok] -->` | szerkezeti | semmit; a szakasz kimarad a nézetből | — |
| Rés | `<!-- RÉS-KEZDET: [rés] -->` … `<!-- RÉS-VÉGE: [rés] -->` | szerkezeti | semmit; a törzs a lexikonoldal résébe kerül (a `res_forras.tsv` `tanulmany` mezője a `motivumok/[ID].md`-re mutat) | — |
| Adat-nézet | `<!-- ADAT-NÉZET: [szakasz] \| forrás: [tábla (mezők)] \| cél: [general.py --cel …] \| SZINT: [szint] -->` | szerkezeti | semmit; a nézetben ide kerül a generált tábla | — |
| Jelölt | `<!-- JELÖLT: [igehely] \| gerinc: [gerinc_elem] \| [rövid indoklás] -->` | kinyerő | egy jelölt-sort, `dontes=nyitva` értékkel (a jelölő nem dönthet) | `adat/jeloltek.tsv` (nem közvetlenül az `elofordulasok.tsv`: SEMA 3/2) |
| Proveniencia-lábjegyzet | `[^kulcs]: proveniencia: [a lekerdez.py sora szó szerint]` | kinyerő, ha `scope≠manual` | egy audit-sort, ha még nincs azonos (`id`, `proveniencia`) sor | `adat/auditok.tsv` (a `lepes` mező forrása: *[javaslat: DT-F23a (2)]*) |
| Adat-hivatkozás | `<!-- ADAT-HIV: [tábla] \| [kulcs] -->` | ellenőrző | semmit; ellenőrzi, hogy a sor létezik; hiánynál kinyerési jelentés-sor | — (a hiányzó sort a #9 / a döntéssel írt adatút pótolja) |
| Adatból számolt érték | `[érték]<!-- ADAT-ÉRTÉK: [tábla] \| [kifejezés] -->` | ellenőrző | semmit; ha a prózában álló érték eltér a táblából számolttól, hiba | — |

**Nem igehely-kulcsú adat a prózában** (szótári idézet, LXX-megfelelő, kapcsolat-indoklás, kapu-eredmény): a `jeloltek.tsv` kulcsa `id` + `igehely`, ezért ezekre jelölt-sor nem írható (`naplok/F78_meres.md` 12. szakasz, 2. pont). A tervezet az `ADAT-HIV` utat adja: a próza a meglévő sorra hivatkozik; ha a sor hiányzik, a generátor kinyerési jelentésben jelzi, és a sort döntéssel, `forras=manual` provenienciával a megfelelő adatút írja. *[javaslat: DT-F23a (3) — kinyerési jelentés vagy új jelölt-tábla]*

**Generált jelölők a forrásban tilosak** (1. pont): `GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`, `GENERÁLT:`, `ÜRES-BLOKK`, `ÜRES-NYELV`.

## 7. A tematikus sablon szabályai — mi kerül át

A `4_PaRDeS_tematikus_sablon.md` v16 (a v17 a P2 domén-mondatát pontosította, tartalmi követelmény nélkül) szabályai:

| Szabály | Sorsa a B-ben |
|---|---|
| 1. pont: mind a hét oszlop kötelező; üres cella `—` (v16, F5.1) | **átkerül a generátorba:** a tábla `ADAT-NÉZET`, a hét oszlopot a `--cel study` írja |
| Jelentés-szöveg: BDB eredeti angol + magyar a cellán belül (v15) | **átkerül a generátorba:** `elofordulasok.tsv` `jelentes_en` + a `forditasok.tsv`; a prózai, bővebb magyarítás a forrásban marad |
| P1–P7 checklist, proveniencia-sor kötelező (v16, F5.3) | **változatlan**; a proveniencia-sor lábjegyzetben áll (6. pont) |
| Logikai kötőszó szerinti bontás (v13) | **változatlan** (1.L szakasz) |
| Kiejtés minden héber/görög szónál | **változatlan** |
| Mélység-engedmény a 2. pontban (2026.09.03) | **változatlan** |
| PaRDeS-rétegfegyelem (a lexikonoldal L7-je) | **változatlan** |
| Napló-jelölés kötelező, a négy trigger, formázási szabály (üres sor a `【NAPLO】` előtt) | **változatlan**; kiegészül: a `【NAPLO】` mindig `belso` (2. pont) |
| Idézés-formázás (blockquote csak eredeti nyelv) | **változatlan** |
| Hangnem (harmadik személy, nincs „mi”-hang) | **változatlan** |
| Nevesített tanítói módszer (öt lépés), forrás-megbízhatóság (✅/⚠️) | **a 7. lépés saját fájljában él**; a forrás hivatkozik rá (DT66 (a) 2.) |
| Fájlnév `[Motívum]_tematikus.md` | **megszűnik**: a forrás `motivumok/[ID].md` |
| Index-frissítés, generált blokkok újragenerálása | **változatlan** (`general.py`) |
| Utólagos bővítés: adat- és naplóréteg ugyanabban a PR-ben | **változatlan** az (a) pontban; a (b) „Kulcsszavak részletesen” kézi frissítése megszűnik (generált) |
| Verzió-címke tanúsítás, nem dátum (v16, F5.2) | **adat**: `motivumok.tsv` `sablon_verzio`; a forrásban nem ismétlődik |
| Minőségi kapu Q1–Q7 | **a forrás kapuja a 8. pont**; a Q2 és a Q7 forrás-oldali nyoma az adatrétegben ellenőrizhető (E4, SEMA 3.8) |
| Lezárási checklist 1. (`/mnt/user-data/outputs/`), 12. (visszahivatkozás a bővítettbe) | **megszűnik / generált**: a visszamutató link az `elofordulasok.tsv` `felmerult_tanulmany` mezőjéből (DT66 (a) 5.) |
| „Tartalmi visszaírás bővített tanulmányokba” (v10) | **nem fér bele:** a lelet kézi bemásolása egy másik kézi forrásba második igazságforrást hoz létre (D34: hivatkozás másolás helyett). *[javaslat: DT-F23a (7) — a szabály megszűnik; a mutató generált; a már visszaírt leletek sorsa a #11-ben: archívum vagy törlés, DT66 (a) 5.]* |
| Terminológia: „Szent Szellem”, igehely-forma (`1Thessz 5:23`), SZPA csak rövid idézet | **változatlan** |
| Konfliktuskezelés: ütközésnél rákérdezés | **változatlan** |

## 8. Minőségi kapu (a forrásra)

A mérce: a lexikonoldal-sablon Minőségi kapuja **L1–L7** + a **DT2 két rés-szabálya** (DT68 (2), DT74 (5)), a szótári részen a **#78 váza**. A forrásra a #64 mérése szerinti átfordítással (`naplok/TEREMT002_PROZA_PROBA_meres.md` 2. szakasz):

- **L1** szerkezeti teljesség: a 4. pont minden aktív `kezi_forras` szakasza jelen van; az inaktív `INAKTÍV`-jelölővel, üres cím nélkül; az `adat` szakasz `ADAT-NÉZET`-jelölővel.
- **L2** napló-jelölés: dátum-, eredet-, döntés-, folyamat- és állapotmondat csak `【NAPLO】`-ban.
- **L3** lexikai vs. tematikus: a nem lexikai kapcsolat „tematikus, nem lexikai” jelölést kap.
- **L4** kereszt-motívum szennyeződés kizárva.
- **L5** nevesített tanítói szakasz: hivatkozás a 7. lépés fájljára, vagy `INAKTÍV` hiányjelzéssel.
- **L6** a)–f) fegyelem; **L7** PaRDeS-rétegfegyelem.
- **DT2/1** minden rés kitöltött vagy explicit hiányjelölésű; **DT2/2** az adatból generált rész `adat`-forrás-jelölésű (`ADAT-NÉZET`).
- **Szótári rész:** a generált nézet 2. szakasza a 5. pont szerint; kitöltetlen szerep explicit üres blokk.

A nézetekre vonatkozó két gépi ellenőrzés (bájtazonosság, nulla `belso` a nyilvános kimenetben): `naplok/MOTIVUM_FORRAS_ci_terv.md` (E28, E29).

## 9. Nyitott pontok (`javaslat`, DT-F23a)

1. A szintjelölő alakja és hatókör-szabálya (2. pont).
2. A proveniencia-lábjegyzet `lepes`-forrása az `auditok.tsv` felé (6. pont).
3. A nem igehely-kulcsú adat kinyerési útja (6. pont).
4. A két új szakasz: 7.N Nyitott kérdések, P Proveniencia-sorok (4. pont).
5. A Nyitott kérdések tételenkénti besorolási szabálya (4. pont, 7.N).
6. Az értelmezői aktiválás (Vitatott pontok, 4. pont) rögzítése (3. pont).
7. A „Tartalmi visszaírás” szabály megszűnése (7. pont).
8. A séma-kérdések: Alátámasztás, Minősítés, Módszertan / kapu-eredmény helye (4. pont 7.K, 7.A, 7.M, 7.Q; `adat/SEMA.md` 3.10.7).

A sablon a #12 pilotja után válik véglegessé; addig a `v0` tervezet.
