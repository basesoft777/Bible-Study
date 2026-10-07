# F22_Zsolt_elokeszites.md — Zsoltárok: előkészítés (a Sonnet-futás NEM indult)

*Számok szkriptkimenetből: `versbeosztas.py` (újrafuttatva ideiglenes kimenetre; a `naplok/F22_versbeosztas.md` és az `f22/versmegfeleltetes.tsv` újragenerálása bájtra azonos, a fájlok változatlanok), `sonnet_koteg.py minta --var 2527`, `tahot_lefedettseg_ellenoriz.py`, saját számláló szkript (TAHOT/Károli kulcsok). Állapot: ⛔ a felhasználó jóváhagyására vár.*

## 1. Versbeosztás (Zsolt)

- Károli: 2527 vers, 150 fejezet; eredeti (TAHOT): 2527 vers, 150 fejezet. Fejezetenként azonos versszám; eltolt pár 0, K-hiány 0, E-hiány 0. A Zsolt-soroknak az `f22/versmegfeleltetes.tsv`-ben 0 sora van.
- **Nincs „Károli n → TAHOT n+1” eltolás.** A Károli-kulcs a héber számozást követi, a felirat mindkét oldalon az 1. vers (pl. Zsolt 3: 9/9 vers, 51:1 és 60:1 is a felirat). A brief „27 jelzett fejezete” nem eltolódás-jelzés.
- **27 jelzett fejezet = 25 `GYENGE` (r(0) < 0,6) + 2 `KORR_ELT`.** A jelzés kizárólag hosszkorreláció; a fejezet-szintű hosszkorreláció a rövid, párhuzamos félsoros versekre gyenge; a könyv szintű igazítás egyik jelzett fejezetben sem talált eltolást.
- Jelzett fejezetek: 6, 12, 24, 26, 33, 34, 58, 74, 82, 91, 104, 105, 107, 113, 114, 115, 118, 119, 121, 122, 129, 135, 136, 145, 147 (`GYENGE`); 112 (d=-1, r=0,65), 149 (d=-1, r=0,79) (`KORR_ELT`). Közülük r(0) a legalacsonyabb: 114 (−0,06), 6 (0,04), 105 (0,14), 113 (0,15), 121 (0,15). A 6-ra, 112-re és 149-re megnéztem a vershossz-párokat (Károli/eredeti szószám versenként): nincs egyirányú eltolás-minta, a hosszak vers szerint ingadoznak.
- 1:2 / 2:1 eset: **nincs** (K-hiány és E-hiány is 0), így a párosításban nem támogatott 1:2 / 2:1 itt nem merül fel; a 4Móz-féle kézi beolvasztás (`f22/versosszevonas.tsv`) nem kell.
- Eredeti nélküli Károli-vers: 0 (`sonnet_koteg.py minta`), eredeti-oldali gazdátlan vers: 0.

## 2. A Zsolt 88/89/140/142 „TAHOT-hiány”

- **Nincs hiány a mostani adatban.** TAHOT Zsolt: 2527 vers = a Károli 2527 verse (K nincs T: 0, T nincs K: 0). Zsolt 88: 19 vers/223 token, 89: 53/599, 140: 14/157, 142: 8/118 (mind teljes versszámmal).
- A CLAUDE.md „hiányzik legalább … Zsolt 88/89/140/142” sora elavult; a `NYITOTT_FELADATOK.md` (621. sor) szerint az F2 (2026.09.14) a pótlást igazolta, és a ténylegesen hiányzó rész Jób 40:1–5 + 41. (a Zsoltárokat nem érinti). Az `tahot_lefedettseg_ellenoriz.py` összesítése: 1 hiányzó fejezet az egész ÓSZ-ben.
- Következmény a párosításra: nincs eredeti nélküli Károli-vers, a `kezi` kényszer nem keletkezik. Kezelési opció tehát csak a dokumentum-javítás: (a) a CLAUDE.md és a brief `kovetkezo` sorának javítása (a hivatkozás elavult) — tartalmi döntés nincs; (b) a hiány-kezelés elhagyása a jóváhagyási feltételekből.

## 3. Szúrópróba és keretterv

- `f22/minta_Zsolt.tsv` előállítva (`sonnet_koteg.py minta --konyv Zsolt --var 2527`): **2527 vers, 253 köteg (10 vers/köteg)**, `--var` egyezik. (Józs mintája is a teljes könyv; ez nem indít futást.)
- Keretbecslés a Józs-mérésből (4 százalékpont / 658 vers / 66 köteg / 14 668 Károli-token; Zsolt 31 222 token): token-arányosan kb. 8,5 pp, köteg-arányosan kb. 15,3 pp → **várható kb. 9–15 százalékpont**, a 70% indítási és 85% megállási szabály szerint belefér. Becslés, nem mérés; a költői kötegek tokenben sűrűbbek (rövid versek, de felirat/párhuzam), a gondolkodási költség eltérhet.
- **Javasolt pontossági szúrópróba (első költői könyv, DT54):** a teljes futás előtt 12 köteg (~120 vers, a 253-ból), rögzített maggal, rétegezve: felirat-versek (X:1), a 27 jelzett fejezet (≥4 köteg), akrosztichon (119, 111–112, 145), rövid párhuzamos versek; Sonnet-futás, majd a felhasználó helyi `zart_osszevet.py`-összevetése. Ez ~5% könyvarány, kb. 0,5–0,7 pp keret. Alternatíva: a teljes futás után mintavétel (olcsóbb, de nincs korai leállás).

## 4. Kért felhasználói döntések (javaslatok; tétel még nincs felvéve)

1. **A versbeosztás jóváhagyása a Zsolt-ra** (`tokenek.VERSBEOSZTAS_JOVAHAGYOTT` + jóváhagyási napló): javaslat: igen, mert a detektor 2527/2527, 0/0/0 és a 27 jelzés zaj; a jóváhagyást a felhasználó adja (nem írtam).
2. **A TAHOT-hiány elavult állításának kezelése** (DT58 javaslat): a CLAUDE.md/brief sor javítása, a feltétel elengedése.
3. **A szúrópróba módja** (DT59 javaslat): előzetes 12 köteg (javasolt) / utólagos / elhagyás.
4. **A Sonnet-futás indítása** (csak Sonnet, DT-F22c szerint; heti keret 85%-nál megállás a köteg végén, mint a Józsnál).

## 5. Mit nem csináltam

Nem írtam a `VERSBEOSZTAS_JOVAHAGYOTT`-ot és a jóváhagyási naplót; nem futtattam kötegeket, nem hívtam modellt; nem szerkesztettem a FELADATOK.md-t, a DONTESEK.md-t, a CLAUDE.md-t; nem vettem fel tételt.
