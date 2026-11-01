# MUHELY_FEED_STASH_naplo.md — F156 (FELADATOK #156)

*Modell-ellenőrzés: kért `sonnet`, tényleges `claude-sonnet-5-5` — egyezik. Futás: 2026-11-01, alap-commit `3a2dbd51`.*

## M0 — a „kész”-kritérium az ISTENTISZT-001 aranymintán

Minden mérő csak olvasva futott; a nulla-diff próba repón kívüli ideiglenes könyvtárba generált. Eredmény pontonként:

| # | kapu | állapot | érték | mérő (proveniencia) |
|---|---|---|---|---|
| 1 | `ellenoriz.py` 1–21: 0 HIBA | **zöld** | 18 RENDBEN, 0 SÉRTÉS; JELENTÉS/KÉZI látszik (nem blokkol) | `scope=motivum:ISTENTISZT-001 \| forras=ellenoriz.py \| ts=2026-11-01` |
| 2 | `futtat.py` E2–E29: 0 hiba a motívum fájljain | **zöld** | 0 HIBA, 500 jelentés (E12 348, E13 107, E27 41, E25 4) | `forras=ellenorzes/futtat.py --valtozott motivumok/ISTENTISZT-001.md lexikon/ISTENTISZT-001_TUDOMANYOS.md` |
| 3 | egyforrású, nulla-diff | **zöld** | `motivumok/ISTENTISZT-001.md` megvan; `general.py --cel lexikon --id ISTENTISZT-001` a lap `ts=` dátumával (`PARDES_DATUM=2026-10-29`) bájtra egyezik (CR-normalizálva) | `forras=general.py (nulla-diff)` |
| 4 | nincs `dontes=nyitva` jelölt | **piros** | 6 nyitva: Ézs 41:25 (F110 szűrő, B osztály) és 5 motívumközi sor (Zsolt 116:4, 1Móz 4:26, Róm 10:12–14; DT280) | `forras=jeloltek.tsv` |
| 5 | `motivum_hatar`: 0 nyitott kérdés | **piros** | gépi rész 0, modelles rész 5 kérdés (K1–K5, `naplok/HATAR_ISTENTISZT-001.md`) | `forras=motivum_hatar.py` |
| 6 | olvasói blokk 100%, kiejtés-hiány 0, „(fordításra vár)” 0 | **piros** | blokk 98/98 fedett (51 bevezetővel, 0 HIÁNY), fordításra vár 0, **kiejtés-hiány 3** (a Jelmagyarázat `י׳`, `ק׳`, `שׁ׳` jelei, generált rész, jóváhagyott héber alak nélkül) | `forras=OLVASOI_blokk_teljesseg_meres.py + kiejtes_szoveg.py` |
| 7 | 0 nyitott lektori kérdés | **nincs mérő** | a lektor-felület tárolója (`naplok/LEKTOR_<ID>.tsv`) nem létezik (DT-F156c) | — |
| 8 | nincs nyitott 🟡 DT / ⛔ feladat | **piros** | 4 megállt feladat (#121, #131, #146, #152) és hozzájuk 🟡 DT-k | `forras=feladatok.py + DONTESEK.md` |

**Összesítés: 3/8 zöld.** Az ISTENTISZT-001 a kritérium szerint **nem kész**, noha a `motivumok.tsv` `statusz`-a `publikálható` (v3).

### Mérés közben megállapított tények

- **Az `ellenoriz.py` kimenetéből a motívumonkénti bontás csak részben vezethető le:** a szakaszok verdiktje globális, motívum csak a 8/c, 18, 19 szakasz soraiban szerepel névvel. Ezért a kapu így számol: SÉRTÉS-szakasz, amely a motívum nevét tartalmazza → piros; SÉRTÉS-szakasz, amelyben egyetlen motívum sem szerepel → minden motívum piros (globális). Ma 0 SÉRTÉS van, tehát minden motívum zöld.
- **A `futtat.py --valtozott` motívumonként levezethető** (a motívum fájljain), 1–4 perc motívumonként; a teljes futás ~20 perc.
- **A 3. kapu nulla-diffje** csak úgy egyezik, ha a generálás a lapban álló `ts=` dátumot kapja (`PARDES_DATUM`); különben a 19 GENERÁLT-KEZDET sor `ts` mezője tér el.
- **A 8. kapu a briefek `ir` mezőjéből köti a feladatot a motívumhoz** (az `ir` tartalmazza a motívum azonosítóját). Az ISTENTISZT-001-re ez 11 feladat, ebből 4 `megallt`. Kérdés a felhasználónak, hogy a „megállt” állapot mindig ⛔-nak számít-e (DT-F156b (c)).

## Teendő-lehetőségek az ISTENTISZT-001-en (⛔ DT-F156b)

Nem zöld: 4., 5., 6., 8. kapu; a 7. nincs mérő. A kapuk kétféleképpen rendezhetők: a lap vagy a forrás javul (kiejtés-jelek, a határ K1–K5 megválaszolása, a megállt feladatok #152/#131/#146/#121), vagy a kritérium pontosodik:

- **4. kapu:** a motívumközi (F127 B2, DT280) nyitva sorok is blokkolnak-e, vagy csak a saját motívum jelöltjei?
- **5. kapu:** a „modelles rész” kérdései mikor számítanak lezártnak (nincs jelölő a megválaszoltságra)?
- **6. kapu:** a Jelmagyarázat gépi jelei (`י׳` stb.) kiejtés-kötelesek-e.
- **8. kapu:** a `megallt` feladat és a 🟡 DT mindig blokkoló-e, vagy csak a motívum tartalmát érintő?

## Futás minden motívumon (lépés 2)

9 motívum, **0 kész (8/8)**, 19/72 zöld kapu. A `motivumok.tsv` 8 motívumot `publikálható`-nak jelöl, a kritérium szerint egy sem kész: az **eltérés-lista** mind a 8 `publikálható` motívumra (KIRALY-001, ISTENTISZT-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001, HAMART-001); a TEREMT-002 `feldolgozás alatt` (4/8).

| motívum | zöld | zöld kapuk |
|---|---|---|
| KIRALY-001 | 1/8 | 1 |
| ISTENTISZT-001 | 3/8 | 1, 2, 3 |
| TEREMT-001 | 2/8 | 1, 4 |
| ALVIL-001 | 4/8 | 1, 2, 3, 4 |
| MENNY-001 | 1/8 | 1 |
| ANTROP-001 | 1/8 | 1 |
| HODIT-001 | 1/8 | 1 |
| HAMART-001 | 2/8 | 1, 5 |
| TEREMT-002 | 4/8 | 1, 2, 4, 8 |

Megjegyzések:

- **3. kapu:** csak az ISTENTISZT-001 és az ALVIL-001 nulla-diffes. A többi publikálható motívumnál az újragenerálás 994–3628 sorban tér el a committolt laptól (migrációra vár, #123), a TEREMT-002-nek nincs lexikon-lapja.
- **2. kapu:** a régi motívumoknál 1–17 HIBA áll (a `--valtozott` mód diff nélkül a motívum fájljainak minden találatát HIBA-ként számolja); az ISTENTISZT-001, az ALVIL-001 és a TEREMT-002 0 HIBA.
- **5. kapu:** „nincs mérő” a `naplok/HATAR_<ID>.md` nélküli motívumokon (csak az ISTENTISZT-001 és a HAMART-001 van meg).

## A két réteg átnézése (⛔)

- A nyilvános JSON fehérlistás: csak `id`, cím, téma, PaRDeS-szint, állásfokozat, kapuk (sorszám, név, állapot), számlálók, a Stash-mezők. **Nem kerül bele:** jelölt-indoklás, a határ-kérdések szövege, a DT-k kérdésszövege, a hibaszövegek, a PR-ok, a negatív kritérium és a fölérendelt fogalom (utóbbi kettő a brief 3.4 szerint a Stash-leírás része, de adattábla-tartalom; **DT-F156e** kérdés: bekerüljön-e a nyilvános Stash-be). A belső réteg a jelölteket és a határ-kérdéseket csak jelölővel/igehellyel hivatkozza (szöveg nélkül).
- A teszt (`eszkozok/teszt_muhely_allapot.py`) ellenőrzi a fehérlistát és azt, hogy hiányzó mérő nem zöld.

## Frissítés menete

```bash
python eszkozok/muhely_allapot.py            # ~20 perc; --motivum ID ... szűkít, --nincs-gh kihagyja a PR-lekérést
python eszkozok/teszt_muhely_allapot.py
```

A kimenet a `generalt/muhely/` (három JSON, GENERÁLT fejléccel); a Dashboard-artifact a nyilvános JSON-ból levezetett táblákat tölti (frissítést egy session végez kérésre).

## Dashboard

A Dashboard-artifact privát; hivatkozása a PR leírásában és a jelentésben áll. A belső fül **hibaszövegeket** tartalmaz: a hivatkozást megosztani csak a belső fül nélküli változat publikálása után szabad.
