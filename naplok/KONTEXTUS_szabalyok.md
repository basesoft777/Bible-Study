# KONTEXTUS — szabályleírás és próbák (F32, K3)

*FELADATOK #32 · a `MUNKAMENET.md` „Kontextus-őrzés” szakaszának gépi ellenőrzése. A CI-implementáció külön ágon készül (D6); itt a `feladatok.py`, a `/kovetkezo` és a szabály leírása áll.*

## K3.0 — hol dől el ma a csomagba sorolás

Két helyen, külön rétegben:

1. **`eszkozok/feladatok.py`, `csomag()` függvény** (a `jeloltek` alparancs `CSOMAG` sora): a jelöltekből gyűjt, legfeljebb 5 tagot; kizárja a `KIZAR`-párt (írás–írás vagy kölcsönös írás–olvasás ütközés), a csomagtagtól függő jelöltet, és az `ir` nélküli (régi, `REGI`) briefet. A `munka` mezőt az F32 előtt nem ismerte.
2. **`.claude/commands/kovetkezo.md` 3b. lépés** (prompt-szöveg): a csomag összeállításának szabályait mondja ki, és a `feladatok.py` kimenetére hivatkozik. A `vegrehajto-*` subagent kiosztása a 6/6b. lépésben, szintén prompt-szöveg.

Következmény: a csomagolási tilalom eddig csak az `ir` és a függések alapján dőlt el, a feladat *fajtájáról* semmi nem döntött. Az F32 a `csomag` alparancsot adja, amelyet a `/kovetkezo` 3b. lépése csomagjavaslat előtt kötelezően hív. A `csomag()` függvényhez (a `jeloltek` kimenetéhez) nem nyúltam: a #49 (F49) ugyanazt a függvényt érinti, és a brief (K-D11) külön alparancsot ír elő; a `jeloltek` `CSOMAG` sora tehát továbbra is csak javaslat, a kötelező kapu a `csomag` alparancs.

## A szabály, amit a `feladatok.py` ellenőriz

**`munka` mező** (`BRIEF_SABLON.md`): `adat` · `ertelmezo` · `folyamat`. Az `ellenoriz` az értékkészletet ellenőrzi; a mező nem kötelező az `ellenoriz`-ben (a régi fejlécek mező nélkül érvényesek, K2).

**Motívumfájlt író `ir`-bejegyzés:** `motivumok/`, `tematikus_lezart/`, `lexikon/` vagy `genezis/` előtagú (könyvtár, fájl vagy glob).

**`csomag <szám> …` (K3.1)** — `NEM_CSOMAGOLHATO` és 1-es kilépési kód, ha a felsorolt feladatok közül bármelyik:

| eset | döntés |
|---|---|
| `munka: ertelmezo` | nem csomagolható |
| `munka: folyamat`, de az `ir` motívumfájlt tartalmaz | nem csomagolható (`ertelmezo`-ként kezelendő) |
| `munka` hiányzik, és az `ir` motívumfájlt tartalmaz | nem csomagolható, amíg a mező ki nincs töltve (K-D4) |
| `munka: adat`; `munka: folyamat` motívumfájl nélkül; `munka` hiányzik és nincs motívumfájl | csomagolható (a mező nélküli, motívumfájlt nem író brief `adat`) |

**`olvas`-ellenőrzés (K3.2, az E18 része)** — az `ellenoriz` `HIBA` sora és a `fuggesek` `OLVAS_HIANY` sora (a `fuggesek` ilyenkor 1-gyel lép ki): ha az `ir` **ID-vel nevesített** motívumfájlt tartalmaz (`motivumok/[ID]*`, `tematikus_lezart/[ID]*`, `lexikon/[ID]*`; az ID a fájlnév elején: `[A-Z]+-[0-9]+`), az `olvas` listájának le kell fednie (`utvonal_egyezik`: azonos fájl, könyvtár-előtag vagy glob):

- a tematikus tanulmányt: `tematikus_lezart/[ID]_tematikus.md`,
- a kereszthivatkozás-naplót: `tematikus_lezart/naplok/[ID]_kereszthivatkozas_naplo.md`.

A hibaüzenet a hiányzó fájl mintáját nevezi meg (`tematikus_lezart/naplok/TEREMT-002*`).

