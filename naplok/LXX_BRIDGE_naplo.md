# LXX_BRIDGE_naplo.md — az F43 futásnapló

*F43 (LXX_BRIDGE) · 2026.10.04 · Modell: sonnet · a döntéstábla (`adat/lxx_dontesek.tsv`) változatlan.*

A napló minden száma a lenti parancsok kimenetéből származik (proveniencia: `scope=lxx_dontesek LD005–LD090 | forras=adat/kulso/lxx_bridge.tsv + konkordancia/LXX_OS + konkordancia/LXX_kivonat_* | ts=2026-10-04`). Ahol nem futott lekérdezés, ott a megjegyzés „értelmezés”.

## 1. Parancsok

```
python eszkozok/lxx_bridge_egyezes.py          # kimenet: naplok/LXX_BRIDGE_egyezes.tsv (86 sor)
cp naplok/LXX_BRIDGE_egyezes.tsv /tmp/e1.tsv; python eszkozok/lxx_bridge_egyezes.py; cmp /tmp/e1.tsv naplok/LXX_BRIDGE_egyezes.tsv   # determinizmus: azonos (DET_OK)
git diff --stat -- adat/lxx_dontesek.tsv        # üres
grep -cE "^H(7498|7497|7496|5303|6093|8004)\b" adat/kulso/lxx_bridge.tsv   # 0
```

A script nem hív hálózatot; a TSV-ket `split('\t')`-bel olvassa, `'\t'.join()`-nal írja.

## 2. Séma és normalizálás (1. lépés)

| Ellenőrző szám | Kártya | Mért |
|---|---|---|
| fejléc | `hebrew_strong`, `greek_strong`, `count` | `hebrew_strong\|greek_strong\|count` — egyezik |
| adatsorok | 3 301 | 3 301 |
| egyedi héber Strong | 1 862 | 1 862 |
| egyedi görög Strong | 1 571 | 1 571 |

Eltérés nincs. A bridge Strong-jai `H####`/`G####` alakúak; a script mindhárom oldalon (bridge, `lxx_dontesek`, `LXX_OS` csupasz szám, régi `LXX_kivonat` `G0746`) egész számra normalizál, a kimenet `H####`/`G####`.

A döntéstáblából LD001–LD004 (a #6 ISTENTISZT-pilot sorai) kimarad; a bemenet az LD005–LD090 = 86 sor (bizonyosság: biztos 61, valószínű 13, nyitott 4, nem_alkalmazható 8 — a kimenet bizonyosság×kategória táblájából összeadva egyezik a DT23-mal).

## 3. Lefedettség (2. lépés)

- A 86 sor mindegyikéhez van `LXX_OS` vers (`vers_strongok_forras=LXX_OS`: 86) **és** régi `LXX_kivonat` sor is (`lefedettseg=OS+kivonat`: 86). Csak-kivonat vagy nincs-vers eset: 0. A tartalék (D4) ezért nem lépett működésbe.
- Az `LXX_OS` `strong_ok` oszlopa: üres = van Strong (a GreekWordList szerint), `nincs_uszbeli_megfelelo` / `lemma_nem_talalhato` = nincs Strong (a forrás korlátja: csak az ÚSZ-ben is előforduló lemmáknak van Strong-ja). A script nem szűr rá; a Strong nélküli tokenek számát soronként a `vers_strong_hiany` oszlop adja (összesen 167 token, 64 soron). **Következmény:** az olyan görög lemma (pl. γίγας, Ραφα, γηγενής), amelynek nincs Strong-ja, a versben álló halmazból hiányzik, így a bridge-egyezés rájuk eleve nem mutatható ki.

## 4. Összesítés (3–4. lépés)

Kategória (86 sor): `egyezik` 24 · `elter` 3 · `lxx_minusz_osszhang` 1 · `lxx_minusz_ellentmond` 0 · `nincs_adat` 46 · `nem_alkalmazhato` 8 · `nyitott_jelolt` 4 · `egyezik_lexema` 0.

| bizonyosság | kategória | db |
|---|---|---|
| biztos | egyezik | 23 |
| biztos | elter | 3 |
| biztos | nincs_adat | 35 |
| valószínű | egyezik | 1 |
| valószínű | lxx_minusz_osszhang | 1 |
| valószínű | nincs_adat | 11 |
| nyitott | nyitott_jelolt | 4 |
| nem_alkalmazható | nem_alkalmazhato | 8 |

**A `nincs_adat` (46) bontása** (a `megjegyzes` oszlopból): 31 sor — a héber Strong nincs a bridge-ben (≥3 szűrés): H7497 (a TAHOT szerinti Strong a rafá-/gigász-sorokban; a bridge a MACULA-címkézésből épül, amely H7498-at használ, de a bridge-ben H7498 sincs), H7496, H6093, H8004, H7043, H5303 mind hiányzik); 14 sor — a héber Strong szerepel, de a bridge-jelöltek egyike sem áll a versben (mind a 14 sorban a döntés görög Strong-ja sincs a bridge-párok között: pl. H7585→θάνατος G2288, H7843→καταφθείρω G2704, H8415→γῆ/πόντος/κῦμα/ἄνεμος/οὐρανός, H2555→ἀδικέω, H3548→ἱεράτευμα); 1 sor — a döntésnek nincs görög Strong-ja (LD010, βόθρος).

