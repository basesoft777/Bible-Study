# F123 X.A — a HAMART-001 adat-előkészítése (munkafájl)

*#123 MIGRACIO2 · 2b. 1. lépés (`munka: adat`) · ág: `claude/f123-hamart-adat-f698da` · modell: claude-opus-5-5 · 2026-11-02*

*Döntés nélküli munkafájl: jelentéstartományt nem választ, prózát nem ír, motívumfájlt (`motivumok/`, `tematikus_lezart/`, `lexikon/`) nem ír (2b). A teljes sorok a mellékelt TSV-kben állnak, minden sor mellett a lekérdezés proveniencia-sorával; ez a fájl összegzés. A lekérdezések naplója: `naplok/F123_lekerdezesek.tsv` (`lekerdez.py --naplo F123`). Munkaszkript: `naplok/F123_adat_keszito.py` (az ALVIL-001/ANTROP-001-é; új alparancsok: `kollok`, `csalad`, `lanc`, `lxx_e`), felmérő eszköz: `eszkozok/motivum_felmeres.py`. Futtatás: `PARDES_DATUM=2026-11-02`, a `c43c1b4d` (main) commiton.*

*Hatókör (DT497 (2), DT508 (2)): csak az X.A. Az X.M1–X.M5, az X.T (a tanulmány 307–316. sora) és minden prózát író lépés a DT585 (a `9_` sablon v1) ⛔ után jön. A HAMART-001 a DT413 szerint az utolsó migrált motívum (előtte új N0-kontroll); az X.A ettől függetlenül futhat (2a., végrehajtási rend). A HAMART-001-nek **van** külön kereszthivatkozás-naplója: `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md`.*

## 0. A motívum az adatrétegben

| Mező | Érték |
|---|---|
| `adat/motivumok.tsv` | A bűn következményeinek gyűrűzése — átok, föld és romlás · **`strukturális`** · tanulmány: `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` |
| negatív kritérium | a hely a gerinc valamelyik elemén (arar, adamá, itzávón, chattát, chámász, sáchat; ἐπικατάρατος, κατάρα, φθείρω-család) vagy megnevezett kollokációján (málé+chámász, sámá+chámász) át a genezisi átok→föld→romlás láncra utal vissza; e lexémák nélkül csak explicit „tematikus, nem lexikai” jelöléssel |
| fölérendelt fogalom | a bűn / hamartológia általában |
| `adat/elofordulasok.tsv` | 52 sor (77 vers); `gerinc_elem`: H0779 7, H0127 7, H7843 7, málé+chámász 6, H2555 4, sámá+chámász 4, H6093 2, G1944 2, H6975+H1863 1, H2403 1, H7451 1, H7043 1, G5356 1, G2671 1, G1311 1, G5351 1, `tematikus:` 5 (1Móz 3:17 → Ézs 24:5-6, Hós 4:1-3; 1Móz 6:5 → Mt 15:19, Mk 7:21-23; 1Móz 6:13 → 2Pét 3:6-7) |
| `adat/jeloltek.tsv` | 223 sor: 52 `beépítve`, 163 `elutasítva`, 8 `nyitva` (Jób 16:18, 31:38; 5Móz 4:25, Bír 2:19, Sof 3:7; 2Pét 3:10, 3:12 — N-F63a/c; 2Tim 3:8 — F108) |

Mért adathiány a soron (nem e menet dolga, az értelmező menet elé): mind az 52 sor `funkcio` mezője üres; a görög sorok (8) és a `tematikus:` sorok `lexikon_szotar`/`jelentes_szam` nélkül állnak.

**A hordozóból következő korlát:** a `strukturális` hordozón sem a #150 formulaikus, sem a #160 lexikai gépi előszűrő nem dönt; az 5 mért hamis kizárás (Ézs 24:5-6, Hós 4:1-3, Mt 15:19, Mk 7:21-23, 2Pét 3:6-7 — mind `tematikus:` sor) mutatja, miért (`naplok/JELOLT_ELOSZURES_LEXIKAI_naplo.md` 8.). Ez a menet ezért nem szűr, hanem a negatív kritérium **gépileg mérhető kitételeit** méri (1b–1e.), sorrendező mezőként.

