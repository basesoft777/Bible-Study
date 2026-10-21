# SZURO_PILOT_ISTENTISZT_naplo.md — F110 (#110), szűrő-szabály pilot az ISTENTISZT-001-en

*Állapot: a DT-F110a elfogadva (orkesztrátor, 2026-10-21; l. `DONTESEK.md`), a 4–6. lépés lefutott; a javítókör 1. körében (ELLENOR_F110 1.) a JSir 3:55 és az 5Móz 32:3 kikerült a `jeloltek.tsv`-ből, az ApCsel 7:59 elutasítva (a számok a 6–7. szakaszban a javított állapotot mutatják); a zárást az orkesztrátor végzi. Ág: `claude/f110-szuro-pilot-2`. Modell: `claude-sonnet-5-5`. Igehely-alak: a `konyv_normalizalo_tabla` szerinti (JSir 3:55); a TAHOT-kivonat és a szimulációs TSV kulcsa még `Sir 3:55`.*

## 1. Bemenet és újralekérdezés (2. lépés)

Forrás: `naplok/F108_ujrascan_elteresek.tsv`, `id=ISTENTISZT-001`, `tabla=ujrascan`: 168 sor `uj_talalat_nem_irva_tul_tag` (H7121+H8034) és 21 sor `uj_jelolt_irva` (G1941). Az igehelyek: `naplok/F110_bemenet.tsv` (a régi, elavult `claude/f110-szuro-pilot` ág lekérdezés-naplóját nem vettem át).

A lekérdezések a mai adaton futottak (`eszkozok/f110_lekerdez_bemenet.py`, naplo: `naplok/F110_lekerdezesek.tsv`):

| parancs | n | a bemenetből benne | proveniencia |
|---|---|---|---|
| `lekerdez.py kollokacio H7121 H8034` | 196 vers | 168 / 168 | `scope=TAHOT-teljes+TAGNT-teljes \| forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv \| strong=H7121+H8034 \| n=196 \| ts=2026-10-21T09:18Z` |
| `lekerdez.py scan G1941` | 31 igehely | 21 / 21 | `scope=TAGNT-teljes \| forras=TAGNT_kivonat.tsv \| strong=G1941 \| n=31 \| ts=2026-10-21T09:18Z` |

A 196 és a 31 egyezik az F108 mérésével (`naplok/F108_MOTIVUM_UJRASCAN_naplo.md`: 196, ill. 31). Egyik bemeneti hely sem esik ki.

## 2. A szűrő-szabály (DT-F110a javaslata)

**Kiinduló kritérium** (`adat/motivumok.tsv`, ISTENTISZT-001, negatív kritérium): az igehelynek aktív, invokáló קָרָא (kárá) + בְּ (be) szerkezetet kell mutatnia („[valaki] hívja segítségül [Isten nevét]”); a passzív נִקְרָא … עַל (nikrá … ál: birtoklás, hovatartozás) kizárja a besorolást, akkor is, ha ugyanazt a két gyököt használja (2Sám 6:2, Jer 7:10-14, 5Móz 28:10; ÚSZ-pár: Zsid 11:16).

**Érvényesítés a már beépített helyeken** (a szabály nem szigorúbb a gyakorlatnál): az `elofordulasok.tsv` 17 + 5 (zsoltár) H7121+H8034 sora (pl. 1Móz 12:8, 1Kir 18:24-26, Jóel 2:32, 2Móz 34:5, Ézs 12:4, Jer 10:25) mind בְּ + שֵׁם szerkezet, aktív igével; a szabály mind a 22-t A- (16) vagy B-osztályba (6) sorolja, K-ba egyet sem (ellenőrzés: `eszkozok/f110_szuro.py` `heber()` függvénye a 22 sorra, ablak = 6 token; a 6 B a birtokos toldalékos alak: Zak 13:9, Jer 10:25, Zsolt 105:1 stb., ahol a kézi olvasás dönt).

### 2.1 Héber oldal (H7121 + H8034), a determinisztikus rész

