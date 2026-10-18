# F117 — az A–D′ osztály sorai a táblában és a tervezetben (a ⛔ 4.1 előtti mérés)

*FELADATOK #117 · ág: `claude/f117-versmegf-javitas` (origin/main 89b30c2e) · végrehajtó: claude-opus-5-5 · 2026-10-18*

proveniencia: scope=ÓSZ, az F117 brief 1. táblázatának A–D′ fejezetei | forras=konkordancia/Karoli_versmegfeleltetes.tsv (sha256 edd6b457…b562) + naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv (sha256 d14a2cf5…c265) + konkordancia/Karoli_1908.tsv (versszám) | eszköz=naplok/F117_tabla_allapot_meres.py | n=346 Károli-vers | ts=2026-10-18

A mérés csak a tábla és a tervezet sorait nézi; szöveg-összevetés nem készült (az a 4.2).

## 1. Eredmény osztályonként

| Osztály | Károli-vers | Sor a táblában | Sor a KK1b-tervezetben | A mai sor osztálya és forrása |
|---|---|---|---|---|
| A — 13 hiányzó fejezet | 264 | 0 | 0 | — (nincs sor) |
| ↳ C — Dán 3:31–33 (az A Dán 3-ának része) | 3 | 0 | 0 | — |
| B — Préd 9:21–23, Jób 39:34–38 | 8 | 8 | 8 | `KEZI` / `kezi_identitas_javitas`, üres `igehely_kjv` |
| D — 1Kir 22:46–49, 54; Ézs 3; Jón 2; 1Sám 24; 1Sám 20:43 | 67 | 67 | 67 | `MT` / `tvtms` 58 (azonosság), `MT` / `szamlalas` 9 (üres KJV: 1Kir 22:46–49, 54; Ézs 3:27; Jón 2:11; 1Sám 24:23; 1Sám 20:43) |
| D′ — 1Kir 22:43–45, 50–53 | 7 | 7 | 7 | `MT` / `tvtms` (azonosság) |
| **Összesen** | **346** | **82** | **82** | |

Fejezetenként (A): 2Móz 35 = 36, 2Móz 36 = 37, Dán 3 = 33, Hós 2 = 22, Hós 13 = 15, Hós 14 = 10, Jób 17 = 15, Jób 37 = 23, Péld 12 = 27, Én 5 = 19, Én 6 = 10, Ézs 4 = 6, Ézs 64 = 11 Károli-vers; mindegyik 0 sorral a táblában és a tervezetben.

## 2. Ami a 4.1-hez számít

1. **A tervezet ugyanúgy lyukas, mint a tábla.** A 264 hiányzó vers a KK1b-tervezetben sincs meg, a B, D és D′ hibás sorai pedig a tervezetben is ugyanazok. A KK4 tehát nem rossz sort választ: a tervezetben nincs jó sor. A KK1b nem futtatható újra a repóból (bemenete a repón kívüli `verse_pairs.jsonl`). A javítás ezért csak új kézi bemenetből jöhet.
2. **A KK4 ma determinisztikus.** Az újrafuttatás repón kívüli kimenettel (`KK4_KIMENET`) bájtra azonos táblát adott (sha256 `edd6b457…b562`, 22 931 adatsor, 9 többsoros tervezet-kulcs feloldva). Ez az alapja az E1 bájtazonossági próbának.
3. **Két művelet kell.** A B, D és D′ esetében (82 vers) meglévő sort kell felülírni. Az A esetében (264 vers) új sort kell pótolni. Az F91-javító csak felülír (`javit()`, a sorszám nem változhat), ezért a pótlás az F91-mintán túlmegy: az alkalmazó modul új sorokat is beszúr, és ellenőrzi, hogy rendezett-e a kimenet.
4. **A tábla 6 oszlopos, nincs `proveniencia` oszlopa.** A soronkénti proveniencia a javító bemenetben élhet. A táblában a `forras` mező (`szoveg_osszevetes_f117`) és egy fejléc-jegyzet hordozza, az F91-sor mintájára.
