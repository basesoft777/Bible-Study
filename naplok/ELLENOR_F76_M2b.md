# Független ellenőrzés — #76 OLVASOI_KONKORDANCIA, M2b (pilot-egyezés javítás)

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`, a kért `opus`-szal egyezik). Fájlíró eszköze nincs; a jelentést az orkesztrátor (Claude Sonnet 5.5) mentette az ellenőr szövege alapján, tömörítve. Tartomány: F76.24–F76.27 (az `origin/main`-hez képest). A szerver-tesztet és a Flask-renderelést az ellenőr nem futtatta: ami ezen múlik, „nem ellenőrizve — eszköz-korlát”.*

**Eredmény: ELTÉRÉS, 7 tétel.**

| # | Súly | Tétel | Állapot |
|---|---|---|---|
| 1 | súlyos | **Rossz ág:** az F76.24–F76.27 a helyi `main`-re került (nem pusholt), az m2b ágon csak az F76.23 volt; a zárónapló ágállítása ezért hamis volt | **Javítva (orkesztrátor):** a négy commit az m2b ágra cherry-pickelve (a brief fejléc ütközése feloldva: `megallt`), a helyi `main` az `origin/main`-re visszaállítva |
| 2 | közepes | Az új `naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md` nincs az `ir` mezőben, a zárónapló ezt nem említette | **Javítva:** az `ir` mezőbe felvéve (és az `ELLENOR_F76_M2b.md`), a zárónapló pontosítva |
| 3 | közepes | A fejléc-számlálók és az útmutató a pilot ÓSZ-szabályát ÚSZ-fejezetekre is alkalmazzák („0 héber + 0 görög”, „0/0”) — `lekerdezesek.py:355,365`, `oldalak.py:215,223`, `fejezet.html:61-65` (kódolvasás; renderelve nem igazolt) | Nyitott: N-F76i (1) |
| 4 | alacsony | Teszt-gyengeségek: az `expectedFailure` a `KeyError`-t is elnyeli; az írásjel-teszt önmagához mér (`db // 1000` tűréssel); az alap-konfig teszt a regiszterhez mér | Nyitott: N-F76i (2) |
| 5 | alacsony | Két blokkcím eltér a pilottól („Angol szó szavanként (BSB/KJV)”, „Így fordítja Károli”); a teszt leképezéssel átengedi | Nyitott: N-F76i (3) |
| 6 | alacsony | „Ebben a versben”: a szófaj-tartalék a nyers szófaj, a pilotban `szofaj_hu` (`blokkok.py:446,521`) | Nyitott: N-F76i (4) |
| 7 | alacsony | Az összevetés 3d sora DT-F76e-t ír DT151 helyett | Nyitott (kis szövegjavítás) |

**OK:** a 10 mintavételes pilot-blokk jelleg/forrás/szöveg egyezik a szerver regiszterével; az írásjelek, TSK (n=68), H6440 (2127), LXX-híd (10 görög szó) a `lekerdez.py`-jal igazolva; DT148–i: a kód nem előzi meg a döntést (Olvasópult versenkénti sor, nincs magyar alapjelentés/BDB-bontás/témaváltó); proveniencia, jelleg- és forrássor az új blokkokon; XSS/escape, SQL-paraméterezés; kiadási kapcsoló (KJV csempe a `kjv` tábla-kizárás alatt); fejléc (`allapot: megallt`, `pr`/`lezarva_osszegzes` üres); DT133 érintetlen, végleges DT/N szám nincs; `adat/` és `konkordancia/` Δ = 0; ⛔ M5–M7 érintetlen; CLAUDE.md-szabályok; CI-szkript HIBA nélkül.

**Nem ellenőrizve — eszköz-korlát:** a tesztfutások (19 új: 14 zöld + 5 várt hiba; 62 OK — végrehajtói futás); Zsolt 22 szakasz és a renderelt DOM; a számlálók teljesítménye (M4, K5).
