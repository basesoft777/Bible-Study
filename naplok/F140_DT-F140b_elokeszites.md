# F140 — DT-F140b Opus-előkészítés (a K1–K10 átvizsgálása)

*#140 GLOSSZA_FORDITAS · M0 ⛔ · 2026-10-25 · a session modellje: `claude-opus-5-5` (orkesztrátori előkészítés, a felhasználó kérésére) · a tétel állapota 🟡 marad; ez a napló **nem dönt**, nem alkalmazza a döntést, az M1-et nem indítja.*

Proveniencia (minden alábbi számra, ahol más nem áll): `scope=konkordancia/TBESH.txt H-sorai + konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv (Strong-szám, Rövid jelentés) + konkordancia/Karoli_1908.tsv + eszkozok/glossza_forditas.py (valaszt, fo_jelolt) | forras=helyi-futtatas | ts=2026-10-25`. Az ellenőrző szkriptek a session scratchpadjában futottak, a repóba nem kerültek; a TBESH-t a `glossza_forditas.py` `tbesh_sorok()`-jától függetlenül, saját feldolgozással olvasták.

## 1. A napló számainak ellenőrzése

A `python eszkozok/glossza_forditas.py --m0` kimenete és a független újraszámolás **minden mért számban egyezik** a `naplok/GLOSSZA_FORDITAS_M0.md` 1. szakaszával: 11 682 nyers H-sor, 11 677 a hatókörben (a H9015–H9019 öt sora kimarad), 11 677 egyedi `entry_id`, 9 579 kapcsolat nélküli és 2 098 kapcsolt sor, 1 097 kapcsolat nélküli sor nélküli alap, 10 676 fordítandó és 1 001 kimaradó sor az A szabály szerint. (A brief befogadáskori előmérésének 11 682 / 8 723 értéke még tartalmazta a H9015–H9019-et.)

Egy tényállítás **nem áll**: a napló K7-je szerint a repóban „nincs” külső API-s fordítószkript. Van: `eszkozok/karoli_strong/api_koteg.py` (Anthropic Message Batches, F77) és `eszkozok/fordit.py` (OpenRouter, F03).

## 2. Új mérések

**K1 — az A változat 1 001 kimaradó sora:** `a Meaning of` 474 · `a Name of` 220 · `a Spelling of` 135 · `a Part of` 87 · `in Aramaic of` 39 · `a group of` 25 · `in Hebrew of` 10 · `combination of` 6 · `a form of` 5; glossza-karakter 11 667 (a 76 437-hez képest kb. +15%).

**K2 — a `fo`-szabály hibaaránya.** A TAHOT előfordulásonként hordozza a glosszát (`Rövid jelentés`; a kettőspont előtti rész). A 1 392 több soros alapból **1 305-nél** a TAHOT többségi `Rövid jelentés`-e egy TBESH-sorhoz illeszthető, 87-nél nem. A 2.2 szabály szerinti `fo` **legalább 174 alapnál** (12,5%) nem az illeszkedő sor, mert a szabály a fájlsorrendet követi. Ebből csak 12 esik a 300 leggyakoribb Strong közé (ezeket a kézi lista elkapná), **162 kézi átnézés nélkül hibás maradna**. A leggyakoribbak:

| Strong | TAHOT-előf. | a 2.2 `fo`-ja | az illeszkedő sor |
|---|---|---|---|
| H6213 | 2 629 | H6213B „to press” | H6213H „to make” |
| H1004 | 2 049 | H1004A „place” | H1004B „house: home” |
| H5892 | 1 090 | H5892A „excitement” | H5892B „city” |
| H7451 | 662 | H7451A „bad: harmful” | H7451C „distress: harm” |
| H6963 | 506 | H6963B „frivolity” | H6963A „voice” |
| H5769 | 438 | H5769H „Everlasting” | H5769G „forever: enduring” |
| H6030 | 332 | H6030A „to dwell” | H6030B „to answer” |
| H4057 | 271 | H4057A „mouth” | H4057B „wilderness” |
| H0899 | 217 | H0899A „treachery” | H0899B „garment” |
| H5483 | 140 | H5483A „swallow” | H5483M „horse” |

A TAHOT többségi `Rövid jelentés`-e 11 Strongnál „LORD”-ot tartalmaz (H0430, H6635, H3068, H0410, H5945, H0136, H7706, H3050, H5943, H5946, H1180): ezek a #138 tárgyai. Ugyanez a 11 Strong az istennevek köre (K5). A `fo`-glossza 101 Strongnál tartalmaz kettőspontot.

**K5 — Károli-szóhasználat.** A `Karoli_1908.tsv`-ben „ÚR” **0**-szor, „Úr” 5 557-szer fordul elő; „Mindenható” 43, „Seregek” 213, „Magasságos” 16 (köztük 1Móz 14:18–22, „magasságos Isten”), „Felséges” 10 (Zsolt 91:1, 9 stb.) versben; a Zsolt 68:5-ben „Jah”.

**K7 — terjedelem.** A 11 677 sorban 8 189 egyedi (glossza, szófaj) pár van (7 039 egyedi glossza): a napló által javasolt gyorsítótárral 100-as kötegben kb. 82 köteg a 117 helyett.

