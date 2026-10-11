# LEKERDEZ_NAPLO M0 — felmérés (F61.1)

*Brief: `F61_LEKERDEZ_NAPLO_BRIEF.md` · ág: `claude/f61-lekerdez-naplo` · 2026.10.11 · nem ellenőrzött, a végrehajtó felmérése*

## 1. A `lekerdez.py` alparancsai és a proveniencia-sor alakja

A sor mindenhol `proveniencia: scope=… | forras=… | [strong=…] | n=… | ts=…` (a `ts()` UTC, percre kerekített). Az alparancsok:

| Alparancs | `scope` | `forras` | `strong` | Megjegyzés |
|---|---|---|---|---|
| `gerinc` | `range:<szakaszok '+'-szal>` | TAHOT/TAGNT (a ténylegesen olvasottak) | nincs | `n` = a gerinc-jelöltek száma |
| `scan` | `TAHOT-teljes` / `TAGNT-teljes` / `range:<szakasz>` | `TAHOT_kivonat.tsv` / `TAGNT_kivonat.tsv` | van | `n` = igehelyek |
| `kollokacio` | `TAHOT-teljes+TAGNT-teljes` | TAHOT+TAGNT | `A+B` | `n` = versek |
| `igealak` | mint a `scan` (teljes) | mint a `scan` | van | `n` = szó-előfordulások |
| `lxx-hid` | `range:<igehely>` | `LXX_OS/<fájl>+TAGNT_kivonat.tsv` | nincs | |
| `tsk` | `range:<igehely>` | `TSK_kereszthivatkozasok.tsv` | nincs | |
| `karoli` | `range:<igehely>` | `Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv` | nincs | hiányzó szövegnél hiba (exit 1), nincs sor |
| `domen` | `SDBH-v0.9.2` / `SDGNT-v1.1` | `SDBH_domenek.tsv+SDBH_SDGNT_anomaliak.tsv` (SDGNT-nél párja) | 1 vagy `A+B` | több ponton `sys.exit(0)`-val zár, a kapcsoló kezelése ezért az `args.func` hívás körül (a `main()`-ben) a tiszta, nem alparancsonként |

Hibaágon (nincs adat, érvénytelen argumentum, `domen` előfeltétel) nincs proveniencia-sor, tehát naplósor sem.

## 2. Az `auditok.tsv` érvényességi szabályai

- Alak: komment-fejléc, oszlopok `id lepes proveniencia datum`, 222 adatsor, a fájl `\n`-re végződik. A SEMA 2.9 `datum` formátuma `2026.09.25`.
- `ellenoriz.py` 1. szabály: az `id` létező `motivumok.tsv`-motívum legyen. **Feladatkód nem felel meg.**
- `ellenoriz.py` 8. szabály: *minden* ID, amely az `auditok.tsv`-ben szerepel, minden „mindig” kötelező datasetet le kell fedjen a `forras` kulcsból (a RETROAKTIV_IDK kivételével). Egy feladatkód-ID tehát sértést adna, mert egyetlen lekérdezés nem fed minden datasetet.
- `ellenoriz.py` 3. szabály (`proveniencia_ervenyes`): a megengedett kulcsok `scope`, `forras`, `ts` + `strong`, `n`. **A `csatorna` kulcs jelenleg érvénytelen** → a `csatorna=cli` sor 3. szabály szerinti SÉRTÉS lenne. Az `ellenoriz.py` `PROVENIENCIA_MEGENGEDETT_TOVABBI_KULCSOK` halmazát bővíteni kell (az `ir` mezőben az `ellenoriz.py` szerepel; ez a brief „az `ellenoriz.py` igazítása”).
- Az `lepes` értékkészletet az `ellenoriz.py` nem ellenőrzi (csak az ID-t), ezért az `adhoc` miatt abban nincs teendő.
- CI: az `eszkozok/ellenorzes/szabalyok.py` E4 szabálya csak a `B3` lépést vizsgálja (`TELJES_SCAN_LEPESEK`); az `adhoc` ezt nem érinti, módosítás nem kell. (Csak olvastam, nem írom.)

## 3. A nyitott kérdés — a motívumon kívüli `adhoc` hely

Az 1. és 8. szabály együtt kizárja, hogy az `auditok.tsv`-be feladatkód-`id` kerüljön (b): a 8. szabály dataset-lefedettséget követelne tőle, az 1. szabály pedig nem létező motívumot jelezne. A (b) az `ellenoriz.py` két szabályának átírását és a CI-t is érintené (szabalyok.py E4 is `id`-ként olvassa).

**Javaslat: (a).** A `--naplo` értéke: ha az ID létező motívum, az `adat/auditok.tsv`-be ír; ha nem (feladatkód, pl. `F61`, `PILOT-…`), a `naplok/<KÓD>_lekerdezesek.tsv`-be, azonos oszlopokkal (`id lepes proveniencia datum`). Az `adhoc` lépés motívumhoz kötött lekérdezésnél is megengedett (az `auditok.tsv`-be kerül). Kérdés a döntőnek: a megkülönböztetés az `id` létezése a `motivumok.tsv`-ben (javaslat), vagy külön kapcsoló (`--naplo-fajl`).

## 4. Nyitott pont a kimenetről (K1/K2 összhangja)

K1 szerint kapcsoló nélkül a kimenet bájtra azonos; K2 szerint a naplósor a *kiírt* proveniencia-sorral egyezik, `csatorna=cli`-vel. Következmény: a `csatorna=cli` csak `--naplo` esetén kerül a kiírt sorba is (kapcsoló nélkül a sor változatlan, `csatorna` nélkül). Ez a javaslat, a döntés a DT102 (2) pontja.
