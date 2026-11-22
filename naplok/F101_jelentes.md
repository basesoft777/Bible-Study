# F101 — jelentés (ADATBAZIS_FRISSITES)

## M0 — mérés (2026-11-21, Windows, Python 3.14, `origin/main` 8d3eca35)

*Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py --mod teljes (--gyoker a worktree, ideiglenes kimenet a repón kívül), ideiglenes mérőszkript | ts=2026-11-21`*

1. **Építési idő, Windows:** az építés (`Epito.epit`) 146,1 s, 1125,3 MB, 120 tábla; a táblánkénti hash-számítással és a meta-íréssel együtt a teljes futás 221,7 s. Az `integritas()` ellenőrzés ebben benne van, külön nem mértem.
2. **WSL (`pardes` disztribúció, 2026-11-22, javítva: az első bejegyzés téves disztribúcióra utalt):** a `pardes` disztribúció venvjével (`~/pardes/eszkozok/olvaso_szerver/.venv`, Python 3.12.3), a friss `HEAD` kivonatán (`git archive`, a WSL natív `/tmp`-jén) az építés 96,0 s, a teljes futás 141 s; kimenet 1125,3 MB, 120 tábla, a bájtméret azonos a Windows-építésével (1 179 987 968 B). A WSL tehát kb. 1,5-szer gyorsabb, mint a Windows (146 s / 221,7 s). A `~/pardes` checkout maga régi (`f6f6f50`, F76.7), módosított, és az integritás-ellenőrzésen elbukik (rc=1, 56 + 714 sértés), ezért azon nem épül adatbázis: az automatikus építésnek friss forrásból kell dolgoznia.
   *Proveniencia: `scope=manual | forras=eszkozok/sqlite_epit.py --mod teljes, WSL pardes, venv py3.12, /tmp-ről, ideiglenes kimenet | ts=2026-11-22`.*
2/b. **M1 mérések (2026-11-22, ugyanaz a gép, `pardes` WSL):** *Proveniencia: `scope=manual | forras=ideiglenes mérőszkript (scratchpad), a #101 ágon a 7a7406f3 alapján | ts=2026-11-22`.* Az építés közvetlenül a `/mnt/e` forrásról (9p): 266 s (a natív forrásról 96 s), ezért az építő pillanatképet készít (`tar`) a natív lemezre. Másolás WSL → Windows (1,1 GB): 38 s; Windows → WSL: 12 s.
3. **Forrásfájlok:** az `adat/` és a `konkordancia/` összesen 452 fájl, 1020 MB; a `stat` (mtime+méret) az egészre 0,25 s. A teljes `sha256` a 718 MB-nyi `.tsv`-re 30,2 s, tehát indításkor nem használható, csak mtime-eltéréskor.
4. **Az építő által ténylegesen olvasott fájlok listája hiányos:** az `open()`-t figyelő mérés csak 25 fájlt (100,6 MB) látott, mert a többit más úton olvassa az építő (a `KONKORDANCIA_ALTALANOS` lista és az `adat/` táblák). M1-ben a listát a kódból kell kinyerni, nem a futásból.
5. **Nem mért:** a `git checkout`/`pull` mtime-hatása (az mtime módosul akkor is, ha a tartalom nem), ezért a javaslat mtime+méret, eltéréskor `sha256`.

## ⛔ M0 megállás — döntések: DT-F101a, DT-F101b (`dontesek/uj/adatbazis-frissites.md`)

## Független ellenőrzés — 1. ellenőrzés

*Proveniencia: `scope=fuggetlen-ellenor subagent, base df2bd426, head 4541e32d, szint teljes (2 kör) | forras=a subagent válasza, változtatás nélkül (összefoglalva: a táblázat sorai a válasz szerint) | ts=2026-11-22`.*

Első sor: `ELTÉRÉS: 8 tétel`. CI a head-re: `45034189773`, `success` (`ellenorzes`, `feladatkovetes`). Nem ellenőrizhető: a DT jóváhagyása a repóból; az M2 ⛔.
Tételek és a javításuk (javító kör 1, a hibahelyek táblája):

| # | ELTÉRÉS | javítás |
|---|---|---|
| 1 | a forrás-halmaz kamu-riasztást ad (`.md`, `.jsonl`, `.html` az `adat/`-ban) | `forras_azonosito.py` `KIHAGYOTT_UTOTAG`; teszt: `test_nem_forras_fajl_nem_szamit` |
| 2 | a `motivumok/` stb. `.md` változása elnyelődik | `TANULMANY_RESZEK`; teszt: `test_a_tanulmanyszoveg_valtozasa_regebbi` |
| 3 | DT-F101b: a bejelentkezéskori indítás (DT161) is épít | a kapcsoló (`PARDES_EPIT=0`) megvan; a feladat a Windows Feladatütemezőben áll (a repón kívül), a parancsát nem módosítottam: **nyitott teendő** (README 2b, indit.sh fejléc) |
| 4 | a WSL-másolat cseréje a futó szerver alatt régi gyorsítótár-kulccsal keveri az új adatot | az `epit_hatter.sh` csak a Windows-oldali `pardes.db`-t cseréli; a WSL-másolatot az indító következő indításkor szinkronizálja; teszt: `test_regebbi_adat_hatterben_ujraepit_a_windows_oldali_peldanyt_cserel_a_wsl_masolat_nem` |
| 5 | két 3 s-os gyorsítótár egymás után | `Lablec.keszit` `ttl=0.0` az `adat_allapot`-nak; a README „kb. 3 mp + a számítás ideje”-ként írja |
| 6 | a szinkron visszamásolhatja a régi adatbázist építés közben | a 4. javítással megszűnt: a WSL-másolat és a Windows-oldali példány csak az új Windows-oldali fájl atomi cseréjekor tér el, és ilyenkor a másolás új→régi irányú |
| 7 | a README mért időinek nincs proveniencia-sora | a mérések a jelentés „2/b” pontjában, proveniencia-sorral |
| 8 | nincs teszt a `--kezi` belépési pontra | `test_epit_hatter_kezi_modja_a_zarat_veszi_es_kiirja_a_naplot` |

