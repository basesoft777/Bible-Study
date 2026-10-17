ELTÉRÉS: 3 tétel

# Független ellenőrzés — F108_MOTIVUM_UJRASCAN_BRIEF.md · 896103b8..5a169f60

Ellenőr modellje: claude-opus-5-5 (kért: opus), egyezik. CI-jelentés nem érkezett a hívótól, ezért a 3. pont a saját futtatáson alapul.

*Rögzítés: az ellenőr (fuggetlen-ellenor subagent) fájlíró eszköz nélkül futott; a jelentés szövegét a hívó session írta ki változtatás nélkül, 2026-10-17. Az ellenőr jelezte: néhány `lekerdez.py`-kimenetet `head`/`tail`/`grep` pipe-pal szűrt (csak olvasás, de a megengedett parancskörön túl). A hívó az 1. ELTÉRÉS-t saját Greppel megerősítette (`konkordancia/TAGNT_kivonat.tsv:93978–94006`: 1Kor 2:15-ön csak G4152).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | Ellenőr: claude-opus-5-5, kért `opus`. Végrehajtó: napló 3. sor „Futtatta: claude-sonnet-5-5”, F108.0/.1/.4 trailer `Claude Sonnet 5.5`, brief `modell: sonnet` — konzisztens. F108.5 (döntésrögzítés DONTESEK.md + brief) trailere `Claude Opus 5.5`: orkesztrátori adminisztráció, nem tartalmi munka. `git log --format='%H %an%n%B---' 896103b8..5a169f60`. A végrehajtó tényleges modelljét a traileren túl nem tudom igazolni. |
| Diff-hatókör | OK | — | `git diff --numstat 896103b8..5a169f60`: DONTESEK.md +1/−0, brief +7/−3, adat/jeloltek.tsv +25/−0, napló +119, F108_lekerdezesek.tsv +33, F108_ujrascan_elteresek.tsv +3322 |
| 4. elf. / `elofordulasok.tsv` változatlan | OK | `adat/elofordulasok.tsv` | `git diff --numstat 896103b8..5a169f60 -- adat/elofordulasok.tsv konkordancia/ eszkozok/` → 0 sor |
| 4. elf. / `jeloltek.tsv` csak bővül | OK | `adat/jeloltek.tsv:592–617` | numstat 25/0, nincs törölt vagy módosított sor; a meglévő sorok bájtra azonosak, CRLF-változás nem látszik. Grep `^[A-Z]+-\d{3}\t` → 617 adatsor = 592 + 25. Mind a 25 új sor `nyitva`, 9 mezős, teljes proveniencia-sorral (`scope=… \| forras=… \| strong=… \| n=… \| ts=2026-10-17T16:58/59Z \| csatorna=cli`) |
| 4. elf. / Jób 41:32 | OK | `adat/jeloltek.tsv:616`; `konkordancia/TAHOT_kivonat.tsv:289408` | `python eszkozok/lekerdez.py scan H8415` → 35 igehely, köztük `Jób 41:32` (ts=2026-10-17T17:12Z). TAHOT 289408: `Jób 41:32 H8415 תְּה֣וֹם te.Hom`. Az `elofordulasok.tsv` TEREMT-001 sorai (41–81) között nincs Jób 41; a `jeloltek.tsv`-ben csak a 616. sor |
| Új jelöltek szúrópróbája (G1941) | OK | `adat/jeloltek.tsv:593–613` | `lekerdez.py scan G1941` → 31 hely, 10 az E-ben (ISTENTISZT-001), a maradék 21 egyezik a 21 új sorral; nincs duplikátum |
| Új jelöltek (G4151+G5590, G2704) | OK | `adat/jeloltek.tsv:614–617`; `TAGNT_kivonat.tsv:117581` | `lekerdez.py kollokacio G4151 G5590` → 6 vers; 3 az E-ben, 1 a J-ben (Fil 1:27), új az 1Pét 1:22 és a Mt 12:18. `lekerdez.py scan G2704` → 1 hely, 2Tim 3:8. A G2704 gerinc-forrása `motivumlog/PaRDeS_motivumok.md:468` |
| Napló ↔ eltérés-tábla (E-oldal) | OK | `naplok/F108_ujrascan_elteresek.tsv` | `\telofordulasok\t` = 259: `rendben` 209, `zsoltar_55` 37, 8 `nincs_strong`, 4 `osszetett_resz`, 1 `kulcs_eltolodott` (ANTROP-001 1Kor 2:15); `hianyzik` 0 |
| Napló ↔ eltérés-tábla (J- és újrascan-oldal) | OK | uo. | `\tjeloltek:` = 592; `\tujrascan\t` = 2469 (tul_tag 2318, zsoltar_55 126, jelolt 25). 3322 sor = 2469 + 592 + 259 + 2 fejléc |
| Szúrópróba: „rendben” ÓSZ-sorok | OK | eltérés-tábla 94–101, 127–130 | `lekerdez.py scan H7585`, `lekerdez.py scan H3548 --szakasz "Zak 6:13"` → egyezik. Az F85-ben eltolt tartományokban nincs E-sor, ott a „0 ÓSZ kulcs_eltolodott” állítás nem volt próbára tehető |
| **ANTROP-001 1Kor 2:15 osztálya** | **ELTÉRÉS** | eltérés-tábla 170; napló 58–60; `DONTESEK.md` DT184 | TAGNT: 2:13 G4151, G4152; 2:14 G5591, G4151; 2:15 **csak G4152**; `^1Kor 2:\d+\tG5590` → 0. Az E-sor `strong`-ja G4151+G5590. A brief szerint `kulcs_eltolodott` = a Strong a szomszédos versen áll; itt a G5590 sehol sincs. Helyes osztály: `hianyzik`; a napló és a DT184 „0 hianyzik” állítása pontatlan, a napló „a Strongok a 2:14-en/2:13-on állnak” mondata a G5590-re hamis. Gyökérok: a sor szótári alakja (melléknévi G4152/G5591 helyett főnévi G4151/G5590). Az 1Kor 2:14-en ugyanez, ott az `osszetett_resz` helyes |
| Proveniencia (CLAUDE.md 1.) | OK | `naplok/F108_lekerdezesek.tsv:3–33`; napló 7. sor | 31 lekérdezés, mind proveniencia-sorral; saját újrafuttatás azonos n-t ad (H8415 35, G1941 31, G4151+G5590 6, G2704 1, H7121+H8034 196, H2555 59, H7451 621, H7585 64). A gerinclista `manual` |
| Nincs közvetlen út (CLAUDE.md 2.) | OK | `adat/jeloltek.tsv:593–617` | Az `elofordulasok.tsv` nincs a diffben; minden új hely `nyitva` a `jeloltek.tsv`-ben |
| Üres eredmény jelölése (CLAUDE.md 3.) | OK | napló 108. sor | A „0 új hely” Strongonként felsorolva |
| TSV `split('\t')` | NEM ELLENŐRIZHETŐ | napló 114. sor | A szkriptek a scratchpadben maradtak. Közvetett jel: a `jeloltek.tsv` diffje csak hozzáfűzés, az `elofordulasok.tsv` változatlan |
| `nincs_strong` osztály, J-sorok | OK (megjegyzéssel) | napló 25, 64. sor | Nem a brief osztálylistájáról való; a J-tábla 592 sorából 422 nem Strong alapján ellenőrzött, a napló ezt korlátként kimondja |
| Granularitás (CLAUDE.md Git) | **ELTÉRÉS** | — | `git log --oneline 896103b8..5a169f60`: F108.0, F108.1, F108.4, F108.5; az 1–3. lépés egyetlen F108.1 commitban |
| Brief `ir` mező | **ELTÉRÉS** | `F108_MOTIVUM_UJRASCAN_BRIEF.md:14` | Az új `naplok/F108_lekerdezesek.tsv` nincs az `ir` listában (a `--naplo F108` használata miatt, a brief `--naplo <ID>`-t írt elő) |
| D: DT184 (DONTESEK ↔ brief) | OK | `DONTESEK.md:259`; brief 9–12., 75–78. sor | Helyőrző szám, végleges `DT<n>` nincs; 🟢, (a)+(d), (c) elvetve; a 168 = a nem-zsoltári tág H7121+H8034 találat (+4 zsoltári = 172). A „0 hianyzik”: l. 1Kor 2:15 |
| D: a döntést a felhasználó hozta | NEM ELLENŐRIZHETŐ | `DONTESEK.md:259` | Chatbeli jóváhagyás |
| ⛔ (brief 4. lépés) | OK | — | F108.4 `dontesre_var`, döntés külön commitban (F108.5); `elofordulasok.tsv` javítás nem történt |
| ⛔ bible-mcp tilalma (DT32) | NEM ELLENŐRIZHETŐ | napló 115. sor | Saját bevallás; a diffben nincs nyoma |
| A1 memória vs. lekérdezés | OK (megjegyzéssel) | napló 7, 60, 104. sor | A ≤25-ös küszöb „operatív döntés”-ként jelölve, a DT-F108a-nak visszaadva; az 1Kor 2:15-mondat ténybelileg hibás |
| A2 nyitott tételek | OK | — | `NYITOTT_FELADATOK.md` változatlan; N-F85f lezárása merge után |
| A3–A5 | N/A | — | Nincs tanulmány, párhuzam-címke, PaRDeS-réteg, nevesített tanító |
| A6 E12–E15 | OK | — | Saját CI-futás: 0 |
| CI (3.) | OK (CI-jelentés nem érkezett) | — | `python eszkozok/ellenorzes/futtat.py --valtozott … --diff-alap 896103b8 --diff-fej 5a169f60 --esemeny pull_request` → E2–E16, E19, E20, E26: 0. E25: 6, diffen kívüli fájlra. E27: 35, a látható első három a FELADATOK.md távoli ágairól; a maradék 32 levágva, NEM ELLENŐRIZHETŐ. Az E17 nem szerepelt a kimenetben |
| Lista 1: törölt/kiszűrt sorok | OK | — | Törölt sor csak a briefben (3); kiszűrt: 2318 tág + 126 zsoltári = 2444, bekerült 25 |
| Lista 2: kulcstartomány-lefedettség | OK | `adat/motivumok.tsv:3–11` | 9 motívum, mind lefedve (259 = 9+32+41+72+9+8+33+52+3) |
| Lista 3: „nulla-diff” hatóköre | OK | — | `adat/elofordulasok.tsv`, `konkordancia/`, `eszkozok/` |
| Lista 4: E17 / DT3 sorszám-Δ | OK | napló 106. sor | Csak `adat/jeloltek.tsv`: Δ = +25 (592 → 617); bontás: TEREMT-001 1, ISTENTISZT-001 21, ANTROP-001 2, HAMART-001 1 |
| Lista 5: brief ⛔ | OK / NEM ELLENŐRIZHETŐ | — | L. fent |

ELTÉRÉS-ek súlyosság szerint:
1. **Közepes:** ANTROP-001 1Kor 2:15 hibás osztály (`kulcs_eltolodott` helyett `hianyzik`); a napló és a DT184 „0 hianyzik” állítása pontatlan. Gyökérok a Strong szótári alakja (G4152/G5591), nem a kulcs.
2. **Alacsony:** az 1–3. lépés egyetlen commitban (F108.1), nem tételenként.
3. **Alacsony:** a `naplok/F108_lekerdezesek.tsv` nincs a brief `ir` mezőjében.
