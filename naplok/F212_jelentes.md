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