**E18 — `munka` nélküli, motívumfájlt író brief (felhasználói elfogadás, 2026.10.04):** az `ellenoriz` `HIBA` sort ad (`E18: hiányzó munka mező …`), a `fuggesek` `MUNKA_HIANY` sort és 1-es kilépést; az `ellenoriz` a CI-n megbukik, a `/kovetkezo` (1. lépés: `ellenoriz` nem 0 → megáll) így nem ajánlja futtathatónak. A mai main-en három brief esne ebbe (`F09`, `F35`, `F36`, a `motivumot_ir` szerint); **döntésem: előzmény-kivétel**, mert a hiba ezeknél eltörné a CI-t, más feladat briefjét pedig nem írhatom át. A `feladatok.py` `MUNKA_ELOZMENY = (9, 35, 36)` listája ezekre `FIGYELEM` sort ad (`ellenoriz`: `FIGYELEM`, nem hiba; `fuggesek`: `FIGYELEM`), a lezárt F35-re semmit; a `csomag` mindhárom előzményre továbbra is `NEM_CSOMAGOLHATO`. Új brief nem kerülhet a listára: aki új motívumot író briefet vesz fel, `munka`-t kell megadjon (a `fuggesek --extra` a befogadáskor is `MUNKA_HIANY`-t ad). Az előzmény-lista akkor szűnik meg, ha az F09 és F36 `munka` mezőt kap (külön, a gazdájuk dolga).

## Ismert korlát — a K3.2 ID-alapú (javaslat: külön feladat)

A K3.2 (`olvas`-ellenőrzés) a motívumot az `ir` fájlnevének elejéről olvasott **ID-ből** ismeri fel (`[A-Z]+-[0-9]+`, pl. `TEREMT-002`), és az `olvas`-ban a `tematikus_lezart/[ID]_tematikus.md` és a `tematikus_lezart/naplok/[ID]_kereszthivatkozas_naplo.md` mintát várja. Következmények:

- **Témanevű tanulmányokra nem fut.** A mai tanulmányok témanevet viselnek (`Tehom_tematikus.md`, `Hadesz_Seol_tematikus.md`, `Segitsegul_hivni_az_Urat_tematikus.md`, így az F09 is ilyet ír), és az ID és a tanulmány között gépi megfeleltetés nincs; az ilyen briefnél az `olvas`-lista teljességéért a brief szerzője felel (K1/3 kézi betartása).
- **Könyvtár- és glob-`ir`** (`lexikon/`, `tematikus_lezart/`, `genezis/`) ID nélkül a K3.2-t nem váltja ki, csak a `munka`-szabályt (K3.1, E18).
- **Javaslat (`/befogad`):** külön feladat a **motívum→tanulmány megfeleltetésre**: egy gépi tábla (pl. `adat/motivum_tanulmany.tsv`: `motivum_id`, `tanulmany`, `naplo`), amelyből a K3.2 az ID-n és a témanevű tanulmányon is ellenőrizni tud. A `feladatok.py` a táblát olvasná; amíg nincs, a fenti kézi felelősség áll. Ezt a feladatot **nem veszem fel** (a `/befogad` a felhasználóé).

**Egyéb korlát:**

- A `jeloltek` `CSOMAG` sora nem szűri a `csomag_hiba` szerint (lásd K3.0).

## Próbák (a parancsok tényleges kimenete)

A fixture-briefek a repón kívüli ideiglenes könyvtárban vannak (`--gyoker`); a kimenetet a `eszkozok/feladatok.py` állította elő a `wt-f32` worktree-ből, a próbaszkript a worktree-n kívül futott. A fixture-ek:

| szám | kód | `munka` | `ir` | `olvas` | várt |
|---|---|---|---|---|---|
| 90 | POZ_ERT | ertelmezo | `motivumok/TEREMT-002.md` | tanulmány + napló | `csomag`: nem; K3.2: rendben |
| **91** | **NEG_ERT** | ertelmezo | `motivumok/TEREMT-002.md` | **csak tanulmány, a napló hiányzik** | K3.2: hiba (a TEREMT-002-re szabott negatív próba) |
| 92 | POZ_ADAT | adat | `adat/y.tsv` | — | csomagolható |
| 93 | POZ_FOLY | folyamat | `BRIEF_SABLON.md` | — | csomagolható |
| 94 | NEG_FOLY | folyamat | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` | semmi | `csomag`: nem; K3.2: hiba |
| 95 | NEG_REGI | (nincs) | `lexikon/` | — | `csomag`: nem (hiányzó `munka`) |
| 96 | POZ_REGI | (nincs) | `adat/y.tsv` | — | csomagolható (`adat`) |
| 97 | NEG_ID_TELJES | ertelmezo | `tematikus_lezart/TEREMT-002_javitas.md` | semmi | K3.2: hiba (a javító kör is) |

```
Fixture-gyoker (a repon kivul): <fixture-gyökér>
Fixture-briefek: F90_POZ_ERT_BRIEF.md, F91_NEG_ERT_BRIEF.md, F92_POZ_ADAT_BRIEF.md, F93_POZ_FOLY_BRIEF.md, F94_NEG_FOLY_BRIEF.md, F95_NEG_REGI_BRIEF.md, F96_POZ_REGI_BRIEF.md, F97_NEG_ID_TELJES_BRIEF.md

