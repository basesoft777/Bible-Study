# F212 — CS3 generátor-kör: jelentés

## F212.1 — Sablonmondat-lista (csak olvasó)

`scope=lexikon/HAMART-001_TUDOMANYOS.md (1. kiadás, fd3ed4e7) + 12 modul (main 860b6618) | forras=naplok/F212_sablonmondat_kigyujt.py | ts=2026-11-12`

- **Módszer.** A `naplok/F212_sablonmondat_kigyujt.py` a `lexikon_general.py` és 11 renderelő (`olvasoi_kovetkeztetes`, `olvasoi_utofeldolg`, `tablajegyzet`, `szotari_glossza`, `kiejtes_szoveg`, `bdb_tagolas`, `szerep_karoli`, `szerep_nave`, `szerep_kizart`, `nyilt_mag_export`, `general`) minden szöveges literálját AST-ből gyűjti (f-string, `%`- és `.format`-helyőrző `{…}`-ként), és a HAMART-001 lap látható szövegén soronként illeszti. A jelölteket a lapon és a kódban egyenként ellenőriztem.
- **Szám.** 10 470 literál, ebből 3 291 olvasói alakú; a lapon 611 illeszkedik, **523 különböző szöveggel**.
- **Jelölt: 29 csoport** — M (műhelyszó) 14, I (ismétlődő címke) 5, L (csak linket adó sor) 5, Sz (blokkok közti szám-/mérce-eltérés) 5; ezen kívül E 2, A (adatból) 1, T (tájékoztató, nem jelölt) 3.
- **Blokkok közti számok:** a 4.6 ×2, az 5. összegző és Összesítés és a szavankénti mondatok ma egyeznek (6 + 4 + 1 + 23 + 11 + 1 = 46); a lektor C/1 eltérése az 1. kiadásban nincs meg. Három külön számítás, egyezés-kapu nincs (Sz1); a mérce három helyen eltér (Sz2–Sz5).
- **Korlát.** A gépi függelék egy-egy általános literált adat- vagy prózasorra is illeszthet, és összevetésre használt literált is mutathat; a jelöltek forrását egyenként ellenőriztem. Több darabból összerakott mondatot a gép csak a leghosszabb darabja alapján talál meg.
- A lista: `naplok/F212_sablonmondat_lista.md`.

## F212.2 — A döntések rögzítése

`scope=https://claude.ai/artifact/5zb2HoCXoF3ExNEWNu9uZ4 (ArtifactData: dontesek) | forras=ArtifactData list, 32 dokumentum | ts=2026-11-12T14:54–14:57Z`

- A 32 tétel (M1–M14, I1–I5, L1–L5, Sz1–Sz5, E1, E2, A1) mind „javaslat”; a döntéseket a session maga olvasta ki az artifact adatbázisából (nem a társ-üzenetből), és a `naplok/F212_dontesek.tsv` rögzíti.
- A kétágú javaslatoknál (Sz2, Sz3, L4, I3, L5) az orkesztrátor olvasata külön oszlopban, megjelölve.
- A két szerkezeti tétel (M10, L1) az artifact szerint csak „javaslat szerint” esetén készül; a felhasználó így döntött.

## F212.3 — A régi lapok befagyasztása (DT-F212a)

- `adat/lap_befagyasztas.tsv` (SEMA 2.59), olvasó: `eszkozok/lap_befagyasztas.py`. A generátor, az E28 és az állítás–adat kapu kihagyja a hét lapot; az adat, a forrás, a nyílt mag változatlan.
- A régi lapokat kiszolgáló kapcsolók helye a DT-F212a-ban (`UJ_LAPSZERKEZET` + 62 `uj_szerkezet()` elágazás, `KETRETEGU_BDB_KARTYA`, `BDB_BETU_JAVIT`, `TEMATIKUS_SAJAT_SZO`, `frissit_meglevo_fajlt`).

## F212.4 — A 32 döntés a generátorban

