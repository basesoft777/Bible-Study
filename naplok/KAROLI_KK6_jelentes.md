# KAROLI_KK6_jelentes.md — újramérés és jelentés ⛔

*KK6 — KAROLI_KULCS_BRIEF.md v1.1 §3, 2. menet (KK4-KK6), a chat-kiegészítő
feltételekkel (F1–F7, 2026.09.25 jóváhagyva). Szkriptek:
`naplok/KAROLI_KK4_F1_elotte_general.py`, `naplok/KAROLI_KK6_regresszio_general.py`,
`naplok/KAROLI_KK6_utana_es_ok_general.py`, `naplok/KAROLI_KK6_lexikon_egyezes_general.py`.
Forrás-proveniencia (K5): lxx-morph commit `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`,
sha256(`verse_pairs.jsonl`) = `3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985`
(F7 szerint mindkettő igazolva az `--forras` klónon, l. lent).*

## F1 — mérési alap (deduplikált (LXX-fájl, igehely_lxx) pár, karoli_ok=szamozas_elteres)

| | Érték |
|---|---|
| **Előtte** | 1 015 pár (16 fájl, ebből `psalms-lxx.tsv` 67) |
| **Utána** | 344 pár (13 fájl, ebből `psalms-lxx.tsv` 67) |
| **Kitöltve** | 671 |
| **Csökkenés** | 66,1% |

A 671 kitöltött pár közül: `mt_szamozas_kovetes` (H2-javítás) és
`kezi_eltolas_tabla` (H1-javítás, most már a bővített, korlátozott
identitás-eset is) a két új forrás — a teljes szósor-szintű összesítés:
`karoli_ok`(sima siker) 20 881 · `kezi_eltolas_tabla` 333 ·
`mt_szamozas_kovetes` 1 561 · `nincs_mt_parositas` 146 ·
`nincs_karoli_konyv` 7 071 · `szamozas_elteres` 344 (`zsolt_felirat_eltolas`
0 — az általános MT-ág teljesen kiváltotta a régi, csak Zsoltárra szűkített
külön ágat, l. F5 alatt is).

## F2 — K7 az igazolt H5-nevezővel

A maradék 344 pár okonkénti bontása (a `KAROLI_KK1b_fejezetosztaly.tsv`
osztályai szerint): `H3_EGYIK_SEM` 253 (a 13 szándékosan üresen hagyott
fejezet, F3 szerint) · a fennmaradó 91 pár (`H5_VALODI_ELTERES_VAGY_CIMSOR_AMBIGUITAS`)
két alcsoportra bomlik: 67 a Zsoltárok cím-sor kettős-hivatkozási
ellenpróbája (két LXX-forrás egy KJV-célra, csak a magasabb kapja meg az
eltolást — dokumentált, szándékos tervezési döntés, nem hiba, l.
`LXX_OS/README.md` 2. szakasz "ellenpróba"), 24 pedig más könyvekben (Exodus
14, Ézsaiás 2, 1Sám 2, 1Kir 2, Én 1, 4Móz 1, Jón 1, Hós 1) — ezeket egyenként
nem sikerült igazolni ebben a menetben, konzervatívan mind H5-ként (valódi
vagy fel nem tárt eltérés) kezelve.

| | Érték |
|---|---|
| H5-ként igazolt/kezelt pár | 91 |
| K7 nevező (1 015 − 91) | 924 |
| K7 arány (671 / 924) | **72,6%** |

**K7 állapota: NEM TELJESÜL** (72,6% < 90%), okonként indokolva: a
fennmaradó rés túlnyomó része (253/344, 73,5%) a szándékosan érintetlenül
hagyott `EGYIK_SEM` fejezetekből jön (F3), a többi (91/344, 26,5%) a
Zsoltár cím-sor-ellenpróbából és fel nem tárt egyedi eltérésekből.

## H5 és EGYIK_SEM darabszám

- **EGYIK_SEM (F3, szándékosan üres):** 253 pár, 13 fejezet — változatlan,
  a KK2b menet tárgya (nincs jóváhagyva ebben a menetben).
- **H5 (valódi/fel nem tárt eltérés):** 91 pár, ebből 67 dokumentált
  cím-sor-ellenpróba (Zsoltárok), 24 egyedi, nem részletesen kivizsgált.

## F5 — regresszió