## K3.1 csomag (--gyoker <fixture>)
$ python eszkozok/feladatok.py csomag 92
  CSOMAGOLHATO	#92	munka: adat
  [kilepesi kod: 0]

$ python eszkozok/feladatok.py csomag 93
  CSOMAGOLHATO	#93	munka: folyamat
  [kilepesi kod: 0]

$ python eszkozok/feladatok.py csomag 96
  CSOMAGOLHATO	#96	munka: adat (alapértelmezés)
  [kilepesi kod: 0]

$ python eszkozok/feladatok.py csomag 90
  NEM_CSOMAGOLHATO	#90	`munka: ertelmezo` — az értelmező munka egy kézben készül, nem kerül csomagba
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py csomag 94
  NEM_CSOMAGOLHATO	#94	`munka: folyamat`, de motívumfájlt ír (`ir`) — `ertelmezo`-ként kezelendő
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py csomag 95
  NEM_CSOMAGOLHATO	#95	hiányzó `munka` mező motívumfájlt író briefben — töltsd ki, addig nem csomagolható
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py csomag 97
  NEM_CSOMAGOLHATO	#97	`munka: ertelmezo` — az értelmező munka egy kézben készül, nem kerül csomagba
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py csomag 92 93 94
  CSOMAGOLHATO	#92	munka: adat
  CSOMAGOLHATO	#93	munka: folyamat
  NEM_CSOMAGOLHATO	#94	`munka: folyamat`, de motívumfájlt ír (`ir`) — `ertelmezo`-ként kezelendő
  [kilepesi kod: 1]

## K3.2 fuggesek / ellenoriz (--gyoker <fixture>)
$ python eszkozok/feladatok.py fuggesek
  # típus	feladat	másik	forrás
  OLVAS_HIANY	91	-	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/TEREMT-002*
  OLVAS_HIANY	94	-	ISTENTISZT-001 motívumot ír (`ir`), de az `olvas`-ból hiányzik a tematikus tanulmány: tematikus_lezart/ISTENTISZT-001*
  OLVAS_HIANY	94	-	ISTENTISZT-001 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/ISTENTISZT-001*
  OLVAS_HIANY	97	-	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a tematikus tanulmány: tematikus_lezart/TEREMT-002*
  OLVAS_HIANY	97	-	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/TEREMT-002*
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py ellenoriz
  HIBA	F91_NEG_ERT_BRIEF.md	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/TEREMT-002*
  HIBA	F94_NEG_FOLY_BRIEF.md	ISTENTISZT-001 motívumot ír (`ir`), de az `olvas`-ból hiányzik a tematikus tanulmány: tematikus_lezart/ISTENTISZT-001*
  HIBA	F94_NEG_FOLY_BRIEF.md	ISTENTISZT-001 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/ISTENTISZT-001*
  HIBA	F97_NEG_ID_TELJES_BRIEF.md	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a tematikus tanulmány: tematikus_lezart/TEREMT-002*
  HIBA	F97_NEG_ID_TELJES_BRIEF.md	TEREMT-002 motívumot ír (`ir`), de az `olvas`-ból hiányzik a kereszthivatkozás-napló: tematikus_lezart/naplok/TEREMT-002*
  8 brief, 5 hiba, 0 figyelmeztetés
  [kilepesi kod: 1]

## a valodi repon
$ python eszkozok/feladatok.py csomag 32 23
  CSOMAGOLHATO	#32	munka: folyamat
  CSOMAGOLHATO	#23	munka: adat (alapértelmezés)
  [kilepesi kod: 0]

$ python eszkozok/feladatok.py csomag 36
  NEM_CSOMAGOLHATO	#36	hiányzó `munka` mező motívumfájlt író briefben — töltsd ki, addig nem csomagolható
  [kilepesi kod: 1]

$ python eszkozok/feladatok.py ellenoriz
  FIGYELEM	F37_TANULMANY_ELLENORZES_BRIEF.md	az `ir` helyettesítő mintát tartalmaz (naplok/): adj meg konkrét fájlt
  70 brief, 0 hiba, 1 figyelmeztetés
  [kilepesi kod: 0]

$ python eszkozok/feladatok.py fuggesek
  # típus	feladat	másik	forrás
  REGI	10	-	ir, olvas hiányzik
  REGI	11	-	ir, olvas hiányzik
  REGI	12	-	ir, olvas hiányzik
  REGI	13	-	ir, olvas hiányzik
  REGI	25	-	ir, olvas hiányzik
  [kilepesi kod: 0]
