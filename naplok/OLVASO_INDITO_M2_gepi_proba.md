# #100 OLVASO_INDITO — M2.1 gépi próba

*Ág: `claude/olvaso-indito` · végrehajtó: `claude-sonnet-5-5` · futás: 2026-10-15 10:08:14 – 10:09:19 (WSL-óra), a kód a commit `4cf24f98` (F100.7). A próbát a session scratch-könyvtárában lévő `proba_m2.py` végezte (nem része a repónak), a WSL `pardes` disztribúció venv-jével.*

## 1. Elv: semmi éles nem módosult

- **Külön port:** 18801 (az éles 8765/8766/8768 nem került érintésre; a 8765-ös felügyelő PID 4690 a próba előtt és után azonos).
- **Ideiglenes adatbázisok:** `~/proba100/forras.db` (a "Windows-oldali" szerepű) és `~/proba100/cel.db` (a "WSL-másolat" szerepű), mindkettő a valódi `~/pardes/pardes.db` másolata; az eltérést a forrás `meta.epites_ts`-ének átírása adta (`2026-10-15T08:00:00Z`, majd `2026-10-16T12:00:00Z`). A valódi `~/pardes/pardes.db` mérete, mtime-ja és `epites_ts`-e a próba előtt és után azonos (938 303 488 bájt; `2026-10-14T09:35:00Z`). Az `indit.sh`-t a `PARDES_FORRAS_DB`, `PARDES_DB`, `PARDES_ZAR` környezeti változókkal irányítottuk az ideiglenes példányokra.
- **Ideiglenes ág:** `proba/m2-agvaltas-100` a próba worktree-jében; a próba végén visszaváltva `claude/olvaso-indito`-ra és törölve. A főcheckout (`Desktop/Bible-Study`) a próbát nem érintette.
- A kód a worktree-ből (`/mnt/c/Users/bases/Desktop/wt-olvaso-indito/…`) futott; a `.bat` parancsikonok a próbában NEM futottak (azok a főcheckout `indit.sh`-ját hívják, ami a merge-ig ott nincs meg; a kipróbálás az M2.2, a felhasználó dolga).

## 2. Eredmény: 36 ellenőrzés, 0 hiba

| Brief-követelmény | Ellenőrzés | Eredmény |
|---|---|---|
| kétszeri kattintás után egy példány, 200 | 6. lépés: két `indit.sh` 0,4 mp különbséggel; utána egy felügyelő-folyamat (gyereke az újratöltő gyereke), `/statusz` és `/1Moz/1/1` 200 | teljesül |
| `.py`/sablonfájl módosítása után ≤5 mp-en belül az új kód | 2. lépés: `touch` ötféle fájlon (`oldalak.py`, `sablonok/alap.html`, `konfig/elemek.toml`, a pilot `bdb_szelet.py`-ja, `statikus/olvaso.css`); a mellékelt (utolsó) futásban 1,0–1,1 mp; egy korábbi, hibás szkriptű futásban az első újraindulás (`oldalak.py`) 3,3 mp volt; valódi tartalmi változás (HTML-megjegyzés a sablonban): 0,1 mp | teljesül (legrosszabb mért: 3,3 mp) |
| a tervező mentése (`arculat.json`) nem indít újra | 2b: `touch` → 4 mp-ig nincs újraindulás | teljesül |
| eltérő `epites_ts` → másolás, a napló kiírja | 1. és 5. lépés: `adatbázis: MÁSOLÁS`; a másolat `epites_ts`-e a forrásé lett; ideiglenes fájl nem maradt | teljesül |
| azonos `epites_ts` → nincs másolás, a napló kiírja | 6. lépés: két indításnál `NINCS másolás`; a másolat inode-ja és mtime-ja változatlan | teljesül |
| a régi példány leállítása | 5. és 6. lépés: a napló "régi példány … leállt", a régi PID megszűnt | teljesül |
| lábléc: ág, commit, építési idő | 1. lépés: `ág: claude/olvaso-indito`, commit `4cf24f98` (a `git_allapot` értéke), az építési idő a másolt adatbázisé | teljesül |
| ágváltás → figyelmeztetés | 3. lépés: ideiglenes ágra váltva a lábléc **újraindítás nélkül** 2,5–2,8 mp-en belül az új ágat mutatja, "Figyelem" sorral (a tartalom nem változott, ezért az újratöltő nem indult újra, a lábléc mégis friss) | teljesül |
| az adatbázis-másolat elavulása → figyelmeztetés | 4. lépés: a "Windows-oldali" forrás `epites_ts`-ét átírva, futás közben, 2,5 mp-en belül "Az adatbázis-másolat régebbi …" a láblécben; az 5. lépésben (újabb kattintás, másolás után) a figyelmeztetés eltűnt | teljesül |

