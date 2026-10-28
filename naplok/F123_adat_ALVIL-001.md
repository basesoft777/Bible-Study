# F123 X.A — az ALVIL-001 adat-előkészítése (munkafájl)

*#123 MIGRACIO2 · 2b. 1. lépés (`munka: adat`) · ág: `claude/f123-alvil-adat` · modell: claude-opus-5-5 · 2026-10-28*

*Döntés nélküli munkafájl: jelentéstartományt nem választ, prózát nem ír, motívumfájlt (`motivumok/`, `tematikus_lezart/`, `lexikon/`) és adattáblát (`adat/*.tsv`) nem ír (2b). A teljes sorok a mellékelt TSV-kben állnak, minden sor mellett a lekérdezés proveniencia-sorával; ez a fájl összegzés. A lekérdezések naplója: `naplok/F123_lekerdezesek.tsv` (`lekerdez.py --naplo F123`). Munkaszkript: `naplok/F123_adat_keszito.py` (alparancsok: `f108`, `szotar`, `proza`, `seol`).*

*Hatókör (DT-F123b, A út): most csak az X.A fut; a szétválasztás (M1–M5), a `motivumok/ALVIL-001.md` forrás és a lexikongenerálás a #131 merge-e után (N-F11d).*

## 1. A törzs összevetése a #108 eltérés-táblájával (2c)

**A törzs nincs újra levezetve** (2c): a meglévő `adat/elofordulasok.tsv` és `adat/jeloltek.tsv` ALVIL-001-sorai vannak összevetve a `naplok/F108_ujrascan_elteresek.tsv` (2026-10-17) ALVIL-001-soraival, és a motívum két Strongjára (H7585, G0086; az `elofordulasok.tsv` `strong` / `gerinc_elem` oszlopa: 64 + 8 sor) a mai TAHOT/TAGNT-en lefutott a scan.

| Mérés | Eredmény |
|---|---|
| `elofordulasok.tsv` ALVIL-001-sorok (ma / F108) | 72 / 72 — a kulcs (igehely + strong) mind egyezik; **új vagy eltűnt sor: 0** |
| `jeloltek.tsv` ALVIL-001-sorok (ma / F108) | 74 / 74 — **új, eltűnt vagy döntést váltott sor: 0** |
| F108-osztály, E-sorok | 57 `rendben`, 15 `zsoltar_55` (mind a 15: „mert osztaly: rendben”, azaz a `zsoltar_55` csak a #55-re utaló osztályozás, a kulcs rendben) |
| F108-osztály, J-sorok | 59 `nincs_strong` (TSK/frázis/kézi forrás, kulcs nem ellenőrizhető), 15 `zsoltar_55` |
| mai scan H7585 | 64 igehely (66 szó-előfordulás); 64 E-ben, 0 csak J-ben, **0 új**; E-sor, amelyet a scan nem ad: 0 |
| mai scan G0086 | 10 igehely; 9 E-vers, 1 csak J-ben (Mt 16:18, `elutasítva` — meglévő döntés, nem változás), **0 új**; E-sor, amelyet a scan nem ad: 0 |
| #110 szűrő | **nem alkalmazandó:** a szűrő az F108 tág gerinc-Strongjainak új helyeire szól (`F110_SZURO_PILOT_ISTENTISZT_BRIEF.md`); az ALVIL-001 két Strongja szűk (64, 10), és új hely nincs |

**Eredmény: eltérés nincs.** Gerinc-elemet érintő változás (Strong be/ki) nincs, ⛔ nem keletkezik; az értelmező menetnek a törzsben nincs mihez nyúlnia (a #109 mintájára csak eltérésnél kellene).

Részletes sorok: `naplok/F123_adat_ALVIL-001_f108_osszevetes.tsv` (146 kulcs-sor + 1 `ujrascan` csak-J sor).

Proveniencia:

- `scope=ALVIL-001: adat/elofordulasok.tsv (72 sor) + adat/jeloltek.tsv (74 sor) × naplok/F108_ujrascan_elteresek.tsv (146 sor) | forras=split('\t'), ág claude/f123-alvil-adat | ts=2026-10-28T15:10Z`
- `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7585 | n=64 | ts=2026-10-28T15:10Z | csatorna=cli`
- `scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0086 | n=10 | ts=2026-10-28T15:10Z | csatorna=cli`