**`egyezik` (24):** LD012, LD013–LD016, LD019, LD020, LD023 (H0127→γῆ G1093), LD022 (H7451→πονηρός), LD025, LD039, LD040 (H2555→ἀδικία), LD031–LD034 (H2555→ἀνομία), LD035–LD038, LD041 (H2555→ἀσέβεια), LD076, LD081 (H3548→ἱερεύς), LD082 (H1121→υἱός). Közülük egy `valószínű`: **LD035** (Mik 6:12, H2555→ἀσέβεια G0763, bridge-count 8); a többi 23 `biztos`.

## 5. Az `elter` és `lxx_minusz_*` sorok egyenként

Az `elter` 3 sorának mindegyikében a „versben álló bridge-jelölt” kizárólag funkciószó (G3588, ὁ — az `adat/grammatikai_strongok.tsv`-ben szerepel), tehát tartalmi ellentmondásról nincs szó; a bridge a döntés Strong-ját a ≥3 szűrés miatt nem tartalmazza.

- **LD017** (1Móz 4:7, H2403, döntés: ἁμαρτάνω G0264, `biztos`): a bridge-párok G0266 (ἁμαρτία, 244), G3588 (7), G0265 (5); a versben csak a G3588 áll; a döntés G0264 nincs a bridge-ben, tartalmi ellentmondás nincs.
- **LD084** (Jób 1:6, H1121, döntés: ἄγγελος G0032, `biztos`): a bridge szerint H1121 → υἱός (3957), G3588 (58), τέκνον (54), G1537 (32); a versben csak G3588 áll; a döntés G0032 nincs a bridge-ben (a „Isten fiai” → ἄγγελοι fordítói döntés pont az, amit a korpusz-szintű lista nem lát).
- **LD085** (Jób 2:1, H1121, döntés: ἄγγελος G0032, `biztos`): ugyanaz, mint LD084.

`lxx_minusz_ellentmond`: 0 sor. `lxx_minusz_osszhang`: 1 sor — **LD006** (Jób 24:19, H7585, `valószínű`): a bridge H7585→ᾅδης G0086 (39), εἰς G1519 (9); egyik sem áll a versben, ami összhangban van a minusz-döntéssel. A 86 sorban a másik `lxx_minusz` sor: LD050 (H5303 — nincs a bridge-ben → `nincs_adat`); az LD004 (Zsolt 116:17) a #6 pilot sora, nem tárgya az F43-nak.

## 6. A 4 `nyitott` sor bridge-jelöltje (a jelölt-lemmák a `megjegyzes`-ből, a Strong-számok a `LXX_OS` verséből feloldva)

- **LD008** (Préd 9:10 → LXX Ecclesiastes 9:8; H7585): jelölt ᾅδης G0086 — a bridge-ben van (H7585→G0086, 39) = `egyezik`; azonban a sor saját versében (Ecclesiastes 9:8) nem áll (a jelölt a szomszéd versből, Ecclesiastes 9:10-ből való — ez maga a nyitott ok, az igehely-számozás).
- **LD009** (Ézs 7:11; H7585): jelölt βάθος G0899 — nincs a H7585 bridge-párjai közt = `elter` (a βάθος a LXX-ben a הַעְמֵק-hez tartozik, a bridge ezt nem mutatja a שְׁאוֹל-hoz); a versben áll. A H7585 bridge-párja a versben csak εἰς G1519 (9), ez nem a kulcsszó megfelelője.
- **LD058** (2Sám 21:22; H7497): a jelöltek (Ραφα, γίγας) Strong nélküliek a `LXX_OS`-ben (`nincs_uszbeli_megfelelo`), a H7497 pedig nincs a bridge-ben → nem mutatható ki, `nincs_adat`.
- **LD064** (Péld 2:18; H7496): γηγενής Strong nélküli (`nincs_uszbeli_megfelelo`), a H7496 nincs a bridge-ben; a ᾅδης G0086 a versben áll, de a H7496-nak nincs bridge-sora → `nincs_adat`.