Bemenet: a vers `TAHOT_kivonat.tsv` sorai (szó-szintű Strong, `Ragozott alak`, `Angol tükörfordítás`). A TAHOT-kivonatban nincs morfológiai oszlop; az ige törzs-/szemléjét az angol tükörfordítás (passzív-e) és a szó-sorrend adja. Szabályok sorrendben, az első illeszkedő dönt; a versben több pár esetén a legkedvezőbb osztály számít:

- **K0** — nincs H7121 és H8034 egymástól legfeljebb 6 tokenre (nincs kollokáció a mondaton belül).
- **K1 passzív** — a H7121 tükörfordítása passzív/megnevezett („is called”, „was called”, „has been called”, „will be called”, „named” stb.): נִקְרָא … (megnevezés, birtoklás) kizár.
- **K2 nincs בְּ** — a H8034 előtt nincs közvetlenül H9003 (be-előtag): nincs קָרָא בְּשֵׁם szerkezet (megnevezés `H0853` tárgyjellel, vagy más). Ha a H8034 után 3 tokenen belül isteni névszó áll, a sor **HATÁRESET**-jelzést kap (a kézi rész olvassa).
- **A** — aktív ige + H9003 közvetlenül a H8034 előtt + isteni névszó a H8034 után 3 tokenen belül (`H3068`, `H0430`, `H0136`, `H0410`, `H3050`, `H1168` Báal): a besorolás-jelölt, **kézi megerősítéssel**.
- **B** — aktív ige + בְּ + שֵׁם, de isteni névszó nincs a közelben (birtokos toldalék, névmás, személy- vagy helynév): **kézi olvasás**, hogy a שֵׁם kire vonatkozik.

### 2.2 Héber oldal, a kézi rész

Az A- és B-osztályú és a HATÁRESET-jelzésű sorokat a kézi olvasás dönti, soronként indoklással; a mérce a negatív kritérium:

1. a שֵׁם **Istené** (vagy a hívott isteneké, mint 1Kir 18:26 Báal), nem emberé, városé, helyé, tárgyé;
2. az ige alanya **hívja** a nevet/személyt (segítségül hívás, kiáltás, kikiáltás-imádás), nem **nevet ad** vagy **névvel szólít**;
3. a **tagadott** invokáció (pl. „nem hívják a nevedet”) bekerülhet, mert a már beépített Jer 10:25 is ilyen;
4. a K2-ből HATÁRESET-jelzésű (nincs בְּ, de isteni névvel áll) sor a **tárgyas** szerkezetben (קָרָא + שֵׁם + isteni név, mint JSir 3:55, 5Móz 32:3) nem automatikus: a DT-F110a (b) opciója szerint kézzel dől el, a (a) opció szerint kiszűrt marad.

### 2.3 Görög oldal (G1941 ἐπικαλέω), a determinisztikus rész

Bemenet: a vers `TAGNT_kivonat.tsv` sorai. A kivonatban nincs morfológiai oszlop; a diatézist az angol tükörfordítás adja. Sorrend, az első illeszkedő dönt:

- **K1 passzív/megnevezett** — a tükörfordítás „is/was/has been/having been/to be called”, „being called”: a passzív ἐπικαλέω, a nikrá-párhuzam („akit X-nek neveznek”; ἐπικληθέν … ἐφ᾽ ὑμᾶς, ἐπικέκληται τὸ ὄνομά μου ἐπ᾽ αὐτούς, θεὸς ἐπικαλεῖσθαι αὐτῶν) kizár.
- **K3 jogi** — a környezetben (±8 token) `G2541` Καῖσαρ vagy `G4575` Σεβαστός: jogi fellebbezés („Caesarra hivatkozom”), nem invokáció.
- **A** — aktív/középigés, és a környezetben (±3 token) isteni szó (`G2962` Úr, `G2316` Isten, `G2424` Jézus, `G3686` név, `G3962` Atya, `G5547` Krisztus): a besorolás-jelölt, kézi megerősítéssel.
- **B** — aktív/középigés, de isteni szó nincs a közelben: kézi olvasás.

### 2.4 Görög oldal, a kézi rész