A `main` ágon *nem* megjelenő figyelmeztetést a gépi próba a worktree-ben nem tudta kipróbálni (a worktree sosem `main`-en áll, és a `main` nevű ág nem hozható létre ideiglenesen); ezt a `teszt_indito.py` fedi (`TesztLablecAlkalmazas`, mindhárom kiadásban: `PARDES_AG=main` esetén nincs `Figyelem:`; ágváltás után van, az ETag változik, a régi ETag-gel nincs 304).

A próbaszkript első két futása (10:05, 10:06) két saját hibám miatt nem teljes (formázási hiba; majd az 5. és 6. lépés megvárta volna a régi példányt, illetve egy végtelen indulásfigyelő-ciklus miatt 90 mp-et várt): a javított szkript harmadik futása az alábbi, teljes napló; az első két futás nem a szerver hibája volt.

## 3. Ismert korlátok (nem hiba a briefhez képest, de a felhasználónak tudnia kell)

1. **Szintaxishibás szerverfájl leállítja a szervert.** Külön próba (ideiglenes másolat, 18802-es port, `def (` hozzáfűzve az `oldalak.py`-hoz): az újratöltő gyereke import közben meghal (`SyntaxError`), a Werkzeug felügyelő (nem 3-as kilépési kód) is kilép, a port elnémul (HTTP 000, 0 folyamat), és a fájl javítása nem indítja újra magától. A parancsikon újra indítja. Ha ez zavaró, javítás lehet egy saját felügyelő, amely hiba után is figyel; ez a brief hatókörén kívül esik, a felhasználó dönthet róla (javaslat: csak akkor, ha a gyakorlatban előfordul).
2. A főcheckout fájljai merge/checkout alkalmával változnak; ez az újratöltőt egyszerre sok fájlra indítja, az újraindulás ilyenkor is ~1–3 mp.
3. A lábléc ága a futó példány kódjának helye szerinti git-állapot (a főcheckout aktuális ága); a worktree-ben futtatott próba-példány a worktree ágát mutatja.

## 4. A próba teljes naplója (a javított szkript futása)