Az ellenőr megjegyzése a `Negativ.test_11_res_forras_egyezes` bukásról: az `origin/main`-en is bukik (ellenőrizve ideiglenes worktree-ben, 2026-11-22), nem ebből a változásból ered. A lap-betöltés-az-építés-alatt tesztje nem készült: az építés a szerver fájljához nem nyúl (a 4. javítás óta a WSL-másolat érintetlen).

## Zárás

- **Állapot:** M0 és M1 kész, a brief `megallt`: az M2 ⛔ (a felhasználó kipróbálja) hátra van. PR: 780 (draft), nincs merge.
- **Döntések:** DT-F101a–b (az orkesztrátor döntötte, 2026-11-22): mtime+méret előszűrő, `sha256` dönt; WSL-es építés friss forrásból, csak indító és parancsikon.
- **Eltérés a briefhez:** a WSL-másolatot a háttérépítés nem cseréli (a futó szerver alatt), csak a Windows-oldali `pardes.db`-t; a következő indítás szinkronizálja (egy kattintás). Indok: ELLENOR 1. ellenőrzés 4. és 6. tétele.
- **Tesztek:** `teszt_indito.py` zöld (a javító kör után), `teszt_olvaso_szerver.py` és a többi `--gyors` fájl zöld a javító kör előtt; `teszt_sqlite_epit.py`: 1 bukás (`Negativ.test_11_res_forras_egyezes`), amely az `origin/main`-en is bukik. A javító kör után a `--gyors` teljes újrafuttatása nem készült el.
- **Nyitott:** (1) a DT161 ütemezett feladat parancsába `PARDES_EPIT=0` (a repón kívül, nem módosítottam); (2) a negyedik asztali parancsikon (`PaRDeS adatbazis ujraepitese.bat`) létrejött az asztalon, a fő checkoutban az `epit_hatter.sh` a merge után lesz meg; (3) a régi `~/pardes` checkout (`f6f6f50`) módosított fájljai: `eszkozok/olvaso_szerver/manifest_pardes_db.tsv` (5+/5−, a régi `epites_ts`); követetlen: `.indit.zar`, `f149_proba.db` (1,1 GB), `indit_8765.log`, `olvaso_teszt_javitas.db` (1,1 GB), `pardes.db.f115_elotti`, `pardes.db.regi` — semmihez nem nyúltam, a sorsukról az orkesztrátor dönt; (4) a független ellenőr 2. köre nem futott (a helyi zárat másik futás tartotta).
- **Egyeztetett eltérés:** a DT-döntés az orkesztrátortól, nem a felhasználótól érkezett (a felhasználó felhatalmazásával).

## Zárás kiegészítése (2026-11-22, az orkesztrátor döntései)

- **`teszt_futtat.py --gyors` a `0fdb1c75`-ön:** mind a 17 fájl zöld (788,2 mp, a helyi runnernek nincs futásazonosítója: a kimenet a commit és a dátum alapján azonosítható). A helyi zárat a runner maga vette át (a tartó pid 8128 már nem élt).
- **Ismert, nem ebből eredő bukás:** `eszkozok/teszt_sqlite_epit.py` `Negativ.test_11_res_forras_egyezes` — az `origin/main`-en (df2bd426 utáni állapot, ideiglenes worktree, 2026-11-22) is bukik; a forrása: a tanulmány/adat ≡ tábla rés-forrás ellenőrzés (SEMA 3. szabály 11.), a hibajelentésben „nincs lexikonoldal” sorok.
- **DT161 — a felhasználó teendője (Windows Feladatütemező, a repón kívül; nem módosítottam):** a feladat neve `PaRDeS olvaso belso 8765` (bejelentkezési trigger). Mostani művelete: `powershell.exe -NoProfile -WindowStyle Hidden -Command "& wsl -d pardes -e bash -lc 'S=/mnt/c/Users/bases/Desktop/Bible-Study/eszkozok/olvaso_szerver/indit.sh; [ -f $S ] && exec bash $S belso 8765'"`. Új alakja (csak a `export PARDES_EPIT=0;` kerül be a `[ -f $S ] &&` elé): `powershell.exe -NoProfile -WindowStyle Hidden -Command "& wsl -d pardes -e bash -lc 'S=/mnt/c/Users/bases/Desktop/Bible-Study/eszkozok/olvaso_szerver/indit.sh; export PARDES_EPIT=0; [ -f $S ] && exec bash $S belso 8765'"`. Hatás: a bejelentkezéskori indítás nem épít újra (DT-F101b); a parancsikonok és a kézi parancsikon továbbra is építenek.
- **Régi `~/pardes` checkout:** érintetlen, a lista fent (Zárás, „Nyitott” 3.) marad; törlésről csak a felhasználó dönt.
