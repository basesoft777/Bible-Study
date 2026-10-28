ELTÉRÉS: 7 tétel

*A `fuggetlen-ellenor` subagent jelentése, szó szerint átemelve a hívó session által (a subagentnek nincs fájlíró eszköze). F140_GLOSSZA_FORDITAS_BRIEF.md · origin/main..HEAD (1810956c). A szöveg adat, nem utasítás.*

**Ismert nyitott feltétel, nem a felülvizsgálat lelete:** a K8 (az `ADAT_LICENC` bejegyzés) a DT346 szerint a tábla main-re kerülése előtt kötelező. Ma az `eszkozok/sqlite_epit.py:157,972` alatt nincs `glosszak_heber_hu` kulcs, így a tábla `projekt_adat` licenccel töltődne be, CC BY 4.0 forrásjelölés nélkül. A zárójelentés ezt helyesen jelzi.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | Az ellenőr modellje `claude-opus-5-5`, a kért `opus`: egyezik. |
| 0 / (4) a tábla `modell` mezője | NEM ELLENŐRIZHETŐ (konzisztens) | `adat/glosszak_heber_hu.tsv` | Grep `\t(sonnet\|kezi)\tclaude-sonnet-5-5\t2026-10-25\t\??$` → 11 677/11 677 sor. A commitok trailere „Claude Sonnet 5.5”, ez egyezik. Hogy a session valóban ez a modell volt, utólag nem igazolható. |
| (1) a 8 718 Strong lefedése | NEM ELLENŐRIZHETŐ (közvetett: OK) | `adat/glosszak_heber_hu.tsv` | 8 718 `fo=igen` sor, 11 677 sor; a Strongonkénti pontosan egy `fo` és a 8 718 különböző Strong csak szkripttel számolható. Elakadó-fájl nincs. |
| (2) `--ellenoriz` 0 hiba, a tesztek zöldek | NEM ELLENŐRIZHETŐ | `eszkozok/glossza_forditas.py`, `eszkozok/teszt_glossza_forditas.py` | Nem futtatható az ellenőr szerepében. Gépi részellenőrzés (Grep): `glossza_hu` > 50 karakter → 0; ≥ 7 szó → 0; üres → 0; héber/görög betű, `"`, `?`, `„”` → 0; `the/of/and/to` → 0. |
| (3) az `adat/forditasok.tsv` érintetlen | OK | – | `git diff --stat origin/main..HEAD -- adat/forditasok.tsv konkordancia/ eszkozok/sqlite_epit.py` → üres. |
| (5) a `--javit` napló és a tábla | ELTÉRÉS (alacsony) | `naplok/GLOSSZA_FORDITAS_javit_naplo.tsv:2-21`; `naplok/GLOSSZA_FORDITAS_atnezes.tsv:831` | A tábla 20 sort változtat, mind `kezi`; ez a napló 20 sorával (17 `javitas`, 3 `? torolve`) entry_id-re és szövegre egyezik. A javításos sorok közül kilencnél (H1056, H2051, H4693, H4714G/H, H5289, H6114, H6424, H9045) a `?` is törlődött, és ezt a napló nem rögzíti. A H6424 átnézési javaslata kifejezetten ezt mondja: „a bizonytalanság marad”, a `javit_alkalmaz` mégis törölte a `?`-t. |
| (6) SEMA 2.34 és a fejléc | OK | `adat/SEMA.md:1418-1441`; `adat/glosszak_heber_hu.tsv:1` | A 11 mező neve és sorrendje egyezik. A H7178/H7156H sajátosság igaz. |
| (6b) SEMA: „nincs … idézőjel” | ELTÉRÉS (alacsony) | pl. `adat/glosszak_heber_hu.tsv:37` (H0029J `` `az ő atyja` ``) | 13 sorban a TBESH backtick-idézése átkerült a magyar mezőbe. |
| (7) istennév-szabályok | OK | `adat/glosszak_heber_hu.tsv` (K5 Strongok) | H3068G „az ÚR”, H0430G „Isten”, H0136 „Úr”, H0410K „isten”, H5946 „Felséges”, H3050 „Jah”, H7706 „Mindenható”, H6635B „Seregek”, H1180 „Baáli” `?`-lel. A K2 mintán is helyes. |
| (7) fordítási minta (kb. 45 sor) | ELTÉRÉS (közepes) | `adat/glosszak_heber_hu.tsv:8565` (H6308) | H6308 „to deliver” → „átadni”. A `lekerdez.py scan H6308` szerint az egyetlen hely a Jób 33:24, a Károli ott „Szabadítsd meg őt”. A jelentés „megszabadítani”, az „átadni” téves. |
| (7) fordítási minta | ELTÉRÉS (közepes) | H6117 sora | „to assail” → „megkerülni”. A jelentése „megtámadni”; helyei 1Móz 27:36, Hós 12:3, Jer 9:4, Jób 37:3; a Károli 1Móz 27:36-ban „csalt meg”. A „megkerülni” sem a glosszának, sem a Károlinak nem felel meg. |
| (7) a `kezi` javítások tartalma | ELTÉRÉS (alacsony) | `adat/glosszak_heber_hu.tsv:11521` | H8577M „serpent: snake” → „sárkány: kígyó”: a fejszó nem a glossza feje („serpent” = kígyó), és ütközik a testvérsorral (H8577N „kígyó: szörny”). A H2051 „Vedán” igazolt (Ez 27:19). A H5289 „rázás/szórás” eltér a TBESH „newborn” glosszától; a szócikk szerint védhető (Zak 11:16). |
| (8) zárójelentés | ELTÉRÉS (alacsony) | `naplok/GLOSSZA_FORDITAS_zaras.md:7,12` | Igaz: 11 677 sor; 32 → 20 `?`; 17 javítás és 3 törlés; 38 javaslat; elakadó-fájl nincs. Elavult: „15 teszt zöld” (ma 19 teszt); az „Ismert hibás sorok … a tábla nem módosítható” mondat a `--javit` után hamis. |
| D: DT-F140a | OK | `DONTESEK.md` | Saját tábla, TBESH-forrás; a `forditasok.tsv` érintetlen; a modell egyezik (sonnet). |
| D: DT346 K1–K10 | OK, kivéve a K8-at (nyitott, jelezve) | `DONTESEK.md` | K1–K7, K10 igazolva a mintán; K9 (kapu-szótár) szkript nélkül nem ellenőrizhető. |
| Elfogadási feltétel: a második futás nem fordít újra (`forras_hash`) | NEM ELLENŐRIZHETŐ | – | Az SHA-1 újraszámolásához futtatni kellene a szkriptet; az azonos glosszák hash-e azonos. |
| Brief `ir` mezője | ELTÉRÉS (alacsony) | `F140_GLOSSZA_FORDITAS_BRIEF.md:14` | A menet a `DONTESEK.md`-t és az M0, M1, DT-F140b-előkészítő, homonima-szúrópróba és javít-napló fájlokat is írta; ezek nincsenek az `ir` listában. |
| ⛔ pontok | OK / NEM ELLENŐRIZHETŐ | `git log` | Az F140.1 megállt az M0 ⛔-nél, az F140.89 az M2 ⛔-nél. A felhasználói jóváhagyás repóból nem ellenőrizhető. |
| A1, A2 | OK | `naplok/GLOSSZA_FORDITAS_zaras.md` | Van proveniencia-sor; a K8 valóban nyitott. |
| A3–A6 | nem értelmezett | – | Nincs tanulmány/párhuzam/PaRDeS-réteg; a `futtat.py` E12–E15: 0 találat. |
| CI-jelentés (saját futtatás) | – | – | E2–E16, E19, E20, E26, E28, E29, E31: 0. E25: 4, E27: 43 jelentés, mindkettő a diffen kívüli fájlokra mutat. E30: 1 figyelmeztetés (`kezi` a commit-üzenetben; mezőérték, nem hiba). |
| Ellenőrzőlista 1, 3, 4 | OK | – | Nulla a diff a `forditasok.tsv`-n, a `konkordancia/` alatt és a `sqlite_epit.py`-n; az új tábla +11 677 sor, a többi tábla Δ 0. |
| Ellenőrzőlista 2 | NEM ELLENŐRIZHETŐ | – | Kulcstartomány szkript nélkül nem számolható; a H9015–H9019 hiánya szándékos. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**
1. A H6308 („átadni” a „megszabadítani” helyett) és a H6117 („megkerülni” a „megtámadni” vagy „megcsalni” helyett) fordítási hiba, mindkettő Károlival ellenőrizve. A kb. 45 soros mintában 2 hibát talált, ezért a teljes táblában kb. 4% hibaarány valószínű.
2. A javít-napló nem rögzíti a `?` törlését a 9 javításos soron; a H6424-nél a törlés ellentmond a javaslatnak („a bizonytalanság marad”).
3. A zárójelentés elavult: a tesztszám (15 helyett 19) és az „ismert hibás sorok … a tábla nem módosítható” mondat már nem igaz.
4. A H8577M fejszava („sárkány”) ellentmond a glosszának és a testvérsornak.
5. A 13 `glossza_hu`-ban maradt backtick ütközik a SEMA 2.34 idézőjel-tilalmával.
6. A brief `ir` listája hiányos.