```
[10:08:14] az éles állapot a próba előtt: {"pardes_db_meret": 938303488, "pardes_db_mtime": 1791972024.7480993, "epites_ts": "2026-10-14T09:35:00Z", "eles_8765_felugyelo_pid": [4690]}
[10:08:26] ideiglenes másolatok kész (12.4 mp)
[10:08:36] a "Windows-oldali" forrás ts=2026-10-15T08:00:00Z, a "WSL-másolat" ts=2026-10-14T09:35:00Z
[10:08:36] == 1. indítás (eltérő epites_ts) ==
[10:08:43] OK    1. indítás: a /statusz 200-zal válaszol, 6.4 mp-en belül a Popen után (a másolással együtt)
[10:08:43] OK    a napló kiírja: MÁSOLÁS (eltérő építési idő)
[10:08:43] OK    a másolat epites_ts-e a forrásé lett (2026-10-15T08:00:00Z)
[10:08:43] OK    nem maradt ideiglenes fájl: ['cel.db', 'forras.db', 'szerver.log', 'zar']
[10:08:43] OK    GET /1Moz/1/1 -> 200
[10:08:43] OK    a lábléc ág- és commit-sora megvan: ('claude/olvaso-indito', '4cf24f98')
[10:08:43] OK    a nem-main ágon (claude/olvaso-indito) a lábléc figyelmeztet
[10:08:43] OK    a lábléc az adatbázis építési idejét mutatja (2026-10-15T08:00:00Z)
[10:08:43] OK    pontosan egy felügyelő-folyamat (PID [7670]; összes folyamat: [7670, 7708])
[10:08:43] == 2. kódfájl touch -> újraindulás (a követelmény: legfeljebb 5 mp) ==
[10:08:44] OK    touch oldalak.py -> újraindult és válaszol: 1.1 mp
[10:08:45] OK    touch sablonok/alap.html -> újraindult és válaszol: 1.1 mp
[10:08:45] OK    touch konfig/elemek.toml -> újraindult és válaszol: 1.0 mp
[10:08:46] OK    touch ../olvaso_pilot/bdb_szelet.py -> újraindult és válaszol: 1.0 mp
[10:08:47] OK    touch statikus/olvaso.css -> újraindult és válaszol: 1.1 mp
[10:08:47] OK    a napló a változásokat kiírja ("Detected change in …"): 5 db
[10:08:47] OK    a felügyelő PID változatlan az újraindulások után ([7670]), gyerek újraindult
[10:08:47] == 2b. az arculat.json módosítása NEM indít újra ==
[10:08:51] OK    arculat.json touch -> nincs újraindulás
[10:08:51] == 2c. valódi tartalmi változás: HTML-megjegyzés a sablonban -> az új kóddal válaszol ==
[10:08:51] OK    a módosított sablon hatása a lapon: 0.1 mp
[10:08:53] OK    a sablon visszaállítása után a jel eltűnt (1.4 mp)
[10:08:53] == 3. ágváltás (ideiglenes ág a worktree-ben) ==
[10:08:53] git:  proba/m2-agvaltas-100
[10:08:56] OK    az ágváltás a láblécben újraindítás nélkül látszik: 2.8 mp
[10:08:56] OK    a lábléc figyelmeztet az új ágra
[10:08:56] OK    ágváltásra (tartalom nélkül) nincs újraindulás, a lábléc mégis friss
[10:08:56] visszaváltva: claude/olvaso-indito | ideiglenes ág törölve: True
[10:08:56] == 4. a Windows-oldali adatbázis újraépül futás közben ==
[10:08:59] OK    a lábléc jelzi, hogy az adatbázis-másolat régebbi: 2.5 mp
[10:08:59] == 5. újabb kattintás (a forrás újabb) ==
[10:09:12] OK    a 2. kattintás után a /statusz 200: 13.3 mp
[10:09:12] OK    a napló: a régi példány leállítva
[10:09:12] OK    a napló: MÁSOLÁS (a forrás ts-e újabb)
[10:09:12] OK    a másolat frissült: 2026-10-16T12:00:00Z
[10:09:12] OK    egy példány fut, a régi PID ([7670]) megszűnt; most: [7771]
[10:09:12] OK    a másolás után a lábléc adatbázis-figyelmeztetése eltűnt
[10:09:12] == 6. azonos epites_ts, kétszer egymás után ==
[10:09:17] OK    a kétszeri kattintás után a /statusz 200
[10:09:17] OK    mindkét indításnál NINCS másolás (azonos építési idő)
[10:09:17] OK    a másolat fájlja érintetlen (azonos inode és mtime)
[10:09:17] OK    a kétszeri kattintás után pontosan egy példány (felügyelő PID: [7836], folyamatok: [7836, 7863])
[10:09:17] OK    GET /1Moz/1/1 -> 200
[10:09:17] OK    GET /statusz -> 200
[10:09:17] a porton hallgató folyamatok száma (felügyelő + gyerek az örökölt socket miatt): 2
[10:09:19] a próba-példány leállítva; peldanyok = ([], [])
[10:09:19] az éles állapot a próba után: {"pardes_db_meret": 938303488, "pardes_db_mtime": 1791972024.7480993, "epites_ts": "2026-10-14T09:35:00Z", "eles_8765_felugyelo_pid": [4690]}
[10:09:19] OK    a valódi ~/pardes/pardes.db és a 8765-ös példány érintetlen
[10:09:19] ideiglenes könyvtár törölve: True
[10:09:19] ÖSSZESEN: 36 ellenőrzés, 0 hiba
```

A szintaxishiba-próba (3.1. pont) kimenete: `elindult: 200` → a hiba beírása után 6 mp: HTTP 000, 0 folyamat, a napló `SyntaxError: invalid syntax` (`oldalak.py`, 367. sor) → a hiba kijavítása után 4 mp: HTTP 000, 0 folyamat (nem indul újra magától).
