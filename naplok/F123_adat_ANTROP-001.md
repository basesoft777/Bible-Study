# F123 X.A — az ANTROP-001 adat-előkészítése (munkafájl)

*#123 MIGRACIO2 · 2b. 1. lépés (`munka: adat`) · ág: `claude/f123-antrop-adat-44e370` · modell: claude-opus-5-5 · 2026-11-02*

*Döntés nélküli munkafájl: jelentéstartományt nem választ, prózát nem ír, motívumfájlt (`motivumok/`, `tematikus_lezart/`, `lexikon/`) és adattáblát (`adat/*.tsv`) nem ír (2b). A teljes sorok a mellékelt TSV-kben állnak, minden sor mellett a lekérdezés proveniencia-sorával; ez a fájl összegzés. A lekérdezések naplója: `naplok/F123_lekerdezesek.tsv` (`lekerdez.py --naplo F123`). Munkaszkript: `naplok/F123_adat_keszito.py` (az ALVIL-001-é; alparancsok: `f108`, `szotar`, `proza`, `rokon`), felmérő eszköz: `eszkozok/motivum_felmeres.py`. Futtatás: `PARDES_DATUM=2026-11-02`, a `c813fd34` (main) commiton.*

*Hatókör (DT-F10a (2)): csak az X.A. Az X.M1–X.M5 (leképezési tábla, szétválasztás, mérés, törzscikk) és minden prózát író lépés a DT-F123c (a `9_` sablon v1) ⛔ után jön. Az ANTROP-001-nek nincs külön kereszthivatkozás-naplója (N18, N-F63b; 2a. 3.); ezt az X.M1 tábla mondja ki.*

## 0. A motívum az adatrétegben

| Mező | Érték |
|---|---|
| `adat/motivumok.tsv` | Pneuma/pszükhé megkülönböztetés · `lexikai` · tanulmány: `tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md` (19 280 bájt) |
| negatív kritérium | a πνεῦμα és a ψυχή (vagy melléknévi alakjuk) egyazon mondaton belül, megkülönböztető szerepben; a puszta „lélek” vagy „szellem” említés a másik nélkül nem elég |
| fölérendelt fogalom | emberi belső élet / antropológia általában |
| `adat/elofordulasok.tsv` | 8 sor; `gerinc_elem` = `strong`: `G4151+G5590` (7), `H5315+H2416` (1: 1Móz 2:7) |
| `adat/jeloltek.tsv` | 11 sor: 8 `beépítve` (az előfordulások), 3 `nyitva` (Fil 1:27, 2026-09-13; 1Pét 1:22 és Mt 12:18, F108, 2026-10-17) |

Mért adathiány a soron (nem e menet dolga, az értelmező menet elé): mind a 8 előfordulás-sor `funkcio` mezője üres, és egyiknek sincs `lexikon_szotar` / `lexikon_entry_id` / `jelentes_szam` értéke (a jelentés-hivatkozás hiánya: `NYITOTT_FELADATOK.md`, F6 tétel).

Proveniencia: `scope=ANTROP-001: adat/motivumok.tsv (1 sor), adat/elofordulasok.tsv (8 sor), adat/jeloltek.tsv (11 sor) | forras=split('\t'), ág claude/f123-antrop-adat-44e370 | ts=2026-11-02`

## 1. A törzs összevetése a #108 eltérés-táblájával (2c)

**A törzs nincs újra levezetve** (2c): a meglévő ANTROP-001-sorok vannak összevetve a `naplok/F108_ujrascan_elteresek.tsv` (2026-10-17) 79 ANTROP-001-sorával, és a két gerinc-elemre lefutott a mai scan. **Módszer-kiigazítás:** a munkaszkript `f108` alparancsa eddig Strongonként scannelt (az ALVIL-001 egytagú elemein); az összetett elemre (`A+B`) most a #108 módján **kollokációt** futtat (két Strong egy versben). Az ALVIL-001 kimenete ezzel nem változik: újrafuttatva, a ts- és ágmező nélkül bájtra azonos (F123.ANTROP.A1 ellenőrzés; a fájl nincs újraírva).

