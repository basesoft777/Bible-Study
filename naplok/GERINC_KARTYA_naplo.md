# GERINC_KARTYA_naplo.md — #124 napló

*Modell-ellenőrzés (2026-10-29): a brief `sonnet`-et kér, a session `claude-sonnet-5-5` — egyezik. Alap: `origin/main` 0e607b2f.*

## 0. mérés

### (a) A motívumok gerinc-elemei (`adat/elofordulasok.tsv`, `gerinc_elem` / `strong`)

Forrás: `adat/elofordulasok.tsv` (261 adatsor), olvasás `split('\t')`-tel. Proveniencia: `scope=adat/elofordulasok.tsv | forras=elofordulasok.tsv | n=262 | ts=2026-10-29`.

| Motívum | Sorok | Gerinc-elemek (`strong` oszlop; db) |
|---|---|---|
| ALVIL-001 | 72 | H7585 (64), G0086 (8) |
| ANTROP-001 | 8 | G4151+G5590 (7), H5315+H2416 (1) |
| HAMART-001 | 52 | H0779, H0127, H7843 (7–7), H2555 (14, ebből 10 sor `strong`=H2555, `gerinc_elem` magyar címke), H6093 (2), 2 sor `tematikus:` jelölés, üres `strong` |
| HODIT-001 | 33 | H7497 (24), H7496 (8), H5303 (1) |
| ISTENTISZT-001 | 33 | H7121+H8034 (23), G1941 (10) |
| KIRALY-001 | 9 | G5010 (4), H3548 (4, ebből 2 összetett: +H4467, +H3678), H8004 (1); 1 sor G5010+G0540+G0282 |
| MENNY-001 | 9 | H1121+H0430 (4), H5303 (2), 3 sor üres `strong` (`referencia:`, `idézet:`, `formula:`) |
| TEREMT-001 | 42 | H8415 (35), G0012 (7) |
| TEREMT-002 | 3 | H8414+H0922 (`gerinc_elem`: „tohu+bohu”) |

**Tanulságok a kártya tervéhez:**
1. A `gerinc_elem` oszlop nem mindig Strong (pl. `málé+chámász`, `tohu+bohu`, `tematikus:1Móz 3:17`); a keresés kulcsa a `strong` oszlop (mint a `jelolt.py`-ban), a `gerinc_elem` a sor megjelenítésében szerepel („melyik gerinc-elemen lóg”). Az üres `strong`-ú sorok (tematikus/referencia/idézet/formula) a kártyán nem keresnek semmit.
2. Az összetett `strong` (`H3548+H4467`) a `jelolt.py`-ban tagonként keresett; ez a tagot (H4467) önállóan is gerincnek veszi. A kártya ezt megtartja (a brief szerint), de az `egy_tag` jelzés láthatóvá teszi.
3. A tág gerinc-Strongok (brief 2.1/4.): a #108 listája az `F108_ujrascan_elteresek.tsv`-ből veendő át a 4. lépésben.

### (b) A #110 szűrője: van-e géppel alkalmazható szabály, és hol áll?

- **Van, de csak az ISTENTISZT-001-re** (H7121+H8034 és G1941), a DT283 szövege szerint (K0–K3, A, B osztályok; ablak 6 token héberben, 3 görögben, jogi 8). A szabály kódja: `eszkozok/f110_szuro.py` (`heber()`, `gorog()`), a paraméterek a fájl elején.
- **Gond:** az `f110_szuro.py` a `main()`-t modul-szinten hívja (nincs `if __name__ == '__main__'` őr), és fix bemenetet (`naplok/F110_bemenet.tsv`) olvas, tehát **nem importálható**. A szűrő a TAHOT-sor 7. oszlopát (angol tükörfordítás) olvassa az igeállapothoz.
- **A DT283 kiegészítése:** a szűrő *nem dönt* — az A/B osztály sem automatikus bevétel, a kézi olvasás dönt. A kártyán ezért a szűrő eredménye **osztály-jelzés** (K1/K2/K3 = `kiszurve: <ok>`, A/B = átjutott, kézi olvasásra), nem bevétel.
- A többi motívum tág Strongjaira nincs szabály → `szuretlen_tag` (a brief szerint).
- **Javaslat:** a szűrő szabály-függvényeit a #124 új `eszkozok/gerinc_szuro.py` fájlba másolja (a lezárt F110 fájljaihoz nem nyúl), és ennek a fájlnak a neve kerül a workflow `paths:` listájába (N-F124b). Az `ir` ezzel bővül (l. DT403).

