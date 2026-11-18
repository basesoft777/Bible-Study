# F226 — helyi bukó tesztek leltára (2026-11-18)

Környezet: WSL `pardes`, `PARDES_DB=/home/basesoft/pardes/pardes.db` (1110 MB, `epites_ts` 2026-11-12T18:53:35Z), `python eszkozok/teszt_futtat.py --gyors` (14 fájl; 13 zöld, 1 HIBA), plusz `teszt_bdb_adatblokk.py` külön. A lassú tesztsort nem futtattam (keretszűkítés). Az F207 (PR #708) N-F207a–e tételeit ismertként kezelem, nem vizsgáltam újra.

Szűkítés (felhasználó, orkesztrátor útján): csak valódi kódhibát javítunk; elavult teszt és elavult DB leltárba megy. Kódhibát nem találtam, ezért **nincs kódváltozás**.

| Teszt | Hiba szó szerinti sora | Ok | Besorolás | Javaslat |
|---|---|---|---|---|
| `olvaso_szerver/teszt_visszhang_kapu.py` `LancAMotivumadatbol.test_bevezeto_a_peshat_magot_es_a_kulcsszavak_szamat_mondja` | `AssertionError: 'Peshat-magjának (1Móz 3–9) azon verse' not found in "#### 4.11. Visszhang: …"` | a generált bevezető szövege ma „A versek a Genezis láncának (1Móz 3–9) azok a versei, …”; a teszt a régi „Peshat-magjának … azon verse” megfogalmazást keresi. A kimenet tartalmilag helyes (mag, szám, kulcsszavak) | (a) elavult teszt | a teszt friss szövegre igazítása külön, nem sürgős tétel |
| ugyanott `Rontott.test_v3_nincs_a_nem_azonositott_helyen` | `AssertionError: '## 4. Szótári háttér …' == '## 4. Szótári háttér …'` (`assertNotEqual(r, self.b)`, 85. sor) | a `replace` nagy `a`-val kezdődő szöveget keres kis `a`-val („a rokon írások lekérdezése…”); a blokkban „A rokon írások…” áll, ezért a csere nem hat | (a) elavult teszt | a keresett szöveg nagybetűs kezdetére igazítás (nem gyengítés) |
| `teszt_bdb_adatblokk.py` `Javitas.test_blokk_javitas_szakasz` | `AssertionError: 'a forrásban `Eccl 17:10` → helyesen `Préd 7:10`' not found in '### ADATBLOKK H7223 …` (255. sor) | az `adat/bdb_igehely_javitas.tsv` 75. sora megvan (H7223 Eccl 17:10 → Préd 7:10); a 2500 karakteres adatblokk a javítás-szakaszt levágja/nem hozza. A bdb_adatblokk generátor kimenete adatfüggő | nem kódhibaként igazolt; (a)/(c) — a brief szerint az 1.0-s adaton is bukik | külön vizsgálat, ha kell; adat/generátor érintése ⛔ |
| `teszt_bdb_adatblokk.py` `KaroliTabla.test_minden_kesz_szocikk_szerepel_proveniencival` | `AssertionError: Lists differ: ['H0001', 'H0006', 'H0034', …] != ['H0001', 'H0002', 'H0003', 'H0005', …]` (a Károli-tábla ~6000 karakternyi sora a ~72 800 karakternyi kész-halmazzal szemben) | a kész szócikkek halmaza (`adat/`) nagyobb, mint amennyi proveniencia-sor a Károli-táblában áll; adat-/DB-állapot kérdése | (c)/adat — ⛔ `adat/` érintetlen | adat-lépcső külön tétele |

Egyéb: a `teszt_futtat.py` első indításakor a WSL-venv-re való újraindítás után a gyerekfolyamat 24 percig várt a saját szülője elavult zárára (`~/.pardes/ellenorzes.zar`, pid 1752, nem élő); a zár törlése után lefutott. Lehetséges futtató-hiba (zár a re-exec után), de egyszeri mérés, nem vizsgáltam; nyitott megfigyelés.

Összegzés: kódhiba 0, kapu- vagy CI-rontás 0; 4 bukás besorolva, mind (a)/(c); javítás nincs.