**A határ-anyag:** `naplok/HATAR_HAMART-001.md` (gépi rész, 2026-10-29): 0 részhalmaz-kérdés, a negatív kritérium gépi próbája strukturális hordozón nem fut, a modelles rész nem futott; `naplok/LEKTOR_HAMART-001.tsv`: 0 kérdés (csak fejléc). Az X.A határkérdése (DT543) ott nem áll kérdésként; nincs mit duplikálni.

Proveniencia: `scope=HAMART-001: adat/motivumok.tsv (1 sor), adat/elofordulasok.tsv (52 sor), adat/jeloltek.tsv (223 sor) | forras=split('\t'), ág claude/f123-hamart-adat-f698da | ts=2026-11-02`

## 1. A törzs összevetése a #108 eltérés-táblájával (2c)

**A törzs nincs újra levezetve** (2c): a meglévő sorok a `naplok/F108_ujrascan_elteresek.tsv` (2026-10-17) 1 570 HAMART-001-sorával vannak összevetve, és a sorok `strong` mezőjének 14 értékére lefutott a mai scan (`f108` alparancs, változatlanul).

| Mérés | Eredmény |
|---|---|
| `elofordulasok.tsv` (ma / F108) | 52 / 52 — **új vagy eltűnt sor: 0** |
| `jeloltek.tsv` (ma / F108) | 223 / 222 — 6 „eltűnt” és 6 „új” sor **egy-egy F114-kulcsjavítás** (a TSK KJV-kulcsa → Károli: Préd 9:3→9:5, 2:11→2:12, 2:17→2:18, 2:22→2:24, Zsolt 55:9→55:10, 140:11→140:12; DT199, az indoklásban jelölve), döntésük változatlan; +1 a #108 által írt `nyitva` sor (2Tim 3:8, G2704, `uj_jelolt_irva`); döntést váltott sor: 0 |
| `KULCS_ELTERES` | 4 — 1Móz 4:10 (H0779), Zsid 6:7 (G2671), Róm 8:20, 8:22 (G5356): mind **tartomány-hatás** (a sor `1Móz 4:10-11`, `Zsid 6:7-8`, `Róm 8:20-22`; a Strong a tartomány másik versében áll), nem kulcshiba |
| mai scan, új hely | **1 299 találat, 1 256 vers**, egyik sincs E-ben vagy J-ben: H7451 607, H2403 269, H0127 186, H7843 117, H7043 73, H2555 39, H6975 8. Az F108 ugyanezeket látta (`uj_talalat_nem_irva_tul_tag` / `zsoltar_55_…`), **kivéve a 8 H6975-öt** (az F108-ban sem): ezek a magányos „tövis”, mert a gerinc-elem a `H6975+H1863` pár, a scan viszont a `strong` mezőt (H6975) futtatta; a pár mérése: 1b. |
| #110 szűrő | nincs HAMART-001-szabály (DT283: csak ISTENTISZT-001); a térkép szerint 99 % `szuretlen_tag` (NYITOTT, F124-tétel); l. 6. |

