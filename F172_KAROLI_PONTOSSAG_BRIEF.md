---
feladat: 172
cim: A Károli–héber/görög szópárosítás pontosságmérése (második modell, emberi szúrópróbával)
kod: KAROLI_PONTOSSAG
tipus: feladat
fazis: folyamat
modell: opus
allapot: folyamatban
ad: a ~599 000 gépi Károli–Strong pár mért pontossága rétegenként (könyvcsoport, héber/görög, bizonyosság), 95%-os konfidencia-intervallummal és hibatípusokkal, egy független második modell vak ellenőrzéséből és a felhasználó szúrópróbájából — a párosítás mint önálló adatkészlet (második adatközlemény) előfeltétele
kovetkezo: "4. lépés: a vak Opus-ellenőrzés kötegei (72 köteg); a külső összevetés 1. adagja a felhasználónál (Bible-Discovery)"
munka: folyamat
olvas: [adat/karoli_strong/, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, f22/versmegfeleltetes.tsv, f22/versosszevonas.tsv, f21p/regi_arany_hibas.tsv, "naplok/F22_*_jelentes.md", naplok/F21P_jelentes.md, eszkozok/karoli_strong/zart_osszevet.py, eszkozok/karoli_strong/szuroproba.py, eszkozok/karoli_strong/meres.py, eszkozok/karoli_strong/arany_ellenoriz.py, adat/SEMA.md]
ir: [dontesek/uj/goofy-turing-b0eb00.md, eszkozok/karoli_strong/pontossag_minta.py, eszkozok/karoli_strong/pontossag_meres.py, eszkozok/karoli_strong/teszt_pontossag.py, eszkozok/karoli_strong/zart_osszevet.py, eszkozok/karoli_strong/pontossag_ellenor.py, eszkozok/karoli_strong/pontossag_kulso.py, f172/]
fugg: []
nem_fugg: [22, 38, 138]
---

# F172_KAROLI_PONTOSSAG_BRIEF.md — A Károli–héber/görög szópárosítás pontosságmérése

*FELADATOK #172 · Modell: opus · v1 · 2026.11.05*

*Befogadva a felhasználó döntésével (2026-11-05): **második modell ellenőriz, emberi szúrópróbával.***

## 1. Cél

Az `adat/karoli_strong/parok_<könyv>.tsv` (133 fájl a könyvtárban; a befogadáskor 598 715 pársor) a #22 gépi párosítása: minden sor „modell-kimenet, javaslat”. Bizonyosság: `magas` (S+C, két modell egyezése; csak 1–2Móz, 52 844 sor) és `alacsony` (S, csak Sonnet; 545 871 sor). A mai támpontok szétszórtak és nem reprezentatívak: Sonnet-pilot 97,3% (1Móz/2Móz/Péld), a 2Móz két modelljének egyezése 96,5%, a többi könyvön egyetlen modell, a régi arany könyvenként 0–17 hármas, a `zart_osszevet.py` (zárt forrású szúrópróba) nyitott. A feladat **egy mért, rétegzett pontosságszámot** ad konfidencia-intervallummal és hibatípusokkal. Ez a párosítást önálló adatkészletként közölhetővé teszi (második adatközlemény), és a `szó-szintű-gépi` azonosítási mód (`adat/SEMA.md`) súlyát is megalapozza.

## 2. Hatókör

**Benne van:**

1. **A második modell: Opus** (a futásban ténylegesen futó modellnév a naplóba, CLAUDE.md). Nem lehet a párosítást végző modellek egyike: **Sonnet** és a „C” modell (**gemini-3.8-flash**, `naplok/F22_1Moz_jelentes.md`, `naplok/F22_2Moz_jelentes.md`). Ha a futtató session nem Opus, a feladat nem indul.
2. **Vak ellenőrzés**: az ellenőr nem a javasolt párt „hagyja jóvá”, hanem a mintába került Károli-szóhoz (a vers Károli-szövegével és a héber/görög szöveggel, TAHOT/TAGNT, Strong-számokkal) **maga jelöli** a megfelelő eredeti szót (vagy „nincs megfelelő”); az összevetés a gépi párral utólag, szkriptben történik. Így a megerősítési torzítás nem mér bele. A bemenet a #22 befagyasztott bemenetével azonos forrású (versmegfeleltetés, versösszevonás), KJV nélkül.
3. **Rétegzett minta** (`eszkozok/karoli_strong/pontossag_minta.py`, rögzített véletlenmag, a mintavételi keret és a rétegsúlyok a jelentésben):
   - nyelv: héber (ÓSZ) és görög (ÚSZ) külön;
   - könyvcsoport — javaslat: ÓSZ: Mózes öt könyve · történeti könyvek · költői és bölcsességi könyvek · próféták; ÚSZ: evangéliumok és ApCsel · levelek · Jelenések;
   - bizonyosság: a `magas` (S+C) réteg külön;
   - **javasolt méret: rétegenként 200 pár** (p≈0,95 mellett ±3 százalékpont, 95%), összesen ~1 600 pár; a végleges méret ⛔ (3. lépés).
   - A `kezi` versek (N-F22e) és a párosítatlan sorok a keretből kimaradnak, a számuk a jelentésben áll.
