# BDB_SZELLEM_TESZT — napló (#73)

*Proveniencia: `scope=eszkozok/teszt_bdb_zaras.py (ág claude/bdb-szellem-teszt, 8f70e4f) + adat/forditasok.tsv BDB/teljes sorok + konkordancia/BDB_teljes_unabridged.tsv | forras=repó-adat, mérés | ts=2026-10-06`. A „main-en is bukik” állítás a #38 naplójából (naplok/BDB_FORDITAS_naplo.md 2613. sor) átvett adat, ebben a menetben nem mértem újra a main-en; az ágon a `forditasok.tsv` a main-nel azonos (1–6. adag a main-en).*

## Felmérés

Kiindulás: 21 teszt, 2 FAIL + 1 ERROR (`test_dtf38g_kezi_javitasok`, `test_szellem_tabla_nagybetus_helyei`, `test_ir_ketszer_futtatva_nem_duplikal`).

| Strong | Hely | Ok | Típus | Kezelés |
|---|---|---|---|---|
| H5674 | 1Kir 22:24 | A `KEZI3` és a `SZELLEM_KOVETELT` a DT-F38g (2) régi alakját várja (`a Szellemről abszolút használatban és מֵאֵת 1Kir 22:24`); a `forditasok.tsv` 176. sora a DT-F38h (c) / N-F38c ✅ átfogalmazás óta `abszolút használatban + מֵאֵת: a Szellem 1Kir 22:24`. A régi szöveg 0-szor áll a sorban. | (i)+(ii): elavult elvárás (teszt-tábla), a szöveg lezárt döntésen alapul | javítva a `KEZI3`-ban, a táblában, a javítólista sorában és a H5674-teszt elavult `assertIn(regi, uj)` állításában |
| H4390 | 2Móz 31:3; 35:31 | A szöveg `Szellemmel betölteni 31:3; 35:31` nagybetűs (DT-F38h (b), 5. adag), de a tábla nem ismeri. | (ii): hiányos tábla, döntés fedi | felvéve: `('Szellemmel', 'Szellemmel betölteni 31:3; 35:31')` |
| H6743 | Bír 14:6 | A 6. adagban keletkezett hely; a tábla nem ismeri. | (ii) | felvéve (lásd lent), a DT52 (d) alapján |
| H2451 | Péld 1:23 | `tanítványainak adja az isteni Szellemet 1:23` nagybetűs, a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT53**, nem módosítva |
| H5117 | 4Móz 11:25-26; Ézs 11:2 | `az ׳י Szelleméről` nagybetűs, a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT53** |
| H5012 | Qal 1. és Hithpael 1. | kétszer `az isteni Szellem hatása alatt prófétál`; a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT53** |
| H3847 | Bír 6:34 | `az ׳י Szelleme felöltözte Gedeont`; a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT53** |

Egyik ok sem (iii) (a fordítás eltérése a javító-tábla szerinti elvárástól: a H5674 szövege a DT-F38h (c) szerinti, nem hiba), tehát **`adat/forditasok.tsv`-hez nem nyúltam**.

### `test_ir_ketszer_futtatva_nem_duplikal` (ERROR) gyökéroka

Stacktrace (az eredeti állapotban):

```
BDB_FORDITAS_zaras3.py, alkalmaz(): SystemExit: a regi reszlet 0-szer all (1 kell): abszolút használatban és מֵאֵת 1Kir 22:24
→ main(): SystemExit: H5674: a regi reszlet 0-szer all ...
```

A teszt a jelenlegi táblából az `uj` részleteket visszacseréli `regi`-re (a zaras3 előtti állapot), majd háromszor futtatja a `main(--ir)`-t. A H5674-nél az `uj` (`a Szellemről abszolút …`) már nincs a szövegben (átfogalmazták), ezért a visszacserélés semmit sem csinál, a `regi` 0-szor áll, és az `alkalmaz` hibát dob. **Nem a javítóréteg nem-idempotens logikája**, hanem a H5674 `KEZI3`-bejegyzésének elavulása: az (iv) típus nem áll fenn, a duplikálás a korábbi (megszűnt) `regi ⊂ uj` helyzetből jött. A `KEZI3`-javítás után az `ir` H5674-ig lefut; a teszt a javítás után **már csak a négy tábla-hiány** miatt áll meg (`SystemExit: a Szellem-tabla nem egyezik a tablaval`, H2451, H5117, H5012, H3847). Ez a ⛔ (DT53) feloldása után zöld lesz.