Az A- és B-osztályú sorokat a kézi olvasás dönti: a hívott **Isten/Úr/Jézus** (nem tanú, nem ember), és a hívás **segítségül hívás/imádság/kiáltás** (nem eskü-tanúhívás, nem megnevezés). A kritérium itt az ÚSZ-oldali megfelelő: aktív, középigés invokáció vs. passzív megnevezés („akit X-nek neveznek”) vagy jogi „hivatkozás”.

## 3. A szimuláció eredménye (a jóváhagyás előtt, a `jeloltek.tsv` érintetlen)

`python eszkozok/f110_szuro.py` → `naplok/F110_szuro_szimulacio.tsv` (soronként osztály, okkód, indoklás).

### H7121+H8034 (168 hely)

| osztály | okkód | db |
|---|---|---|
| A | A_be_isten | 1 |
| B | B_be_nem_nevszo | 13 |
| K | K0_nincs_par | 12 |
| K | K1_passziv | 38 |
| K | K2_nincs_be | 104 |
| | **összesen** | **168** |

Ebből a K2-ben 4 HATÁRESET (nincs בְּ, de isteni névvel): 1Móz 16:13, 2Móz 17:15, 5Móz 32:3, JSir 3:55 (a TAHOT-kulcs: `Sir 3:55`).

Az automatikusan kiszűrt: **154** hely (K0 + K1 + K2); a kézi olvasásra váró: **14** (1 A + 13 B) + a 4 HATÁRESET.

Előzetes kézi olvasás (a TAHOT angol tükörfordítása alapján; a végleges döntés a jóváhagyott szabály futtatása után):

- **Ézs 45:3** (A): „I [am] Yahweh who calls by name your” — Isten **hívja** Círust névvel, nem invokáció → elutasítva (a szabály A-osztálya tehát nem jelent automatikus bevételt: a kézi megerősítés elengedhetetlen).
- **Ézs 64:6** (B): „and there not [is one who] calls on name your” — tagadott invokáció (Jer 10:25 precedens) → beépítve-jelölt.
- **Ézs 44:5** (B): önazonosítás („with the name of Jacob he will call out”) → határeset, kézi döntés a szabály szerint (nem Isten neve).
- **Ézs 40:26, 41:25, 43:1, 45:4; 2Móz 31:2, 35:30; 4Móz 32:38, 32:42; Bír 18:29; Józs 21:9; 1Krón 6:65** (B): személy-/helynévvel, névvel szólítás → elutasítva.
- **JSir 3:55** (HATÁRESET): „I called name your O Yahweh” — tárgyas invokáció → a (b) opcióval beépítve-jelölt.
- **5Móz 32:3** (HATÁRESET): „the name of Yahweh I will proclaim” — kikiáltás (a 2Móz 34:5 és 33:19 már beépített בְּ-es párja) → a (b) opcióval határeset, kézi döntés.
- **1Móz 16:13, 2Móz 17:15** (HATÁRESET): megnevezés (az Úr nevének adása egy helynek/oltárnak) → elutasítva.

Várható végeredmény a 168-ból: **0–4 bekerülő** (Ézs 64:6; (b) opcióval JSir 3:55, esetleg 5Móz 32:3, Ézs 44:5), a többi kiszűrve. Ez nem hiba: a 168 új hely túlnyomó része megnevezés (נִקְרָא, „X nevét hívta”), amit a negatív kritérium kizár; a szűretlen bevétel (DT184 (c)) ezeket vitte volna be.

### G1941 (21 hely, `nyitva` jelöltek a `jeloltek.tsv`-ben)

| osztály | okkód | db | helyek |
|---|---|---|---|
| K | K1_passziv | 12 | ApCsel 1:23, 4:36, 10:5, 10:18, 10:32, 11:13, 12:12, 12:25, 15:17; Mt 10:3; Jak 2:7; Zsid 11:16 |
| K | K3_jogi | 6 | ApCsel 25:11, 25:12, 25:21, 25:25, 26:32, 28:19 |
| A | A_aktiv_isten | 2 | ApCsel 7:59; 2Kor 1:23 |
| B | B_nincs_isten | 1 | Mt 10:25 |
| | **összesen** | **21** | |

