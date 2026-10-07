# F37 T6 — utófeladat-javaslat a régi tanulmányok javítására

*2026.10.07 · `claude/tanulmany-ellenorzes` · forrás: `naplok/TANULMANY_AUDIT.md` (gépi, jelentés mód), `naplok/TANULMANY_AUDIT_ugynok.md` (ügynöki), `DONTESEK.md` DT-F37a/b. **Ez javaslat:** új sor a `FELADATOK.md`-be csak a `/befogad` paranccsal, a felhasználó jóváhagyásával kerül (D22, brief T6).*

## Kiindulás

- 23 tanulmány; ebből 16-ban van ügynöki ELTÉRÉS vagy RÉSZBEN (1., 3., 4., 5. vagy 6. pont), 7 tiszta (`1Moz_3v1-6`, `1Moz_3v7-24`, `1Moz_7v1-24`, `1Moz_8v1-22`, `1Moz_12v1-20`, `1Thessz_5v23`, `Rom_8v10`).
- Gépi találat (jelentés mód): E13 206, E8 32, E12 195; E20, E9, E2, E15 nulla.
- Két korlát köti a javítást: **DT-F37-2** (egy tanulmány egy menet, nem kötegelhető) és a `CLAUDE.md` K1-szabálya (az értelmező prózába aki belenyúl, az egészet olvassa). Emiatt a javaslat két feladat: egy gépi, prózát nem érintő, és egy tanulmányonkénti tartalmi.
- A D8 szerint a módosított sor kötelező módba kerül: amit egy javítás megérint, annak az E13/E8 szerint is rendben kell lennie. A gépi találatokat ezért nem kell külön, egyben javítani; a tartalmi menet a megérintett sorokon rendezi őket.

## A javaslat — gépi rész (folyamat, egy menet)

1. **E8 versformátum, 32 hely 13 tanulmányban** — formai csere, a próza értelmét nem érinti. Táblát író szkript, eltérés-összevetéssel (minta: `eszkozok/igazolas_migracio.py`).
2. **Az alap sablon kivezetése** — a Tanulmány sablon „mint az alap sablonban” hivatkozásainak tartalmát a Tanulmány sablonba emelni, utána az `sablonok/1_PaRDeS_alap_sablon.md` archívumba (nem törlés).
3. Elfogadás: a 32 E8-találat 0; a Tanulmány sablon nem hivatkozik az alap sablonra; a tanulmányok prózája bájtra azonos az E8-sorokon kívül.

## A javaslat — tartalmi rész (tanulmányonként egy menet, modell: opus)

**Nyitó ⛔ (DT-F37a feltétele):** a feladat elején a felhasználó tételenként dönt az öt ⚠️-vita-esetről, mindegyiknél a három választás egyikével: **elfogadott projekt-olvasat** (marad, jelölve) / **feltételessé teendő** / **a Sod-ból törlendő**. Súlyossági sorrend és előzetes értékelés:

| # | Tanulmány | Vita | Előzetes értékelés |
|---|---|---|---|
| 1 | `1Moz_9v1-17` | *kesét* = hadi íj | a legsúlyosabb: a Remez és a Sod feltételesség nélkül épül a vita egyik oldalára |
| 2 | `1Moz_15` | 15:6 imputáció | kimondott projekt-munkahipotézis; valószínűleg elég jelölni |
| 3 | `1Moz_1v1` | *creatio ex nihilo* | saját lexikai érv: ha van proveniencia-sora, a DT-F37b szerint nem forrás nélküli lezárás — ellenőrizendő |
| 4 | `1Moz_1v2-2v3` | Isten képmása | mint a 3.: a „Lexikai megerősítés … ÚJ” proveniencia-sora ellenőrizendő |
| 5 | `1Moz_14` | Melkizedek | a Sod feltételesnek jelöli („Ha …”) — a DT-F37b szerint nem ⛔; tájékoztató sor |

**Menetsorrend** (a leletek súlya szerint; minden menet a teljes tanulmányt olvassa, K1):