## H6743 felvétele (Bír 14:6)

BDB-forrás (`konkordancia/BDB_teljes_unabridged.tsv`, H6743 szócikk, Qal): „especially of sudden possession by (אֱהִֹים) י ׳רוּחַ, with עַל, with person Judg 14:6 **the Spirit . . . rushed upon him**, so 14:19; 15:14; 1Sam 10:6, 10; 11:6”. A forrás maga nagybetűs, az Úr/Isten Szelleméről szól. A `forditasok.tsv` szövege: `Bír 14:6 a Szellem . . . rárontott`. Tábla: `'H6743': [('Szellem', 'Bír 14:6 a Szellem')]` (a kontextus egyszer áll).

## Állapot a megállásnál

Az `eszkozok/teszt_bdb_zaras.py` 21 tesztből még 1 FAIL + 1 ERROR (mindkettő a négy döntésre váró Strong miatt); `test_dtf38g_kezi_javitasok` és a H5674/H4390/H6743 tábla-sorok zöldek. Döntésre vár: DT53 (`DONTESEK.md`).

## DT53 alkalmazása (F73.3)

*Proveniencia: `scope=eszkozok/teszt_bdb_zaras.py, teszt_forditas_kapuk.py, teszt_normalizal.py, teszt_emeles.py, teszt_ellenoriz_13.py, ellenoriz.py + konkordancia/BDB_teljes_unabridged.tsv (H2451) | forras=repó-adat, mérés | ts=2026-10-06`*

Döntés: DT53 **1. opció** (felhasználó, 2026.10.06): mind a négy hely nagybetűs marad. A H2451 forrásszövege (`BDB_teljes_unabridged.tsv`): „gives her pupils the divine spirit 1:23” — a DT-F38g (3) szerint („ahol a BDB szövege maga mondja: divine spirit”) nagybetűs.

A `SZELLEM_KOVETELT` új sorai (`naplok/BDB_FORDITAS_zaras3.py`), a kontextus mindegyiknél egyszer áll:

| Strong | Szóalak | Kontextus |
|---|---|---|
| H2451 | Szellemet | `tanítványainak adja az isteni Szellemet 1:23` |
| H3847 | Szelleme | `az ׳י Szelleme felöltözte Gedeont` |
| H5012 | Szellem ×2 | `1 az isteni Szellem hatása alatt prófétál` (Qal/Niph.), `1 Az isteni Szellem hatása alatt prófétál` (Hithp.) |
| H5117 | Szelleméről | `az ׳י Szelleméről 4Móz 11:25-26` |

Regresszió: `teszt_bdb_zaras.py` 21/21 OK (a `test_szellem_tabla_nagybetus_helyei` és a `test_ir_ketszer_futtatva_nem_duplikal` is zöld); `teszt_forditas_kapuk.py` 69 OK; `teszt_normalizal.py` 63 OK; `teszt_emeles.py` 10 OK; `teszt_ellenoriz_13.py` 9 OK; `ellenoriz.py` SÉRTÉS 0 (RENDBEN 11, KÉZI 2, JELENTÉS 3). A brief 5. lépésének „`emeles.py ellenoriz` SÉRTÉS 0” feltétele a globális `ellenoriz.py`-t jelenti (az `emeles.py ellenoriz` egy-Strongos alparancs, a #38 naplója is az `ellenoriz.py`-t futtatta). Az `adat/forditasok.tsv` változatlan (`git diff --stat` csak a táblát, a naplót, a `DONTESEK.md`-t és a briefet mutatja).

Következik: 6. lépés ⛔ — `fuggetlen-ellenor`, utána lezárás és a #38 fejlécének váltása.

## Lezárás (F73.5)

A felhasználó jóváhagyása (2026.10.06): a #38 fejléce vált (`fugg: [34, 56, 72, 73]`, `allapot: fut`, `kovetkezo: Folytatás: a 7. adag …`); a javítólista H5674-sora marad (ELLENOR_F73 2. eltérés: a `iras` mező mindkét döntést megnevezi). A #73 fejlécébe `nem_fugg: [38]` került: a #73 olvassa a #38 által írt fájlokat, ezért a `feladatok.py` levezetett #73 → #38 függést és ezzel kört jelzett, holott az irány fordított (DT52 (a)); utána `feladatok.py ellenoriz` 0 hiba. A #73 lezárva, a merge a felhasználóé.
