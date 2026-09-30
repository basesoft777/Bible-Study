# ELLENOR_F21P_3.md — F21_KAROLI_STRONG_PILOT_BRIEF.md · 3. kör (P3b) · `d992d0b..4e95af4`

*A `fuggetlen-ellenor` 3. körös jelentése; a fájlba az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze), a táblázat a jelentés szövegét adja, a hosszú számtételes cellák rövidítésével. Saját commitok: e88de8d, d6539df, eade0f5, 044db60, 64cb6c1, cac96c6 [bot], b6cd350, 44e62f2, d15ac1a, cba5abb; merge 4e95af4. Ítélet: **NEM TISZTA** — hiba: nincs; figyelmeztetés: 1; megjegyzés: 6. A szkriptek újrafuttatása és a prompt-hashek újraszámolása a szerepkorlát miatt nem volt ellenőrizhető; minden számot kézzel ellenőrzött a `futasnaplo.tsv`-ből és a generált TSV-kből.*

| pont | eredmény | indok |
|---|---|---|
| 1a P3b-sorok a naplóban | OK | `f21p/futasnaplo.tsv:170-346`: F1V2 170–209, F2V2 210–247, F5V2 248–267, F6V2 268–286, F3V2B 287–312, F4V2 313–346; a `prompt_sha256_12` minden v2-es sorban `a9f0f07c67b9`, az F4V2-ben `c6eae95e6ca5`. A hashek újraszámolása NEM ELLENŐRIZHETŐ. |
| 1b költség futásonként | OK | F1V2 0,137698; F2V2 0,032072; F5V2 0,072390; F6V2 0,012887; F3V2B 0,256110; F4V2 0,359317 (34 soros kézi összeg 0,359316); P3b összesen 0,870474; kumulatív **1,605068 USD** ≤ 2 (megállási küszöb) ≤ 3 (plafon). |
| 1c kapuhiba a naplóból | OK (az F4V2 kivételével, l. 3b) | Első próbálkozások `kapuhiba_db`: F1V2 160/200, F2V2 141/200, F5V2 72/100, F6V2 57/100, F3V2B 28/200; végleges: F1V2 84, F2V2 55, F5V2 48, F6V2 24, F3V2B 0; egyezik a jelentéssel. |
| 2 befagyasztás, régi kimenetek | OK | `git diff --numstat d992d0b..HEAD` a befagyasztott fájlokon és a régi válaszokon: 0; a `futasnaplo.tsv`: csak hozzáadás (177 0); a bot-commit csak `f21p/futasnaplo.tsv` és `f21p/valaszok/*V2*.jsonl`. |
| 3a F4V2-feltételek a kódban | OK | `futtat.py`: a `biro_utasitas` az alapprompt utasításrészét cseréli a `prompt_v2`-re; a `biro_rogzites` az A∩B linkeket, a `biro_kenyszer` a 6a/6b pontot adja; a `valasz_ellenoriz_futashoz` a kapu 5 pontja után a 6. pontot is alkalmazza; kapuhibás A/B esetén nincs rögzítés (dokumentált). |
| 3b F4V2 első próbás kapuhibája | **figyelmeztetés** | A jelentés és a TSV szerint első próbára 27/193, de a napló `kapuhiba_db` összege az első próbálkozásoknál 41 (41 vers kapott újrakérést). Ok: a `meres.hibatipusok` csak az ötpontos kaput futtatta újra, a 6. pontot (rögzítés) nem. Következmény: legalább 14 versben a C első válasza megsértette az A–B rögzítést; a végleges 0, de a jelentés ezt nem mondta ki, és az első próbás arányt 14,0%-nak adta 21,2% helyett. **Javítva (F21.31):** a teljes kapun számolt első próbás arány 41/193 (21,2%), kapupontonként (1: 4, 1-json: 20, 3: 2, 4: 1, 6: 14), EGYEZIK keresztellenőrző sorral. |
| 3c mentett F4V2-válaszok | OK | 193 `ok`, 0 `kapuhiba`, 0 nem üres `hibak`. |
| 3d nincs modell által írt Strong (K5) | OK | Grep `\b[HG]\d{3,4}[a-zA-Z]?\b` az F1V2, F2V2, F3V2, F3V2B, F4V2, F5V2, F6V2 fájlokban: 0 találat. |
| 4 számok (több mint 12 egyezés) | OK | A+B+C 85,7455 [79,6322–92,3303]; rétegösszeg 41,1791+7,5782+16,6169+20,3713 = 85,7455; A+B 27,9545; F3V2 1020/1090 = 93,58%; F3V2B 1025/1102 = 93,01%; lefedettség 1020/1051 és 1025/1051; A+B alacsony 2617/3754 = 69,7% és 781/1139 = 68,6%; A+B+C alacsony 2086/3493 = 59,7% és 616/1064 = 57,9%; régi arany A+B 18/32 és 18/30, A+B+C 28/32 és 28/30; Δ −0,57 pp [−1,64; +0,53]; F4V2 193 vers = 95+25+25+48; magas 338 + közepes 70 + alacsony 581 = 989; KJV 59/63, 71/91, különbség 15,63 pp, relatív eltérés-csökkenés −65,6%. |
| 5a minősítés megalapozottsága | OK | A+B: (1) magas 338/358 = 94,4% < 98%, (2) 64,5%, (3) 56,2/60,0%, (5) 69,7% bukott; (4) 29,15 ≤ 60 teljesül. A+B+C: (1) 94,4%, (2) 94,1%, (3) 87,5/93,3%, (4) 92,33 > 60, (5) 59,7% (alt: 27,9%): mind bukott. A minősítés az (1) miatt az értelmezéstől és az alt olvasattól függetlenül áll. |
| 5b értelmezés mint nyitott tétel | megjegyzés | Az A+B döntőbíró nélküli meghatározása és a G4 „kapuhibás” ág két olvasata jelölt a jelentésben, de nyitott tételként (DT, jelentés (e)) nem szerepelt. **Javítva:** DONTESEK DT21 k), jelentés (e). |
| 5c PD6 és a korrigált érték | OK | `megfelelt/nem felel meg` kizárólag A+B vagy A+B+C sorban; a korrigált és (c) érték „Opus-besorolás, nem mérés” jelöléssel. |
| 6 KJV a v2-adaton | megjegyzés | A jelentés helyes, de a `lezarva_osszegzes` és a zárás nem mondta ki, hogy az N29 VAGY-szabályának 1. mérőszáma formálisan teljesül (alulállítás). **Javítva.** |
| 7a brief | OK | `allapot: lezarva`, `ag`, `pr: #92`, `lezarva_osszegzes` egy sor; PD11, v1.3, v1.4 megvan. |
| 7b összegzések egymás között | megjegyzés | A C két futásának eltérése a briefben ±0,5 pp, a zárásban ±0,6 pp (a mért: −0,57 pp pontosság, +0,48 pp lefedettség). **Javítva** (egységesen a két mért érték). |
| 7c DONTESEK | megjegyzés | A DT5, DT6, DT7, DT18 sértetlen, a DT21 🟡, a DT22 ✅; a DT21 kérdésszövegében elavult állítás maradt („az A+B+C nem mért”). **Javítva.** |
| 7d FELADATOK, adat, konkordancia | OK | `git diff --numstat origin/main..HEAD -- adat konkordancia FELADATOK.md` → 0. |
| 8a proveniencia a generált kimenetekben | OK | `F21P_meres_p3b.md`, `F21P_C_diff_F3V2B.md`, `F21P_jelentes.md`, `meres_p3b_eredmeny.tsv`, `koltseg_vetites_p3b.tsv`, `F21P_arany_szuroproba.md`: `scope … forras … ts` megvan. |
| 8b `c_diff_f3v2b_besorolas.tsv` | megjegyzés | Nincs fejléc és proveniencia (kézi Opus-besorolás, `manual` jelölés járna). **Javítva (F21.31):** `# MANUAL:` fejlécsor mind a négy kézi besorolásfájlon. |
| 8c csv, wrapper, normalizálás | OK | `import csv` 0 találat; az utf-8 wrapper mindhárom új szkriptben megvan. |
| 8d kulcs-grep | OK | 0 találat. |
| 8e workflow | OK | `git diff d992d0b..HEAD`: csak +8 kommentsor; a jogosultságok, a push-feltételek és a kulcs helye változatlan. |
| 9 CI | OK | `eszkozok/ellenorzes/futtat.py … --pr-cim "[ELLENŐRZŐ] F21: …"` → minden szabály 0 találat. |
| Régi P3-számok a jelentésben | OK | A jelentés törölt sorai csak címsorok, a fejléc és két következmény-mondat; a 0,734594 átkerült a :316 sorba. |
| Szkriptek újrafuttatása, bájtazonosság, prompt-hashek | NEM ELLENŐRIZHETŐ | Szerepkorlát. |
| A1–A6, ellenőrzőlista 1–5 | OK / n.é. | A1 OK (l. 5b); A2 OK; A3–A5 n.é.; A6 OK; ellenőrzőlista 1–5 OK. |
| Régi commit-üzenetek (75496f0, 6d94610, ac6fb49) | megjegyzés, elfogadva | A történet nem íródik át. |

**Eltérések súlyossági sorrendben** (hiba: nincs; figyelmeztetés: 1; megjegyzés: 6): (1) F4V2 első próbás kapuhibája (javítva); (2) az értelmezések nem voltak nyitott tételként felvéve (javítva); (3) a KJV-szabály 1. mérőszáma nem volt kimondva (javítva); (4) ±0,5/±0,6 pp eltérés (javítva); (5) a DT21 elavult szövege (javítva); (6) a kézi besorolás proveniencia-jelölése (javítva); (7) ékezet nélküli régi commit-üzenetek (elfogadva).

**NEM TISZTA** (a megállapítások az orkesztrátor szerint javítva; a javítás ellenőrzése a 4. körben)
