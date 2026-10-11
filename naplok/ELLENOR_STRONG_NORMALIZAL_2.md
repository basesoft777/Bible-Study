# ELLENŐR (2. kör) — F62_STRONG_NORMALIZAL_BRIEF.md · origin/main...HEAD (F62.0–F62.5, a4a8c3d1)

*A jelentést a `fuggetlen-ellenor` subagent adta (nem volt fájlíró eszköze); a fő session írta ki, tömörítve. A teszteket, az `ellenoriz.py`-t és a `betolt.py` összevetését a fő session futtatta (22/22, 11/11, sértés 0, stdout és `--md` bájtra azonos; az új változat két stderr-figyelmeztetést ír: H410, H883). Az ág le van maradva a main mögött; az E5 hiba (`F86_…`) ebből ered.*

**Összegzés: ELTÉRÉS: 6 tétel (mind alacsony súlyú, javítás: F62.6)**

1. **K4** — az ellenőrzés nem zár eltérés nélkül.
2. **(1h)** `scan H20447` hibaüzenete („A Strong-szám H0779 alakú legyen") azonos a valódi javítás üzenetével, és ellentmond a `teszt_strong_util.py` `test_05b` szándékának; ugyanígy `scan G020447` → „G0086 alakú legyen" (`lekerdez.py:51-52`).
3. **(2c)** `domen h779` hibát ad, de nem a helyes alakot (`lekerdez.py:636`: a regex kis-nagybetű-érzékeny); a `scan h0779` elfogadott, a két alparancs eltér.
4. **(3d)** A SEMA 1.2 bővítése más eszközökben nincs leltározva: `emeles.py:57`, `lexikon_general.py:56`, `ellenoriz.py:626` a `G20447`-et elutasítja.
5. A brief `ir` mezője nem tartalmazza az `eszkozok/strong_meres.py`-t és az `adat/SEMA.md`-t; a `kovetkezo` elavult.
6. **(5c)** Az M0 7. pontjának fájlszáma: „10 fájl" ↔ 9 (10+38+1 ≠ 48).

## OK
G20447 (2) / G20833 (1) találat scan, igealak, kollokacio szerint; a TAGNT-ben nincs több ötjegyű G-kulcs; H-ötjegyű hiba (rc=1); nullázatlan/túlnullázott bemenet hiba a helyes alakkal; `domen H779` hiba; `domen H0032a` és `A0002` változatlan (kimondott kivétel); SEMA.md csak az egysoros G-kiegészítés; DT94 helyőrző-alakú; a `betolt.py` stderr-figyelmeztetés a K2-ben; `strong_meres.py` a repóban, proveniencia-sorral, hatókör kimondva (113 = 108 + 5); zárás 14 sor; adattábla Δ=0; nincs végleges DT/N szám; ⛔ sorrend betartva (a chatbeli jóváhagyás repóból nem igazolható).

## NEM ELLENŐRIZHETŐ az ellenőr által
`strong_meres.py` futtatása (a „1 068 624 / 0" állítás); DT94 chatbeli jóváhagyása.
