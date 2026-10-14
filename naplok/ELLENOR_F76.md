# ELLENŐR — F76_OLVASOI_KONKORDANCIA_BRIEF.md · origin/main..claude/olvasoi-konkordancia (F76.0–F76.6)

*A független ellenőr (`claude-opus-5-5`, a kért modell `opus`, egyezik) jelentése. Az ellenőrnek nem volt fájlíró eszköze, ezért a jelentést az orkesztrátor mentette ide, tartalmilag változtatás nélkül, tömörítve. Az ellenőr jelzése: néhány `futtat.py`-kimenetet `grep`/`head`/`tail` csővel szűrt (csak olvasás).*

**Eredmény: ELTÉRÉS, 8 tétel.** A hatókör M0+M1; az M2–M7 hiánya nem hiba.

## Rendben (OK)
- Modell: a commitok Co-Authored-By sora Sonnet 5.5, a brief `modell: sonnet` (az önazonosság repóból nem igazolható).
- `ir` mező betartva (8 fájl; a `DONTESEK.md` és a saját brief koordinációs fájl). A `sqlite_epit.py` érintetlen.
- DT-F76c egyezik a chatben rögzített hat döntéssel (a konkrét `MemoryMax=2G`/`AllowedCPUs=0` érték az M0 6/5 és 4.3/3 pontban áll, nem a DONTESEK-cellában).
- Mért számok: 39 blokk, szótő-táblák (66 824 / 72 720 sor), pilot-számok (58,8%, 24,8%, 93 ms) egyeznek a forrásokkal.
- ⛔ M0 rendben; ⛔ M5–M7 nem kezdődött el; `allapot: megallt` megengedett.
- `adat/` és `konkordancia/` alatt 0 változás. `futtat.py`: E2–E16, E19, E20, E26: 0; E25: 3 és E27: 34 régebbi, nem F76-hoz kötődő találat.

## Eltérések (súlyossági sorrendben)
1. **E1 — K4 frissesség (közepes–magas).** A K4 „a meta hashek egyeznek a TSV-kkel” előírása és a kód eltér: a manifestet a `frissesseg.py --manifest-keszit` ugyanannak a db-nek a `meta` soraiból írja, ezért a „meta = manifest” egyezés definíció szerint igaz, TSV-összevetést nem jelent. A TSV-oldali D5 (`db_meres.py`) az M1-ben nem futott és nem naplózott. (`M0.md:213`, `frissesseg.py:1-10, 77-82`, brief `:76`.) A meta ↔ tábla-hash rész helyes.
2. **E2 — hamis zöld (közepes).** `frissesseg.py --csak-meta` `--manifest` nélkül semmit nem ellenőriz, mégis „FRISS ÉS ÉP”, kilépési kód 0 (`frissesseg.py:86-100`).
3. **E3 — be nem váltott igazolás (közepes).** `M0.md:30` szerint az F79/F92/F95 építők és tesztek 3.12-n való futását az M1 csomag-tesztje igazolja; a 4.3-ban csomag-teszt nincs (`M0.md:257`).
4. **E4 — elavult szöveg (alacsony–közepes).** `M0.md:13, 32, 217, 221` és a `DONTESEK.md:221` „Alkalmazás” mezője döntés előtti/M1 előtti állapotot ír.
5. **E5 — hivatkozás nem létező belépési pontra (alacsony).** `M0.md:213` `adatbazis.py --frissesseg`-et említ, a megvalósítás a külön `frissesseg.py`, ami a 3.1 szerkezetlistában (`:39-53`) sem szerepel.
6. **E6 — előre meghozott M2-döntés (alacsony).** A `caddy` az M1-ben települt (letiltva), holott az `M0.md:236` szerint az M2 dönt Caddy és nginx között.
7. **E7 — hiányzó nyitott tételek a tervből (alacsony).** N-F94f, N-F94d, N-F92a (`NYITOTT_FELADATOK.md:60, 65, 66`) a #76-nak címzett, az M0 3.6/9. szakasza nem említi.
8. **E8 — jelöletlen memória-állítás (alacsony).** `M0.md:287` „~40–60 MB RSS” nem mért és nincs jelölve.

## Nem ellenőrizhető
- `pardes.db`- és WSL-mérések (EXPLAIN, ms, bájt, sha): a forrás meg van nevezve.
- ⛔ M1: írásos nyom az M1 telepítésének jóváhagyásáról a repóban nincs (a jóváhagyás a chatben történt).
- Python-verzió: a brief törzse (`:46, :53, :78`) még 3.11-et ír (egyeztetett eltérés, E1-ként jelölve az M0-ban).
- CI-jelentés nem volt.