| Sor | Tanulmány | Javítandó |
|---|---|---|
| 1 | `1Moz_9v1-17` | ⚠️-vita (DT-F37a 1.), Sod (feltételesség), ⚠️ képviselő RÉSZBEN |
| 2 | `1Moz_14` | Strong: 14:22 H5375 → H7311 (הֲרִמֹתִי); Sod RÉSZBEN (feltételes, marad) |
| 3 | `1Moz_4v1-24` | Strong: 4:2 H1892 → H1893 (személynév; a *hevel*-szójáték értelmezésként marad, a Strong-adat javul); ⚠️ Nód „mások”; angol *later* a Sod-ban |
| 4 | `1Moz_1v1` | Strong: 1:1 אֵת = H0853; két csonka ⚠️-hivatkozás (32., 177. sor); ⚠️-vita (DT-F37a 3.); Sod: az idő teremtése |
| 5 | `1Moz_6v9-22` | Strong: 6:17 H5315 nincs a versben (*rúach chajjim*) |
| 6 | `1Moz_15` | ⚠️-vita (DT-F37a 2.); Sod: Mt 27:45 párhuzam |
| 7 | `1Moz_1v2-2v3` | ⚠️-vita (DT-F37a 4.); elavult ⭐-jegyzet (272. sor, TEREMT-002) |
| 8 | `1Moz_10v1-11v32` | ⚠️ „hetven nép” képviselő nélkül; nyelvzavar-⚠️ RÉSZBEN; `Jób 38:41` Károli-számozása (`Jób 39:3`) |
| 9 | `1Moz_13v1-18` | ⚠️ „mint a föld pora”: név nélküli oldalak |
| 10 | `1Moz_16` | elavult „Motívumnaplózásra váró elemek” jegyzet (198–203. sor); Sod RÉSZBEN |
| 11–16 | `1Moz_2v4-7`, `1Moz_2v8-25`, `1Moz_9v18-29`, `Zsid_4v12`, `1Moz_4v25-5v32`, `1Moz_6v1-8` | csak RÉSZBEN-leletek (Sod-levezetés vagy ⚠️ „mások”/„néhány értelmező”) |

**Szabályok a menetekhez:** forrás nélküli ⚠️-oldalt név nélkül nem szabad „kitölteni” — ha nincs megnevezhető képviselő, az oldal törlendő vagy explicit „képviselő nem azonosítva” jelölést kap (`CLAUDE.md` 3. szabály); a 7. pont (magyar szó ↔ Strong) a #22-ig kihagyva (DT-F37-4).

## Nem ebbe a feladatba tartozó, külön befogadandó tételek

- A T4 7. pontjának részleges bekapcsolása az 1–5Móz-ra és Józsuéra — külön döntés (DT-F37-4).

## A menet eltérései (a zárójelentésbe is)

- A T1 a brief `ir` listáján kívül is átírta a sablonnevet (`sablonok/4_`, `5_`, `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md`, a gyorsreferencia, a tanítói lista; a `Javasolt_…` fájlt a végrehajtó jelentése kihagyta, a független ellenőr találta meg); enélkül az elfogadási feltétel („a „Bővített sablon” név élő hivatkozásban nem fordul elő”) nem teljesült volna.
- Két kis módosításnál inline Python és `sed` futott magyar szöveggel (`CLAUDE.md` Shell-szakasz); mindkettő hiba nélkül lefutott, a kimenet ellenőrizve.
- Az F37.3 commit-üzenete 28 tesztet ír, a valós szám akkor 27 volt; a történet nem íródik át.
- A brief T6 1. pontja („Frissítsd a `FELADATOK.md` saját sorát”) nem teljesült, szándékosan: a #37 sora a `FELADATOK.md` generált blokkjában áll, amelyet csak a `main`-re futó Action ír (D25, `FELADATOK.md` „Állapot és új feladat”); az állapotot a brief fejléce viszi.
- A `CLAUDE.md` TAHOT-hiánylistájának elavulását a menet jelentette; a `main` közben javította (DT58, `07fcb39`), ezért külön tétel nem kell.
- A `naplok/TANULMANY_AUDIT.md` első változata a proveniencia-sorban a `f25faa6` commitot nevezte meg, amelyben a generátor még nem volt benne; a jelentés újragenerálva (F37.10), a tartalma változatlan (433 találat).
- A „valódi ⚠️-vita” meghatározását és a T5 4–5. pontjának ítéleteit a végrehajtó hozta (`manual`); a meghatározást a DT-F37b pontosította.