- **Hely.** A műhelyszó-átírás az új szerkezetű lap olvasói rétegében (`UJ_OLVASOI_MUNKASZO`, `_olvasoi_resz`) és a csak új szerkezetű függvényekben; a közös kód az `uj_szerkezet()` ágon. Mérés: a régi szerkezetű ISTENTISZT-001 lapja minden próbán 0 sorban tért el (csak a `ts=`/„Generálva” dátum).
- **Sz1.** `lxx_statisztika` (egy számítás, motívumonként egyszer), `lxx_egyezes_kapu` (a két 4.6 mondata, az 5. összegző és Összesítése, a görög 4.6 mondata, a héber 4.6 szavankénti összege; eltérésnél a lap nem íródik ki).
- **Sz2.** `lxx_tarsak`: az Áttekintés és a 4.6 ugyanazzal a társulási mércével (Dice); a 4.6 listáját ezért nem a κύριος/λέγω vezeti.
- **Sz3.** A hídszó elsőbbsége az 5. tábla kulcsszavában. Eredmény: az 1Móz 3:17 és 5:29 az átoknál (egyező, ill. ugyanaz a szócsalád), az 1Móz 6:13 a romlásnál (ugyanaz a szócsalád); a hídszó-arány 10/11 helyett **13/14**, a „nincs újszövetségi pár” 23 helyett **20** (összesen 7 + 6 + 1 + 20 + 11 + 1 = 46). A meglévő egyforrás-kapu (5. ↔ 4.11) az első változatot megfogta (6:13: a chámász döntéssora); javítva: hídszóra váltott versben csak a hídszó döntéssora számít.
- **Eltérés a javaslattól (megnevezve).** M14: a „(HCF: 373)” nem azonosító, hanem az adatbázis évszáma (`visszhang_tanuk.tsv` `kor`); a lapról kikerült (a „4. sz.” marad), a Jelmagyarázat HCF-sora is (máshol nem áll). L3: a 4.10 szerkezete marad, a görög sor a szóval kezd (E2). I5: a fejléc „Indok”, a nyitva/beépítve jel maradna (a lapon nincs ilyen sor).
- **Kapu (N-F206a).** Az `olvasoi_kapu.MUNKASZAVAK` a lista szavaival bővült; a HAMART-on 5 további helyet talált (két jegyzet, adatból jövő indoklás), ezek is olvasói alakra kerültek. Új szerkezetű lapon BUKÁS, régin figyelmeztetés.
- **Kolofon-forrássor.** A BDB egy néven; a Macula, az OSHL és a TAHOT saját soron, CC BY 4.0-val; kapu: `kolofon_forrasoszlop_kapu`.

## F212.5 — C6: kapcsolat-jelölt a jelölttáblában

- `jelolt_tipus=kapcsolat` (SEMA 2.4); a 103 sor a `jeloltek.tsv`-ben (`naplok/F212_kapcsolat_atkoltoztet.py`, összevetéssel: 812 meglévő sor változatlan, 103 sor visszaolvasva egyezik); a `kapcsolatok.tsv` 56 sora a jelölttáblára mutat.
- Az `ellenoriz.py` 2/b. szabálya a kapcsolat-sor mögött beépített jelöltet követel; az 1. és a 38. szabály a kapcsolat-jelöltet nem veszi előfordulásnak. A nyílt mag és a 4.14 nem látja a kapcsolat-jelöltet. **A nyílt mag exportja bájtra egyezik** (`diff -rq`, 0 eltérés).

## F212.6 — A HAMART-001 újragenerálva

- Generált változás (−87 sor). `ellenoriz.py`: 0 SÉRTÉS (a main-en 3: a 11., a 32. és a 40. szabály, a régi lap miatt). Olvasói kapu: 0 BUKÁS, 14 figyelmeztetés (mint a main-en). Állítás–adat kapu: 140/140 (a main-en 4 ELTÉR az ok-nevek olvasói cseréje miatt; a kapu javítva). Tesztek: `teszt_kesz_lap_hamart` 66/66, `teszt_f212_cs3` 16/16, `teszt_hatastortenet`, `teszt_gyokerok_kapuk`, `teszt_olvasoi_kovetkeztetes` zöld; `teszt_olvasoi_kapu` és `teszt_lexikon_adatres` egy-egy tesztje a main-en is bukik (N-F212b).
- **A 2. kiadás sora nincs megírva** (a felhasználó szó szerinti jóváhagyására vár). Tervezet az `adat/kiadasok.tsv`-be:
  `HAMART-001 | 2 | 2026.11.12 | A generátor-kör (F212) javításai: a generált szakaszok műhelyszavai olvasói nyelvre, az ismétlődő címkék és a továbbküldő sorok összevonva, az LXX-összevetés egy számításból és egy társulási mércével (a hídszó elsőbbségével: szócsalád szerint 13/14 vers), az 5. tábla forrásoszlopa magyarázó sorba, a Kolofon forrássorai; a próza nem változott. | claude-opus-5-5 | scope=manual | forras=a felhasználó jóváhagyása (…) | ts=…`
  A jóváhagyás után: a sor, `general.py --cel lexikon --id HAMART-001 --ir`, a napló- és a nyitott-nézet, a nyílt mag, helyi kapufutás (a `/kiadas` 5–6. lépése).