### (c) A tanulmányfájl-nevek értelmezhetősége

Mérés: a `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `tematikus_lezart/` `*.md` fájljai, a reguláris minta `^<könyv>_<fej>[v<vers>][-[<fej>v]<vers>]_…`.

- **Géppel értelmezhető: 23 igeszakasz-tanulmány** (`genezis/` 20: `1Moz_1v1` … `1Moz_16`; `ujszovetseg/` 3: `1Thessz_5v23`, `Rom_8v10`, `Zsid_4v12`; plusz `1Moz_14_bovitett`-hez hasonló fejezet-egészek). Alakok: `1Moz_14` (teljes fejezet), `1Moz_12v1-20` (span), `1Moz_1v2-2v3`, `1Moz_4v25-5v32` (fejezethatáron át), `Rom_8v10` (egy vers).
- **Nem igeszakasz-tanulmány, kizárandó a lefedettségből (10 fájl):** a `tematikus_lezart/` 8 motívum-tanulmánya és a 2 `Konnyu_ellenorzes_*` összesítő a `genezis/`-ben.
- **Nem értelmezhető (1 fájl):** `melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md` — több szakasz egy névben. Az 1Móz 14:18-20-at a `1Moz_14_bovitett` már lefedi; a Zsolt 110:4 és a Zsid 5–7 *feldolgozatlan* marad (kézi bejegyzés kell, vagy a térkép hibalistájába kerül).
- A könyvnév-tokenek (`1Moz`, `Rom`, `Zsid`, `1Thessz`) a `Konyv_normalizalo_tabla.tsv` magyar rövidítéseire (`1Móz`, `Róm`, `Zsid`, `1Thessz`) leképezendők; az ékezetlen → ékezetes megfeleltetés a táblából építhető, a nem egyezők a hibalistára kerülnek.
- **Következtetés a DT-F124d-hez:** a fájlnevekből a lefedettség **vers-pontosan levezethető**, ezért a kézi lefedettségi lista (DT-F124d) **nem kell**. A térkép a lefedett *verseket* zárja ki, nem a teljes fejezetet (egy egyverses tanulmány, pl. `Rom_8v10`, nem zárja ki a Róm 8-at). Az egy melyelemzés-fájl a hibalistán marad.

### (d) Alap-összevetés három szakaszra (a `jelolt.py` kimenete)

A `jelolt.py --szakasz` (nem ír) sorszámai, amelyekkel a kártya soraiból a `jelolt.py`-sorok halmazának egyeznie kell (4. lépés tesztje):

| Szakasz | Jelleg | `jelolt.py` sor | „új jelölt” | Megjegyzés |
|---|---|---|---|---|
| 1Móz 6:1-8 | feldolgozott, ismert előfordulásokkal | 10 | 1 | MENNY-001 (H0430, H1121, H5303) és HAMART-001 már előfordulás/jelölt; ISTENTISZT-001 `1Móz 6:4` H8034 egyedül, kollokáció nélkül → ilyen zajt a kártya `egy_tag`-gel jelöli |
| 1Móz 17:1-27 | feldolgozatlan (a következő tanulmány, #13) | 26 | mind | zaj nagy része a tág H1121/H0430 (MENNY-001) és H7121/H8034 (ISTENTISZT-001): ezek a `szuretlen_tag` / szűrő tárgyai |
| Mt 24:37-39 | ÚSZ-szakasz | 0 | 0 | üres eredmény; a kártyának explicit „0 találat” + proveniencia-sort kell adnia |

Megjegyzés: a kártya tényleges kimenetét a 4. lépés után vetem össze (ehhez a kártya kódja kell); a mérés itt a `jelolt.py` oldala.


## 3. Döntés (DT403) — alkalmazva

**Felhasználó, 2026-10-29, az orkesztrátor chatjében, szó szerint: „minden legyen teljes”** (az orkesztrátor üzenetében idézve, értelmezése: a javaslatok teljes elfogadása). (1) a térkép kimenete commit a `main`-re; (2) új `eszkozok/gerinc_szuro.py`. A DT-F124d nem kellett (l. 0.(c)). A DT404 (előminősítés) nyitva marad, alapértelmezés: kimarad.

## 4. A kártya próbája (4. lépés) — három szakasz a `jelolt.py`-val összevetve

Futás: `futtat()` valós adaton, minden szakaszra a kártya (id, igehely, Strong) halmaza **azonos** a `jelolt.py` halmazával (a teszt is ellenőrzi: `teszt_gerinc_kartya.py` `Egyezes`, 5 szakasz).

| Szakasz | Kártya = `jelolt.py` sor | Szűrő | Állapot | Kollokáció | Proveniencia-sor |
|---|---|---|---|---|---|
| 1Móz 6:1-8 (feldolgozott) | 10 = 10 | 7 `szuretlen_tag`, 1 kiszűrve (ISTENTISZT-001 H8034, K0), 2 szűrés nélkül | 7 már előfordulás, 2 már jelölt: elutasítva, 1 új | 4 kollokáció, 1 `egy_tag` | 6 |
| 1Móz 17:1-27 (feldolgozatlan) | 26 = 26 | 20 `szuretlen_tag`, 6 kiszűrve | 26 új | 10 kollokáció, 16 `egy_tag` | 7 |
| Mt 24:37-39 (ÚSZ) | 0 = 0 | — | — | — | 4 (n=0 mind) |

- A `jelolt.py` az 1Móz 6:4 ISTENTISZT-001 H8034-et „új jelölt”-ként adta; a kártya a #110 szűrőjével **kiszűri** (K0: nincs H7121+H8034 pár a versben), a mellékletben megmarad.
- A `jelolt.py`-nak „már jelölt” állapotú sorai a kártyán a jelölt döntésével jelennek meg (`már jelölt: elutasítva`).
- Az 1Móz 17:1-27 20 sora tág gerinc-Strong szűretlen sora (főleg MENNY-001 H1121/H0430, ANTROP-001 H5315): ezek nem kerülnek a `jeloltek.tsv`-be `--ir`-rel.
- `egy_tag` zaj: a MENNY-001 `H1121+H0430` kollokációjának egyik tagja egyedül sem ad motívum-előfordulást; a jelzés ezt láthatóvá teszi (a `jelolt.py` ezt nem különböztette meg).

## 5. A térkép próbája (5. lépés)

Próbafutás: `python eszkozok/gerinc_terkep.py --kimenet <ideiglenes könyvtár a repón kívül>` (≈6 s). Két futás **bajtra azonos** (`cmp`, és a teszt `ValosAdat`); az `adat/*.tsv` változatlan (a teszt hash-eli). 1064 fejezet kap legalább egy találatot vagy szűretlen/nyitva jelzést.

**Lefedettség (a fájlnevekből):** 401 fedett vers, 23 értelmezett tanulmányfájl; **1 nem értelmezhető** (`melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md`) — a Zsolt 110:4 és a Zsid 5–7 ezért feldolgozatlannak számít (a Zsid 5–7-ben a KIRALY-001 gerinc-elemeinek találatai így a térképen maradnak).

**A legjobb 20 fejezet** (a `main` 0e607b2f + a F124 ág állapotára; a végleges térképet az Action írja):

| # | Fejezet | Különböző motívum | Motívumok | Kollokációs találat | Összes találat | Nyitva | Szűretlen tag |
|---|---|---|---|---|---|---|---|
| 1 | 4Móz 32 | 2 | ISTENTISZT-001, KIRALY-001 | 2 | 3 | 0 | 25 |
| 2 | 5Móz 17 | 1 | KIRALY-001 | 1 | 2 | 0 | 18 |
| 3 | Jer 28 | 1 | KIRALY-001 | 1 | 2 | 0 | 9 |
| 4 | Jer 33 | 1 | KIRALY-001 | 1 | 2 | 0 | 5 |
| 5 | 2Móz 31 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 10 |
| 6 | 2Móz 35 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 7 | Józs 21 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 22 |
| 8 | Bír 18 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 21 |
| 9 | 1Sám 1 | 1 | KIRALY-001 | 1 | 1 | 0 | 13 |
| 10 | 1Krón 6 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 51 |
| 11 | 2Krón 29 | 1 | KIRALY-001 | 1 | 1 | 0 | 23 |
| 12 | Zsolt 49 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 13 | Zsolt 80 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 7 |
| 14 | Ézs 40 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 8 |
| 15 | Ézs 45 | 1 | ISTENTISZT-001 | 1 | 1 | 0 | 9 |
| 16 | Jer 13 | 1 | KIRALY-001 | 1 | 1 | 0 | 10 |
| 17 | Róm 8 | 1 | ANTROP-001 | 0 | 14 | 0 | 0 |
| 18 | 1Kir 1 | 1 | KIRALY-001 | 0 | 11 | 0 | 37 |
| 19 | ApCsel 2 | 1 | ANTROP-001 | 0 | 9 | 0 | 0 |
| 20 | 1Kor 12 | 1 | ANTROP-001 | 0 | 8 | 0 | 0 |

**Motívumonként a `szuretlen_tag` arány:** ANTROP-001 71 % (431 szűrt / 1 033 szűretlen), HAMART-001 99 % (8 / 1 234), ISTENTISZT-001 0 % (11 / 0), KIRALY-001 74 % (225 / 643), MENNY-001 100 % (0 / 5 496). **Következtetés:** a térkép csak az ISTENTISZT-001 találatait tekinti szűrtnek; a többi motívum rangsora a szűrő-szabály (külön tétel) hiánya miatt jórészt a szűretlen oszlopban él. A lista ezért ma a kollokációs ISTENTISZT-001/KIRALY-001 helyeket (4Móz 32, 5Móz 17, Jer 28/33, …) emeli ki, nem a „valódi” tematikus sűrűséget.

## 6. Workflow (6. lépés)

`.github/workflows/gerinc_terkep.yml`: `push` a `main`-re az `adat/`-tábláira, a TAHOT/TAGNT-re, a könyvnév-táblára, a tanulmánymappákra (`genezis/**`, `ujszovetseg/**`, `melyelemzesek/**` — a lefedettség bemenete, a brief `paths:` listáját ezzel bővítettem) és a három eszközre; heti `schedule`; `workflow_dispatch`. A `feladatok.yml` mintája: `[bot]` actor kimarad, `concurrency` csoport, a `pardes-feladatok` App tokenje, `git pull --rebase` a push előtt, commit-üzenet UTF-8 fájlból, nincs diff → nincs commit. **Az App jogosultsága nem bővül:** a `feladatok.yml` leírása szerint a `pardes-feladatok` App Contents: read and write jogú a repóra, és a `main` ruleset bypassa; ugyanazok a titkok. A workflow ágon nem fut le írással; **a próbája a `workflow_dispatch` a merge után — a felhasználó lépése**, ahogy a brief előírja.

## 7. ⛔ A 2.3 szövegmódosítások szövege (jóváhagyásra; az átírást a #125 végzi)

**`MUNKAMENET.md`, A3b-sor:** „jelölt-generálás meglévő motívumokhoz → **gerinc-kártya** (a vak olvasás után)”; ma mivel fut: `python eszkozok/gerinc_kartya.py --szakasz "…" --osszevet <tanulmány>`; megjegyzés: az A1–A2 kártya nélkül készül (A4 torzítás); a kártya csak jelölt, `--ir` csak `új` sort ír `nyitva`-val, a kiszűrt és a `szuretlen_tag` sor soha nem íródik be; a `jelolt.py` régi kimenete megmarad.

**`MUNKAMENET.md`, új A3c-sor:** „kártya ↔ kulcsszó-táblázat összevetés” — végrehajtó (`gerinc_kartya.py --osszevet`) + kutató; kimenet: két lista a kereszthivatkozás-naplóba, üresen is (explicit „üres” jelöléssel); az „olvasás talált, kártya nem” lista az A4 ⛔ bemenete. Ha a `kulcsszavak.tsv`-ben nincs sor a tanulmányhoz, az összevetés nem végezhető el (az A3 még nem futott); a kártya ezt kiírja, a listák nem töltendők ki.

**`MUNKAMENET.md`, „Mi hiányzik” után, egy mondat:** „A következő igeszakasz kiválasztását a gépi, ütemezett prioritási térkép támogatja (`naplok/GERINC_TERKEP.md`, `eszkozok/gerinc_terkep.py`, GitHub Action); csak jelölt-sűrűséget mutat, a kiválasztás a tanulmány előtt történik.”

**`sablonok/2_PaRDeS_bovitett_sablon.md` (v21 → v22), a 2. pont után:** „A kulcsszó-táblázat a gerinc-kártya **előtt** készül (vak olvasás; a 3. kiválasztási szempont, a »Motívum-kapcsolódás«, nem hivatkozik a kártyára). A kártya és az összevetés két listája a 4. pont kötelező naplójába kerül, üres eredménynél is; a »kártya talált, olvasás nem« hely jelöltként a `jeloltek.tsv`-n át, döntéssel, az »olvasás talált, kártya nem« kulcsszó az A4 ⛔ elé.” A changelog-sor a fájl elején. A `4_PaRDeS_tematikus_sablon.md` P1–P7 nem változik.

*Állapot: jóváhagyva (DT405, 2026-10-29); ezt a #125 írja át, a #124 a szöveget nem alkalmazza.*

## 8. Nem teljesíthető / korlátok (tételesen)

1. **A workflow éles próbája** csak merge után lehetséges (`workflow_dispatch`); ágon nem futtatható írással. A kimeneti `naplok/GERINC_TERKEP.tsv/.md` ezért **nincs az ágon**; az első példányt az Action írja.
2. **A tág gerinc-Strongok szűrője** csak az ISTENTISZT-001-re létezik (DT283); a többi motívum 100 %-ban `szuretlen_tag` (térkép: ANTROP-001 71 %, HAMART-001 99 %, KIRALY-001 74 %, MENNY-001 100 %). Külön tétel(ek).
3. **`kulcsszavak.tsv`** ma csak fejlécet tartalmaz, ezért az `--osszevet` valós adaton csak az „összevetés nem végezhető el” ágat adja; a két lista tartalmát a szintetikus tesztek igazolják.
4. **A `melyelemzesek/` többszakaszos fájlneve** nem értelmezhető (1 fájl, a hibalistán): a Zsolt 110:4 és a Zsid 5–7 feldolgozatlannak számít, amíg nincs kézi bejegyzés (új tétel, ha kell).
5. **N-F124a** (a kártya-fájl helye): nyitva; a `--md` tetszőleges útvonalra ír, a brief javasolt helye `[könyv-mappa]/naplok/[tanulmány]_gerinc_kartya.md` vagy `naplok/kartyak/`.
6. **N-F124c** (térkép ↔ #81 Károli-ujjlenyomat): nyitva, nem a #124 hatóköre.
7. **`egy_tag` sorok `--ir`-je:** a brief szerint az `új`, nem kiszűrt, nem `szuretlen_tag` sorokat írja, ezért a nem-tág összetett gerinc-elemek `egy_tag` sorai is `nyitva` jelöltként íródnak (indoklásukban jelölve). Ha ez zajt ad, szigorítás külön döntés.
8. **A 2.3 szöveg átírása** a #125-re vár; a 7. pont ⛔ jóváhagyás nélkül nem alkalmazott.

## 9. Eltérések a briefhez / javítókör (ELLENOR_F124)

- **A kártya nem importálja a `jelolt.py` függvényeit** (a brief technikai döntése szerint építenie kellene rájuk). Ok: a verses index, az `egy_tag`/kollokáció és a tartomány-igehelyek kezelése nem fér a `jelolt.py` függvényeibe. A sorhalmaz egyezését (id, igehely, Strong) 5 valós szakaszon a `teszt_gerinc_kartya.py` `Egyezes` őrzi; a `jelolt.py` változatlan. A `gerinc_kartya.py` docstringje ezt rögzíti.
- **Térkép-`ts`:** a tanulmánymappáknál csak a fájlnevek változása (hozzáadás/törlés/átnevezés) számít; a `general.py`, `lekerdez.py`, `strong_util.py` bekerült a bemenetbe és a workflow `paths:` listájába.
- **Kiszűrt `nyitva` jelölt** a `nyitva_db`-ben marad (már látott hely); a `Sir` (Siralmak) kanonikus helyre került a rangsorban.
- **Nyitott tételek felvéve:** DT404 (`DONTESEK.md`), N-F124a, N-F124c és két további tétel (`NYITOTT_FELADATOK.md`).
- **Az `[ELLENŐRZŐ]` PR-cím** kötelező (E16: a workflow ellenőrző-fájl); a PR címe ezt viseli.