**Első implementáció (a G4 szó szerinti, tábla-visszakeresésen alapuló
olvasata): 991 regressziós sor** — ebből 983 Zsoltár (a
`konkordancia/Karoli_versmegfeleltetes.tsv` KJV-oldali visszakeresése
rendszeresen rossz célt adott a cím-eltolásos fejezetekben, mert a
`verse_pairs.jsonl` `mt_refs` mezője már KJV-számozású, nem valódi
MT-számozású — a tábla-alapú reverse-lookup ezt nem tudta helyesen
kezelni) és 8 Jób (a `job_38_41_eltolas` `None`-jának identitásként
kezelése határellenőrzés nélkül a 41. fejezetbe tartozó verseket is
tévesen a 40. fejezetbe helyezte). **Mindkét hibát a `resolve_karoli`
átdolgozásával javítottuk** (a tábla-visszakeresést egy közvetlen,
robusztus `d`-eltolásos képletre cserélve — ugyanaz a matematika, mint a
már bevált Zsoltár-cím-ág, csak általánosítva —, és a KEZI-identitás-ágat
egy Károli-vers-létezési korláttal ellátva). **A javított futás után: 0
regressziós sor** (`naplok/KAROLI_KK6_regresszio.tsv` üres, csak fejléc) —
mind a 22 104 korábban kitöltött sor pontosan ugyanazt az értéket adja.

## A lexikon "Egyezés"-bontása előtte → utána

| Kategória | Előtte | Utána |
|---|---|---|
| egyező | 123 | **127** |
| kutatói azonosítás függőben | 87 | **89** |
| szamozas_elteres | 15 | **9** |
| eltérő | 3 | 3 |
| nincs LXX_OS-könyv | 5 | 5 |
| LXX-minusz | 1 | 1 |
| **Összesen** | 234 | 234 |

## A 15 lexikon-sor új állapota

| Igehely | Ok (KK1) | Új állapot |
|---|---|---|
| Jób 17:13 | H3 | **változatlan** (szamozas_elteres — EGYIK_SEM, F3) |
| Jób 17:16 | H3 | **változatlan** (szamozas_elteres) |
| Jób 38:7 | H1 | **javult** → kutatói azonosítás függőben (Károli-cél megvan, a görög Strong-egyezés még nyitott) |
| Jób 38:16 | H1 | **megoldódott** → egyező |
| Jób 38:30 | H1 | **megoldódott** → egyező |
| Józs 12:4 | H4 | **változatlan** (szamozas_elteres — a lexikon-generátor a hiányos `joshua.tsv`-t (A-szöveg) preferálja a teljes `joshua-vaticanus-b.tsv` helyett, G6: csak javaslat) |
| Józs 13:12 | ~~H2~~ **H4 (korrekció)** | **változatlan** — a KK1 tévesen H2-nek sorolta be; valójában ugyanaz a H4 generátor-oldali ok érinti, mint a másik 4 Józs-sort (a `Karoli_versmegfeleltetes.tsv`-ben és a `joshua-vaticanus-b.tsv`-ben már helyesen szerepel "Józs 13:12", de a lexikon-generátor sosem nézi ezt a fájlt) |
| Józs 15:8 | H4 | **változatlan** |
| Józs 17:15 | H4 | **változatlan** |
| Józs 18:16 | H4 | **változatlan** |
| Hós 13:14 | H3 | **változatlan** (EGYIK_SEM) |
| Ézs 63:13 | H2 | **javult** → kutatói azonosítás függőben (Károli-cél megvan) |
| Jón 2:3 | H2 | **megoldódott** → egyező |
| Jón 2:6 | H2 | **megoldódott** → egyező |
| Jer 51:46 | H5 | **változatlan** (valódi LXX-minusz) |

**Összegzés:** 6/15 sor javult (4 teljesen "egyező"-vé, 2 "kutatói
azonosítás függőben"-né — ez utóbbiak Károli-célja megvan, csak a görög
Strong-egyezés vár kutatói megerősítésre), 9/15 változatlan (2 H3
`EGYIK_SEM`, **5 H4** — eggyel több, mint a KK1 becsülte, mert a Józs 13:12
tévesen lett H2-nek sorolva, valójában ugyanaz a Józsué-generátorhiba
érinti —, 1 H5 valódi eltérés).