| Mérés | Eredmény |
|---|---|
| `elofordulasok.tsv` sorok (ma / F108) | 8 / 8 — kulcs mind egyezik; **új vagy eltűnt sor: 0** |
| `jeloltek.tsv` sorok (ma / F108) | 11 / 9 — a különbség a #108 által írt 2 `nyitva` sor (1Pét 1:22, Mt 12:18: `uj_J_sor_a_108_ota`, az F108-ban `uj_jelolt_irva`); döntést váltott sor: 0 |
| F108-osztály, E-sorok | 4 `rendben`, 3 `osszetett_resz` (Luk 1:46 csak G5590, Luk 1:47 csak G4151, 1Kor 2:14 csak G4151), 1 `hianyzik` (1Kor 2:15: G4152, a főnév egyike sincs) |
| mai kollokáció G4151+G5590 | 6 vers: 3 előfordulás (1Thessz 5:23, Zsid 4:12, 1Kor 15:45), 3 `nyitva` jelölt (Fil 1:27, 1Pét 1:22, Mt 12:18), **0 új**; `KULCS_ELTERES` 4: Luk 1:46, 1:47, 1Kor 2:14, 2:15 — a fenti F108-osztállyal azonos, nem új eltérés |
| mai kollokáció H5315+H2416 | 61 vers: 1 előfordulás (1Móz 2:7), **60 nem E/J hely, mind ismert az F108-ból** (49 `uj_talalat_nem_irva_tul_tag`, 11 `zsoltar_55_uj_talalat_nem_irva`); a #108 óta új hely: 0 |
| #110 szűrő | **nincs ANTROP-001-szabály:** a `eszkozok/gerinc_szuro.py` csak az ISTENTISZT-001 elemeire szűr (DT283), minden más tág elem `szuretlen_tag` (`NYITOTT_FELADATOK.md`, F124-tétel: ANTROP-001 71 %). A 60 H5315+H2416-hely szűretlen marad; l. 6. 3. |

**Eredmény: gerinc-elemet érintő eltérés (Strong be/ki) nincs.** A #108 óta a mai TAHOT/TAGNT-on nincs új hely; a négy kulcseltérés a régi `G4151+G5590`-tétel (`NYITOTT_FELADATOK.md`, F3.4) mért alakja, l. 6. 2.

Részletes sorok: `naplok/F123_adat_ANTROP-001_f108_osszevetes.tsv` (8 E + 11 J + 63 újrascan-sor).

Proveniencia:

- `scope=ANTROP-001: adat/elofordulasok.tsv (8 sor) + adat/jeloltek.tsv (11 sor) × naplok/F108_ujrascan_elteresek.tsv (79 sor) | forras=split('\t'), ág claude/f123-antrop-adat-44e370 | ts=2026-11-02T10:47Z`
- `scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=G4151+G5590 | n=6 | ts=2026-11-02T10:47Z | csatorna=cli`
- `scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H5315+H2416 | n=61 | ts=2026-11-02T10:47Z | csatorna=cli`

## 1b. A görög gerinc-elem rokon alakkal és versablakkal (a negatív kritérium két kitétele)

