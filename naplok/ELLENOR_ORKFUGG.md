# ELLENŐR — F39_ORKESZTRATOR_FUGGES_BRIEF.md · c66f7cb..cc1a60e (1. kör)

*A `fuggetlen-ellenor` jelentése; az ügynöknek nincs fájlíró eszköze, ezért az orkesztrátor mentette. Az ügynök a `ellenoriz`, `fuggesek`, `jeloltek` és a tesztek futtatását nem végezhette (NEM ELLENŐRIZHETŐ); ezeket az orkesztrátor futtatja a javítás után.*

## 1. kör: ELTÉRÉS, 6 tétel (súlyossági sorrend)

1. `eszkozok/feladatok.py:457-472`: ha egy explicit `fugg` levezetett éllel esik egybe és kölcsönös párt alkot, az explicit függés kizárássá válik és elvész (DT-F39e, K6 sérül). A tesztek nem fedik.
2. `eszkozok/feladatok.py:463-472`: a kölcsönös élek törlése a kör-keresés előtt elrejtheti a kettőnél hosszabb kört (példa: A↔B, A→C, C→B), pedig ez a DT-F39g szerint hiba.
3. A brief `allapot: dontesre_var` maradt `fut` helyett; a „#32 a #39 lezárásáig nem indul” megkötés kikerült a fejlécből, így a `KIZAR 32 39` pár nem blokkol.
4. `DONTESEK.md:40-45`: a DT-F39a–e és g „🟢 alkalmazásra vár”, de a kód alkalmazza őket.
5. `naplok/F39_probafuttatas.md:47`: a #23→#37 él indoklása hibás; a valódi ok az `ATALAKITASI_TERV.md.md` (F23:11 olvassa, F37:12 írja), nem a `sablonok/`.
6. `F39_…_BRIEF.md:20`: a törzsszöveg változott. *(Orkesztrátori megjegyzés: a „Megjegyzés” szakaszt a felhasználó kérte a címsor alá, a DT-F39g döntésében; nem hiba.)*

## OK pontok
Hatókör (8 fájl); más brief fugg/nem_fugg/olvas/ir változatlan; FELADATOK.md és `.github/` diff üres; a teszt az `eszkozok/teszt_feladatok.py`-ból fut; K2–K5, K8, DT-F39a–e (kód), ⛔ M0-megállás, CLAUDE.md-szabályok, A6 (E2–E16, E19: 0 találat).

## NEM ELLENŐRIZHETŐ (az ügynök szerepe miatt)
K1, K7 (`ellenoriz`, tesztek, CI), a #23/#35/#38 tényleges jelöltlistája, a CI-jelentés egyezése.
