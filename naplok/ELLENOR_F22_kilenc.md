# ELLENOR_F22_kilenc — F22, a kilenc hiányzó kis könyv (origin/main..913f567, ág: claude/youthful-clarke-5h6vk1)

*A független ellenőr (`fuggetlen-ellenor`) jelentése, az orkesztrátor másolta fájlba (az ellenőr nem tud fájlt írni). Eredmény: **ELTÉRÉS: 3 tétel**, mindhárom javítva ugyanezen az ágon; az orkesztrátor mindhárom eltérést saját méréssel is igazolta (a futásnapló `koltseg_usd` oszlopa; a `_munka/*.json` hibaüzenetei).*

## Eltérések

1. **Költség (D43, `kovetkezo`):** a kilenc könyv összege **4,450088 USD**, nem 5,3811 (a futásnapló 99 új sora; a main utolsó `futo_osszeg_usd` értéke 81,494589, az ágé 85,944677). A kumulatív 85,944677 USD helyes. Javítva: 4,4501.
2. **Régi arany (D43, `kovetkezo`):** a kilenc könyvben 7 hármas van, 6 egyezik (Sof 1/1, Hab 1/2, Ámós 2/2, Jóel 1/1, Én 1/1), nem „7/8”. Javítva: 6/7.
3. **Formátumhibás egész köteg:** a Mal, Ámós, Jóel és Sir jelentésének 20. sora tévesen „nincs”-et állított. Négy köteg egésze nem érvényes JSON volt az 1. próbán: Mal k001 (10 vers), Ámós k006 (10), Jóel k008 (3), Sir k009 (10); a javító kör 0-ra hozta. Javítva a jelentésekben és a D43-ban.

## Igazolt pontok (az ellenőr saját lekérdezésével)

- **Versbeosztás:** 797 vers, 44 fejezet; a Károli- és TAHOT-kulcshalmaz azonos; a TAHOT-sorszámok egyeznek a `szavak_*` er-soraival; a Sir 3:13, Sir 5:7, Hag 1:15 tartalmilag megfelel (nem elcsúszás). A jóváhagyási sorok a felhasználó közvetlen ellenőrzésére hivatkoznak, a detektorra nem; hogy a felhasználó valóban ellenőrzött-e, a repóból nem igazolható.
- **Táblák:** séma és proveniencia rendben; `kezi` 0, `+1000` kulcs 0; végleges kapuhiba 0; az `atnezes.tsv` fájlok csak fejlécesek; versösszevonás a kilenc könyvben 0.
- **Költség:** egyik könyv sem érte el a vers × 0,0074 × 1,5 plafont; a batchek soros futása (19:07–20:14 UTC) igazolt.
- **Mal 11/55:** a k001 (10 vers) nem érvényes JSON volt az 1. próbán, a k002-ből csak a Mal 1:14 bukott (kapuszabály 3); mindkettő a 2. próbán 0.
- **Hab 3:10 H8415:** a jelentés leírása pontos (hu „víz” → H4325, „ár” → H2230, „hullám” → H8415; TAHOT-glosszák: water/storm/abyss); a régi arany sora tartalom-alapú, közepes. A `regi_arany_hibas.tsv`-be való felvétel tartalmi döntés, a felhasználóé.
- **Rétegek:** generált fájl, `FELADATOK.md`, `DONTESEK.md`, `f21p/`, `konkordancia/` nem változott; `csv` modul nincs; kulcs-kiszivárgás (`sk-ant-`, `sk-or-`) 0; végleges DT/N szám nincs; a `f22/_munka/` nem került be.

## Nem ellenőrizhető az ellenőr számára

K3 (a `prompt_v3` hash újraszámolása; a futásnapló 99 sorában `84f12ca7aafb`, ugyanaz, mint a main soraiban), K7 (`egyesit.py` újrafuttatása), a teljes gépi `--ellenoriz`, a D36 saját worktree, a CI-jelentés. Az `eszkozok/ellenorzes/futtat.py` E27 hibái (`FELADATOK.md` 18. és 54. sor: „a hivatkozott commit nem létezik”) a sekély klón miatt valószínűleg környezetiek; a diff a `FELADATOK.md`-t nem érinti.