Előzetes kézi olvasás: **ApCsel 7:59** (István „imádkozik … Uram Jézus” — Károli) → invokáció, beépítve-jelölt (a 1Kor 1:2, ApCsel 2:21 és 9:14 igéje párhuzam); **2Kor 1:23** („hívom bizonyságul” — Károli) → esküformás tanúhívás, nem segítségül hívás → elutasítva; **Mt 10:25** („Belzebubnak hívták” — Károli) → megnevezés → elutasítva. A 12 + 6 K-sor automatikus elutasítás, indoklásként a K1/K3 okkóddal.

## 4. A lépések (a DT-F110a jóváhagyása után; végrehajtva, l. 6–8.)

4. A jóváhagyott szabály futtatása szkriptből (kézi rész: a soronkénti döntés a naplóba).
5. A `jeloltek.tsv` bővítése (csak új H7121+H8034 sor; csak a szűrőn átjutók `nyitva`), a 21 G1941-sor döntés/indoklás mezője; írás előtt sorösszevetés, a többi sor bájtra azonos.
6. Átvihetőség-mérés (motívumonként egy mondat: a negatív kritérium tartalmaz-e gépileg ellenőrizhető jegyet), a kiszűrt helyek okonkénti számossága (sorszintű lista: `naplok/F110_szuro_szimulacio.tsv`).

## 5. Fájlok

- `eszkozok/f110_lekerdez_bemenet.py` — a 2. lépés (kigyűjtés + újralekérdezés).
- `eszkozok/f110_szuro.py` — a szabály determinisztikus része (szimuláció, csak a naplót írja).
- `naplok/F110_bemenet.tsv`, `naplok/F110_lekerdezesek.tsv`, `naplok/F110_szuro_szimulacio.tsv`.

## 6. A jóváhagyás és a kézi olvasás (4. lépés)

A DT-F110a elfogadva két pontosítással: az A osztály sem automatikus bevétel; a határesetek (b) szerint kézi olvasásra mennek. Mérce: aktív ige, a שֵׁם Istené, funkció hívás/kiáltás/kikiáltás-imádás, nem névadás.

### 6.1 Héber (168 hely): 2 `nyitva`, 166 kiszűrve (javítókör 1. kör után; az F110.4-es állapot: 4 / 164)

| csoport | db |
|---|---|
| automatikus kiszűrés (K0 12 + K1 38 + K2 nem határeset 100) | 150 |
| kézi olvasás után kiszűrve (A 1 + B 11 + határeset 2) | 14 |
| K2_nincs_be marad (JSir 3:55, 5Móz 32:3; „tartalmilag invokáció, de a formulán kívül esik (fölérendelt fogalom)”) | 2 |
| kézi olvasás után `nyitva` (Ézs 41:25, Ézs 64:6) | 2 |
| **összesen** | **168** |

Kézi olvasás, soronként (a tábla csak az átjutottakat kapja; a kiszűrtek sorszintű listája: `naplok/F110_szuro_szimulacio.tsv`, a kézi okok itt):

| igehely | osztály | döntés | indoklás |
|---|---|---|---|
| JSir 3:55 | K2 határeset | K2_nincs_be marad (kiszűrve; a jeloltek.tsv-ből kivéve, ELLENOR_F110 1.; „tartalmilag invokáció, de a formulán kívül esik (fölérendelt fogalom)”) | „I called name your O Yahweh”: aktív, Isten neve, hívás a gödörből; בְּ nincs |
| 5Móz 32:3 | K2 határeset | K2_nincs_be marad (kiszűrve; a jeloltek.tsv-ből kivéve, ELLENOR_F110 1.; „tartalmilag invokáció, de a formulán kívül esik (fölérendelt fogalom)”) | „the name of Yahweh I will proclaim”: kikiáltás-imádás (a 2Móz 33:19 és 34:5 párja); בְּ nincs |
| Ézs 41:25 | B | nyitva (**eltérés a vártól, jelezve**) | „he will call on name my”: aktív קרא + בְּ + שֵׁם, az Úr beszél; a szöveg és a בְּשֵׁם szerkezet alapján a motívum-menet dönt |
| Ézs 64:6 | B | nyitva (**eltérés a vártól, jelezve**) | „there not [is one who] calls on name your”: tagadott invokáció (Jer 10:25 precedens) |
| 1Móz 16:13 | K2 határeset | kiszűrve | névadás |
| 2Móz 17:15 | K2 határeset | kiszűrve | névadás (oltár) |
| Ézs 45:3 | A | kiszűrve | Isten hívja Círust névvel |
| Ézs 44:5 | B | kiszűrve | Jákob neve, nem Isten neve |
| Ézs 40:26, 43:1, 45:4 | B | kiszűrve | Isten névvel szólít |
| 1Krón 6:65, Józs 21:9, 4Móz 32:38, 4Móz 32:42, Bír 18:29 | B | kiszűrve | városok/hely névadása |
| 2Móz 31:2, 35:30 | B | kiszűrve | Becalél névvel szólítása |

