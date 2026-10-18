# ELLENOR_TSK_VERSSZAM — F114_TSK_VERSSZAM_BRIEF.md · origin/main (be85d5de)..HEAD (6d298a40)

Ellenőr: `fuggetlen-ellenor` subagent, modell: claude-opus-5-5 (kért: `opus`, egyezik). A végrehajtó naplói és a 12 commit trailere `claude-sonnet-5-5` / „Claude Sonnet 5.5”, egymással konzisztensek.
*A fájlt az orkesztrátor írta ki az ellenőr szó szerinti jelentéséből (az ellenőrnek nincs írási eszköze); az 1. eltérést az orkesztrátor a `Karoli_versmegfeleltetes.tsv`-n külön megerősítette (scope=`igehely_kjv` üres sorok | forras=`awk` a `Karoli_versmegfeleltetes.tsv`-n | ts=2026-10-18): 161 üres KJV-sor, ebből `MT|szamlalas` 86, `MT|lxx_os_etalon_f91` 66, `KEZI|kezi_identitas_javitas` 8, `KJV|lxx_os_etalon_f91` 1; `1Sám 17:12` → üres KJV, MT 17:12, a TSK-ban 16 sor.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| G-átváltó helyessége / E3 | ELTÉRÉS (súlyos) | `eszkozok/tsk_kulcs.py:70-75` | Az üres `igehely_kjv` értéket az átváltó „nincs pár”-nak veszi. A táblában azonban 86 nem-felirat sor üres az LXX-hiány miatt (MT/szamlalas), holott a KJV-vers létezik és azonos: 1Sám 17:12–31, Jer 33:14–26, Józs 8:30–35, 1Kir 6:11–14, Péld 18:23–24, 4Móz 6:27, Jer 48:45–47. **Regresszió:** `lekerdez.py tsk "1Sám 17:12"` → 0 sor, „nincs KJV-pár”, pedig a TSK-ban 16 sor van rá, és `karoli "1Sám 17:12"` azonos tartalmat ad. `tsk "Jer 23:5"` → „3 sor kimarad”, köztük Jer 33:14 és 33:16, pedig a Károli Jer 33:15 létezik. A felmérő E. része ugyanebből a táblából számolja a „helyes” halmazt (`tsk_versszam_felmeres.py:102-113`), így körkörös: a 0/0 ezt a hibát nem foghatja meg. |
| G-átváltó (N-F41a) | ELTÉRÉS | `Karoli_versmegfeleltetes.tsv:15995` | A `tsk "Jón 2:1"` a KJV 2:1 (ima) TSK-ját adja, de `karoli "Jón 2:1"` = KJV 1:17. Ismert N-F41a táblahiba; a modul docstringje nem említi, a mérés körkörös. |
| A1 | ELTÉRÉS | `naplok/TSK_VERSSZAM_jelentes.md` E3 | Jelöletlen, hamis tényállítás: a nincs-pár kulcsok „KJV-versek, amelyeknek a Károliban nincs azonos tartalmú párja (pl. 1Sám 17:12–31…)”. |
| D N-F114b | ELTÉRÉS | `NYITOTT_FELADATOK.md` | A brief 2. és 5. pontja szerint külön tételként nyitandó; a `NYITOTT_FELADATOK.md`-ben nincs. |
| Brief fejléc | ELTÉRÉS (enyhe) | `F114_TSK_VERSSZAM_BRIEF.md:12` | A `kovetkezo` mező elavult (az F114.8 lefutott). |
| E1 (öt fogyasztó) | OK | a diff 5 fájlja | mind a `tsk_kulcs`-on át olvas; a sqlite `minta` ága egyenértékű. Mellékes: `olvaso_pilot/adat.py:552` proveniencia-sora nem nevezi meg a versmegfeleltetést. |
| E2 / TSK érintetlen | OK | — | `git diff --numstat origin/main..HEAD -- konkordancia/TSK_kereszthivatkozasok.tsv`: üres. |
| E6 / DT-F114b ÚSZ | OK | `tsk_kulcs.py:21-26`, README, N-F114a | a korlát mindenütt kimondva; teszt: `test_usz_azonossag_kimondott_korlat`. |
| E7 / DT-F114a | OK | `adat/jeloltek.tsv` | numstat 7/7, csak `igehely` és `indoklas` vége; ütközés nincs; mind a 7 pár egyezik a megfeleltetéssel. |
| DT-F114c / render_diff | OK | `render_diff_osztalyoz.py:478-522` | 43 elem; a negatív teszt a listán kívüli `Róm 8:1`-et és a más motívumbeli `Zsolt 6:5`-öt `ismeretlen`-nek méri; a DT191 többi ága érintetlen. |
| DONTESEK | OK | DT-F114a/b/c | helyőrzők, 🟢, felhasználói idézettel. |
| A2 | OK | N-F09g, N-F114a | `tsk "Préd 9:12"` → Kol 3,23 Votes=71 első; `tsk "Zsolt 18:6"` → nincs Zsolt 50,15; `tsk "Zsolt 16:10"` → Zsolt 49,16. |
| A3–A5 | NEM ALKALMAZHATÓ | — | nincs tanulmány, Remez/Sod, tanító a diffben. |
| A6 / E12–E15 | OK | — | `futtat.py`: 0 találat. |
| CI | saját futtatás | — | `futtat.py --valtozott <19 fájl> --diff-alap origin/main --diff-fej HEAD` → exit 0. |
| Írási halmaz / ⛔ | OK | — | `eszkozok/ellenorzes`, `.github`, `motivumlog`, `FELADATOK.md` érintetlen; a ⛔ 3.1, 3.6, 3.7 megállásai a változtatás előtt. |
| Tesztek, E3 reprodukció, `teszt_bdb_vers_jelentes` | NEM ELLENŐRIZHETŐ | — | az ellenőr parancskörén kívül. |

## ÖSSZEGZÉS — ELTÉRÉS: 5 tétel

1. Az átváltó az üres-KJV (LXX-hiányos) sorokat „nincs pár”-nak veszi — regresszió (1Sám 17:12: 16 → 0 TSK-sor; Jer 23:5 elveszíti a Jer 33:14/16 célt); a 0/0 mérés körkörös.
2. Jón 2:1 kulcsa hibás (N-F41a), a modul nem jelzi.
3. A jelentés hamis tényállítása az 1Sám 17:12–31-ről (A1).
4. Az N-F114b nincs megnyitva.
5. A brief `kovetkezo` mezője elavult.
