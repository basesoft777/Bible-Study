*A `fuggetlen-ellenor` (claude-opus-5-5) jelentése szó szerint; a subagent fájlt nem tudott írni, a fájlba a #12 session mentette (2026-11-02), változtatás nélkül. A javítókör: `naplok/F12_TEREMT002_LEXIKON_naplo.md` 10. szakasz.*

ELTÉRÉS: 15 tétel

# ELLENOR_F12_TEREMT002_LEXIKON — `F12_TEREMT002_PROZA_BRIEF.md` · `cccd17a8..f58f38e8`

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | tényleges `claude-opus-5-5`, kért `opus` |
| 0b `modell` mezők | NEM ELLENŐRIZHETŐ | `adat/forditasok.tsv` +9 sor; `motivumok/naplok/TEREMT-002_tanitoi_kereses.md:14` | `git diff cccd17a8..f58f38e8 -- adat/`: 8 sorban `claude-sonnet-5-5` (subagent), 1 sorban `claude-opus-5-5`. A subagent tényleges modellje a repóból nem mérhető. A napló 7. sorában `claude-opus-5-5`, ez a session modellje. |
| 0c `modell` (UBS H8414) | ELTÉRÉS | `adat/forditasok.tsv:30442` | A `modell` mező `claude-sonnet-5-5`, a 2. tagot („kietlenség”) viszont a megjegyzés szerint az opus session írta át. A mező a végső szöveg tényleges szerzőjét nem adja vissza. |
| DT-F12a | OK | `adat/lexikon_hivatkozasok.tsv` +2; `adat/elofordulasok.tsv` (3 sor) | diff: H8414 `1`, H0922 `tagolatlan`. A három sor: BDB/H8414/1/formlessness/formátlanság. |
| DT-F12b | ELTÉRÉS (részleges) | `adat/bdb_szakasz_hu.tsv:9345` | Megtörtént: KEZI_HIVATKOZAS sor, `bdb_vers_jelentes.tsv` (49:19 → Ézs 49:4, `forras_javitas`). Igazolás: `lekerdez.py scan H8414 --szakasz "Ézs 49:19"` → n=0; a `scan H8414` 19 verse között ott az Ézs 49:4. A gerinc magyar szakaszszövegében viszont maradt „értéktelenség 49:19”. N-F12a megvan. |
| DT-F12c | OK (adat) | `adat/lxx_dontesek.tsv` LD091–LD096 | `lekerdez.py lxx-hid "1Móz 1:2"`: G0517 ἀόρατος, ἀκατασκεύαστος Strong nélkül. `"Jer 4:23"`: G3762 οὐθέν. `"Ézs 34:11"`: G2048 ἐρήμου, σπαρτίον/γεωμετρίας Strong nélkül. A sorok ezzel egyeznek. A lapon megjelenő hiba külön sor (LXX-H0922). |
| DT-F12d / A5 | OK · tartalom NEM ELLENŐRIZHETŐ | `motivumok/naplok/TEREMT-002_tanitoi_kereses.md` | Mind a 18 név a `sablonok/PaRDeS_tanitok_lista.md`-n áll (Derek Prince: 16., 24. sor). A gap-ek explicitek, a hiány is („kiinduló-állapot olvasat képviselője nincs”). A derekprince.com/sermons/372 tartalma webes forrás, nem ellenőrizhető. |
| DT-F12e | OK | `adat/motivumok.tsv` | diff: `statusz` = `feldolgozás alatt`, `v1` változatlan |
| DT-F12f | OK | `adat/funkcio_kapcsolok.tsv` | diff: `SZOTARI_GERINC TEREMT-002 aktiv`, új `KAROLI_MEGFELELOK TEREMT-002 aktiv` |
| DT-F12g | OK (kód) · nulla-diff NEM ELLENŐRIZHETŐ | `eszkozok/szerep_karoli.py` (KOTOSZO) | diff ellenőrizve. A 9 lapra állított A/B nulla-diffet nem tudom futtatni. |
| DT-F12h | OK | `NYITOTT_FELADATOK.md` (N-F12c) | N-F12c felvéve; a lapon „függőben” áll (`lexikon/TEREMT-002_TUDOMANYOS.md:546`) |
| ⛔ DT-F12a–h döntője | NEM ELLENŐRIZHETŐ | `DONTESEK.md` DT-F12a–h | Mindegyiket az orkesztrátor hozta, a felhasználó 2026-11-02-i felhatalmazására hivatkozva. Maga a felhatalmazás a repóban nem igazolható. |
| ⛔ 4.7 (próbalap a felhasználónak) | ELTÉRÉS | `naplok/F12_TEREMT002_LEXIKON_naplo.md:106` | A brief szerint „a felhasználó a próbalapot látja” az éles írás előtt. A napló csak ennyit ír: „az orkesztrátor jóváhagyta az éles írást”. A felhasználó megtekintésének nincs nyoma. |
| ⛔ 4.9 (merge) | OK | — | nem történt merge |
| Brief-fejléc | ELTÉRÉS | `F12_TEREMT002_PROZA_BRIEF.md:9,11` | `allapot: fut`, `kovetkezo: "0. mérés kész; ⛔ DT-F12a–e az orkesztrátornál"` – elavult. A napló 169. sora szerint a fejléc `megallt`. |
| 5.1 | OK | `adat/elofordulasok.tsv` | `jelentes_en` = „formlessness”, `jelentes_hu` = „formátlanság”: a -/1/- szöveg szó szerinti része, funkció-értelmezés nincs benne |
| 5.2 | OK | `adat/szotar_szakasz_cimke.tsv:20` | Egyetlen gépi sor (`szakasz_cimke_levezet.py`, DT439): a H8414 -/1/-. A H0922 tagolatlan (DT438), a -/2/--t egyik motívumsor sem használja. Az ISTENTISZT-001 ugyanígy csak a használt szakaszokat címkézi (Grep a táblán). |
| 5.3 | OK | `lexikon/TEREMT-002_TUDOMANYOS.md:114` | Grep „fordításra vár”: egyetlen találat, a jelmagyarázat |
| 5.4 | OK | lap 345–360, 464–509 | gerinc és 13–14. szerep a lapon |
| 5.5 | ELTÉRÉS | `naplok/F12_TEREMT002_LEXIKON_naplo.md:96`; `NYITOTT_FELADATOK.md` N-F12b | A tesztek nem zöldek: a napló maga 11 bukást rögzít, a main-en is. Az `ellenoriz.py` és a `feladatok.py ellenoriz` futtatása számomra nem megengedett, így NEM ELLENŐRIZHETŐ. |
| 5.6 / 8(b) L2 | ELTÉRÉS | lap `:818`, `:821` | A lapon folyamat- és dátummondatok állnak egyes szám első személyben, 【NAPLO】 nélkül („nyertem ki”, „ebben a menetben nem vontam be”, „a session utólag ellenőrizte (2026.11.02…)”). A „7. pont 7. tétel” hivatkozás elavult: a forrás 7. pontjában ma két kérdés van (`motivumok/TEREMT-002.md:214–215`). A napló L2-t ✅-nak mondja. |
| 5.7 / 8(c) | ELTÉRÉS | napló `:144–145`; lap 3. szakasz | A brief szerint ami az arany lapon megvan, az itt is megvan, vagy explicit hiányjelölést kap. A „Rokon szavak” és az „Új felismerés” blokkhoz a lapon nincs hiányjelölés, ezt a napló maga is elismeri. Az LXX-sor ✅-t kapott, holott a H0922 döntései nem jelennek meg (l. LXX-H0922). |
| 5.8 / 8(d) | OK | napló `:148–165` | a „fordított irány” táblája megvan, 12 sorral |
| 5.9 | OK | — | `git diff --stat`: TEREMT-001 fájlt nem érint. `git diff … -- naplok/*.py \| grep csv`: üres. |
| 8(a) CI | ELTÉRÉS | `motivumok/TEREMT-002.md` (E5) | Saját `futtat.py --valtozott … --diff-alap cccd17a8 --diff-fej f58f38e8 --pr-cim "[ELLENŐRZŐ] …"` futás: **E5 HIBA: 4** törölt címsor. A napló 114. sora szerint ezt az „F12.9” `TÖRLÉS-SZÁNDÉKOS:` sora oldja fel, de F12.9 commit nincs: `git log` szerint a legutolsó az F12.8, és egyik commit-üzenetben sincs `TÖRLÉS-SZÁNDÉKOS`. Tartalmilag a négy blokk archiválva van (`archivum/…_regi.md` = régi fájl +1 sor), a HIBA azonban áll. |
| CI-egyezés (3.) | OK | — | A saját futásom szakaszonként és számra egyezik a kapott `ci_jelentes.md`-vel (E5 4, E12 200, E13 35, E25 3, E27 40, E30 9). E17 egyik kimenetben sincs. |
| Commit-granularitás | ELTÉRÉS | `5d2505bc` | Az „F12.7c” (a BDB H0922 `tagolatlan` fordítássora) külön commit nélkül az F12.7-be került: `git log -S "F12.7c (E19"` → `5d2505bc`. |
| A1 | ELTÉRÉS | `motivumok/TEREMT-002.md:115` (lap `:533`) | Az állítás: „a szótár a *tohu* két jelentését éppen ott választja szét, ahol a motívum határa húzódik”. A `bdb_vers_jelentes.tsv` H8414 -/1 alatt azonban a 3 motívumvers mellett további 8 nem-motívumvers áll: Ézs 45:18, 24:10, Jób 26:7, 5Móz 32:10, Jób 6:18, 12:24, Zsolt 107:40 (Grep `^H8414\t`, 155750–155759). A BDB-határ tehát nem a motívumhatár. Értelmezés áll adatállításként; a bekezdés utolsó mondata csak részben veszi vissza. |
| A2 | ELTÉRÉS (enyhe) | `NYITOTT_FELADATOK.md:67` (N-F12d) | Az N-F12d három fájlt nevez meg. Grep `DT-F131z` `eszkozok/`: 7 fájl, 10 előfordulás; a `bdb_rovidites.py`, a `lexikon_general.py`, az `olvaso_szerver/blokkok.py` és a `teszt_bdb_rovidites.py` kimaradt. A többi N-F12 valóban nyitott (N-F12a/g a lap 341. és 353. során látszik; az N-F12f: `epit_uj_fajl` a 4884. sorban). |
| A3 | OK | forrás `:85`, `:137` | Az Ézs 45:18, az Ézs 24:10 és a mérőkötél „tematikus, nem lexikai” címkét kapott. `scan H8414` → mindkét Ézs-vers *tohu*-vers, `kollokacio H8414 H0922` → csak a 3 vers. |
| A4 | OK | forrás `:133–147` | A Sod („a rend … a Teremtő szavának ajándéka”) a Drash 141. sorából („rendezett állapot… a hozzá való viszonyban áll fenn”) vezethető le, a „visszafelé mutatja” pedig a Remez 135. sorából. A Remez megfigyelései feltételesen jelöltek. |
| A6 E12 | NEM ELLENŐRIZHETŐ | — | 200 figyelmeztetés, a kimenet csak 3-at mutat. A teljes lista a megengedett paranccsal nem kérhető le. |
| A6 E13 / kiejtés | ELTÉRÉS | lap `:9`, `:104`, `:106`, `:129`; forrás `:11` | A kiejtés lapon belül sem egységes: a Kivonatban „tóhu vá-vóhu”, a címben és a 124. sorban „tóhú vávóhú”. A token-kiejtés „וָבֹ֔הוּ (vábóhú)”: a dages nélküli bét magánhangzó után v, tehát helyesen vávóhú. Az 1/a-ban az 1Móz 1:2 kapcsolódás-sora kiejtést kap, az Ézs 34:11-é (129. sor) nem. |
| Lap: LXX-H0922 | ELTÉRÉS | lap `:398`, `:549` | Az összesítés „LXX-minusz=0”, az `adat/lxx_dontesek.tsv`-ben viszont két `lxx_minusz` sor van (LD094, LD096). A 6. pont H0922-sora („eltérő 2 · azonosításra vár 1”) a H8414-ét másolja; a H0922 tényleges állása 1 `eltero_forditas` + 2 `lxx_minusz`. Sem a napló, sem N-F12 tétel nem említi. |
| Lap: sablonos következtetések | ELTÉRÉS | lap `:394`, `:539`, `:412` | A motívumnak nincs görög szava, a lap mégis ezt írja: „a görög Ószövetség csak a helyek 0%-án használja ugyanazt a szót”. A 7. pont szerint „a szótár ezt a párt nem ismeri; a kapcsolatot csak a fordítás (LXX) mutatja”, holott a SECE-listán ott a G0517 és a G2048, éppen az LXX-megfelelők (LD091, LD095; `lxx-hid` kimenet). |
| Lap: kolofon | ELTÉRÉS | lap `:915`; `adat/motivumok.tsv` (TEREMT-002) | A „Sablon-megfelelőség” cella üres, jelölés nélkül. A `sablon_verzio` üres maradt, holott a napló 0.3 E5 pontja szerint a 6. lépés kitölti. |
| Ellenőrzőlista 1: törölt/kiszűrt sorok | OK | — | `git diff --numstat -- adat/`: adatsor nem törlődött. Módosult: `elofordulasok` 3, `motivumok` 1, `funkcio_kapcsolok` 1, `bdb_vers_jelentes` 1 (+ fejléc), `bdb_forras_javitas` fejléc 1. A forrásfájlból 98 sor törlődött, ebből 4 címsor, mind archiválva. |
| Ellenőrzőlista 2: kulcstartomány | OK | — | Az LXX-sorok 3 vers × 2 Strong = 6/6, a `res_forras` 9/9 rés, a SECE 6 G-Strongjának fordítása 6/6, a `lexikon_hivatkozasok` H8414 és H0922 is megvan |
| Ellenőrzőlista 3: nulla-diff hatóköre | NEM ELLENŐRIZHETŐ | napló `:107`, `:110` | Az állítás csak a DT-F12g kódváltozásra vonatkozik (9 lap) és arra, hogy a lap az F12.8 után változatlan. Nem fedi az F12.2b-t (`bdb_vers_jelentes`/`bdb_forras_javitas`), sem a `lexikon_general.py` változásait más lapokon. Saját futtatással nem igazolható. |
| Ellenőrzőlista 4: sorszám-Δ (fejléc nélkül) | OK | — | `git diff --numstat`: auditok +3, bdb_forras_javitas +1, bdb_vers_jelentes 0, elofordulasok 0, forditasok +9, funkcio_kapcsolok +1, lexikon_hivatkozasok +2, lxx_dontesek +6, motivumok 0, res_forras +9, szotar_szakasz_cimke +1. `konkordancia/` 0. Egyik sem éri el a \|Δ\| ≥ 10-et. |
| Ellenőrzőlista 5: ⛔ | l. a ⛔ 4.7 és ⛔ DT-F12 sorokat | — | — |
| Tanulmány-ellenőrzés (F37 T4) | nem él | — | A tartományban nincs `*_bovitett.md` és `*_tanulmany.md` fájl |

**Az ELTÉRÉS-ek súlyossági sorrendben:**
1. CI E5 HIBA áll, a hivatkozott F12.9 nem létezik.
2. A lap LXX-blokkjai ellentmondanak az adatnak (H0922, LXX-minusz=0).
3. A1: a BDB-határ ≠ motívumhatár állítás.
4. Sablonos következtetések egy görög szó nélküli motívumon.
5. ⛔ 4.7: nincs nyoma, hogy a felhasználó látta a próbalapot.
6. 5.5: a tesztek nem zöldek.
7. 8(c): Rokon szavak / Új felismerés jelölés nélkül.
8. DT-F12b részleges (49:19 a `bdb_szakasz_hu.tsv`-ben).
9. L2: folyamat- és dátummondatok a lapon.
10. A kiejtés nem egységes.
11. A kolofon cellája üres.
12. A brief-fejléc elavult.
13. Az N-F12d hatóköre hiányos.
14. A UBS H8414 `modell` mezője.
15. Az F12.7c nem kapott külön commitot.
