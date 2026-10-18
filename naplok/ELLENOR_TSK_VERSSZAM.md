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

---

# Újraellenőrzés — origin/main (be85d5de)..HEAD (6a47fe96); a javító menet: 95035cd8..HEAD

Ellenőr: `fuggetlen-ellenor` subagent, claude-opus-5-5 (kért: `opus`, egyezik). *Az orkesztrátor írta ki az ellenőr jelentéséből; a táblasorokat (1Kir 22:45–49, Jób 39:34–38, Préd 9:21–23) a `Karoli_versmegfeleltetes.tsv`-n megerősítette (scope=a felsorolt kulcsok | forras=grep | ts=2026-10-18).*

| pont | eredmény | indok |
|---|---|---|
| Előző 1. kód (MT-tartalék csak MT/szamlalas, 86 sor) | OK | `tsk_kulcs.py:84-88`; `tsk "1Sám 17:12"` n=16; `tsk "Jer 23:5"` eléri a Jer 33,14/16-ot (1 sor kimarad: Ézs 4:2, tábla-lyuk, a (b) szerint) |
| Előző 1. negatív esetek | OK | Hós 14:2, Zsolt 18:1, Jób 39:34, Préd 9:21, Zsolt 13:1: „nincs KJV-pár” |
| Előző 1. az MT/szamlalas-tartalék tartalmi helyessége | **ELTÉRÉS** | az 1Kir 22:46–49-en a Károli-tartalom a KJV 22:45–48 (`karoli "1Kir 22:46"` = Josafát egyéb dolgai), az MT-tartalék eltolt TSK-párt ad (22:46 → a paráznák-hivatkozások). A main identitása ugyanezt adta (nem regresszió), de a „86 sor azonos számú” premissza hamis, teszt nincs rá. Rokon, nyitott tétel nélküli táblahibák: Károli 1Kir 22:54 = KJV 22:53, Jón 2:11 = KJV 2:10, Ézs 3:27 = KJV 3:26; a szomszédos `tvtms` sorok (1Kir 22:43–45, 50–53; Jón 2:10; Ézs 3:26) azonosságot adnak eltolt tartalomra. |
| F. rész nem körkörös | OK, korláttal | a régi elérés a `Karoli_1908.tsv`-ből; helyes halmazt nem számol, hibás új párt nem fog meg (a docstring kimondja) |
| `F114_elveszett_sorok.tsv` osztály-oszlopa | **ELTÉRÉS** | a `kategoria(src)` a KJV-kulcsot Károli-kulcsként keresi ki (`felmeres.py:156-158,185`); 24 KJV-kulcs (195 forrás-, 155 célsor) rossz okkal címkézve. A „Jób 39:34–38, Préd 9:21–23: a KJV-ben nincs ilyen vers” hamis: Károli Préd 9:21–23 = KJV 10:1–3, Jób 39:34–38 = KJV 40:1–5, Dán 3:31–33 = KJV 4:1–3; Préd 2:26, Zsolt 13:6 Károli-összevonásban. Ezeknek van Károli-otthonuk, mégis elvesznek. |
| Előző 2. (Jón 2:1 a docstringben) | OK | `tsk_kulcs.py:90` |
| Előző 3. (jelentés E3) | **ELTÉRÉS** (részben javult) | az új mondat mind a 161 üres-KJV sorra azonosságot állít (a 66 feliratsorra, a 8 KEZI-re, az 1Kir 22:46–49-re hamis); az E3 táblázat (`:19,23,24`) a DT-F114d előtti számokat mutatja jelölés nélkül (friss: 21 309; 272/4 211; 282/3 446) |
| Előző 4. (N-F114b) | OK | `NYITOTT_FELADATOK.md:134` |
| Előző 5. (brief fejléc) | OK | — |
| DT-F114d | OK formailag | 🟢, idézet, Hós 13/14, Én 6 indok igazolva; a tényalapban a fenti két hamis premissza áll |
| N-F54a bővítés | OK | 13 fejezet, 235/3 653 forrás, 243/2 360 cél |
| Írási halmaz, TSK érintetlen, jeloltek 7 sor, render_diff 43 + negatív teszt | OK | — |
| Tesztek | OK | `teszt_tsk_kulcs.py` 12 OK; `teszt_render_diff_osztalyoz.py` 74 OK |
| CI | OK | `futtat.py` exit 0; E25/E27 találatok a diffen kívül |
| A1 | ELTÉRÉS | l. fent |
| A3–A5 | NEM ALKALMAZHATÓ | — |