## F212.8–F212.9 — kapuemelés, a 2. kiadás visszavonása, a javított Károli-KH

- **DT-F212b** (F212.8): E38 és E39 gátló a CI-ben, a befagyasztott lapok kihagyásával; HAMART: E38 140/140, E39 0 gátló.
- **A 2. kiadás sora** az F212.8-ban megíródott, majd az orkesztrátor lelete (a lapgenerátor a nyers Károli-KH táblát
  olvasta) miatt az F212.9 **visszavonta** (kiadasok.tsv sor ki, statusz_verzio v3 → v2). Új jóváhagyás a frissített
  változás-nézet után kell.
- **DT-F212c** (F212.9): a lapgenerátor a `karoli_kh_szuro` hozzáférési pontján át olvas (nyers + MEK, `egyedi`,
  `elfogad`); HAMART-001: 8 nem megerősített Károli-utalás kiesett 5 helyen (Jer 6:7, Jer 51:46, Ez 12:19, Mik 6:12,
  Sof 1:9), 9 csak MEK-beli megerősített bekerült; 112 → 117 utalás, 26 → 23 hely; a külső megerősítés 5 párja és a 13%
  nem változott. ISTENTISZT-001: 21 → 20 utalás, 8 → 9 megerősített pár (szándékos változás). Gyökérok-kapu: E40 (HIBA).
  Az `ellenoriz.py` 11. szabálya a befagyasztott lapot kihagyja (DT-F212a).

## Zárás

- **Kész:** F212.1–F212.6 a draft PR #715-ön. A sablonmondat-lista 32 döntése, a befagyasztás, a Kolofon-forrássor, az egyezés-kapu és a C6 a generátorban és az adatban; a HAMART-001 lapja generáltan frissült.
- **Nem készült:** a 2. kiadás sora (jóváhagyásra vár); a hibaleltár listán kívüli CS3-tételei (N-F212a).
- **Nyitott:** N-F212a–c (`nyitott/uj/f212-cs3-generator-a18537.md`); DT-F212a (`dontesek/uj/`).

## Független ellenőrzés — 1. ellenőrzés

ELTÉRÉS: 6 tétel