**A tág új helyek a negatív kritérium lexémalistája szerint:** a H7451 (ra'), a H7043 (qalal) és a magányos H6975 **nincs** a kritérium felsorolásában, bár egy-egy E-sor `gerinc_elem`-je (1Móz 6:5, 8:21, 3:18; ez az N-F63e tárgya). Csak listán kívüli Strongot hordozó vers: **651**; legalább egy listán belüli Strongot hordozó: **605**.

**Eredmény: gerinc-elemet érintő eltérés (Strong be/ki) nincs** (2c ⛔ nem nyílik).

Részletes sorok: `naplok/F123_adat_HAMART-001_f108_osszevetes.tsv` (52 E + 229 J — a 6 „eltűnt” F108-sorral — + 1 395 újrascan-sor).

Proveniencia:

- `scope=HAMART-001: adat/elofordulasok.tsv (52 sor) + adat/jeloltek.tsv (223 sor) × naplok/F108_ujrascan_elteresek.tsv (1570 sor) | forras=split('\t'), ág claude/f123-hamart-adat-f698da | ts=2026-11-02T13:06Z`
- a 14 scan proveniencia-sora (pl. `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7451 | n=621 | ts=2026-11-02T13:07Z | csatorna=cli`) a `naplok/F123_lekerdezesek.tsv`-ben.

## 1b. A kritérium kollokációi és az összetett gerinc-elem (`kollok`)

`python naplok/F123_adat_keszito.py kollok HAMART-001 H4390+H2555,H8085+H2555,H6975+H1863` — a #108 módján (`lekerdez.py kollokacio`, egy versben).

| Pár | Hely | Előfordulás | **Új** |
|---|---|---|---|
| málé+chámász (H4390+H2555) | 8 | 8 (a 6 `málé+chámász` sor + 1Móz 6:11, 6:13) | 0 |
| sámá+chámász (H8085+H2555) | 4 | 4 | 0 |
| H6975+H1863 (kóc + dardar) | 2 | 1 (1Móz 3:18) | **1 — Hós 10:8** |

Sorok: `naplok/F123_adat_HAMART-001_kollokacio.tsv`. Proveniencia: `scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H4390+H2555 | n=8 | ts=2026-11-02T13:17Z | csatorna=cli`; a másik kettő (`n=4`, `n=2`) a sorokon és a lekérdezés-naplóban.

## 1c. A φθείρω-család (`csalad`)

A kritérium „φθείρω-család” kitétele. A család **nem kézi lista**: a TAGNT `Szótő` mezőjéből, ékezet nélkül illesztve (`φθειρ|φθορ|φθαρ`), 9 Strong; a privatív alakok (`α(δια)φθ-`) külön jelölve. Minden tag `lekerdez.py scan`-nel naplózva.

| Strong | Szótő | Típus | Előfordulás | Jelölt | **Új** |
|---|---|---|---|---|---|
| G5351 | φθείρω | pozitív | 1 | 7 | 0 |
| G5356 | φθορά | pozitív | 1 | 7 | 0 |
| G1311 | διαφθείρω | pozitív | 1 | 4 | 0 |
| G2704 | καταφθείρω | pozitív | 0 | 1 (2Tim 3:8) | 0 |
| G1312 | διαφθορά | pozitív | 0 | 0 | **6** — ApCsel 2:27, 2:31, 13:34, 13:35, 13:36, 13:37 |
| G5349 | φθαρτός | pozitív | 0 | 0 | **6** — Róm 1:23, 1Kor 9:25, 15:53, 15:54, 1Pét 1:18, 1:23 |
| G0861 | ἀφθαρσία | privatív | 0 | 2 | 6 |
| G0862 | ἄφθαρτος | privatív | 0 | 0 | 8 |
| G0090 | ἀδιαφθορία | privatív | 0 | 0 | 1 |

Mért tény, nem állítás: a G1312 hat helye a Zsolt 16:10 idézete és magyarázata (a test nem lát rothadást) — az ALVIL-001 közelében (ApCsel 2:27, 2:31 ALVIL-001-előfordulás). A privatív alakok a romlás ellentétét mondják; hogy a kritérium „családja” kiterjed-e rájuk, értelmezés.

Sorok: `naplok/F123_adat_HAMART-001_csalad.tsv`. Proveniencia: soronként `scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=<G…> | n=… | ts=2026-11-02T13:17Z | csatorna=cli`.

## 1d. A lánc-lexémák együttállása (`lanc`) — sorrendező mező, nem szűrő

A kritérium szerint a hely a gerinc valamelyik elemén át a láncra utal vissza; ez gépileg nem dönthető. Mérhető közelítése: hány **különböző** lánc-lexéma (a kritérium 14 Strongja: H0779, H0127, H6093, H2403, H2555, H7843, G1944, G2671 és a pozitív φθείρω-tagok) áll egy versben, illetve ±1 versen belül, azonos fejezetben. Az egylexémás hely is tartozhat ide (pl. a Jer 17:5 vagy az 5Móz 27 E-sorai), a kétlexémás is eshet ki.

| Alap | Előfordulás | Jelölt | **Új** |
|---|---|---|---|
| ≥2 lexéma egy versben | 9 | 2 (Mal 1:14, 2Pét 2:12 — mindkettő `elutasítva`) | **6** |
| ≥2 lexéma csak a ±1 ablakban | 8 | 0 | **16** |

A 22 új vers ≈ 14 hely: 5Móz 9:26–27 (H2403+H7843), 5Móz 19:15–16 (H2403+H2555), 1Kir 8:34–35, 1Kir 13:34, 1Kir 14:15–16, 2Kir 17:22–23, 2Krón 6:25–26, Neh 9:1–2 (H0127+H2403), Zsolt 25:18–19 (H2403+H2555), Ez 12:19 (H0127+H2555), Ez 28:17 (H2555+H7843; a 28:16 E-sor), Hós 9:9 (H2403+H7843), Mik 6:13 (H2403+H2555; a 6:12 E-sor), Mal 3:11 (H0127+H7843). Mind a 22 a 1. szakasz 1 299 tág találata közül való.

Sorok: `naplok/F123_adat_HAMART-001_lanc_ablak1.tsv`. Proveniencia: `scope=TAHOT-teljes+TAGNT-teljes: legalább 2 különböző lánc-lexéma (…) egy versben vagy ±1 versen belül, azonos fejezet | forras=konkordancia/TAHOT_kivonat.tsv, TAGNT_kivonat.tsv (lekerdez.load_tahot/load_tagnt), split('\t') | állapot: adat/elofordulasok.tsv, adat/jeloltek.tsv (HAMART-001) | ts=2026-11-02T13:17Z`

## 1e. LXX-híd a héber előfordulás-verseken (`lxx_e`)

A 6. lépés: a 43 héber E-sor 62 versére `lekerdez.py lxx-hid` (62 naplózott lekérdezés), és megnéztem, áll-e az LXX-versben a kritérium görög eleme (G1944, G2671, G2672 καταράομαι, a pozitív φθείρω-tagok).

| Eredmény | Vers |
|---|---|
| kritérium-görög az LXX-ben | **31** — G1944 (1Móz 3:14, 3:17, 4:11, 9:25, 5Móz 27:15–26, 28:16–19, Jer 17:5), G2672 (1Móz 5:29, 8:21, 12:3), G5351 (1Móz 6:11), G2704 (1Móz 6:12, 6:13, 6:17, 9:11), G1311 (Zsolt 14:1, 53:2) |
| nincs | 31 — köztük minden `chámász`-sor (az LXX itt ἀδικία/ἀσέβεια-félét hoz, nem a kritérium szavát) és a két `tematikus:` ÓSZ-sor |
| nincs LXX-vers | 1 — Jer 51:46 (az LXX Jer 28; a `lxx-hid` nem talált párt) — a 31 „nincs” egyike |

Mért tény: az LXX-beli szó nem bizonyít visszautalást, és a hiánya sem zár ki. A G2672 (καταράομαι) a kritérium felsorolásában nincs (ott: κατάρα G2671), itt jelölt mezőként áll.

Sorok: `naplok/F123_adat_HAMART-001_lxx_hid.tsv` (62 sor, mindegyiken a saját `lxx-hid` proveniencia-sorával, pl. `scope=range:1Móz 3:14 | forras=LXX_OS/genesis.tsv+TAGNT_kivonat.tsv | n=40 | ts=2026-11-02T13:18Z | csatorna=cli`).

## 2. Szótári sorok, hiányzó fordítások, szerepenkénti nyers kínálat (2b)

A motívum Strongjai az `elofordulasok.tsv` `strong` mezője szerint: **H0127, H0779, H2403, H2555, H6093, H6975, H7043, H7451, H7843; G1311, G1944, G2671, G5351, G5356** (14). A H1863 (a 1Móz 3:18 pár másik tagja), a H4390/H8085 (a kollokációk igéi) és a 1c. új családtagjai (G1312, G5349, G2704) nincsenek benne: a szótári kínálat a sorokon álló Strongokra szól; ha az értelmező menet ezeket gerinc-elemnek veszi, a munkaszkripttel pótolhatók.

**Szótári sorok:** 1 180 sor (héber 1 061, görög 119), `naplok/F123_adat_HAMART-001_szotar.tsv` (forrás, kulcs, hossz, SHA-1-előtag, kivonat, a generátor szerinti `forditasok.tsv`-kulcs és állapota, proveniencia).

**Szerepenkénti nyers kínálat** (`adat/szotar_szerepek.tsv`): `naplok/F123_adat_HAMART-001_szerepkinalat.tsv`, mind a 26 szerephez van sor. A 10., 12. és 14. szerep, mint az ALVIL-001-nél és az ANTROP-001-nél, jelölt állapot, nem szótári forrás. Jelentéstartomány nincs kiválasztva (a 2. lépés D50-döntése).

**Hiányzó fordítások — 265 kulcs** (`naplok/F123_adat_HAMART-001_forditas_hiany.tsv`; **a `forditasok.tsv`-be nincs írva**, a pótlás külön adatfeladat, 2b):

| Szótár | Mező | Kulcs | Strongonként (a legnagyobbak) |
|---|---|---|---|
| BDB | forditas_hu | 112 | H7451 27, H7043 25, H2403 20, H7843 12, H0127 11, H0779 8 |
| UBS_DBH | definicio_hu + glosszak_hu | 88 | H7043 22, H7451 18, H2403 14, H7843 14 |
| tW_szocikkek | forditas_hu | 25 | H2403 5, H7451 5 |
| UBS_DNTG | definicio_hu + glosszak_hu | 16 | G2671, G5351, G5356 4–4 |
| TBESH | forditas_hu | 9 | mind a 9 héber Strong |
| TBESG, MCGED, LSJ | forditas_hu / glosszak_hu | 5–5 | mind az 5 görög Strong |

A hiány 102 kulcsa (38 %) a kritérium-listán kívüli H7451 és H7043 szótári soraira esik (BDB 52, UBS_DBH 40, tW 8, TBESH 2); ha az N-F63e ezeket kiveszi a gerincből, a pótlandó kör ennyivel szűkül.

Proveniencia: minden sor saját proveniencia-mezővel; a futás: `scope=HAMART-001 Strongjai (14) × adat/szotar_szerepek.tsv | forras=naplok/F123_adat_keszito.py szotar | ts=2026-11-02T13:08Z`

## 3. Felmérő lekérdezés (2d. 1.) — `eszkozok/motivum_felmeres.py`

`python eszkozok/motivum_felmeres.py HAMART-001 --ki naplok/F123_felmeres_HAMART-001` (változatlan eszköz). Kimenet: `naplok/F123_felmeres_HAMART-001.md` és három TSV, **teljes egészében az értelmező menet elé** (2c). Mért tény, nem állítás; a közös szókészlet nem bizonyít idézést.

| Blokk | Eredmény | Fájl |
|---|---|---|
| (a) kísérő szavak | 390 Strong a 77 motívumversben (60 grammatikai kizárva). Leggyakoribb: H3605 כֹּל (27), H0559 אָמַר (25), H0776 אֶרֶץ (19), H0543 אָמֵן (12/24 — az 5Móz 27 „ámen”-sora), H0120 אָדָם (8), H4390 מָלֵא (8), H1818 דָּם (7), H1320 בָּשָׂר (6) | `…_kiserok.tsv` |
| (b) szomszédos motívumok, azonos fejezet | 7 pár: ISTENTISZT-001 (1Móz 4, 12), MENNY-001 (1Móz 6, távolság 1 vers), TEREMT-001 (1Móz 8, Jel 11), ALVIL-001 (Hab 2, 3 vers), KIRALY-001 (Zsid 6); közös vers egyiknél sincs | `…_szomszedok.tsv` |
| (c) válasz-szavak ±3 vers (H6030, H8085, G0191, G1522, G0611) | 30 találat 25 motívumversnél | `…_valasz.tsv` |

A (c) blokk nem semleges a HAMART-001-en: a H8085 (sámá) maga a `sámá+chámász` kollokáció igéje, így az Ézs 60:18, Jer 6:7, Jer 51:46, Hab 1:2 találata önmaga. A válasz-szólista az ISTENTISZT-001-felmérés paramétere.

Proveniencia: a `naplok/F123_felmeres_HAMART-001.md` három sora (ts=2026-11-02T13:09Z) és minden TSV-sor utolsó mezője.

## 4. Próza-lefedettség (2d. 2.) — mérés, nem kapu

**Helye:** a motívum naplója (`motivumok/naplok/HAMART-001_*`); az X.A a forrásréteget nem írja, ezért az eredmény itt és a `naplok/F123_adat_HAMART-001_proza_lefedettseg.tsv`-ben áll; **az értelmező menet viszi át**. Módszer: az ALVIL-001-é (`proza` alparancs); bemenet a tanulmány **és** a kereszthivatkozás-napló.

| Kategória (a kézi rések említésszáma) | Előfordulás-sor |
|---|---|
| tárgyalja (4+) | **28** |
| érinti (1–3) | **22** — köztük a teljes `málé+chámász`-csoport (Ez 7:23, 8:17, Zsolt 74:20, Mik 6:12, Sof 1:9: 2–3 említés), Hab 2:8, 2:17, Jer 51:46, Gal 3:10, Mt 15:19 |
| nem nevezi meg | **2** — 1Móz 3:23 (H0127; a tanulmány egésze 1-szer, a rések 0-szor), 1Móz 9:15 (H7843; a tanulmány 0-szor, csak a napló) |

| Rés | Méret | Igehely-említés |
|---|---|---|
| kivonat | 886 B | 4 |
| miert_fontos | 7 342 B | 37 |
| ertelmezes | 7 840 B | 31 |
| modszertan | 8 150 B | 95 |
| minosites | 18 137 B | 299 |
| 2b (szótári adat, nem próza) | 37 B | 0 |

A lefedettség a rések között egyenetlen: az említések 64 %-a a `minosites` (kereszthivatkozás-minősítés) résben áll, az értelmező prózában (`ertelmezes`, `miert_fontos`) 68. A `modszertan` résben áll az N-F55c régi LXX-forrásneve (javítása a migráció része, nem az X.A-é).

Proveniencia: `scope=HAMART-001: adat/elofordulasok.tsv (52 sor) × kézi rések (2b 37 B, ertelmezes 7840 B, kivonat 886 B, miert_fontos 7342 B, minosites 18137 B, modszertan 8150 B; forrás: a tanulmány és a kereszthivatkozás-napló) + a fájlok egésze + lexikon/HAMART-001_TUDOMANYOS.md (118554 bájt, generált) | forras=saját számláló (naplok/F123_adat_keszito.py proza) | ts=2026-11-02T13:09Z`

## 5. Ami az előző X.A-kból itt nem alkalmazandó

- A 2e. Seól-scan (ALVIL-001) és a `rokon`/`lxx` alparancs (ANTROP-001 összetett görög elemére): itt a kritérium kitételeit az 1b–1e. új alparancsai mérik.
- Az X.T (a tanulmány 307–316. sorának besorolása, `naplok/F11_T3_besorolas.tsv`) és az N-F55b/N-F55c (lxx-hid audit-sorok, a `modszertan` forrásneve) a szétválasztás (X.M1–X.M3) része.
- A gerinc-címkék és az `SZOTARI_GERINC` `kivetel` sorának törlése (X.K, N-F148c) az értelmező menet és az X.M5 része.

## 6. Döntések és nyitott pontok

A három ⛔-kérdést az orkesztrátor döntötte el, a felhasználó 2026-11-02-i felhatalmazásával: »… a döntéseket fogadja, és hozza is meg«. A tételek: `DONTESEK.md` DT542, DT543, DT544.

1. **DT542 (a), a kritérium-mérések új helyei:** 27 `nyitva` jelölt a `jeloltek.tsv`-ben (F123.HAMART.A12, `naplok/F123_jelolt_ir_HAMART-001.py`; a HAMART-001 sorai: 223 → 250), indoklás-típusonként:
   - „kollokáció (1Móz 3:18 gerinc-pár)” — 1: Hós 10:8;
   - „φθείρω-család — a kritérium lexémája” — 12: G1312 ApCsel 2:27, 2:31, 13:34–37 (a sorokon az **ALVIL-001-közelség** jelölve: a Zsolt 16:10 idézetének közege, az ApCsel 2:27 és 2:31 ALVIL-001-előfordulás — motívumközi kérdés lehet); G5349 Róm 1:23, 1Kor 9:25, 15:53, 15:54, 1Pét 1:18, 1:23;
   - „lánc-együttállás — gyenge, strukturális közelítés; az értelmező menet dönt” — 14 hely (az egymást követő versek egy hely): 5Móz 9:26-27, 5Móz 19:15-16, 1Kir 8:34-35, 1Kir 13:34, 1Kir 14:15-16, 2Kir 17:22-23, 2Krón 6:25-26, Neh 9:1-2, Zsolt 25:18-19, Ez 12:19, Ez 28:17, Hós 9:9, Mik 6:13, Mal 3:11.

   **A 15 privatív alak (ἀφθαρσία, ἄφθαρτος, ἀδιαφθορία) ellentétes jelentés, nem jelölt;** a sorai a `naplok/F123_adat_HAMART-001_csalad.tsv`-ben maradnak. Beépítés vagy elutasítás egyik új sorra sincs: az a B5 az értelmező menetben.
2. **DT543, módosított (b), a tág helyek (F124):**
   - a negatív kritérium lexémalistáján **belüli** Strongot hordozó **605 vers** szűretlen marad, az értelmező menet kézi átnézésére, a lánc-mérés (1d.) sorrendjében; a sorok a `naplok/F123_adat_HAMART-001_f108_osszevetes.tsv`-ben;
   - a listán **kívüli** Strongot hordozó **651 vers** (H7451 573, H7043 71, magányos H6975 7) blokk-kizárása **most nem történik**: meglévő E-sorok `gerinc_elem`-je (1Móz 6:5 H7451, 1Móz 8:21 H7043) ezekre a Strongokra mutat, a kizárás ellentmondana az adatnak, amíg az N-F63e el nem dől. A 651 vers `N-F63e-függő` jelöléssel vár: `naplok/F123_adat_HAMART-001_nf63e_fuggo.tsv` (F123.HAMART.A13; `nf63e` alparancs). A „jelöltlista” itt ez a munkafájl-tábla, nem a `jeloltek.tsv`: a 651 vers a 605-höz hasonlóan nem kap jelöltsort, amíg a döntés nincs meg (a `jeloltek.tsv` `dontes` mezője zárt: `nyitva` 651 sorral a nyitott jelöltek közé keverné őket);
   - az N-F63e a Kiadóra kerül tartalmi kártyaként (7.).
3. **DT544 (a):** a 8 régi `nyitva` sor (Jób 16:18, 31:38; 5Móz 4:25, Bír 2:19, Sof 3:7; 2Pét 3:10, 3:12; 2Tim 3:8) az értelmező menetre marad.

Nyitott (nem az X.A dolga):

4. **Hiányzó fordítások (265 kulcs):** külön adatfeladat (`forditasok.tsv`, a #123 `ir`-jén kívül; 2b), API-keretből — a költés a felhasználóé. Az N-F63e (1) válasza 102 kulccsal szűkítené.
5. **A Kiadó-kártya felvétele (7.):** a brief `ir`-jén kívüli fájlokat írna, ezért az orkesztrátoré.
6. **N-F160b:** ha az értelmező menet elutasított sort termel, a gépi előszűrő a HAMART-001-en újramérendő (DT500) — strukturális hordozón a szabály nem dönt, a mérés csak a hamis kizárásokat számolja.
7. **Az értelmező menet bemenete az X.A-ból:** 35 `nyitva` jelölt (8 régi + 27 új), a 605 szűretlen vers a lánc-sorrendben, a 651 N-F63e-függő vers, a próza-lefedettség átvitele a `motivumok/naplok/`-ba (2 meg nem nevezett előfordulás), az LXX-híd (1e.) és a felmérés (3.), valamint a 2. pont szótári kínálata.

## 7. Az N-F63e Kiadó-kártyája (tartalom, felvételre)

*Forrás: `hatar`, motívum: HAMART-001, címke: `tartalmi`, kiadás: 1. A kártya felvétele a `naplok/HATAR_HAMART-001.md` Modelles részébe és a `lektor_kerdesek.py --motivum HAMART-001` futtatása, a gombok következménye az `eszkozok/lektor_felulet/osszefoglalo_HAMART-001.tsv`-be — mindhárom a #123 `ir`-jén kívül, ezért itt csak a tartalom áll (DT543).*

**K-N-F63e — A gerinc-lexémák és a negatív kritérium: maradjon-e a H7451 (ra', gonoszság) és a H7043 (qalal, megátkoz/könnyűvé tesz) a HAMART-001 gerincében?**

**A jelenlegi határ** (az adatból):
- Negatív kritérium (`adat/motivumok.tsv`): a hely a gerinc valamelyik elemén — **arar (H0779), adamá (H0127), itzávón (H6093), chattát (H2403), chámász (H2555), sáchat (H7843); ἐπικατάρατος, κατάρα, φθείρω-család** — vagy a málé+chámász, sámá+chámász kollokáción át a genezisi átok→föld→romlás láncra utal vissza. A **H7451 és a H7043 nincs a felsorolásban.**
- Fölérendelt fogalom (a hígulás iránya): a bűn / hamartológia általában.
- Mégis: két beépített előfordulás ezekre a Strongokra épül — **1Móz 6:5** (`gerinc_elem`=H7451: „a gonoszság … a szív minden gondolat-alkotásában”) és **1Móz 8:21** (`gerinc_elem`=H7043: „az ígéret nem a 3:17 arar-t vonja vissza, hanem egy másik…”); a 1Móz 3:18 a H6975+H1863 **pár** (a magányos H6975 nem gerinc-elem).
- A mai scan e két Strongra (és a magányos H6975-re) **651 új verset** ad, amely egyetlen kritérium-lexémát sem hordoz (H7451 573, H7043 71, H6975 7); ezek most `N-F63e-függő` jelöléssel várnak.
- *(proveniencia: scope=adat/motivumok.tsv (HAMART-001 negativ_kriterium), adat/elofordulasok.tsv (52 sor), naplok/F123_adat_HAMART-001_nf63e_fuggo.tsv (651 sor) | forras=split('\t') | ts=2026-11-02T13:26Z; előzmény: N-F63e, DT97 (C), naplok/JELOLTEK_RETRO_lelet_meres.md)*

**Válaszok és következményük:**

| Gomb | Mit jelent | E-sor mozdul | Új vers | Egyéb |
|---|---|---|---|---|
| **Kivesszük** (a kritérium listája az irányadó) | a H7451 és a H7043 nem gerinc-elem; a 1Móz 6:5 és 8:21 a kritérium „tematikus, nem lexikai” jelölésével marad (`gerinc_elem` = `tematikus:…`), vagy az értelmező menet más gerinc-elemet talál a versben | **2** (1Móz 6:5, 8:21: a `gerinc_elem` és a `strong` mező) | **651** blokk-kizárás (`elutasítva`, közös indoklás: „nem a negatív kritérium lexémája”) a `jeloltek.tsv`-n át | 102 hiányzó fordítási kulcs kiesik a pótlandó körből; a negatív kritérium szövege nem változik |
| **Maradnak** (a kritérium listája bővül) | a H7451 és a H7043 gerinc-elem; a negatív kritérium felsorolása kiegészül velük (`adat/motivumok.tsv`) | **0** | **7** blokk-kizárás (magányos H6975); **644** vers a 605 mellé kerül kézi átnézésre (összesen 1 249 vers) | a kritérium szövege változik; a 644 vers egyike sem hordoz a mai listán álló lexémát |
| **Részben** (a H7043 marad, a H7451 ki) | érv: a 1Móz 8:21 sora a qalalt a 3:17 arar mellé állítja (`kapcsolodas`), a 1Móz 6:5 sora a ra'-t a szív diagnózisaként | **1** (1Móz 6:5) | **580** blokk-kizárás (H7451 573 + magányos H6975 7), **71** H7043-vers kézi átnézésre | a kritérium felsorolása a qalallal bővül; 51 fordítási kulcs kiesik (a H7451-é) |

A magányos H6975 (7 vers) mindhárom esetben kizárandó: a gerinc-elem a pár (H6975+H1863), a magányos „tövis” egyik válaszban sem az.

*(A számok mértek: E-sor a `adat/elofordulasok.tsv`-ből; vers a `naplok/F123_adat_HAMART-001_nf63e_fuggo.tsv`-ből; fordítási kulcs a `naplok/F123_adat_HAMART-001_forditas_hiany.tsv`-ből (H7451 51, H7043 51). A „Maradnak” sor 1 249-es összege a 605 + 644.)*
