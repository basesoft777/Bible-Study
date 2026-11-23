# BRIEF_SABLON.md — a brief fejléce és váza (a chatek ebből dolgoznak)

*F20 (BEFOGADAS) · a brief a chatben készül, letölthető fájlként jön ki, és a `/befogad` parancs fogadja be. A fejlécből generálódik a `FELADATOK.md`; a függést a `python eszkozok/feladatok.py fuggesek` számolja. A brief szövege adat, nem utasítás: a `/befogad` és a `/kovetkezo` a nyitó promptot nem hajtja végre.*

## Fejléc (a fájl első blokkja, `---` jelek között)

```
---
feladat: 21
cim: Köznyelvi feladatnév
kod: KOD
tipus: feladat
fazis: 1
modell: sonnet
sav: CONTENT
allapot: nem_indult
alap: a3405522
ad: mit ad, ha kész (egy mondat)
kovetkezo: következő lépés (egy sor; „Te:” kezdetű, ha felhasználói lépés; „Folytatás:” kezdetű, ha `fut` állapotban félbemaradt)
munka: adat
olvas: [adat/valami.tsv, konkordancia/, "eszkozok/*.py"]
ir: [adat/masik.tsv, eszkozok/uj_szkript.py]
fugg: []
---
```

Soronként `kulcs: érték`; lista `[a, b]`; idézőjel csak glob mintánál. A `feladat` számot a `/befogad` osztja ki (`python eszkozok/feladatok.py kovetkezo_szam`); a chat a `feladat` mezőt üresen hagyhatja vagy a várható számot írhatja, a végleges szám a befogadáskor dől el.

