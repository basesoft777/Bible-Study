ELTÉRÉS: 9 tétel

# ELLENOR_F38_adag6_2 — független ellenőrzés, 2. kör

- Brief: `F38_BDB_FORDITAS_BRIEF.md` (+ DT-F38j, N-F38x, `beerkezo/F38d_SZELLEM_TESZT_JAVITAS_BRIEF_TERVEZET.md`)
- Tartomány: `0ba75ea..HEAD` (F38.355, F38.356 ×2), PR #228; viszonyítási alap: main `bdae91d`
- Az ellenőr nem írhatott fájlt; a jelentést az orkesztrátor mentette tömörítve (az OK sorok összevonva). Futtatás (gyökcsoport-szkript, tesztek) az ellenőr szerepében nem megengedett: NEM ELLENŐRIZHETŐ.

## Eltérések súlyossági sorrendben

1. (közepes) `beerkezo/F38d_…:71` téves előfeltevés: szerinte a H5674 „a Szellemről” marad; a DT-F38h (c) átfogalmazta, a 176. sor ma „a Szellem 1Kir 22:24”.
2. (közepes) `beerkezo/F38d_…:48`: a tábla-okok (ii) javítása jóváhagyás nélkül engedett; a H2451, H5117, H5012, H3847 nagybetűs helyei soha nem lettek eldöntve (DT-F38g (3): helyenkénti tartalmi mérlegelés); ⛔ kell. A H4390-et a DT-F38h (b) fedi.
3. (alacsony–közepes) A brief `lezarva_osszegzes` (11. sor) idő előtti (a #38 nyitott) és elavult szövegű.
4. (alacsony) Nem létező F38.311 commitra hivatkozás több helyen (F38_zaras, naplo, a tervezet 27. sora); a mérés az F38.310a commitban van.
5. (alacsony) A naplóban két „## M6” fejezet.
6. (alacsony) Két commit viseli az F38.356 azonosítót.
7. (alacsony) A main-en bukó Szellem-teszt okát a szöveg „H5674”-nek tulajdonítja; a teszt a H4390, H2451, H5117, H5012, H3847 miatt is bukik (naplo 2612, F38_zaras:6, DONTESEK:60).
8. (alacsony) Az `ir:` listán kívül írt fájlok: `beerkezo/F38d_…`, `naplok/BDB_FORDITAS_gyokcsoport_meres.py`, `naplok/F38_zaras.md`, `naplok/ELLENOR_F38_adag6.md`.
9. (alacsony) `ELLENOR_F38_adag6.md` nem az előírt formátumú (első sor, táblázat), és nem hű másolat.

## Rendben (saját lekérdezéssel)

- Újramért számok a kimeneti TSV-ből igazolva: 7 990 Strong; 7 479 rokonos; csak_bdb 5 702 (71,4% / 76,2%); TWOT-os 5 486, ebből 3 229 (58,9%); 2 504 TWOT nélküli; H1121 TWOT 254. A 2 275 csoport NEM ELLENŐRIZHETŐ (kódolvasás szerint a javítástól nem változik). Megjegyzés: az unió miatt 221 Strong több gyökcsoportba, 207 több TWOT-hoz kerül (a naplóban nem szerepel a nagyságrend).
- DT-F38j: 8 oszlop, nincs duplikátum, (a)–(d) pontosan rögzítve; N-F38x helyőrző, nincs végleges szám.
- Teszthiba-állítás kódolvasással: 21 teszt, a main-en 2 FAIL + 1 ERROR; az ágon a H6743 8. elemként.
- `forditasok.tsv`: +242, régi sorok bájtra azonosak; a 0ba75ea..HEAD szakasz nem érinti. Más `adat/`, `konkordancia/` Δ=0; a gyökcsoport import nélkül maradt; a 7. adag nem indult.
- `futtat.py`: E2–E16, E19, E26: 0; E25 3 régi találat.