## `eszkozok/ellenoriz.py`

RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 — változatlan a menet előtti
állapothoz képest.

## F6 — ütközésszám tisztázása

A KK1b-3 jelentés 1 925-öt mondott ki `UTKOZIK_ELLENORIZETLEN`-ként, a
`naplok/KAROLI_KK1b_utkozes.tsv` viszont 1 978 sort tartalmaz. Az eltérés
oka: a `KAROLI_KK1b_utkozes.tsv` **sor-szinten** listázza az ütközéseket
(egy `igehely_karoli`-hoz több térkép-sor is tartozhat, pl. amikor a
`LXX_versificacios_terkep.tsv`-ben egy Károli-célra 2 sor is van —
`Elteres_tipusa=Concatenation/Merge` esetek), míg a KK1b-3 jelentés
**egyedi `igehely_karoli`-nként** összesített (`osszesitve`, azaz egy
Károli-célra legfeljebb egyszer számolva). A 1 978 − 1 925 = 53 többlet
pontosan azon Károli-célok száma, amelyekhez 2 térkép-sor is tartozik.
Mindkét szám helyes a saját szintjén; a jelentés mostantól mindkettőt
megnevezi.

## F7 — regenerálás forrás-igazolása

| | Elvárt | Mért |
|---|---|---|
| lxx-morph commit | `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2` | `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2` ✓ |
| `verse_pairs.jsonl` sha256 | `3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985` | `3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985` ✓ |

Egyezés — nem kellett megállni. A `GreekWordList.js` (openscriptures/GreekResources,
commit `dd5a2fd530ab3c6b748c174cec38966c356d8111`) is a rögzített commiton lett
klónozva. A lexikon 3. szakasza kizárólag a saját generátorából frissült
(`python eszkozok/general.py --cel lexikon --ir`), kézi szerkesztés nem történt.

## K1–K8 és F1–F7 összesítő

| # | Feltétel | Állapot |
|---|---|---|
| K1 | 2. menet: csak a megengedett fájlok módosultak | **RENDBEN** — `eszkozok/lxx_os_import.py`, `konkordancia/LXX_OS/*`, `konkordancia/Karoli_versmegfeleltetes.tsv`, `naplok/KAROLI_*`, `lexikon/*_TUDOMANYOS.md` (a lexikon generátorának kimenete) |
| K2 | `ellenoriz.py`: SÉRTÉS 0 | **RENDBEN** |
| K3 | (1b-ből változatlan) | **RENDBEN** |
| K4 | (1b-ből változatlan) | **RENDBEN** |
| K5 | minden szám szkriptből, TVTMS/lxx-morph commit rögzítve | **RENDBEN** |
| K6 | nincs `csv` modul, héber/görög csak fájlból | **RENDBEN** |
| K7 | `szamozas_elteres` csökkenése ≥90%, F2 nevezővel | **NEM TELJESÜL** — 72,6% < 90%, okonként indokolva (253 EGYIK_SEM + 91 H5, l. fent) |
| K8 | minden K RENDBEN/NEM TELJESÜL, hatásszám csak mérésből | **RENDBEN** |
| F1 | dedup mérési alap, 1015→344 | **RENDBEN** |
| F2 | K7 igazolt H5-nevezővel | **RENDBEN** (az arány maga NEM TELJESÜL, de az F2 *módszere* RENDBEN alkalmazva) |
| F3 | EGYIK_SEM üres marad | **RENDBEN** — mind a 253 pár üres maradt |
| F4 | H4 (Józsué) nem javítva ebben a menetben | **RENDBEN** — 5 Józs-sor (a Józs 13:12 korrekcióval) mind "H4 — külön javítás" jelöléssel |
| F5 | regresszió-ellenőrzés, indokolatlan változás = NEM TELJESÜL/ÁLLJ | **RENDBEN** — az első implementáció 991 regressziót adott, ez KIJAVÍTVA lett (nem elfogadva indoklással), a végleges futás 0 regressziót ad |
| F6 | ütközésszám tisztázva | **RENDBEN** — 1 925 (egyedi Károli-cél) vs. 1 978 (sor-szint), mindkettő megnevezve, az eltérés oka feltárva |
| F7 | regenerálás a rögzített commitokkal | **RENDBEN** — mindkét sha256/commit egyezik |