4. **Kalibráció**: az ellenőr a régi arany hármasokon (`f21p/`, `eszkozok/karoli_strong/arany_ellenoriz.py`) is fut; az ellenőr saját egyezése az arannyal a jelentésben külön szám (az ellenőr megbízhatósága).
5. **Emberi szúrópróba (a felhasználó)**: javaslat **120 pár** — 60 véletlen az ellenőr és a gépi pár **egyezéséből** (a közös hiba becslésére) és legfeljebb 60 az **eltérésekből** (döntőbíráskodás: ki tévedett). Forma: kitölthető tábla `f172/szuroproba_felhasznalo.tsv` (vers, Károli-szó, a két jelölt eredeti szó, Strong, üres `itelet` és `megjegyzes` oszlop); a lektor-felületen való megjelenítés a 3. lépés ⛔-jének választása.
6. **Mérés** (`eszkozok/karoli_strong/pontossag_meres.py`, teszttel): rétegenkénti és súlyozott összpontosság, **Wilson-féle 95%-os intervallum**, az eltérések hibatípusai (javaslat: rossz szó a versben · hiányzó pár · fölös pár · Strong-szám eltérés azonos szón · többszavas egység hibás bontása · versmegfeleltetési hiba), a szúrópróba ítéleteivel korrigált becslés.
7. **Jelentés**: `naplok/KAROLI_PONTOSSAG_jelentes.md` — keret, minta, ellenőr-kalibráció, rétegenkénti pontosság CI-vel, hibatípusok, a szúrópróba eredménye, korlátok; proveniencia-sor minden számhoz (CLAUDE.md 1. szabály).

**Nincs benne:** a párok javítása (`adat/karoli_strong/` csak olvasott; a talált hibák tétel, N-F172…); a `bizonyossag` mező átírása; a második adatközlemény megírása; a `zart_osszevet.py` zárt forrású összevetése (külön, ha a felhasználó adja a bemenetet); a lefedettség (recall) teljes mérése — a pontosság (precision) a cél, a párosítatlan szavak aránya csak leíró szám a `szavak_<könyv>.tsv`-ből.

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md): `opus`. Olvasd: `adat/SEMA.md` 2.20, a `F22_*_jelentes.md` összesítő számai (csak kivonat), `naplok/F21P_jelentes.md`.
1. Keret és rétegek: a pársorok rétegenkénti száma a fájlokból (TSV `split('\t')`, CLAUDE.md), a `kezi`/párosítatlan kizárások; `f172/keret.tsv`.
2. Mintavétel (`pontossag_minta.py`), `f172/minta.tsv`; teszt a determinizmusra (ugyanaz a mag → ugyanaz a minta). Commit (`F172.1`).
3. ⛔ **A felhasználó dönt**: a rétegek és a mintaméret (javaslat: 8 réteg × 200), a szúrópróba mérete (javaslat: 120) és formája (TSV vagy lektor-felület), az ellenőrzés költsége és útja (Opus-subagentek az előfizetésből, kötegelve, vagy API-keret). Tétel `dontesek/uj/<ágnév>.md`-be (`DT-F172a`), megállás.
4. Vak ellenőrzés kötegekben (Opus), a válaszok `f172/ellenor/`-be, a futtató modell nevével. Kalibráció az aranyon. Commit kötegenként (`F172.2.<n>`).
5. Összevetés és mérés (`pontossag_meres.py` + `teszt_pontossag.py`); a szúrópróba-tábla előállítása. Commit (`F172.3`).
6. ⛔ **A felhasználó szúrópróbája**: a `f172/szuroproba_felhasznalo.tsv` kitöltése; amíg nincs kész, a feladat `dontesre_var` („Te: szúrópróba”).
7. A korrigált becslés, a jelentés; független ellenőr (`fuggetlen-ellenor`); draft PR. A talált rendszerhibák nyitott tételként (`nyitott/uj/<ágnév>.md`, `N-F172…`).

## 4. Elfogadási feltételek

- Az ellenőr modellje a futásnapló szerint nem Sonnet és nem gemini; a ténylegesen futott modellnév minden kötegnél rögzítve.
- A minta reprodukálható (rögzített mag, teszt); a keret és a rétegsúlyok a jelentésben.
- Minden rétegre: n, pontosság, Wilson 95% CI; súlyozott összpontosság CI-vel; héber és görög külön is.
- Az ellenőr kalibrációja az aranyon külön szám; a hibatípusok megoszlása rétegenként.
- A felhasználó szúrópróbájának ítéletei beépítve (a korrigált becslés mellett a nyers is áll).
- Az `adat/karoli_strong/` változatlan (`git diff --stat` 0 sor).

## 5. Döntésnapló

- `nem_fugg: [22, 38, 138]` (befogadás, 2026-11-05): a #38 csak olvasott táblát (normalizáló tábla) ír; a mérés a #22 **mai** állapotát méri (a befogadáskor 598 715 pár); a #22 hátralévő része (N-F22e, a 20 `kezi` vers) a keretből kimarad, és a jelentés a mért commitot rögzíti. A #138 a `TAHOT_kivonat.tsv`-t írhatja; a mérés a futáskori commit TAHOT-állapotán fut, ezt a jelentés rögzíti.
- A második modell választása (Opus) a befogadáskor rögzítve, a felhasználó döntése (2026-11-05) szerint; a javaslat az orkesztrátortól.
- A szúrópróba módja megváltozott (a felhasználó, 2026-11-05, az orkesztrátoron át): a kézi jelölő tábla helyett összevetés egy független, Strong-címkés forrással (Bible-Discovery, Strong-os Károli HUN modul, zárt licenc), amelyből a felhasználó versadagokat másol be. Ezért a `zart_osszevet.py` kibővítése a hatókörbe kerül (a 2. „Nincs benne” e pontja érvénytelen); a forrás szövege csak mérésre, a repóba nyersen nem kerül (DT32-elv). A méret és a forma: DT-F172a.