**K10:** a forrás-glossza legfeljebb 6 szó; 4 szónál hosszabb 16 sor.

## 3. Ajánlás kérdésenként

| # | Ajánlás | Indok |
|---|---|---|
| K1 | **elfogad (B)** | A számok igazolva. Az A 474 `a Meaning of` jelentésárnyalatot (`house: temple`) és 220 névsort dobna el; a B ára +1 001 rövid sor. A brief maga nyitja meg („kimaradnak, vagy külön jelölve”), tehát a B a brief keretén belül van. |
| K2 | **módosít** | Az (a) marad (teljes fordítás, `fo` oszlop, a kettőspont-levágás a #139-é), de a `fo` **kiválasztási szabálya** változzon: az a sor, amelynek glosszája (a kettőspont előtt) egyezik a TAHOT többségi `Rövid jelentés`-ével (1 305 alap); ahol nem illeszthető (87), vagy a többség „LORD” (a 11 istenneves Strong), ott a 2.2 heurisztika, illetve a K5-lista. Ok: a 2.2 szabály legalább 174 kiemelt sort (H6213, H5892, H6963 …) rosszul választ, és ezek 93%-át a 300-as kézi lista nem fedi. A TAHOT-oszlop csak a kiválasztásban dönt, szöveg nem kerül át belőle; a #138 által változtatott 11 Strongot a kivétel kezeli, így a `nem_fugg: [138]` tartható. Ez a brief olvasott oszlopait bővíti, ezért kifejezett igen kell. |
| K3 | **elfogad (a)** | A kettőspont a TBESH szerkezetét őrzi; a #139 determinisztikusan vághat. A furcsa árnyalatok („fiú: -éves”) csak nem-`fo` sorokban állnak. |
| K4 | **elfogad (a)** | A brief és a projekt szótári konvenciója; a próba sorai következetesek. |
| K5 | **módosít (kiegészít)** | (i) Az „az ÚR” nem a Károli 1908 alakja (ott „az Úr”); a H0136 „Úr”-tól való megkülönböztetéshez ajánlott megtartani, de a promptban **projekt-konvencióként**, ne Károli-alakként nevezze. (ii) A lista a TAHOT-ban „LORD”-ot hordozó 11 Strongból csak ötöt rögzít. Kiegészítési javaslat: H3050 „Jah” (TBESH „LORD”; Károli Zsolt 68:5), H7706 „Mindenható”, H6635B „Seregek”, H5943/H5946 (arám „Most High”) „Felséges”, H1180 „Baáli” (vagy átírás + `?`). (iii) A H5945B „Felséges” elfogadható, de a Károli vegyes (1Móz 14: „magasságos”). (iv) Összhang kell a #138 DT-F138b-vel (még 🟡), hogy a szó-lap két forrása ne adjon eltérő istennév-alakot. |
| K6 | **elfogad** | A `?` a `megjegyzes`-be kerül, a szövegbe nem (a kapu ezt fogja). A próbában 6/101 sor `?`: az M1-ben több száz várható; az M2 zárójelentése sorolja fel őket külön. |
| K7 | **elfogad (a), a napló javításával** | A (b) nem nulláról induló fejlesztés (van `api_koteg.py`-minta), de API-kulcsot és költséget kíván; a DT-F140a (b) Sonnetet ír, ezt az (a) is teljesíti. Feltételek: minden folytató session modell-ellenőrzéssel (sonnet), a `modell` mezőben a tényleges név; a gyorsítótár (~82 köteg) csak azonos (glossza, szófaj) párra. |
| K8 | **elfogad, időzítéssel** | Az `ADAT_LICENC`-bejegyzés kerüljön be, **mielőtt** a tábla a main-re és a `pardes.db`-be kerül, különben a CC BY 4.0 forrásjelölés nélkül töltődik be. Az F99-precedens szerint (a TAHOT a szűrésben döntött, ezért a listán van): `['TBESH', 'projekt_adat']`, és ha a K2-módosítás elfogadott, `['TBESH', 'TAHOT', 'projekt_adat']`. |
| K9 | **elfogad (a)** | Új angol szólista dataset-behozatal (playbook 2. pont) volna, aránytalan; a forrás 4+ betűs szavainak tilalma és a kivétel-lista a valódi hibát (fordítatlanul hagyott glossza) fogja. |
| K10 | **elfogad (50/6)** | A forrás legfeljebb 6 szó; a 40/5 a nevek és a kettőspontos glosszák („(Libanon erdejének) háza”, „kiirtásra szentelni; elpusztítani”) miatt fölösleges újrafordításokat okozna. |

## 4. Mire kell kifejezett igen

- **K2:** a `fo` kiválasztása a TAHOT többségi `Rövid jelentés`-ével (a brief olvasott oszlopainak bővítése).
- **K5:** a kibővített istennév-lista (11 Strong) és az „az ÚR” projekt-konvencióként nevezése.
- **K8:** a licenc-bejegyzés időzítése (M1 előtt vagy a tábla main-re kerülése előtt) és a lista tartalma.
- A többi (K1, K3, K4, K6, K7, K9, K10) a napló javaslatával egyezik; ezekre elég az egyszerű jóváhagyás.
