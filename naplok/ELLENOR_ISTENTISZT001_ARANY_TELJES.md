ELTÉRÉS: 3 tétel

# ELLENOR_ISTENTISZT001_ARANY_TELJES

*A `fuggetlen-ellenor` jelentése, a végrehajtó mentette (az ellenőrnek nincs fájlíró eszköze). A táblázat az eltérés- és lényegi sorokat a jelentés szerint adja, rövidítve; a végén a javítókör a végrehajtóé.*

- **Megbízás:** a DT-F131q (`DONTESEK.md` utolsó sora) és az N-F131f; nincs külön brieffájl.
- **Tartomány:** `0e607b2f..1692c56f` (6 commit).
- **Ellenőr:** a tényleges modell `claude-opus-5-5`, a kért modell `opus`, tehát egyezik.
- **Korlát:** az ellenőr a szerepe szerint a `naplok/*.py` mérőszkripteket és a `teszt_bont`-ot nem futtathatta. Ezeket a pontokat NEM ELLENŐRIZHETŐ-nek jelölte, és fájlolvasással, Grep-pel egészítette ki.

| pont | eredmény | fájl:sor | indok |
|---|---|---|---|
| DT (1) 2Móz 33:19, 34:5; Jer 10:25, Zsolt 79:6, Ézs 64:6 | OK | `adat/elofordulasok.tsv:37-41` | Az értékek a döntés szerintiek. A többlet a `funkcio` mezőben megvan: „B-eset”, „tagadó forma”. |
| DT (1) 1Kir 18:24 | OK | `:17`; `adat/forditasok.tsv:3` | Szó szerint egyezik a BDB-fordítással, csak a ׳י áll feloldva. |
| DT (1) 1Kir 18:25–26, `jelentes_en` | OK (megjegyzéssel) | `adat/bdb_szakaszok.tsv:29941-29942` | A „Baál nevével” és a „with name of Baal” BDB-szöveg. A 18:24 `jelentes_en`-jéből elmaradt a BDB vezető „of”-ja, a ׳י feloldva áll. Ez a menet előtti érték. `lekerdez.py scan H7121 --szakasz "1Kir 18:24-26"` → 3 hely (`ts=2026-10-29T11:20Z`). |
| DT (2) `jelentes_szam` | OK | `:21,37-39` | 7 sor, 10 mező, más mező nem változott. |
| DT (3) szabály | OK | `eszkozok/bdb_jelolt/hu_illeszt.py:97-101,143` | Valódi jelölőt dobó esetet nem talált. Grep: 395 `^[ivx].`-találat a `forditasok.tsv`-ben, mind bibliográfia. |
| DT (3) minta | OK | H8034, H8040, H3808, H6035, H7356 | Mind javítás; az angol szakaszok igazolják. |
| DT (3) a szkript számai | NEM ELLENŐRIZHETŐ | `naplok/ISTENTISZT001_siglum_hatas.py` | Az „54 Strong, 3 sor rontás” állítást egyik szkript sem reprodukálja (E1). |
| a „6 jelölő nélküli szakasz” | **ELTÉRÉS (E2)** | `DONTESEK.md:467` | A két Strongnak 8 `jelolo_nelkul` sora van. A kiválasztás szempontja nincs megadva. |
| lexikonlap | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:116,122,123,125` | Csak a 4 minősítő-mondat esett ki. Helyőrző: 0. |
| N-F131f számai | részben OK / **ELTÉRÉS (E1)** | `NYITOTT_FELADATOK.md:54` | A 9 664 / 674 / 3 326 rendben. A mezőszintű számok és a „H7121/H8034 nem érintett” állítás nem reprodukálható a hivatkozott szkriptből. |
| helyőrző az `eszkozok/` alatt | OK | – | 0 találat. |
| helyőrző a `naplok/*.py` alatt | **ELTÉRÉS (E3)** | `naplok/ISTENTISZT001_nf131ab_rendezes.py:1`, `naplok/ISTENTISZT001_teljes_meres.py:1` | N-F131a/b maradt a docstringben; a számkiosztás `.py`-ban nem cserél. |
| CI (saját futtatás) | OK | – | A `futtat.py` kilépési kódja 0. JELENTES: E12 357, E13 119, E25 4, E27 40 (main-szintű). E30 1 FIGYELMEZTETES: a `funkcio` mezőnév a 96aeed6f üzenetében. |
| A1–A6, a ⛔-pontok | OK | – | A generátor és a `bdb_szakasz_hu.tsv` nem változott; csak ISTENTISZT-001 sorok változtak. |

## Javítókör (végrehajtó, 2026-10-29)

1. **E1:** a `naplok/ISTENTISZT001_siglum_hatas.py` mostantól kiírja a tábla elavultságának mezőszintű számait és a H7121/H8034 érintettségét. A két elvetett változatot `--tag` és `--betus` kapcsolóval reprodukálja. Kimenet:
   - **végleges:** 9 Strong, 20 sor, rontás 0;
   - **`--tag`:** 54 Strong, 182 sor, **73 sor rontás 13 Strongban**;
   - **`--betus`:** 16 Strong, 34 sor, 3 sor rontás (H7442);
   - **elavultság:** 674 → 4 000 Strong, 9 664 → 25 228 sor, 3 326 új, 98 eltérő Strong; mezőnként `forditas_forras_hash` 1 685, `hu_kezdet` 1 388, `szoveg_hu` 1 362, `hu_hossz` 1 315, `kategoria` 184, `horgony` 22; a H7121 és a H8034 nem érintett.

   Az ellenőr gyanúja tehát helyes volt. A DT-F131q „54 Strong, 3 sor rontás” állítása két változatot mosott össze, ezért a sor javítva: az első változat 54 Strong / 73 sor rontás, a második 16 Strong / 3 sor rontás.
2. **E2:** a DT-F131q (3) pontja kimondja a kiválasztást. A 6 szakasz a 8 `jelolo_nelkul` sorból azok, amelyeknek nincs saját magyar szövege; a két sorszám-2 `fej` sor saját magyar szakaszt kap.
3. **E3:** a helyőrző kikerült a két szkript docstringjéből. Ugyanígy javítva a #506-os `naplok/ISTENTISZT001_arany_javitas_meres.py:3` is. A régebbi `naplok/F131_*.py` DT-F131-hivatkozásai a main-en is megvannak, ezekhez a menet nem nyúl (a PR felsorolja).
4. **A `teszt_bont`, nem futtatott pontok:** a végrehajtó futtatta.
   - `test_kotetszamos_siglum`: OK.
   - `HuIlleszt.test_ellenoriz` és `test_osszefuzo_a_mai_adaton_valtozatlan`: bukik, a tábla elavultsága miatt (N-F131f, a következő menet).
   - `Determinizmus` két tesztje: bukik. A `bont.py`-t és a `forras_javit.py`-t futtatja, és egyik sem olvassa a változott fájlokat.
5. **Nulladiff a teljes lexikonon** (az ellenőr nem futtathatta): azonos generátorral, a régi (977b813c) és az új `elofordulasok.tsv`-ből 8 lapot generáltam. Csak az ISTENTISZT-001 tér el. A többi lap a main-en is eltér a mai generátorkimenettől; ez korábbi, a menettől független elavultság.
