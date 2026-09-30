# ELLENOR_F21P_2.md — F21_KAROLI_STRONG_PILOT_BRIEF.md · 2. kör · `ac6fb49..bb229b6`

*A `fuggetlen-ellenor` 2. körös jelentése (commitok: 725ddf8, 61f28e7, bb229b6; a teljes ág: `origin/main...bb229b6`). A fájlba az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze). Ítélet: **NEM TISZTA** — hiba: nincs; figyelmeztetés: nincs; megjegyzés: 2. Az 1. kör (`ELLENOR_F21P.md`) nyolc javítási pontja mind rendben van, egyetlen szám sem változott. A szkriptek újrafuttatása a szerepkorlát miatt most sem volt ellenőrizhető.*

| pont | eredmény | indok |
|---|---|---|
| (1) régi arany, mindkét érték | OK | A jelentésben és a `F21P_meres_v2.md` b) szakaszában: kizárás nélkül 93,8% (30/32) „a 95% alatt”, a PD9 szerinti kizárással 100,0% (30/30); a kizárás a futás után, a C két nem-egyezése alapján történt; az 1Móz 13:4 vitatható/hibás. DT21 i). |
| (2) A+B+C „nem mért (PD8)” | OK | Vezető mondat, (a) tábla, brief `lezarva_osszegzes`, DT21. |
| (3) kapuhiba mint megfigyelés; A+B régi arany | OK | A (b) címe „csak a rögzített öt feltétel”; „Megfigyelés (nem feltétel)”: 41,0% (82/200), 76,0% (152/200), 53,0% (106/200), 197/200; A+B régi arany 60,0% (3/5) bukott. |
| (4) P-K4, (b2) vs. `meres_eredmeny.tsv` | OK | 13 szám egyezik (A R1 pontosság 129/161; A∩B R1 52/61; A∪B R4 pontosság 101/142; A∩B régi arany 3/5; A–B link_egyezés R1 93/286, R3 219/453, Összes 748/1413; F6 R1 végleges kapuhiba 13/100; nem_egyező linkarány 665/1413 stb.); kézi aritmetika rendben (1413−748 = 665; 62+53+53+29 = 197). |
| (5) proveniencia | OK | 10/10 generált fejlécben `scope … forras … ts`. |
| (5b) proveniencia: `F21P_arany_szuroproba.md` | **megjegyzés** (új lelet) | A fájlból hiányzott a proveniencia-sor. **Javítva** az orkesztrátor által (F21.22): a `szuroproba.py` GENERÁLT-fejlécet ír `scope`/`forras`/`ts`-sel. |
| (6) P5 „Eltérés a brieftől” | OK | A bootstrap egysége a 10 verses köteg, DT21 f) nyitott, nincs jóváhagyva. |
| (7) `lezarva_osszegzes` intervallumai | OK | F3 42 USD (90%: 38–47), F3V2 42 USD (90%: 38–46); egyezik a `koltseg_vetites.tsv`-vel. |
| (8) gondolkodási mód a korlátok között | OK | Új sor: A/B kikapcsolva, C `minimal`; az F1–F6 `gondolkodas_token=0` nem mérés. DT21 j). |
| Régi számok megvannak? | OK | A jelentés mind a 11 törölt sorának új változata megtartja a régi számokat; minden más változás fejléc, új sor vagy új szakasz. |
| Generált TSV-k számai | OK | Fájlonként 1 sor változott (fejléc); a `meres_eredmeny.tsv` érintetlen. |
| Szkript-változások | OK | Csak fejléc-szöveg, új `tokenek.generalas_ts()`, új magyarázó bekezdés és küszöb-viszony sor a `meres_v2`-ben; számítási logika nem változott. |
| Adat-, bemenet- és aranyfájlok érintetlenek | OK | `git diff --numstat ac6fb49..HEAD -- adat konkordancia FELADATOK.md f21p/valaszok f21p/futasnaplo.tsv f21p/arany_opus.jsonl f21p/arany_opus_v2.jsonl` → 0. Az arany v2 sha256-ját az orkesztrátor ellenőrizte (egyezik az `f21p/arany_opus_v2.sha256`-tal). |
| DT18 fájlvégi újsor | OK | Pótolva. |
| Kulcs-grep | OK | 0 találat. |
| CI (saját futtatás) | NEM ELLENŐRIZHETŐ (feltételes) | Egyetlen találat E16 (PR-cím nélkül); `--pr-cim "[ELLENŐRZŐ] F21: …"`-mal nincs találat. |
| Szkriptek újrafuttatása, bájtazonosság | NEM ELLENŐRIZHETŐ | Szerepkorlát. Közvetett jel: a generált TSV-k törzse bájtra azonos, csak a `ts`-fejléc változott. |
| Ékezet nélküli commit-üzenetek (75496f0, 6d94610, ac6fb49) | megjegyzés, elfogadva | A történet nem íródik át; az új commitok ékezetesek. |
| Ellenőrzőlista 1–5 | OK | Törlés csak a jelentésben (11 sor, mind átfogalmazva), DONTESEK 2, brief 1 sor; adat/ nem változott; új ⛔ nincs. |

**Megjegyzések súlyossági sorrendben:** (1) a szúrópróba-fájl proveniencia-sora hiányzott (javítva, F21.22); (2) három régi commit-üzenet ékezet nélküli (elfogadva).

**NEM TISZTA** (csak megjegyzés-szintű eltérésekkel; az (1) javítva, a (2) elfogadva)