## ÖSSZEGZÉS — ELTÉRÉS: 3 tétel

1. A DT-F114d tényalapja és az elveszett-sorok napló osztályozása hamis (24 kulcs rossz kulcson címkézve; Préd 9:21–23 / Jób 39:34–38 / Dán 3:31–33 KJV-párja létezik). A felhasználó a (b)-t részben ezen a premisszán választotta.
2. Az MT/szamlalas-tartalék az 1Kir 22:46–49-en eltolt párt ad (nem regresszió); rokon `tvtms` táblahibák nyitott tétel nélkül.
3. A jelentés E3 túláltalánosít, a táblázata elavult számokat mutat.

---

# Harmadik ellenőrzés — origin/main (be85d5de)..HEAD (7b845d8e); a második javító menet: 2253319a..HEAD

Ellenőr: `fuggetlen-ellenor` subagent, claude-opus-5-5 (kért: `opus`, egyezik). *Az orkesztrátor írta ki az ellenőr jelentéséből.*

| pont | eredmény | indok |
|---|---|---|
| `ok` oszlop (`F114_elveszett_sorok.tsv`) | OK | 510 sor: `tabla_lyuk_fejezet` 478, `tablahiba_kjv_par_letezik` 25 (12 forráskulcs / 198 sor; 13 célvers / 188), `kivetel_nincs_par_1Kir_22_46_49` 7; Károli-szöveggel mintavételezve (Préd 9:21 = KJV 10:1, Jób 39:34 = KJV 40:1, Dán 3:31 = KJV 4:1, Hós 14:2 = KJV 14:1) |
| DT-F114d helyesbítés | OK | jelölt szakasz; az idézet és a (b) indoka bájtra azonos |
| `NINCS_PAR_KIVETEL` | OK | 1Kir 22:46–49, scope=manual, negatív teszt; `tsk "1Kir 22:46"` n=0. Megjegyzés: az 1Kir 22:45 (Károli = KJV 22:44) eltolt, a teszt pozitív esetként rögzíti (N-F54a alatt ismert) |
| 1Kir 22:54, Jón 2:11, Ézs 3:27 MT-tartaléka | OK (ártalmatlan) | a KJV-vers nem létezik, a TSK-ban 0 sor; a kár a szomszédos `tvtms` sorokon van (nem regresszió) |
| E3 számok | OK | 21 306; 275/4 245; a régiek jelölten felülírva. A céloldali +29 / +27 különbség NEM ELLENŐRIZHETŐ |
| E1 — azonosság-állítás | **ELTÉRÉS** | `TSK_VERSSZAM_jelentes.md:28`, N-F54a (3), `tsk_kulcs.py:41-42`: a „86 MT/szamlalas sor létező, azonos számú KJV-vers” még hamis az 1Kir 22:54, Jón 2:11, Ézs 3:27, 1Sám 20:43, 1Sám 24:23 sorra (a KJV-vers nem létezik); a „eltolt párt kap” állítás téves (0 TSK-sor) |
| E2 — N-F54a teljessége | **ELTÉRÉS** | az Ézs 3:1–26 (Károli 3:1 = KJV 2:22), Jón 2:2–10 (Károli 2:9 = KJV 2:8), 1Sám 24:1–22 (Károli 24:2 = KJV 24:1) egészében eltolt azonosságot kap; a lista csak a szomszédokat nevezi meg, az 1Sám 24 és 20:43 hiányzik |
| E3 — oszlopnév | **ELTÉRÉS** (enyhe) | `azonos_szovegu_karoli_vers_tablasora` valójában az azonos *számú* Károli-vers táblasora; a 099456fe címe „Károli-kulcs”, a címkézés KJV-kulcs szerinti |
| Írási halmaz, TSK, jeloltek 7 sor, Δ, render_diff, CI (`futtat.py` exit 0), DT-F114a/b/c, A2, A6 | OK | — |
| Tesztek | NEM ELLENŐRIZHETŐ | parancskörön kívül; kódolvasás alapján összhangban |

## ÖSSZEGZÉS — ELTÉRÉS: 3 tétel (dokumentációs/hatóköri; adatot nem ront, nem regresszió)

1. E1: a szűkített azonosság-állítás még 5 sorra hamis; az „eltolt pár” állítás téves.
2. E2: az N-F54a nem gyűjti az Ézs 3, Jón 2:2–10, 1Sám 24 teljes eltolódását és az 1Sám 20:43-at.
3. E3: félrevezető oszlopnév és commit-cím.