Az F110.4-es állapotban négy hely volt `nyitva`; a javítókör 1. körében a JSir 3:55 és az 5Móz 32:3 a felhasználó döntése szerint kiszűrve maradt (a kritérium nem változik; a két hely a fölérendelt fogalmon át tartozna ide, a kritériummódosítás a motívum azonosságát írná át, ez nem a szűrő-pilot dolga). A vártnál két sorral több kerül be (Ézs 41:25 és Ézs 64:6): mindkettő a szabály szerint átjutó aktív בְּ-s invokáció, `nyitva` döntéssel, tehát nem kötelez; az orkesztrátor eldöntheti, hogy a motívum-menetben marad-e.

### 6.2 Görög (21 hely)

| döntés | db | helyek |
|---|---|---|
| elutasítva, automatikus K1 | 12 | ApCsel 1:23, 4:36, 10:5, 10:18, 10:32, 11:13, 12:12, 12:25, 15:17; Mt 10:3; Jak 2:7; Zsid 11:16 |
| elutasítva, automatikus K3 | 6 | ApCsel 25:11, 25:12, 25:21, 25:25, 26:32, 28:19 |
| elutasítva, kézi | 3 | 2Kor 1:23 (esküformás tanúhívás), Mt 10:25 (megnevezés), ApCsel 7:59 (nincs ὄνομα — invokáció a formulán kívül; ELLENOR_F110 2.) |
| nyitva marad | 0 | — |

**Eltérés a brief 4. szakaszától:** „a 21 G1941-sor egyike sem `nyitva`”; az orkesztrátor eredeti döntése szerint az ApCsel 7:59 `nyitva` maradt; a javítókör 1. körében (ELLENOR_F110 2.) elutasítva, így a brief 4. szakaszával egyezik: a 21 G1941-sor egyike sem `nyitva`.

## 7. Írás a `adat/jeloltek.tsv`-be (5. lépés)

`python eszkozok/f110_ir.py`: 636 → 640 sor (a javítókör 1. körében `eszkozok/f110_ir2.py`: 2 sor törölve, 638 sor; ApCsel 7:59 elutasítva; az új sorok közül 2 `nyitva`). 21 módosult sor (a G1941: `dontes`, `indoklas`, `datum`), 4 új sor (mind `nyitva`, `jelolt_tipus=elofordulas`, `forras_kereses` = a kollokáció proveniencia-sora). Az összes többi sor bájtra azonos (a szkript soronként vet össze, eltérésnél nem ír; split/join, nem `csv`). `python eszkozok/ellenoriz.py`: RENDBEN 14, SÉRTÉS 0, KÉZI 2, JELENTÉS 3 (a 2 KÉZI és 3 JELENTÉS nem F110-eredetű). Egyik új sor sem került az `elofordulasok.tsv`-be (2. szabály).

## 8. Átvihetőség-mérés (6. lépés)

A kérdés: tartalmaz-e a motívum negatív kritériuma (`adat/motivumok.tsv`) gépileg ellenőrizhető jegyet, amelyre a héber/görög szűrő épülhet. A tág Strongos motívumok a #108 `uj_talalat_nem_irva_tul_tag` sorai szerint (szám- és becslés nélkül):