A negatív kritérium két, gépileg mérhető kitételt tartalmaz, amelyet a szó szerinti kollokáció nem fed: „**vagy melléknévi alakjuk**” (ψυχικός G5591, πνευματικός G4152) és „**egyazon mondaton belül**” (a mondat átnyúlhat a vershatáron, pl. Luk 1:46–47). Ugyanezt a két pontot nevezi meg a gépi előszűrő lexikai kiterjesztése (N-F150a (1); a #160 PR #580 a jelolt_eloszures.py-ban). A mérés: (G4151 | G4152) × (G5590 | G5591), azonos versben és ±1 versben, azonos fejezetben (`python naplok/F123_adat_keszito.py rokon ANTROP-001 G4151,G4152 G5590,G5591 1`). **A versablak a mondathatár gépi közelítése, nem a mondathatár**; a kimenet mért mező, ítélet nélkül.

| Alap | Alak | Előfordulás | Jelölt | **Új** |
|---|---|---|---|---|
| azonos vers | főnévpár | 3 | 3 | 0 |
| azonos vers | rokon alakkal | 1 (1Kor 2:14) | 0 | **3** — 1Kor 15:44, 1Kor 15:46, Júd 1:19 |
| szomszéd vers (±1) | főnévpár | 1 (Luk 1:46–47) | 0 | **5** — Luk 9:55–56, ApCsel 4:31–32, ApCsel 20:23–24, 2Kor 1:22–23, 1Pét 3:19–20 |
| szomszéd vers (±1) | rokon alakkal | 4 (1Kor 2:13–14, 2:14–15, 15:44–45, 15:45–46) | 0 | **1** — Júd 1:19–20 |

- **Kontroll:** a négy kulcseltéréses előfordulás (Luk 1:46, 1:47, 1Kor 2:14, 2:15) mind megjelenik; a rokon alak és a versablak tehát a meglévő törzset visszaadja.
- **Az új helyek egyike sincs a `jeloltek.tsv`-ben.** Az 1Kor 15:44 és 15:46 a tanulmányban egyszer áll, a 15:44 is csak egy prooftext-lista „1Kor 15:44-45” tagjaként (a „Az összevetés eredménye” bekezdésben); a 15:46-ot és a Júd 1:19-et a tanulmány nem említi (saját grep, 2026-11-02).
- A **héber** elemre (H5315+H2416) rokon alak vagy versablak nincs mérve: a negatív kritérium a görög szópárról szól, a héber megfelelő (pl. a H7307 rúah + H5315) kiválasztása mező-hipotézis (2. lépés, B3/P2), nem determinisztikus lépés.

Sorok: `naplok/F123_adat_ANTROP-001_rokon_ablak1.tsv` (21 sor). A beírásuk a `jeloltek.tsv`-be döntés: l. 6. 1.

Proveniencia: `scope=TAHOT-teljes+TAGNT-teljes: (G4151 | G4152) × (G5590 | G5591) egy versben vagy ±1 versen belül, azonos fejezet | forras=konkordancia/TAGNT_kivonat.tsv, TAHOT_kivonat.tsv (lekerdez.load_tagnt/load_tahot), split('\t') | állapot: adat/elofordulasok.tsv, adat/jeloltek.tsv (ANTROP-001) | ts=2026-11-02T10:48Z`; a négy kollokáció-pár proveniencia-sora (G4151+G5590 n=6, G4151+G5591 n=2, G4152+G5590 n=0, G4152+G5591 n=2) a `naplok/F123_lekerdezesek.tsv`-ben.

## 2. Szótári sorok, hiányzó fordítások, szerepenkénti nyers kínálat (2b)

A motívum Strongjai az `elofordulasok.tsv` `strong` mezője szerint: **G4151, G5590, H2416, H5315**. A rokon alakok (G4152, G5591) nincsenek benne: a szótári kínálat a sorokon álló gerinc-Strongokra szól; ha a 6. 2. kérdés a soron álló szót választja, a két melléknév szótári sorai a munkaszkripttel pótolhatók.

**Szótári sorok:** 685 sor, `naplok/F123_adat_ANTROP-001_szotar.tsv` (forrás, kulcs, hossz, SHA-1-előtag, 160 karakteres kivonat, a generátor szerinti `forditasok.tsv`-kulcs és annak állapota, proveniencia). A nagy szám a két tág héber szó (H5315, H2416) BDB-szakaszaiból és Károli-megfelelőiből jön (héber 13. szerep: 331 sor).

**Szerepenkénti nyers kínálat** (`adat/szotar_szerepek.tsv`, 13 szerep × 2 nyelv): `naplok/F123_adat_ANTROP-001_szerepkinalat.tsv`. Mind a 26 szerephez van sor; üres szerep nincs. Az ALVIL-001-hez hasonlóan három szerep jelölt állapot, nem szótári forrás (10. kiejtés, 12. Nave — a négy Strong a motívum verseire illesztve, 14. rejtett/hamis párhuzam — a 13.-ból származtatva). Jelentéstartomány nincs kiválasztva (a 2. lépés D50-döntése).

**Hiányzó fordítások — 98 kulcs** (`naplok/F123_adat_ANTROP-001_forditas_hiany.tsv`; a kulcsok a `lexikon_general.py` `forditas_ehhez` hívásai szerint; **a `forditasok.tsv`-be nincs írva**, a pótlás külön adatfeladat, 2b):

| Szótár | Strong | Mező | Kulcs |
|---|---|---|---|
| TBESH | H5315, H2416 | forditas_hu (`teljes`) | 2 |
| TBESG | G4151, G5590 | forditas_hu (`teljes`) | 2 |
| BDB | H5315, H2416 | forditas_hu (`nyelvi_hatter`) | 2 |
| LSJ | G4151, G5590 | forditas_hu | 2 |
| MCGED | G4151, G5590 | glosszak_hu | 2 |
| UBS_DBH | H2416 (12 jelentés), H5315 (7) | definicio_hu + glosszak_hu | 38 |
| UBS_DNTG | G4151 (11 jelentés), G5590 (9) | definicio_hu + glosszak_hu | 40 |
| tW_szocikkek | G4151 5, G5590 2, H2416 3, H5315 1 cikk | forditas_hu | 11 (köztük a gépi illesztés furcsasága: a H5315-höz a `other/member` cikk, mert a cikk Strong-listáján szerepel) |

A 98 a 2026-11-01-i N-F148a-mérés (ANTROP 120 hívás / 122 jelölés a lapon) más mércéje: ott a generált lap minden `forditas_ehhez` hívása számít, itt csak a négy gerinc-Strong szótári kulcsai.

Proveniencia: minden sor saját proveniencia-mezővel (a `szotar`/`szerepkinalat`/`forditas_hiany` TSV utolsó oszlopa); a futás: `scope=ANTROP-001 Strongjai (G4151, G5590, H2416, H5315) × adat/szotar_szerepek.tsv | forras=naplok/F123_adat_keszito.py szotar | ts=2026-11-02T10:49Z`

## 3. Felmérő lekérdezés (2d. 1.) — `eszkozok/motivum_felmeres.py`

`python eszkozok/motivum_felmeres.py ANTROP-001 --ki naplok/F123_felmeres_ANTROP-001` (az ALVIL-001-nél készült eszköz, változatlanul). Kimenet: `naplok/F123_felmeres_ANTROP-001.md` és három TSV, **teljes egészében az értelmező menet elé** (2c). Mért tény, nem állítás; a közös szókészlet nem bizonyít idézést.

| Blokk | Eredmény | Fájl |
|---|---|---|
| (a) kísérő szavak | 67 Strong a motívum 8 versében; 20 grammatikai Strong kizárva. Leggyakoribb: G2316 θεός (4 motívumvers), G0350 ἀνακρίνω, G0444 ἄνθρωπος, G2198 ζάω, G2962 κύριος (2–2) | `naplok/F123_felmeres_ANTROP-001_kiserok.tsv` |
| (b) szomszédos motívumok, azonos fejezet | **0 pár — üres eredmény** (a 6 fejezetben: 1Móz 2, 1Thessz 5, Zsid 4, 1Kor 15, Luk 1, 1Kor 2 más motívum előfordulása nincs) | `naplok/F123_felmeres_ANTROP-001_szomszedok.tsv` |
| (c) válasz-szavak ±3 vers (H6030, H8085, G0191, G1522, G0611) | **0 találat — üres eredmény** | `naplok/F123_felmeres_ANTROP-001_valasz.tsv` |

Az üres (b) és (c) mért eredmény, nem hiány (CLAUDE.md 3. szabály). A (c) válasz-szólistája az ISTENTISZT-001-felmérés példájának paramétere; az ANTROP-001-re nem szabott.

Proveniencia: a `naplok/F123_felmeres_ANTROP-001.md` három sora (ts=2026-11-02T10:50Z) és minden TSV-sor utolsó mezője.

## 4. Próza-lefedettség (2d. 2.) — mérés, nem kapu

**Helye:** a brief szerint a motívum naplójába (`motivumok/naplok/ANTROP-001_*`); az X.A a forrásréteget nem írja, ezért az eredmény itt és a `naplok/F123_adat_ANTROP-001_proza_lefedettseg.tsv`-ben áll; **az értelmező menet viszi át**, proveniencia-sorával. Módszer: az ALVIL-001-é (4. szakasz; `proza` alparancs), a kézi rések a `adat/res_forras.tsv` `tanulmany` forrású sorai.

| Kategória (a kézi rések említésszáma) | Előfordulás-sor |
|---|---|
| tárgyalja (4+) | **8 a 8-ból** — 1Móz 2:7 (6), 1Thessz 5:23 (9), Zsid 4:12 (5), 1Kor 15:45 (7), Luk 1:46 (10), Luk 1:47 (10), 1Kor 2:14 (10), 1Kor 2:15 (9) |
| érinti (1–3) | 0 |
| nem nevezi meg | **0** |

| Rés | Méret | Igehely-említés |
|---|---|---|
| kivonat | 760 B | 9 |
| miert_fontos | 3 247 B | 31 |
| ertelmezes | 5 389 B | 15 |
| modszertan | 971 B | 12 |
| minosites | 75 B | 0 — a törzs: „A kereszthivatkozás-minősítés ennél a motívumnál nem készült el.” (nincs napló) |
| 2b (szótári adat, nem próza) | 37 B | 0 — a törzs: „Nincs kiegészítő szótári adat.” |

A kis motívumon a próza minden előfordulást tárgyal; a lefedettségi rés nem az előfordulásokon, hanem a **jelölteken** van: a 3 `nyitva` jelölt (Fil 1:27, 1Pét 1:22, Mt 12:18) és az 1b. 9 új helye közül a tanulmány csak az 1Kor 15:44-et említi, egy prooftext-listában. Ezek elbírálása az értelmező menet dolga (B5).

Proveniencia: `scope=ANTROP-001: adat/elofordulasok.tsv (8 sor) × kézi rések (2b 37 B, ertelmezes 5389 B, kivonat 760 B, miert_fontos 3247 B, minosites 75 B, modszertan 971 B; forrás: tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md) + a fájl egésze + lexikon/ANTROP-001_TUDOMANYOS.md (70315 bájt, generált) | forras=saját számláló (naplok/F123_adat_keszito.py proza) | ts=2026-11-02T10:50Z`

## 5. Ami az ALVIL-001 X.A-jából itt nem alkalmazandó

- A 2e. Seól-scan (`seol`, `seol_ablak`): az ALVIL-001 saját tétele (DT-F123d), itt nincs megfelelője.
- A #131-megfigyelés (BDB-szakaszok `kezi` `teljes` sora): az ANTROP-001 két héber Strongjának BDB-szakaszai a 2. pont szótár-TSV-jében állnak; a gerinc-címkék (`adat/szotar_szakasz_cimke.tsv`) és az `SZOTARI_GERINC` `kivetel` sorának törlése (X.K, N-F148c) az értelmező menet és az X.M5 része, nem az X.A-é.

## 6. Nyitott kérdések (itt nincs döntés)

1. **Az 1b. 9 új helye a `jeloltek.tsv`-be** (2. szabály: minden jelölt ott megy át). A 3 azonos versű, rokon alakos hely (1Kor 15:44, 15:46, Júd 1:19) a negatív kritérium betűje szerint kollokáció; a 6 szomszéd-verses hely a mondathatár gépi közelítése. Beírás `nyitva`-ként, döntés nélkül, vagy a naplóban hagyás az értelmező menetig: döntés (l. a DONTESEK.md helyőrzőjét, ha keletkezik).
2. **A `G4151+G5590` gerinc-elem az 1Kor 2:14/2:15-ön (`NYITOTT_FELADATOK.md`, F3.4)**, mért alakban: 2:14 G4151 + G5591, 2:15 G4152 (és 2:14–15 párként G4152 + G5591); ugyanez a Luk 1:46 (G5590) / 1:47 (G4151) összetett sorain. A kérdés változatlan: a `gerinc_elem` a motívum magját nevezi-e meg (marad), vagy a soron álló szót. A 2c szerint gerinc-elemet érintő kérdés, tehát ⛔, nem az X.A döntése.
3. **A H5315+H2416 60 szűretlen tág helye** (`NYITOTT_FELADATOK.md`, F124-tétel). Az ANTROP-001-re nincs #110-típusú szűrő; a negatív kritérium a görög szópárról szól, a héber elem egyetlen sora (1Móz 2:7) a tanulmányban is „tematikus, ellentétező párhuzam, NEM lexikai folytonosság”. Hogy a 60 hely szűrő-szabályt kap-e, vagy a héber elem kizáró indoklással zárul, határkérdés.
4. **Hiányzó fordítások (98 kulcs):** külön adatfeladat (`forditasok.tsv`, a #123 `ir`-jén kívül; 2b), API-keretből — a költés a felhasználóé.
5. **N-F160b:** ha az értelmező menet elutasított sort termel, a gépi előszűrő az ANTROP-001-en újramérendő (DT-F160b).