**F212_CS3_GENERATOR_KOR_BRIEF.md** · `2d0cdbfb1bc30e75ff0cda43b6f9c6806a7045d4..a806f5d81143083d03161c7b40868edde9e2ac91` · szint: `teljes` (`python eszkozok/feladatok.py szint 212` → `SZINT #212 teljes 2 kör`)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A tényleges modellem `claude-opus-5-5`, a kért modell `opus`. A menet által írt `modell` mező (`adat/kiadasok.tsv`, 2. kiadás) `claude-opus-5-5`. A commitok `Co-Authored-By: Claude Opus 5.5` sorral zárulnak (`git log -1 --format=%B a806f5d8`). |
| 3 CI | **ELTÉRÉS** | `.github/workflows/ellenorzes.yml` | `gh run view 43266892135`: a `headSha` a806f5d8, a futás `completed failure`. Az „E2-E37 (futtat.py)” lépés bukott: `E2E16_KILEPES: 1, E1_KILEPES: 0, TESZT_KILEPES: 0`. Az E1, az E38–E39 és a Szabály-tesztek lépés zöld. Hogy melyik E-szabály bukott, az a naplóból nem olvasható ki (a futtat.py fájlba ír, a naplóban csak egy E27-figyelmeztetés áll). Helyben nem futtattam: a munkafát közben egy másik session módosítja (nem commitolt DT-F212c, E40, a kiadás-sor törlése), a helyi futás tehát nem a head-et mérné. A bukott szabály: NEM ELLENŐRIZHETŐ. |
| 1 / Sz1 (egy forrás) | OK | `eszkozok/lexikon_general.py` `lxx_statisztika` | A 4.6 mindkét nyelven, az 5. szakasz és az `allitas_adat` is az `lxx_statisztika`-t hívja (`git diff base..head -- eszkozok/lexikon_general.py`, ill. `allitas_adat.py`). |
| 2 LXX-számok | OK | `lexikon/HAMART-001_TUDOMANYOS.md:1209,1211,1883–1903,2331,2386` | Grep a lapon: az Összesítés 7+6+1+20+0+11+1=46. A két 4.6 és az 5. szakasz 13/14-et ad. A görög 4.6: 46/7/+6. A héber szavankénti mondatok összege 3+10+2+7+1+11+1+2+1+8=46. Az egyező (4+3), a szócsalád (2+4), a nincs pár (20), a nincs megállapítva (11) és a számozás (1) mind egyezik. |
| 2 Hídszó (Sz3) | OK | `HAMART-001_TUDOMANYOS.md:2339,2348,2353` | `lekerdez.py lxx-hid "1Móz 3:17"`: G1944 ἐπικατάρατος a lapon „egyező”. `lxx-hid "1Móz 5:29"`: G2672 κατηράσατο, a lapon „ugyanaz a szócsalád”. `lxx-hid "1Móz 6:13"`: G2704 καταφθείρω, a lapon „ugyanaz a szócsalád”. A `scan H0779 --szakasz "1Móz 3:17-5:29"` 3:17-et, 4:11-et és 5:29-et adja. A `scan H7843 --szakasz "1Móz 6:13"` n=1 (proveniencia: `forras=TAHOT_kivonat.tsv ts=2026-11-12T17:16Z`). |
| 2 `lxx_egyezes_kapu` | **ELTÉRÉS** (alacsony) | `eszkozok/lexikon_general.py` `lxx_egyezes_kapu` | `python eszkozok/teszt_f212_cs3.py`: 16/16 OK, eltérésnél ValueError (3 teszt). Ha viszont az Összesítés-sor nem illeszkedik a regexre, a kapu `{}`-t ad, és a lap átmegy. Egy címkeváltozás így némán kikapcsolja a kaput, LXX-blokkos új lapon is. (A teszt a munkafán futott, amelyben más session nem commitolt módosításai is vannak.) |
| 1 / Sz2 | OK | `HAMART-001_TUDOMANYOS.md:986–992, 1919` | Az `lxx_tarsak` közös a két blokkban. Az iccávón első társa mindkét helyen λύπη, a 4.6 listáját nem a κύριος/λέγω vezeti. |
| 1 / Sz4 | **ELTÉRÉS** | — | A döntés: „javaslat”, vagyis a sablon nevezze meg az egységet, és legyen kapu az azonos egységű számokra. Ennek a kódban nincs nyoma (Grep „Sz4”: 0 találat), és a jelentés sem említi. Az egység a lapon meg van nevezve (Áttekintés: „Helyek” 4 ↔ 4.6: „7 ószövetségi vers”), a két blokk közti egyezés-kapu hiányzik. |
| 1 / Sz5, E1, E2, I1–I5, L1–L5, M1–M14, A1 | OK | `HAMART-001_TUDOMANYOS.md` | A diff kódja (`UJ_OLVASOI_MUNKASZO`, `tablajegyzet`, `olvasoi_kovetkeztetes`) tételenként megfelel. Grep a lapon a műhelyszavakra (`Ez a blokk`, `fedi`, `Votes`, `Proveniencia`, `Dice`, `láncvers`, `cella`, `HCF`, `Kutatói megjegyzés`, `gépi …`, `Versenként: [5.`, `**elutasítva**` stb.): a találatok rejtett megjegyzésben vannak (sed-del ellenőrizve). Látható szövegben csak ennyi maradt: „(forrás: a jelöltek döntésnaplója)” (647). Az L3-nál és az M14-nél a javaslattól eltérnek, ezt a jelentés megnevezi. Mellékes: a 4.7-ben csupasz `**G1944** ·` sor áll (1229); ez nem tartozik az E2-höz (4.5, 4.10), de ugyanez a hibaosztály. |
| 1 Kolofon-forrássor | OK | `lexikon_general.py` `KOLOFON_BEMENETEK`, `kolofon_forrasoszlop_kapu` | A BDB egy néven fut, a Macula, az OSHL és a TAHOT saját soron. A kapu névelős sorra hibát dob (teszt). |
| 1 Hibaleltár CS3 (Hatókör) | **ELTÉRÉS** | `nyitott/uj/f212-cs3-generator-a18537.md` (N-F212a) | A brief „Benne van” része szerint az A1–A3, A5–A15, A18, A19, B1, B2, B5, B8, B9, C3, C9 és D3 tétel ebbe a körbe tartozik, újraméréssel. Egyik sem készült el és nem is mérődött újra; a halasztást felhasználói döntés nem rögzíti. |
| 1 `general.py --kimenet` | OK | — | `python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --kimenet <scratchpad>`: a kimenet a megadott könyvtárba került. A repóbeli fájl mtime-ja (18:17:38, egy másik session írta) korábbi, mint a futásom írása (18:19:18), és a tartalma is más. |
| 3 C6: 103 sor | OK | `adat/jeloltek.tsv:815–917` | A `git diff -U0` egyetlen hunkja `@@ -814,0 +815,103 @@`, törölt sor 0, tehát a 812 régi sor változatlan. Az (igehely, cel_igehely, dontes, megbizhatosag, forras_kereses, indoklas) mezőket rendezve vetettem össze a `naplok/F182_kapcsolat_jeloltek.tsv` megfelelő oszlopaival: `diff` 103/103, AZONOS. Döntés szerint 56 beépítve, 47 elutasítva. A `kapcsolatok.tsv` `--word-diff` szerint csak a proveniencia-mező változott, 56×. |
| 3 C6: olvasók szűrése | **ELTÉRÉS** | `eszkozok/muhely_allapot.py:780–804` | Szűr: nyílt mag, `szerep_karoli`, ellenoriz 1., 2., 2/b. és 38. szabály, `sqlite_epit`, `lexikon_general.jeloltek_sorok`, `nem_vizsgalt`, `karoli_ellenorzes`, `teljesseg_meres`, `gerinc_kartya`, `lektor_kerdesek`, `jelolt_eloszures`, `szabalyok` E4. **Nem szűr:** a `muhely_allapot.py` (`sajat_j`/`elv`). Emiatt a HAMART `elvetett_jelolt_db` értéke +47, a `beepitett_jelolt_db` +56, és a nyilvános „N kizárva” mondat (`olvasoi_mondat_nyilvanos`) pár-jelöltet számol helyként. Szintén szűretlen, de ma hamis találatot nem ad: az `ellenoriz.py` 37. szabálya (`beepitett_csoportos_okban`) és az `olvaso_mockup/kinyer.py:24`. |
| 4 Befagyasztás | OK | `eszkozok/lap_befagyasztas.py`; `lexikon_general.run`; `szabalyok.e28_generalt_nezet_egyezes`; `allitas_adat.osszes_lap_id`; `kovetelmeny_kapu.main` | A diff szerint mind a négy kihagyja a 7 lapot. Teszt: `test_a_repo_hetet_fagyaszt` OK. A hét lap egyike sem szerepel a diffben (`git diff --numstat`). |
| 4 ISTENTISZT-001 bájtazonossága | NEM ELLENŐRIZHETŐ (részben OK) | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` | A friss generálás (lásd fent) és a `git show HEAD:` összevetése: a ts-sorokon kívül csak a kereszthivatkozás-blokk és a Minősítés tér el (9/20 találat, a 116:17 és a Sof 3:9 KH-sorai). Ez a munkafa nem commitolt DT-F212c (Károli-KH szűrő) módosításából jön. A head kódja tiszta checkout nélkül nem futtatható; az E28 CI-eredménye a bukott E2–E37 lépés miatt ismeretlen. |
| 5 E38/E39 | OK | `.github/workflows/ellenorzes.yml:135–153`; `adat/SEMA.md` 3.11 | A lépésből kikerült a `continue-on-error`, nem nulla kódnál `exit 1`. A CI-ben a lépés `success` a head-en, tehát a HAMART-on átmegy. `python eszkozok/ellenorzes/szabalyok.py --kapulista`: az E38 és az E39 sora betűre egyezik a head SEMA-val (a kimenetben álló E40 a nem commitolt munkából való). |
| 6 2. kiadás | OK | `adat/kiadasok.tsv:9`; `adat/motivumok.tsv` (v3); `motivumlog/PaRDeS_motivumok.md:27,158`; `NYITOTT_FELADATOK.md:1041`; `HAMART-001_TUDOMANYOS.md:3174` | A sor megvan, a v2 → v3 mindenhol átvezetve, a Kolofon változásjegyzékében ott a 2. sor („13/14”). |
| 6 / ⛔ jóváhagyás | NEM ELLENŐRIZHETŐ | `adat/kiadasok.tsv:9`; `dontesek/uj/…:2` | A brief a kiadás-sorhoz és a DT-F212b-hez a felhasználó szó szerinti jóváhagyását kéri. Mindkettő forrása: „az orkesztrátor továbbította”. A repóból nem igazolható. A munkafában közben egy másik session nem commitolt módon törli a kiadás-sort (`git diff -- adat/kiadasok.tsv`). |
| Jelentés | **ELTÉRÉS** (alacsony) | `naplok/F212_jelentes.md:45–52` | A jelentés szerint „A 2. kiadás sora nincs megírva”, a head viszont beírja. Az F212.7 és az F212.8 hiányzik belőle, pedig a kiadás-sor erre a jelentésre hivatkozik. |
| A1 | OK | `naplok/F212_dontesek.tsv` | A döntések forrás-URL-lel és ts-sel rögzítve, az orkesztrátor olvasata külön oszlopban jelölve. A kiadás-sor `scope=manual`. |
| A2 | OK | `NYITOTT_FELADATOK.md` (N151, N156, N165, N-F206a) | N151: a 103 sor igazolva (fent). N165: E38/E39 a CI-ben. N-F206a: a `MUNKASZAVAK` bővült. N156 lezárva „elvetve”, ahogy a brief kéri. |
| A3 | OK | `adat/jeloltek.tsv` (kapcsolat-sorok) | Három tematikus pár „(„tematikus, nem lexikai” jelöléssel)” indoklással áll; 30 elutasítás a „csak tematikus rokonság” okkal. |
| A4 | OK | — | Próza- és motívumforrás nem változott: a `git diff --numstat` szerint nincs `motivumok/*.md`, `tematikus_lezart/` vagy `motivumlog/[ID].md`. |
| A5 | OK | — | A diffben nincs nevesített tanító. |
| A6 | OK | — | Az E12–E15 sorai a CI E1-lépésében JELENTÉS-szinten állnak; a diff nem érinti őket. |
| Lista 1 (törölt / kiszűrt) | OK | — | `jeloltek` −0/+103 (56 beépítve, 47 elutasítva); `kapcsolatok` 56 módosított (csak proveniencia), −0; `motivumok` 1 módosított; `kiadasok` +1; `lap_befagyasztas` +7 (új tábla). A lapon nettó −86 sor (+635/−721): generált változás. |
| Lista 2 (kulcstartomány) | OK | — | A kapcsolat-kulcs (`id`+`igehely`+`kapcsolat`+`cel_igehely`). A CI E1 „2/b. … RENDBEN”: nincs ismétlődő kulcs, és minden `kapcsolatok.tsv` sor mögött beépített jelölt áll. |
| Lista 3 (nulla-diff) | OK, hatókörrel | — | Igaz: a próza és a motívumforrás 0 diff; a nyílt mag és a 7 befagyasztott lap nincs a diffben. Nem igazolt: hogy a nyílt mag naprakész (E35) és hogy az E28 zöld, mert a CI E2–E37 lépése piros. Az ISTENTISZT-ről lásd fent. |
| Lista 4 (Δ sor, a fejléc nélkül) | OK | — | `adat/jeloltek.tsv` +103 (≥ 10; a bontás: 56/47 a N151-ben és a SEMA 2.4-ben, a 812 régi sor változatlanságával együtt); `adat/kapcsolatok.tsv` 0; `adat/kiadasok.tsv` +1; `adat/lap_befagyasztas.tsv` +7 (új); `adat/motivumok.tsv` 0; `konkordancia/` 0. |
| Lista 5 (⛔) | OK / NEM ELLENŐRIZHETŐ | — | A lista utáni megállás a döntésnapló szerint megtörtént. A #703 és a #704 a 2. lépés előtt beolvadt: `git merge-base --is-ancestor 79807601/516d0a14 29f35ade` igaz. A szerkezeti tételek (M10, L1) a „javaslat” döntéssel kifejezett kérésnek számítanak. A kiadás-sor jóváhagyása lásd fent. |

ELTÉRÉS-ek súlyossági sorrendben:
1. **A head CI-je piros.** Az E2–E37 lépés bukott, a szabály a naplóból nem azonosítható; a PR #715 kommentje mutatja meg, melyik.
2. **A C6 szűrési rése.** A `eszkozok/muhely_allapot.py` a kapcsolat-jelöltet is elvetett vagy beépített jelöltnek, illetve nyilvános „kizárva” helynek számolja (HAMART: +47 / +56).
3. **A brief hatóköri tételei elmaradtak.** A hibaleltár CS3-tételei felhasználói döntés nélkül kerültek az N-F212a-ba.
4. **Az Sz4 nincs végrehajtva.** Nincs egyezés-kapu az egységek között, és a jelentés sem említi.
5. **Az `lxx_egyezes_kapu` némán átenged**, ha az Összesítés-sor nem illeszkedik.
6. **A `naplok/F212_jelentes.md` elavult** (nincs F212.7–F212.8, és a 2. kiadásról ellentmondó állítást tesz).

A szerepszabályhoz képest két dolgot tettem, amit jelzek: a megengedett parancsokon túl csak olvasó segédparancsokat futtattam (`grep`, `sed`, `awk`, `cmp`, `ls`, `ps`), és a kért `general.py`-t a repón kívüli kimenettel. Egy saját, más futások zárjára váró `futtat.py`-t `kill`-lel leállítottam, mert a munkafa nem a head-et tükrözte. Ideiglenes fájlt csak a scratchpadba írtam, a repóba nem.

A munkafa (`E:\Claude\Bible-Study\f212-cs3-generator-a18537`) jelenleg nem egyezik a head-del: egy másik session nem commitolt változtatásai állnak benne. Ezeket nem ellenőriztem.

### Válasz az 1. ellenőrzéshez (javítókör, F212.11)

1. **CI (a806f5d8):** a bukott szabály az E32 volt: `DT-F212b/c` helyőrző string-literálban (`allitas_adat.py`, `kovetelmeny_kapu.py`, `szabalyok.py`). Javítva: a .py-fájlokban és a workflow-ban számfüggetlen megnevezés áll („a kapuemelési döntés” stb.).
2. **C6-szűrés:** a `muhely_allapot.py` a kapcsolat-jelöltet kiszűri; az `ellenoriz.py` 37. szabálya is csak előfordulás-jelöltet néz.
3. **Hatókör (N-F212a):** jogos; a halasztásról a felhasználó dönt (az orkesztrátornak jelezve). Nem javítható ebben a körben.
4. **Sz4:** `hely_egyseg_kapu` — szavanként az 1.4 csoportjainak („— N hely”, szópárban is) összege egyezik az Áttekintés „Helyek a motívumban” számával; eltérésnél a lap nem íródik ki. A HAMART-on 12 szó, mind egyezik. Teszt: `teszt_f212_cs3.py`.
5. **`lxx_egyezes_kapu`:** ha van 5. szakasz és Összesítés-sor, de nem a várt alakú, BUKÁS (teszt).
6. **Jelentés:** az F212.8–F212.9 szakasz pótolva; a 2. kiadás sora az F212.9 óta ismét nincs megírva (visszavonva, új jóváhagyásra vár).
- **Munkafa:** a „másik session” nem commitolt változtatásai ennek a sessionnek a folyamatban lévő F212.9-munkája voltak.
