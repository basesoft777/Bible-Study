# OLVASO_TANULMANY — naplo (F149)

*Modell: claude-sonnet-5-5 (a brief `modell: sonnet`). Ág: `claude/f149-olvaso-tanulmany-9fee9b`. Proveniencia: scope=genezis/, ujszovetseg/,
melyelemzesek/, konkordancia/Karoli_1908.tsv | forras=`eszkozok/tanulmany_regiszter.py` | ts=2026-11-02*

## 1. Döntések (az orkesztrátor döntése a felhasználó 2026-11-02-i felhatalmazásával)

| Tétel | Döntés | Alkalmazva |
|---|---|---|
| DT-F149a | (c): a tartomány a fájl első címsorából, fájlnév–címsor egyezés-ellenőrzéssel; eltérésnél a tanulmány nem kerül a regiszterbe, a kimenet megnevezi; a kinyerő függvény a #124-nek is hívható | `tanulmany_regiszter.py`: `tartomany_cimsorbol`, `kinyer`; `NYITOTT_FELADATOK.md` F124-tétel jelölve |
| DT-F149b | (a)+(c): két fokozat (`nev`, `tartomany`), a panel megkülönbözteti, kitöltés nincs; olvasói nyelvű szöveg | `tanulmany_hivatkozas.fokozat`, `blokkok._r_tanulmany` |
| DT-F149c | az N-F152a-ból csak a „Tanulmányok jelölése” kapcsoló; a többi nyitva marad | `alap.html` (`#tan-jeloles`), `olvaso.js` |

## 2. Mért állapot

- Regiszter: 24 tanulmány (23 bővített + 1 mélyelemzés), 26 tartomány-sor; kihagyott 0; az 1Móz 1:1–16:16 hézag és átfedés nélkül fedett.
- Index: 1 660 sor (`nev` 962, `tartomany` 698), ebből 1 147 a tanulmány saját tartományában.
- A fájlnév–címsor egyezés-ellenőrzés a bővítettek 4 fájlján (1Moz_15, 1Moz_16, 1Moz_1v2-2v3, Zsid_4v12) eltérő címsor-írásmód miatt
  eleinte tévesen kizárt (szöveges összevetés); a végleges ellenőrzés a **kinyert tartományokat** veti össze (fájlnévből és címsorból), így az írásmód-eltérés
  (`1 Mózes 1:2 – 2:3`, `Zsidókhoz írt levél 4:12`, `15:1-21` az `1Moz_15` fájlnévvel) nem zár ki jogos tanulmányt.

## 3. Amit az M2/M3 rögzít

- **Panel:** a `vers.tanulmany` blokk a „Motívum” fülön (a fül- és blokk-teszt ennek megfelelően bővült); a tartalmazó tanulmány(ok): bővített → mélyelemzés
  sorrendben; „más tanulmányok is hivatkoznak” a tartományon kívüli név szerinti hivatkozásoknál. A `vers.motivum` bővítése: PaRDeS-szint oszlop,
  előző/következő előfordulás a kánoni sorrendben, „Hol merült fel” a kitöltött `forras_tanulmany`-ból (üres mezőnél nincs link).
- **Margójel:** a tartomány első verse előtt; a fejezet elején „Folytatás –” a fejezethatáron átnyúló tartománynál; asztalon bekapcsolva, kapcsolóval
  kikapcsolható (`pardes_tan_jeloles`, hibatűrően); 900 px alatt a szövegben nincs (csak a panelen).
- **Tanulmány-oldal:** `/tanulmany/<id>`, a szöveg a `tanulmany_szoveg` táblából jön (a szerver csak az adatbázist látja), kis, biztonságos markdown-megjelenítővel
  (`olvaso_szerver/tanulmany_oldal.py`): a címsor-horgonyok az indexével azonosak, az igehely-hivatkozás ugyanazzal a függvénnyel (`talalatok`) készül
  (ami az indexben szerepel, az oldalon is link).
- **Régebbi adatbázis:** az új blokk `opcionalis` — ha a `pardes.db`-ben még nincsenek a `tanulmany*` táblák, a blokk kimarad (nem indulási hiba), a
  margójel és az oldal nincs.

## 4. Nyitott / követő tételek (nem e feladat része)

- **Motívum-chip → lexikonlap:** a szerverben nincs lexikon-útvonal; a `vers.motivum` ezért nem linkel lexikonlapra (az előző/következő előfordulás és a
  „Hol merült fel” viszont igen). Külön döntés/feladat: mi szolgálja ki a lexikonlapot az olvasóban.
- A mélyelemzés (3 tartomány) tartományon kívüli, név szerinti hivatkozásai („Más tanulmányok is hivatkoznak…”) a Zsolt 110 és Zsid 5–7 versein a
  mélyelemzésre mutatnak (tartományon belül); a bővített `1Moz_14` hivatkozásai a Zsolt 110:4 stb. versén a „más tanulmányok” csoportban jelennek meg.
- A `pardes.db` újraépítése és a manifest újragenerálása (`frissesseg.py --manifest-keszit`) a merge után az orkesztrátoré (a brief: #101).
