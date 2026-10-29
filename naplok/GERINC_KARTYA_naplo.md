# GERINC_KARTYA_naplo.md — #124 napló

*Modell-ellenőrzés (2026-10-29): a brief `sonnet`-et kér, a session `claude-sonnet-5-5` — egyezik. Alap: `origin/main` 0e607b2f.*

## 0. mérés

### (a) A motívumok gerinc-elemei (`adat/elofordulasok.tsv`, `gerinc_elem` / `strong`)

Forrás: `adat/elofordulasok.tsv` (262 sor), olvasás `split('\t')`-tel. Proveniencia: `scope=adat/elofordulasok.tsv | forras=elofordulasok.tsv | n=262 | ts=2026-10-29`.

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
- **Javaslat:** a szűrő szabály-függvényeit a #124 új `eszkozok/gerinc_szuro.py` fájlba másolja (a lezárt F110 fájljaihoz nem nyúl), és ennek a fájlnak a neve kerül a workflow `paths:` listájába (N-F124b). Az `ir` ezzel bővül (l. DT-F124a).

### (c) A tanulmányfájl-nevek értelmezhetősége

Mérés: a `genezis/`, `ujszovetseg/`, `melyelemzesek/`, `tematikus_lezart/` `*.md` fájljai, a reguláris minta `^<könyv>_<fej>[v<vers>][-[<fej>v]<vers>]_…`.

- **Géppel értelmezhető: 24 igeszakasz-tanulmány** (`genezis/` 20: `1Moz_1v1` … `1Moz_16`; `ujszovetseg/` 3: `1Thessz_5v23`, `Rom_8v10`, `Zsid_4v12`; plusz `1Moz_14_bovitett`-hez hasonló fejezet-egészek). Alakok: `1Moz_14` (teljes fejezet), `1Moz_12v1-20` (span), `1Moz_1v2-2v3`, `1Moz_4v25-5v32` (fejezethatáron át), `Rom_8v10` (egy vers).
- **Nem igeszakasz-tanulmány, kizárandó a lefedettségből (10 fájl):** a `tematikus_lezart/` 8 motívum-tanulmánya és a 2 `Konnyu_ellenorzes_*` összesítő a `genezis/`-ben.
- **Nem értelmezhető (1 fájl):** `melyelemzesek/1Mozes_14_18-20_Zsolt110_4_Zsid5-7_melyelemzes.md` — több szakasz egy névben. Az 1Móz 14:18-20-at a `1Moz_14_bovitett` már lefedi; a Zsolt 110:4 és a Zsid 5–7 *feldolgozatlan* marad (kézi bejegyzés kell, vagy a térkép hibalistájába kerül).
- A könyvnév-tokenek (`1Moz`, `Rom`, `Zsid`, `1Thessz`) a `Konyv_normalizalo_tabla.tsv` magyar rövidítéseire (`1Móz`, `Róm`, `Zsid`, `1Thessz`) leképezendők; az ékezetlen → ékezetes megfeleltetés a táblából építhető, a nem egyezők a hibalistára kerülnek.
- **Következtetés a DT-F124d-hez:** a fájlnevekből a lefedettség **vers-pontosan levezethető**, ezért a kézi lefedettségi lista (DT-F124d) **nem kell**. A térkép a lefedett *verseket* zárja ki, nem a teljes fejezetet (egy egyverses tanulmány, pl. `Rom_8v10`, nem zárja ki a Róm 8-at). Az egy melyelemzés-fájl a hibalistán marad.

### (d) Alap-összevetés három szakaszra (a `jelolt.py` kimenete)

A `jelolt.py --szakasz` (nem ír) sorszámai, amelyekkel a kártya soraiból a `jelolt.py`-sorok halmazának egyeznie kell (4. lépés tesztje):

| Szakasz | Jelleg | `jelolt.py` sor | „új jelölt” | Megjegyzés |
|---|---|---|---|---|
| 1Móz 6:1-8 | feldolgozott, ismert előfordulásokkal | 10 | 1 | MENNY-001 (H0430, H1121, H5303) és HAMART-001 már előfordulás/jelölt; ISTENTISZT-001 `1Móz 6:4` H8034 egyedül, kollokáció nélkül → ilyen zajt a kártya `egy_tag`-gel jelöli |
| 1Móz 17:1-27 | feldolgozatlan (a következő tanulmány, #13) | 23+ | mind | zaj nagy része a tág H1121/H0430 (MENNY-001) és H7121/H8034 (ISTENTISZT-001): ezek a `szuretlen_tag` / szűrő tárgyai |
| Mt 24:37-39 | ÚSZ-szakasz | 0 | 0 | üres eredmény; a kártyának explicit „0 találat” + proveniencia-sort kell adnia |

Megjegyzés: a kártya tényleges kimenetét a 4. lépés után vetem össze (ehhez a kártya kódja kell); a mérés itt a `jelolt.py` oldala.

## 3. ⛔ Döntési pont — DT-F124a (és a szűrő fájlja)

A kérdés, az opciók és a javaslat a `DONTESEK.md`-ben (DT-F124a). A DT-F124d (lefedettségi forrás) a (c) mérés szerint **nem szükséges**.
