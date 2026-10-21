ELTÉRÉS: 2 tétel
# ELLENOR_F128 — F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md · 72eee13d..4b41242b

*A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette el (az ellenőrnek nincs fájlíró eszköze). Az `origin/main..HEAD` kétpontos diff a main azóta érkezett F110-munkáját fordított előjellel hozza, ezért az ellenőrzés a merge-base-hez mér (19 fájl). Tényleges modell: `claude-opus-5-5`.*

## Eltérések (súlyossági sorrendben)

1. **Generált tábla fejléce.** Az ág módosítja a `hu_illeszt.py`-t és a `forditas_kapuk.py`-t, ezért az `adat/bdb_szakasz_hu.tsv` `# forras` sorának `kód@` és `forditas_kapuk.py@` hash-e elavul; a `hu_illeszt.py --ellenoriz` (`hu_illeszt.py:287-294`) a teljes fájlt veti össze, így a 3 `teszt_bont --ellenoriz` bukása nem csak a CRLF-checkouttól és a main-en már meglévő elavulástól (`bdb_szakaszok.tsv`, 10-19) függ. A napló (`naplo.md:248-251`) csak a CRLF-et és a `forditas_kapuk`/`bdb_szakaszok` hasht nevezi meg, a `kód@` hasht nem. A tábla újragenerálása nincs az `ir`-ben: a felhasználó dönt.
2. **CI E16.** A PR érinti az `eszkozok/ellenoriz.py`-t, ezért a PR címének `[ELLENŐRZŐ]` előtaggal kell kezdődnie; előtag nélkül `E16 HIBA`, előtaggal 0 találat.

Megjegyzés: az ág nincs a main csúcsára alapozva (F110 merge, DT283/DT284); a `DONTESEK.md` végén merge-ütközés várható.

## Rendben
- Az ág csak az `ir`-ben szereplő fájlokat módosította; adattábla nem íródott (`forditasok.tsv`, `bdb_szakasz_hu.tsv`, `bdb_szakaszok.tsv` érintetlen); adatsor-törlés 0, táblasor-Δ 0.
- H8415 kézi sor érintetlen; `szakasz_beir` `--kezi-marad` nélkül megáll rajta (`teszt_szakasz_bemenet.py:258`).
- DT-F128a–g: hét helyőrzős, 🟢 sor, végleges DT-szám nincs az ágon; kódírás egyik ⛔-t sem előzte meg (F128.1 → .3 → .4; .8 → .9 → .10).
- `prompt_v5.md`: a v4-hez képest 51 beszúrás, 0 törlés. A régi `teljes` út változatlan; a `teljes` BDB-sorok száma 674, az új összefűző a mai adaton ugyanazt adja.
- Szakasz-kapu, bemenet-előállító, 13. szabály `sz<n>` ága: kódban és tesztekben rendben; E2–E15, E19, E20, E26, E28, E29, E31: 0 találat.

## Nem ellenőrizhető (az ellenőr szerepéből)
Tesztek és a main-en állítólag meglévő hibák (`teszt_olvaso_szerver` 2, `teszt_pilot_aranymintaval`) futtatása; a modellhívás hiánya; a száraz próba számai (a szkriptek a repón kívül); az, hogy a DT-F128a–g döntéseket a felhasználó hozta-e (a repóból nem igazolható).