| motívum (tág Strong) | gépi jegy a negatív kritériumban? | mondat |
|---|---|---|
| ISTENTISZT-001 (H7121+H8034) | igen | a קָרָא + בְּ + שֵׁם szerkezet, az aktív/passzív ige és az isteni névszó szó-sor szinten ellenőrizhető; a kézi rész a שֵׁם referense (a pilot igazolta) |
| KIRALY-001 (H3548) | részben | Melkizedek megnevezése (H4442/G3198) vagy a „rendje szerint” formula a versben gépileg ellenőrizhető; a BDB „priest-king” jelentése nem szerepel a TAHOT-sorokban, az kézi |
| MENNY-001 (H1121+H0430) | igen | a בְּנֵי (הָ)אֱלֹהִים szomszédsági minta (H1121 és H0430 egymás mellett, esetleg H9009-cel) és a H5303 nefilim gépileg ellenőrizhető, a רפאים (H7496) kizárás Strong-szinten adott; a kézi rész az „elohim” jelentése (bírák, isten) |
| ANTROP-001 (H5315+H2416) | részben | a két szó egyazon versben állása (kollokáció) gépi; a „megkülönböztető szerep” értelmezés, kézi |
| HAMART-001 (H2403, H7451, H0127, H7843, H7043, H2555) | alig | a kritérium a genezisi átok→föld→romlás láncra való visszautalás; gépileg csak a megnevezett kollokációk (málé+chámász, sámá+chámász) ellenőrizhetők, az egyes tág Strongokra (H2403, H7451) nincs kizáró gépi jegy; külön szűrő-szabály kell, vagy a tág Strongok gerinc-szerepe felülvizsgálandó |

Következtetés: a pilot sémája (negatív kritérium, determinisztikus rész: Strong + kollokáció + igealak/törzs; kézi rész: referens és funkció) közvetlenül átvihető a MENNY-001-re, részben a KIRALY-001-re és az ANTROP-001-re; a HAMART-001 tág Strongjaira nem, ott a szűrőnek nincs gépi horgonya a puszta Strong-találatnál.

## 9. Megjegyzés

A `jeloltek.tsv` írása (F110.4) a DONTESEK-bejegyzés (DT-F110a) rögzítését megelőzte; a sorrend utólag nem javítható, tényként rögzítem (ELLENOR_F110 3.). A zárójelentést az orkesztrátor írja.

## 10. A lexikon-nézet (ELLENOR_F110 E28, a 7. tétel)

A `python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --ir` lefutott, a diff 41 beszúrt és 39 törölt sor volt. Fennálló eset: **(b)** — a változás nem csak a jeloltek-delta közvetlen következménye: a `ts=` jelölők (2026-10-20 → 2026-10-21) és a `kizart` blokk száma (91 → 93) mellett a `kapcsolodo` blokk magyarázó sorában `DT277` helyett `DT-F127b` jelent meg (main-beli sodródás, nem az F110 hatása). A CI E28 fix dátummal (`PARDES_DATUM=2026-10-20`) generál, így a `ts=` jelölők nem számítanak; ezzel a dátummal a generátor diffje 2 sor: (1) a `kizart` blokk jelöltszáma 91 → 93 (ez a jeloltek-delta közvetlen következménye), (2) a `kapcsolodo` blokk magyarázó sorában `DT277` → `DT-F127b` (az `eszkozok/lexikon_general.py:2116` literálja, nem a `general.py`; main-beli sodródás, nem az F110 hatása). A (2) miatt a lexikon-fájl **nem lett commitolva** (`git checkout`, érintetlen), az E28 ismert kivétel: a lexikon csak a main-beli sodródás (lexikon_general.py:2116) javítása után generálható újra; az F110 saját deltája (91→93 jelölt) ott jelenik meg. A lexikon újragenerálásáról brief-tervezet: `beerkezo/Fnn_LEXIKON_UJRAGEN_BRIEF.md` (csak tervezet, a FELADATOK-ba nincs felvéve).

A `NYITOTT_FELADATOK.md` generált blokka (6. tétel) a generátorral újra előállt (F110.16); csak a 110-es delta változott (nyitott jelöltek 49 → 30, az ISTENTISZT-001 nyitott-száma 21 → 2).