Összefoglalva: a bridge a 4 nyitott sor közül egyiket sem dönti el.

## 7. Módszertani megjegyzések

1. **A bridge korpusz-szintű**, ≥3 előfordulásra szűrt; a ritka (és a vers-szinten épp a legérdekesebb) fordítói megfelelők hiányozhatnak. Ezért a `nincs_adat` nem negatív lelet.
2. **A bridge és a Macula szó-szintű illesztés közös forrásból (MACULA-címkézés) származik**, így az `egyezik` nem független bizonyíték a SEMA 2.11 „két független forrás” értelmében (l. a (a) javaslatot).
3. **Funkciószó-zaj:** a bridge-párok közt a G3588 gyakran ott van; a metszetben szereplő funkciószó nem tartalmi egyezés. A 3 `elter` sor mind ilyen.
4. A 24 `egyezik` sor közül 23 már `biztos`; bizonyosság-emelési jelölt csak LD035 (valószínű + egyezik).

## 8. ⛔ Döntési javaslat (a DONTESEK.md-be szánt szöveg; NEM beírva)

**DT-F43 — az `lxx_bridge` ellenőrzés (F43) tanulságai és kérdései**

(a) *Számít-e a bridge-egyezés második független forrásnak a SEMA 2.11 `biztos` definíciójához?* Opciók: 1. igen — a módszer eltér (korpusz-szintű összesítés, nem vers-szintű illesztés), így a `valoszinu` + `egyezik` sor `biztos`-ra emelhető; 2. nem — a bridge ugyanabból a MACULA-címkézésből származik, mint a Macula szó-szintű illesztés, ezért csak tájékoztató; az emelés nem automatikus. **Javaslat: 2., azzal, hogy az `egyezik` sorok a DT-sorban név szerint felsorolva kapnak felhasználói emelési lehetőséget** (a DT23 (a) mintájára: „a felhasználó soronként biztosra állíthatja”). Az egyetlen `valószínű` + `egyezik` sor: **LD035** (Mik 6:12, H2555→ἀσέβεια G0763, bridge-count 8). A 23 `biztos` + `egyezik` sor (LD012, LD013–LD016, LD019, LD020, LD022, LD023, LD025, LD031–LD034, LD036–LD041, LD076, LD081, LD082) már `biztos`, változatlan.

(b) *Az `elter` és `lxx_minusz_ellentmond` sorok:* `lxx_minusz_ellentmond` nincs. Az `elter` 3 sora (LD017, LD084, LD085, mind `biztos`) csak funkciószó-metszetet mutat; tartalmi ellentmondás nincs. Opciók: 1. újranyitás `nyitott`-ra; 2. marad a döntés, a bridge-eltérés a `megjegyzes`-be. **Javaslat: 2. mindhárom sorra** (a bridge ≥3 szűrése és a funkciószó-metszet miatt az eltérés nem érdemi; a döntés dokumentált alapja a Macula + LXX_OS). A `megjegyzes`-bővítést külön menet végezze, ha a felhasználó kéri.

(c) *A 4 `nyitott` sor (LD008, LD009, LD058, LD064) bridge-jelöltje:* a bridge egyiket sem dönti el (LD008: ᾅδης a bridge-ben van, de másik versben áll; LD009: βάθος nincs a H7585 bridge-párjai közt; LD058, LD064: Strong nélküli jelölt, H7497/H7496 a bridge-ben nincs). **Javaslat: mind a 4 marad `nyitott`.**

(d) *Forráspolitika-kiegészítés (D17 mellé):* „Nem kereskedelmi (NC) vagy csak-hivatkozási licencű forrás nem kerül a repóba, származtatott adaton át sem; HF-dataset importja előtt a kártya attribúciós táblája ellenőrizendő. Kizárva: CrossWire `GreekHebrew` és `HebrewGreek` (Pierre Leblanc, Abbott-Smith + Hatch–Redpath alapján; „copyrighted, free non-commercial distribution”) és származékaik (pl. NuBerea/lxx-analysis, NuBerea/crosswire-greekhebrew).” Elfogadás/elvetés a felhasználó döntése.

**Megállás:** a feladat itt felfüggesztve; a (a)–(d) döntések a felhasználóra várnak. A 6. lépés (`fuggetlen-ellenor`, `naplok/ELLENOR_LXX_BRIDGE.md`, push, draft PR) az orkesztrátor feladata.
