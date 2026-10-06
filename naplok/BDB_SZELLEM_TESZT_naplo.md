# BDB_SZELLEM_TESZT — napló (#73)

*Proveniencia: `scope=eszkozok/teszt_bdb_zaras.py (ág claude/bdb-szellem-teszt, 8f70e4f) + adat/forditasok.tsv BDB/teljes sorok + konkordancia/BDB_teljes_unabridged.tsv | forras=repó-adat, mérés | ts=2026-10-06`. A „main-en is bukik” állítás a #38 naplójából (naplok/BDB_FORDITAS_naplo.md 2613. sor) átvett adat, ebben a menetben nem mértem újra a main-en; az ágon a `forditasok.tsv` a main-nel azonos (1–6. adag a main-en).*

## Felmérés

Kiindulás: 21 teszt, 2 FAIL + 1 ERROR (`test_dtf38g_kezi_javitasok`, `test_szellem_tabla_nagybetus_helyei`, `test_ir_ketszer_futtatva_nem_duplikal`).

| Strong | Hely | Ok | Típus | Kezelés |
|---|---|---|---|---|
| H5674 | 1Kir 22:24 | A `KEZI3` és a `SZELLEM_KOVETELT` a DT-F38g (2) régi alakját várja (`a Szellemről abszolút használatban és מֵאֵת 1Kir 22:24`); a `forditasok.tsv` 176. sora a DT-F38h (c) / N-F38c ✅ átfogalmazás óta `abszolút használatban + מֵאֵת: a Szellem 1Kir 22:24`. A régi szöveg 0-szor áll a sorban. | (i)+(ii): elavult elvárás (teszt-tábla), a szöveg lezárt döntésen alapul | javítva a `KEZI3`-ban, a táblában, a javítólista sorában és a H5674-teszt elavult `assertIn(regi, uj)` állításában |
| H4390 | 2Móz 31:3; 35:31 | A szöveg `Szellemmel betölteni 31:3; 35:31` nagybetűs (DT-F38h (b), 5. adag), de a tábla nem ismeri. | (ii): hiányos tábla, döntés fedi | felvéve: `('Szellemmel', 'Szellemmel betölteni 31:3; 35:31')` |
| H6743 | Bír 14:6 | A 6. adagban keletkezett hely; a tábla nem ismeri. | (ii) | felvéve (lásd lent), a DT52 (d) alapján |
| H2451 | Péld 1:23 | `tanítványainak adja az isteni Szellemet 1:23` nagybetűs, a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT-F73a**, nem módosítva |
| H5117 | 4Móz 11:25-26; Ézs 11:2 | `az ׳י Szelleméről` nagybetűs, a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT-F73a** |
| H5012 | Qal 1. és Hithpael 1. | kétszer `az isteni Szellem hatása alatt prófétál`; a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT-F73a** |
| H3847 | Bír 6:34 | `az ׳י Szelleme felöltözte Gedeont`; a tábla nem ismeri; döntés nem volt. | (ii), döntésre vár | **⛔ DT-F73a** |

Egyik ok sem (iii) (a fordítás eltérése a javító-tábla szerinti elvárástól: a H5674 szövege a DT-F38h (c) szerinti, nem hiba), tehát **`adat/forditasok.tsv`-hez nem nyúltam**.

### `test_ir_ketszer_futtatva_nem_duplikal` (ERROR) gyökéroka

Stacktrace (az eredeti állapotban):

```
BDB_FORDITAS_zaras3.py, alkalmaz(): SystemExit: a regi reszlet 0-szer all (1 kell): abszolút használatban és מֵאֵת 1Kir 22:24
→ main(): SystemExit: H5674: a regi reszlet 0-szer all ...
```

A teszt a jelenlegi táblából az `uj` részleteket visszacseréli `regi`-re (a zaras3 előtti állapot), majd háromszor futtatja a `main(--ir)`-t. A H5674-nél az `uj` (`a Szellemről abszolút …`) már nincs a szövegben (átfogalmazták), ezért a visszacserélés semmit sem csinál, a `regi` 0-szor áll, és az `alkalmaz` hibát dob. **Nem a javítóréteg nem-idempotens logikája**, hanem a H5674 `KEZI3`-bejegyzésének elavulása: az (iv) típus nem áll fenn, a duplikálás a korábbi (megszűnt) `regi ⊂ uj` helyzetből jött. A `KEZI3`-javítás után az `ir` H5674-ig lefut; a teszt a javítás után **már csak a négy tábla-hiány** miatt áll meg (`SystemExit: a Szellem-tabla nem egyezik a tablaval`, H2451, H5117, H5012, H3847). Ez a ⛔ (DT-F73a) feloldása után zöld lesz.

## H6743 felvétele (Bír 14:6)

BDB-forrás (`konkordancia/BDB_teljes_unabridged.tsv`, H6743 szócikk, Qal): „especially of sudden possession by (אֱהִֹים) י ׳רוּחַ, with עַל, with person Judg 14:6 **the Spirit . . . rushed upon him**, so 14:19; 15:14; 1Sam 10:6, 10; 11:6”. A forrás maga nagybetűs, az Úr/Isten Szelleméről szól. A `forditasok.tsv` szövege: `Bír 14:6 a Szellem . . . rárontott`. Tábla: `'H6743': [('Szellem', 'Bír 14:6 a Szellem')]` (a kontextus egyszer áll).

## Állapot a megállásnál

Az `eszkozok/teszt_bdb_zaras.py` 21 tesztből még 1 FAIL + 1 ERROR (mindkettő a négy döntésre váró Strong miatt); `test_dtf38g_kezi_javitasok` és a H5674/H4390/H6743 tábla-sorok zöldek. Döntésre vár: DT-F73a (`DONTESEK.md`).
