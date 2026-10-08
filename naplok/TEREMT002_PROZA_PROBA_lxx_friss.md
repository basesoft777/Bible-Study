# F64 M1 — LXX friss futás és a régi audit-sorok eltérése (munkajegyzet)

*FELADATOK #64 · `F64_TEREMT002_PROZA_PROBA_BRIEF.md` M1 · DT69 (1) · ág `claude/f64-teremt002-proza-proba` · 2026.10.08 · a mérési jelentés (M3) és a #12b bemenete; nem döntés*

A próza (`motivumok/TEREMT-002.md`, 2. pont „Septuaginta”) LXX-állításai a három előfordulás-versre futtatott friss `python eszkozok/lekerdez.py lxx-hid "<igehely>"` lekérdezésen állnak (`LXX_OS`). Az `adat/auditok.tsv` nem változott (DT69); a régi sorok a #42 óta kivezetett `LXX_kivonat_*.tsv`-re mutatnak. Az összevetés oszlopai a `naplok/FORRASKIVEZETES_M5_eltereslista.tsv` szerint (`eszkozok/lxx_osszevetes.py` docstring): kategória, régi / új szószám, Jaccard, csak a régiben / csak az újban álló Strong-ok.

## 1. A három előfordulás-vers

| Igehely | Régi audit-sor (`auditok.tsv`) | Friss futás | Eltéréslista | Csak régi | Csak új |
|---|---|---|---|---|---|
| 1Móz 1:2 | `scope=range:1Móz 1:2 \| forras=LXX_kivonat_Genezis.tsv+TAGNT_kivonat.tsv \| n=19 \| ts=2026-09-25T11:03Z` | `scope=range:1Móz 1:2 \| forras=LXX_OS/genesis.tsv+TAGNT_kivonat.tsv \| n=19 \| ts=2026-10-08T06:21Z` | `strong_eltero`, 19/19, 0,85 | G0180, G1065 | G1093 |
| Jer 4:23 | `scope=range:Jer 4:23 \| forras=LXX_kivonat_Jeremias.tsv+TAGNT_kivonat.tsv \| n=17 \| ts=2026-09-25T11:03Z` | `scope=range:Jer 4:23 \| forras=LXX_OS/jeremiah-lxx.tsv+TAGNT_kivonat.tsv \| n=17 \| ts=2026-10-08T06:21Z` | `nagy_eltero`, 17/17, 0,79 | G1065, G3364 | G1093, G3756 |
| Ézs 34:11 | `scope=range:Ézs 34:11 \| forras=LXX_kivonat_Ezsaias.tsv+TAGNT_kivonat.tsv \| n=23 \| ts=2026-09-25T11:03Z` | `scope=range:Ézs 34:11 \| forras=LXX_OS/isaiah.tsv+TAGNT_kivonat.tsv \| n=23 \| ts=2026-10-08T06:22Z` | `strong_eltero`, 23/23, 0,89 | G3685 | G2730 |

**A próza szempontjából:** az eltérés a Strong-címkézésben van, a szószám mindhárom versben azonos. A friss futásban a γῆ/γῆν G1093 (a régiben a multihalmazban helyette G1065 áll), a Jer 4:23 tagadószava οὐκ G3756 (régi: G3364), az Ézs 34:11 κατοικήσουσιν G2730 (régi: G3685). *Az egyes régi címkék szóhoz rendelése a multihalmaz-különbségből következtetett, nem lekérdezett.* Az 1Móz 1:2 ἀκατασκεύαστος szava a friss futásban **Strong-szám nélkül** áll; a régi multihalmazban egy ott nem szereplő G0180 van — valószínűleg ennek a szónak a régi címkéje (következtetés). A friss futásból ezért az ἀκατασκεύαστος ÚSZ-előfordulása nem számolható (üres, nem negatív lelet).

**A pár fordítása változatlan:** a `naplok/T1_TEREMT002_scan.md` 5. pontjának (2026.09.25, régi forrás) három fordítása — ἀόρατος καὶ ἀκατασκεύαστος; οὐθέν; σπαρτίον γεωμετρίας ἐρήμου — a friss futásban szóra azonos. A scan.md ÚSZ-híd példája (G0517 → Kol 1:15, Róm 1:20) a friss futásban is áll (G0517: 5 ÚSZ-vers: 1Tim 1:17, Kol 1:15, Kol 1:16, Róm 1:20, Zsid 11:27). A próza egyetlen állítása sem a régi Strong-címkén áll.

**Ami a régi auditban nem látszott:** a friss Ézs 34:11 LXX-vers állatlistája (ὄρνεα, ἐχῖνοι, ἴβεις, κόρακες, ὀνοκένταυροι) eltér a héberétől, és a *bohu*-köveknek (אַבְנֵי־בֹהוּ) nincs görög megfelelője a versben. A próza ezt rögzíti (2. pont).

## 2. A többi 55 régi `lxx-hid` audit-sor

A TEREMT-002 58 régi `lxx-hid` sorából 55 a jelöltek (elutasított kereszthivatkozás- és önálló *tohu*-versek) versein futott; forrásonként: Ézsaiás 21 (ebből 1 a fenti), Ezékiel 7, Jóel 5, Zsoltárok 5, Jób 4, Jeremiás 3 (1), Genezis 2 (1), Malakiás 2, a többi könyv 1–1.
`scope=adat/auditok.tsv, LXX_kivonat-forrású sorok | forras=adat/auditok.tsv (grep) | n=58 | ts=2026-10-08`

Ezeket a #64 nem futtatta újra: a próza a jelölt-versekről LXX-állítást nem tesz. Az öt zsoltár-sor az eltéréslista szerint: Zsolt 80:6 és 80:7 `zsoltar_eltolas` (a régi kivonat egy verssel eltolt, N17), Zsolt 104:30 `strong_eltero`, Zsolt 107:40 `nagy_eltero`, a Zsolt 33:6 nincs a listán (azonos). *Pontosítás az M0-hoz:* az M0 5. pontja mind az öt zsoltár-sort az eltolásra épülőnek írta; a lista szerint ez kettőre áll.
`scope=Zsolt 33:6, 80:6, 80:7, 104:30, 107:40 | forras=naplok/FORRASKIVEZETES_M5_eltereslista.tsv | n=4 | ts=2026-10-08`

## 3. A #12b-nek

- A „függő (#12b)” LXX-helyek: **1Móz 1:2, Jer 4:23, Ézs 34:11** (a próza 2. pontja és a Kivonat).
- A régi 58 audit-sor forrása kivezetett fájl; ha a #12b az `auditok.tsv`-re épít, a három előfordulás-vers sorait a friss futással kell újraírni (a #64 nem írja, DT69).
- Az ἀκατασκεύαστος Strong-hiánya az LXX_OS-ben: a lexikonoldal LXX-szakasza erre a szóra Strong-alapú hidat nem tud adni.
