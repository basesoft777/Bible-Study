# ELLENŐR — célzott újraellenőrzés: #99 BDB_SZELETELO

*A `fuggetlen-ellenor` subagent jelentése (claude-opus-5-5, a kért `opus`); az ellenőrnek nincs író eszköze, a jelentést az orkesztrátor mentette. Hatókör: a `naplok/ELLENOR_F99.md` 1–6. és 8–10. pontja (a 7. az M3 tervezetébe ment); a vizsgált javítások `b2df5df5..8129ebbf` (F99.33–F99.44). A generátort, a teszteket és a hash-számítást nem futtatta.*

**Eredmény: ELTÉRÉS, 3 tétel.**

| pont | eredmény | lényeg |
|---|---|---|
| 1a Ézs 3 próba | OK | `lekerdez.py karoli "Ézs 3:1"` → az MT 2:22 szövege; `scan H0113 --szakasz "Ézs 3"` → csak 3:2; a tábla H0113 „3:1” sora MT Ézs 3:1 → Károli 3:2 (`adat/bdb_vers_jelentes.tsv:1358`); 8/8 szúrópróba (H2952, H3308, H3427, H4384, H4100, H4421, H4595, H3519). |
| 1b Ézs 3 és DT173 (b) | **ELTÉRÉS (döntés kell)** | Az adat helyes, de a forrása nem fér a (b)-be: az F85 az Ézs 3-ról csak rögzíti, hogy a Macula hibás (`F85_macula_elvetve.tsv:3`, `F85_jelentes.md:46`), MT → Károli megfeleltetést nem ad; az `F85_esetlista.tsv`-ben nincs Ézs 3-sor. A +1 eltolás a Károli-szövegből jön (kód és SEMA kimondja), kb. 218 sor (209 + 9) új forrásból, új döntési sor nélkül; a DT173 „Alkalmazva” része még az F99.29 állapotát írja. Opciók: (a) a DT173 kiegészítése helyőrzős tétellel (Ézs 3: Károli-szöveg + TAHOT forrás), (b) az Ézs 3 vissza az N-F99e-be, a régi kulccsal. |
| 1c Dán 4 (az F99.29 hibája) | OK | Az F85 esetlista szerint WLC Dán 3:31–4:34 → Károli azonos szám; kb. 590 sor mt = karoli; `scan H7624` → 4:31, 4:34. A régi hiba nincs jelen. |
| 1d Hós 2 | OK | MT 2:1 → K 1:10, 2:2–3 → K 1:11, 2:n → K 2:(n−3); szúrópróbák (H1180, H0781, H6030) egyeznek; az M223 (H8034) most Hós 2:16, `sigla_igazolt`. |
| 1e Ézs 64, Én 6/7, Hós 14 | OK | szúrópróbák egyeznek; a korábbi F85-fejezetek is. |
| 1f TAHOT-arányok | NEM ELLENŐRIZHETŐ (teljes) / OK (minta) | 22 soros saját mintán 22/22. |
| 1g maradék | OK | 1Krón 12, 5Móz 5 a régi kulcson, N-F99e-ben rögzítve. |
| 2 szűrés hamis poz./neg. | OK | a kulcs és a vak kitöltések egyeznek a napló 9.14 tábláival (3/25 hamis pozitív: M001, M109, M159; 7/22 hamis negatív; 1/3 M223); a H2623, H4912, H8034 és a 7 `sigla_igazolt` sor a javítási tervezetben. Módszertani megjegyzés: az (A) oszlop a `nem_bibliai`-ból öröklődő sorokra „nem alkalmazható”. |
| 3 LF-hash, bájt-teszt | OK (kód) / NEM ELLENŐRIZHETŐ (futás) | `fajl_hash` CRLF→LF után számol; a skip-feltétel megszűnt. |
| 4 fejléc proveniencia | OK | minden bemenet hash-sel (BDB, Macula 39 fájl, versmegfeleltetés, Karoli_1908, F85_macula_elvetve, F85_esetlista, OSHL, Strong_szotar, TAHOT); a kód-hash négy fájlt fed. A hash-értékek helyessége NEM ELLENŐRIZHETŐ. |
| 5 H3027 pilot-teszt | OK | az elvárás az aranyminta szerinti, `ISMERT_HIBA` ággal. |
| 6 licenc | OK | az OSHL és a TAHOT (CC BY 4.0) az `ADAT_LICENC`-ben; a `datasetek.tsv` +4 sor, sorvég-csere nincs a blobban. |
| 8 nyitott tételek | OK | N-F99a–e; az N-F99d sorai (`:48750`, `:28077`, `:28087`) a Neh 7:68-on. |
| 9 megjegyzés | OK | összhangban a kóddal. |
| 10a `ir` | OK a mai diffre / **ELTÉRÉS** | a `naplok/ELLENOR_F99_ujra.md` nincs az `ir`-ben. |
| 10b–g | OK | zárónapló őszinte; DT170 és DT177 helyesbítés négy helyen; a brief-tervezetek `nem_indult`, a `FELADATOK.md` érintetlen. Megjegyzés: a javítási tervezet `olvas` mezője az elavult `F85_kulcsvaltas.tsv`-t sorolja. |
| 10c napló összegző számai | **ELTÉRÉS** | `BDB_SZELETELO_M0.md:22-23` elavult. Mért: `szurt=1` 528 (napló 531), `atkulcsolt_f85` 2 992 (1 099), `azonos_tahot` 551 (645), `nincs_karoli` 201 (234), Károli-vers 159 187 (159 151). A 9.13 „514 sor” igaz, de a tábla 1 894 sora változott (kb. 1 379 csak címkeváltás). |
| CI | OK (saját futás) | E2–E16, E19, E20, E26: 0; E25: 6, E27: 35 (régi, a diffen kívül). CI-jelentéssel való összevetés NEM ELLENŐRIZHETŐ. |
| L1–L5 | OK | Δ0 a tartományban; a tábla +160 616 / aranyminta +658 / `datasetek.tsv` +4 / OSHL 0; nincs befogadás, merge vagy `FELADATOK.md`-írás. |

## ELTÉRÉS-ek súlyosság szerint
1. Az Ézs 3 forrása kívül esik a DT173 (b)-n (kb. 218 sor), és a DT173 „Alkalmazva” része elavult. Az adat helyes (TAHOT és Károli-szöveg igazolja), ezért nem a visszavonást javasolja, hanem felhasználói döntést.
2. A napló 0. összegzésének számai elavultak (`BDB_SZELETELO_M0.md:22-23`); a 9.13 nem bontja az 1 894 változott sort.
3. A brief `ir` mezőjéből hiányzik a `naplok/ELLENOR_F99_ujra.md`.

NEM ELLENŐRIZHETŐ: a fejléc-hashek értéke és a bájtazonos újragenerálás; a tesztek futása; a teljes TAHOT-megerősítési arányok; az E27 csonkolt 32 sora; a CI-jelentéssel való összevetés. A merge-ről a felhasználó dönt.