```

A valódi repón a `feladatok.py ellenoriz` 0 hibát ad (a mai briefek egyike sem nevesít motívum-ID-t az `ir`-ben), a `fuggesek` kimenete az F32 módosítása előtt és után azonos (99 sor, 0 `OLVAS_HIANY`).

*(A kimenetből a `FUGGES`, `KIZAR`, `SORREND`, `KOR` és kölcsönös-függés `FIGYELEM` sorokat a terjedelem miatt kihagytam; ezek változatlanok.)*

## K4.0 — a #23 ága és menete

- `git fetch` után a `git branch -r` listájában nincs `F23` / `MOTIVUM_FORRAS` / `motivum-forras` nevű ág (egyetlen ág sem hivatkozik a #23-ra; a `claude/f32-kontextus` az F32 saját ága).
- `git log --all --grep=F23`: csak a befogadás (`cf5d77c`, `f6a73c3`, `7d9bd38`) és a függés-feloldás (`52f7a58`, F22.1) commitja; menet nem futott, a brief `allapot: nem_indult`.
- Eredmény: nincs nyitott ág, a K4 megállás nélkül, a main-en lévő briefen végrehajtható. A fejléc `fugg: [32]` lett; a `nem_fugg: [22]` marad (a `32` nem volt benne, így kivenni nincs mit; a `nem_fugg: [22]` az F22.1 felülírása).
- Értelmező lépés: a #23 nem tartalmaz (M0 csak olvas és mér, M1 sablon- és sématerv, motívumfájlt nem ír), ezért `munka: ertelmezo` jelölés és `olvas`-kiegészítés nem kellett; a #23 `munka` mezője nincs kitöltve (adatnak számít, mert nem ír motívumfájlt).

## Javítás az ellenőri kör után

- Az F33 és az F42 `ir`-je nem tartalmaz motívumfájlt (`grep '^ir:.*(motivumok|tematikus_lezart|lexikon|genezis)/' *_BRIEF.md`: csak F09, F35, F36), a fenti állítás javítva.
- A `kovetkezo.md` duplikált csomag-sora egyszer áll.
- `git diff --stat origin/main..claude/f32-kontextus -- tematikus_lezart motivumok lexikon genezis generalt_proba adat konkordancia`: üres (motívumfájl és adattábla nem változott).

## Frissítés a 2. ellenőri kör után

- A „valódi repó” próbák (`70 brief, 0 hiba, 1 figyelmeztetés`; a `fuggesek` kimenete előtte és után azonos) az F32.9 előtti kódból valók. A jelenlegi kódban az F09 és F36 `FIGYELEM`/E18-sort ad; a kimenet: `71 brief, 0 hiba, 3 figyelmeztetés` (F09, F36 előzmény + F37 régi jelzés). A MUNKA_HIANY- és előzmény-viselkedést az `eszkozok/tesztek/test_feladatok_kontextus.py` fedi (19 teszt).
- Az `MUNKA_ELOZMENY` kivétel DT-F32c (🟡) alatt: felhasználói döntésre vár, jóváhagyás nem volt. *(Elavult: a DT-F32c eldőlt, l. lent; a tesztszám azóta 20.)*

## DT-F32c alkalmazása (1. opció, 2026.10.04)

- `feladatok.py jeloltek`: a `munka` nélküli, motívumfájlt író brief kihagyási oka „hiányzó `munka` mező (E18, DT-F32c): kitöltésig nem futtatható”; a `FIGYELEM`-szint (CI) változatlan.
- **Hatókör:** a `jeloltek` csak 1. fázisú briefet vizsgál. A valódi F09 és F36 2. fázisú, így rájuk ez az ág nem fut; a védelem a `kovetkezo.md` 1. lépésének szabálya, amely az `ellenoriz`/`fuggesek` E18 `FIGYELEM`-sorára épül (ellenőri 3. kör, 1. eltérés).
- `kovetkezo.md` 1. lépés: az E18 `munka`-figyelmeztetésű feladat nem ajánlható futtathatónak.
- Tesztek: `test_elozmeny_brief_csak_figyelem` (+ jelölt-kizárás), új `test_elozmeny_brief_kitoltve_jelolt`; `test_feladatok_kontextus.py`: 20 teszt, OK.
- Valódi repó: `ellenoriz` → `71 brief, 0 hiba, 3 figyelmeztetés` (rc=0); `jeloltek` → egyetlen JELOLT #43 (az F09/F36 2. fázisú, ma amúgy sem jelölt).
