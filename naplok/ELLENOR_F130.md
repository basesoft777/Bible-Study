ELTÉRÉS: 7 tétel

# ELLENOR_F130 — F130_TANITOI_KERESES_ISTENTISZT_BRIEF.md · origin/main (8a55586d)..HEAD (a95ecb2a)

*A `fuggetlen-ellenor` subagent jelentése; a fájlt az orkesztrátor írta le, mert az ellenőrnek nincs fájlíró eszköze. Az ellenőr tényleges modellje: `claude-opus-5-5` (a kért: `opus`, egyezik).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 / modell-mezők | ELTÉRÉS | `naplok/F130_TANITOI_KERESES_ISTENTISZT_naplo.md:3,7`; commit 02f4d302 | Az F130.2a (DONTESEK) commit `Co-Authored-By: Claude Sonnet 5.5`, holott a brief modellje `opus`, a többi hat commit Opus. Az M4-ben forrást megnyitó Sonnet subagent tényleges modellneve sehol nincs rögzítve, a napló csak „friss Sonnet subagent”-et ír. A tanítói fájl `Modell` mezője (`:14`) összhangban van a `.claude/agents/tanito-kereso.md:5` `model: sonnet` értékével. A subagent tényleges nevét a repó nem őrzi: NEM ELLENŐRIZHETŐ. |
| Elf. 1 (7. sablon, négy pont) | OK | `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md:9–150` | Megvan a Fejléc, az 1. Kiinduló motívum-kivonat, a 2. Névsor, a 3. Keresések és a 4. Összegzés. A `Dátum` 2026.10.20, nem `manual`. |
| Elf. 2 (✅/⚠️: mű, hely, URL, dátum) | OK, megjegyzéssel | uo. `:70–75` | Mind a 6 ⚠️ sorban van mű, sorozat/rész/kód, URL, lekérési dátum. A 71–74. sor belső helye csak „átirat”, a pontos hely a sorozatrész. M4: a napló 1–7. sora (`naplok/F130_…_naplo.md:13–21`). |
| Elf. 2 / URL-elérhetőség mintán | NEM ELLENŐRIZHETŐ | — | Az ellenőr parancskörében nincs webes lekérés. |
| Elf. 3 (gap explicit) | OK | uo. `:76,82,88–120,124–150` | A meg nem nyitott forrás (`devotionals/c-r022-038`, Rhema 403, olvashatatlan PDF) nincs ✅/⚠️-ként felvéve. |
| Elf. 4 (archívum bájtra) | OK | `archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md:1` | Az egyetlen eltérés az `ARCHÍV` 1. sor; a bfd94bdb a main változata. |
| Elf. 5 (nincs rés-jelölő, lexikon nem változott) | OK | — | `RÉS-` a tanítói fájlban: 0; `git diff --stat origin/main..HEAD -- lexikon/ adat/ konkordancia/`: üres. |
| Elf. 6 (ISTENTISZT-001.md csak 376/378/380) | OK | `motivumok/ISTENTISZT-001.md:376,378,380` | Három hunk, numstat 3/3, az új szöveg szó szerint a napló javaslata (`naplo:38–46`). A jóváhagyás a repóban csak közvetítve áll: NEM ELLENŐRIZHETŐ. |
| Elf. 7 / CI | ELTÉRÉS | `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md:0` | `python eszkozok/ellenorzes/futtat.py --valtozott <a 6 fájl> --diff-alap origin/main --diff-fej HEAD`: **E5 HIBA: 3** — törölt címsor „TÖRLÉS-SZÁNDÉKOS:” jelölés nélkül (`## Eredet`; `## Az átvett eredmény …`; `### A nevesített tanítói egyezés-keresés eredménye …`). `git log origin/main..HEAD -i --grep=SZÁNDÉKOS --grep=SZANDEKOS`: 0 commit. Az F130.3 „SÉRTÉS 0” állítása ezt nem fedi. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | Nem volt CI-jelentés. |
| DT-F130a / b | OK | `F127_LEXIKON_HALO_RES_BRIEF.md:14` | `fugg: [126, 130]`; az archiválás nem törlés. |
| DT-F130c (egyeztetett eltérés) | ELTÉRÉS (forma) | `DONTESEK.md:348` | A „Felhasználó, 2026-10-20 (chat): 1.” a javaslat-oszlopba került és felülírta az „a felhasználó dönt az M4 előtt” szöveget; a döntés-oszlop `—` maradt (a DT270–272 sorokban a döntés a 7. oszlopban áll). Sorrend: az M4 (71348f7f) a döntés rögzítése (02f4d302) előtt készült. |
| A1 (memória vs. lekérdezés) | ELTÉRÉS | `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md:56` | Az indoklás: „nincs ismert, a motívumhoz … köthető dedikált tanításuk” — öt jóváhagyott tanítót (Osborn, Kuhlman, Lindsay, Savelle, Price) hagy ki keresés nélkül, emlékezetből tett hiányállítással, értelmezésként nem jelölve. |
| A1 / „32 igehely (22 ÓSZ, 10 ÚSZ)” | OK | uo. `:22` | `elofordulasok.tsv`: 32 sor, ebből ÚSZ 10. A 2Móz 33:19 és 34:5 a study saját B-esete. |
| A1 / verzifikáció | ELTÉRÉS | uo. `:26` | `lekerdez.py karoli "Jóel 2:32"` a „De mindaz, a ki az Úrnak nevét hívja segítségül…” szöveget adja; a „Jóel 3:5” egészen más vers. A „Jóel 2:32 (Károli 3:5)” jelölés hibás; a study szerint a 3:5 az MT-számozás (`motivumok/ISTENTISZT-001.md:41`). Helyes: „Jóel 2:32 (MT 3:5)”. |
| A1 / idézetek | OK | uo. `:26–34` | Róm 10:12, 10:14, 1Kor 1:2, 2Tim 2:22, Zsolt 116:4, 116:13, 2Kir 5:11, ApCsel 9:21, 1Kir 18:26, Sof 3:9, Jer 10:25 egyezik a `lekerdez.py karoli` kimenetével. |
| A2 | OK | — | A diff nem érinti a `NYITOTT_FELADATOK.md`-t. A Hagin-gap hozzáférési korlátja nem kapott N-tételt; megfontolandó, nem hiba. |
| A3 | OK | uo. `:29` | A study `:307` sora ugyanezt mondja. |
| A4 | OK | `motivumok/ISTENTISZT-001.md:302–308` | A diff nem módosít Remez- vagy Sod-réteget. |
| A5 | OK | `sablonok/PaRDeS_tanitok_lista.md:11–38` | Mind a 13 keresett és az 5 nem keresett név a jóváhagyott listán van. |
| A6 | OK | — | E12–E15: 0 találat. |
| Napló belső ellentmondás | ELTÉRÉS | `naplok/F130_TANITOI_KERESES_ISTENTISZT_naplo.md:7` | A napló szerint a DT-F130c 🟡 → 🟢 rögzítése nem történt meg; a HEAD-en már 🟢 (F130.2a). |
| Pontatlan M4-hivatkozás | ELTÉRÉS | `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md:145` | „a 6 ⚠️ és a Wommack-sor forrását … megnyitotta” — két Wommack-sor van (`:88`, `:89`), a napló csak a *Receive Jesus*-t ellenőrizte. |
| Lista 1 – törölt sorok | OK | — | 25 törölt sor: 20 a tanítói fájl régi törzse (archiválva), 3 az ISTENTISZT-001.md jóváhagyott cseréje, 2 a brief fejléce. |
| Lista 2 – kulcstartomány | OK, megjegyzéssel | uo. `:26–36` | 29 hely csomópont, 2 kizárva, az 1Pét 1:17 nincs említve. |
| Lista 3 – nulla-diff hatóköre | OK | — | A „bájtra azonos” a commitolt blobokra áll. |
| Lista 4 – TSV Δ | OK | — | `adat/`, `konkordancia/`: Δ = 0. |
| Lista 5 – ⛔ betartása | NEM ELLENŐRIZHETŐ | a95ecb2a | A forrás csak az M4 után változott; a jóváhagyásnak a repóban csak az orkesztrátor közvetítése a nyoma. |
| 7. (#22) | kihagyva: #22 | — | — |

ELTÉRÉS-ek súlyossági sorrendben:
1. **E5 HIBA 3** — nincs `TÖRLÉS-SZÁNDÉKOS:` jelölés a felülírt tanítói fájl három címsorának törléséhez; a PR-en a CI elbukik.
2. **Hibás verzifikációs jelölés** — „Jóel 2:32 (Károli 3:5)” a tanítói fájl 26. sorában; helyesen „(MT 3:5)”.
3. **A1** — öt jóváhagyott tanító emlékezetből tett hiányállítással, keresés nélkül kihagyva (`:56`).
4. **DT-F130c oszlopcsúszás** — a döntés a javaslat-oszlopban, a döntés-oszlopban `—` (`DONTESEK.md:348`).
5. **Modell-dokumentáció** — az F130.2a Sonnet-társszerzős commit az opus-briefen; az M4-subagent tényleges modellje nincs rögzítve.
6. **Elavult állítás a naplóban** a DT-F130c rögzítéséről (`naplo:7`).
7. **Pontatlan M4-lefedettségi mondat** (`:145`).

Megjegyzések:
- A `motivumok/ISTENTISZT-001.md:374` keltezett NAPLO-sora szerint a tanítói fájl `Dátum` és `Modell` mezője `manual`; a HEAD-en ez már nem igaz (a G6 tiltotta a módosítást, ezért nem ELTÉRÉS).
- Az ellenőr két Bash-hívásban csövön vágta a git kimenetét (kívül a megengedett parancskörön); csak olvasás volt.