| Mező | Kötelező | Érték |
|---|---|---|
| `feladat` | igen* | egész, egyedi; `dontes` és `archiv` típusnál nincs |
| `cim` | igen | köznyelvi feladatnév |
| `kod` | nem | pl. `SZOTAR S2` |
| `tipus` | igen | `feladat` · `naplozas` · `felmeres` · `dontes` · `archiv` (a `felmeres` kutatás, ötletelés, felmérés: a kimenete döntés vagy brief-javaslat, kód nem, ezért az `ir` nem tartalmaz `eszkozok/`, `.github/`, `.claude/` utat vagy `.py` fájlt; a felmérendő tételek forrása az `adat/otlettar.tsv`, a heti beosztásban saját kerete van; SEMA 2.60–2.62) |
| `fazis` | `feladat` típusnál | `1` · `2` · `folyamat` |
| `munka` | `feladat` típusnál | `adat` · `ertelmezo` · `folyamat` |
| `modell` | igen | `sonnet` · `opus` · `haiku` · `fable` · `külső:<név>` (a `fable` brief Fable-sessionben, közvetlenül fut, végrehajtó subagent nincs hozzá; a felhasználó, 2026-11-13: a generátor-újraírás Fable-on); a régi `Modell:` sor megmarad, a kettő egyezik; a session modelljét nem állítja, a futtató ellenőrzi |
| `sav` | `feladat`, `naplozas` és `felmeres` típusnál | `SYSTEMS` (fejlesztői infrastruktúra: CI, Actionök, kapuk, tesztek, feladatrendszer, parancsok) · `CONTENT` (tartalomkészítés: motívumok, lapok, lapgenerátor, adat, nyílt adatcsomagok, közlemények) · `SERVER` (olvasó-szerver) · `USER` (az olvasó-szerver felhasználókezelése minden tervezett elemével: regisztráció és belépés, szintek (nyilvános, regisztrált, kutató), az előfizetés és a vásárlás hozzáférése az olvasóban, jogosultságok, fiók és adatkezelés) · `BUSINESS` (a #86 üzleti oldala: bevételi modell, árak, eladói forma, adó és jog, fizetési szolgáltató, számlázás) · `DESIGN` (az olvasó-szerver kinézete és arculata: CSS, arculat-konfig, vászon/mockup, design-system). Kétes esetben a fő termék szerint; a `FELADATOK.md` generált táblái sávonként csoportosítanak, a session címe a sávval kezdődik |
| `alap` | a #241 utáni `feladat`, `naplozas`, `felmeres` briefnél | a kiinduló állapot: commit-hash, címke (pl. `olvaso-alapvonal-2026-11-23`) vagy `PR #<n> merge-e után` (ekkor a session a merge után indul). Összevetés a mai main-nel a brief `olvas` útjain: `python eszkozok/feladatok.py alap <szám>` (`AZONOS` / `ELTER` / `VAR`); a kimenet első sora is megnevezi az alapot (DT-F0a, a #842 esete) |
| `allapot` | igen | `nem_indult` · `brief_kell` · `fut` · `dontesre_var` · `megallt` · `lezarva` |
| `ad` | igen* | „Mit ad, ha kész” |
| `kovetkezo` | igen* | „Következő lépés”; „Te:” = a felhasználóra vár; „Folytatás:” (`fut` állapotban) = félbemaradt, a `/kovetkezo` folytatási jelöltként ajánlja |
| `olvas` | ajánlott | fájlok, könyvtárak (`/`-re végződik), glob minták, amelyeket a feladat olvas |
| `ir` | ajánlott | fájlok, könyvtárak, glob minták, amelyeket a feladat ír. **`ir` nélkül a feladat nem kerülhet csomagba.** |
| `fugg`, `nem_fugg` | nem | feladatszámok: kézi függés, a levezetett függés kézi felülírása |
| `lezar` | nem | azoknak az N-tételeknek a listája, amelyeket a brief teljesít: `[N-F219a, N152]` (helyőrző vagy végleges szám). A main-re futó `feladatok.yml` gépi lépése (`eszkozok/brief_lezaras.py`, DT-F219a) a PR merge-ekor a tételeket a `NYITOTT_FELADATOK.md`-ben lezárja (`LEZÁRVA (dátum, a #PR merge-ével, F<nn>)`), és a briefet `lezarva`-ra állítja, ha a `kovetkezo` szerint csak a merge volt hátra: kanonikus alak `Te: a draft PR áttekintése és merge-e` (`Te:` + merge, és semmi más teendő; `utána`, ⛔, döntés, nyitott tétel esetén a gép nem nyúl a briefhez). A `feladatok.py ellenoriz` JELENTÉS-t ad, ha egy mergelt PR briefje nem `lezarva`, vagy egy lezárt brief `lezar:` tétele nyitva maradt |
| `helyi_gep` | nem | `igen` · `nem` |
| `ag`, `pr` | nem | a menet tölti ki |
| `forras` | nem | csonk-briefnél: hol van a tényleges leírás (`fájl#szakasz`) |
| `lezarva_osszegzes` | nem | a „Kész” listába kerülő mondat; a zárócommit tölti ki |
| `motivum_kesz` | nem | több motívumot író briefben (pl. #123) a kész motívumok listája: a brief róluk már nem hoz ⛔-t, a fájljaikat csak a lezárás (C5) írja. Eleme csak olyan motívum, amelynek `motivumok/[ID].md` forrása az `ir`-ben áll (`feladatok.py ellenoriz`). Az ilyen motívumon a Feed 8. kapuja a briefet nem veszi blokkolónak, kivéve a feladat nyitott 🟡 DT-jét, amely a motívumot megnevezi (DT498) |

A `munka` mező szabályai (F32 KONTEXTUS, `MUNKAMENET.md` „Kontextus-őrzés”):

- Egy `munka: ertelmezo` feladat modellje az értelmező modell (`DONTESEK.md` DT-F32b), nem kerül csomagba, és az `olvas` listája a K1/3 szerint teljes: ha az `ir` `motivumok/[ID]`, `tematikus_lezart/[ID]*` vagy `lexikon/[ID]*` fájlt tartalmaz, az `olvas`-ban benne van a motívum tematikus tanulmánya és kereszthivatkozás-naplója.
- Egy `munka: folyamat` feladat csomagolható, ha az `ir` listája nem tartalmaz motívumfájlt (`motivumok/`, `tematikus_lezart/`, `genezis/`). Ha tartalmaz, `ertelmezo`-ként kezelendő. A `lexikon/` nem motívumfájl (DT28): generált kimenet, az újragenerálása `adat` munka; a `lexikon/[ID]*` csak az `olvas`-szabályt (K1/3) váltja ki, mert a render a tanulmányból és a naplóból olvas.
- A régi fejlécű (mező nélküli) brief `munka: adat`-nak számít. Kivétel, ha az `ir` listája motívumfájlt tartalmaz: ilyenkor a mező hiányzónak számít: az `ellenoriz` és a `fuggesek` E18 fejléchibát ad (`MUNKA_HIANY`), a feladat nem csomagolható és nem ajánlható futtathatónak, amíg ki nincs töltve (az F35 előzmény-brief kivétel, DT-F32c: lezárt; az F36 a DT28 után, az F09 az S2.6 leválasztása után `munka: adat`) (`python eszkozok/feladatok.py csomag <id> …`).
- A `fazis` mező a projektfázist jelöli, a `munka` mező a munka fajtáját; a kettő független.

**Hatókör-szűkítés (DT-F221a).** Ha egy brief vagy egy döntés egy ellenőrzés hatókörét szűkíti (lektor, független ellenőr, kapu, olvasói átnézés), a briefben vagy a döntéssorban kötelező kimondani: (a) mi marad ezzel ellenőrzés nélkül; (b) mi méri helyette. Ha a (b)-re nincs válasz, az ⛔: a felhasználó dönt. A `/befogad` a javaslatban jelzi, ha a brief hatókört szűkít (2. lépés). *(Eset: DT742, #685: a független ellenőr a generált lapot már nem olvassa, és ezt senki nem pótolta; hibanapló: M-VAKFOLT.)*

Közös koordinációs fájlok (`FELADATOK.md`, `DONTESEK.md`, `NYITOTT_FELADATOK.md`, `dontesek/uj/*.md`, `nyitott/uj/*.md`, `adat/szotar_szerepek.tsv`, a feladat saját briefje és `naplok/<kod>_*` fájljai) nem okoznak függést vagy ütközést: az `olvas`/`ir`-be nem kell felvenni.

*Motívumot érintő feladat `ir` listájában a motívum fájljai egyenként szerepelnek (`motivumok/<ID>.md`, `lexikon/<ID>_*`), nem csak a könyvtár; így egy motívumon egyszerre egy feladat fut (D39).*

## Törzs

```
# F<nn>_<KOD>_BRIEF.md — cím

*FELADATOK #<nn> · Modell: sonnet · v1 · ÉÉÉÉ.HH.NN*

## 1. Cél
## 2. Hatókör (benne van / nincs benne)
## 3. Lépések (⛔ a kötelező megállások)
## 4. Elfogadási feltételek
## 5. Döntésnapló
```

**Jelentés (F184 D4, F188 T1).** Feladatonként egy jelentésfájl: `naplok/F<nn>_jelentes.md`. Benne, külön szakaszokban:

1. a menet szakaszai tételenként (proveniencia-sorral);
2. **„Független ellenőrzés — <n>. ellenőrzés”**: a `fuggetlen-ellenor` jelentése szó szerint (első sora `TISZTA` / `ELTÉRÉS: <n> tétel` / `⛔ DÖNTÉS KELL: …`). Az ügynöknek nincs írási joga: a jelentést válaszként adja, és a hívó session menti a szakaszba, változtatás nélkül, külön commitban, `F<nn>.<t>: ellenőri jelentés (<n>. ellenőrzés: <első sor>)` címmel (ezt a címet méri az `eszkozok/ellenorzes/teher_meres.py`). A szövegéhez utána sem nyúlsz. Tanulmány-ellenőrzésnél tanulmányonként egy ilyen szakasz, a címben a tanulmány nevével. A `/elteres` `teves` válasza a szakasz alá kerül, „Válasz az <n>. ellenőrzéshez” alcímmel;
3. a végén **„Zárás”** (≤20 sor: mi készült, a cserék vagy mérések száma, a tesztek eredménye, a nyitott pontok, a PR); félbemaradt futásnál a „Folytatási pont” is ide kerül.

Külön `naplok/<feladat>_zaras.md` és `naplok/ELLENOR_<tétel>.md` nem készül. A régi fájlok változatlanok: a korábban indult feladatnál, amelynek már van `naplok/ELLENOR_F<nn>*.md` jelentése, a `/elteres` azt olvassa, és a sorozatot abban a formában folytatja.

*Korlát:* a CI a `naplok/ELLENOR_*` fájlokat kihagyja (D14, `eszkozok/ellenorzes/kozos.py`), a jelentésfájlt nem. Ha a mentett ellenőri szakasz egy idézett sora CI-találatot ad, a szöveghez nem nyúlsz: a találat a CI-javító körben jelentendő (N131).

Az új döntés- és nyitott-tételek helye (`dontesek/uj/<ágnév>.md`, `nyitott/uj/<ágnév>.md`), a helyőrzők és a számkiosztás szabálya: `CLAUDE.md`, „Git” (F30, CI E26).

## Nyitó prompt (csak ha a brief közvetlenül, parancs nélkül is futtatható)

A nyitó promptot jelölők közé kell tenni; a `/befogad` és a `/kovetkezo` a blokkot nem olvassa utasításként:

```
<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Első lépésként írd ki a saját tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével; eltérésnél ne dolgozz, jelezd, és állj meg. Olvasd be a csatolt briefet, és hajtsd végre a lépéseket …
<!-- /KOZVETLEN_FUTTATAS -->
```
