# ELLENOR_F11_M — az M2 részellenőrzése (az M6 később bővíti)

Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `c74677aa..c0b3bd6b` (`claude/f11-m2`), utóellenőrzés `e67f352f`-ig · ellenőr: `fuggetlen-ellenor`, modell `claude-opus-5-5` (kért: `opus`, egyezik).

*A fájlt az orkesztrátor írta ki az ellenőr jelentéséből, mert az ellenőr szerepének nincs fájlíró eszköze. A „parancskörön kívüli” futtatásokat az orkesztrátor pótolta; ezek a 2. szakaszban állnak, külön jelölve.*

## 1. Az ellenőr megállapításai (c74677aa..c0b3bd6b)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | Az ellenőr `claude-opus-5-5`, a kért `opus`. A menet adattábla-`modell` mezőt nem írt. |
| hatókör | OK | — | `git diff --numstat`: `DONTESEK.md` +1, `F11_MIGRACIO_BRIEF.md` +4/−3, `eszkozok/general.py` +642/−2. Minden az `ir` mezőn belül. Az M3-hoz nem nyúlt, `motivumok/ISTENTISZT-001.md` nincs. |
| törölt sorok | OK | brief `:8-12`, `general.py:1597,1701` | 5 törölt sor: 3 a brief fejlécében, 2 bővített sor a `general.py`-ban. Adatsor nem tűnt el. |
| TSV Δ (E17) | OK | — | `adat/*.tsv` és `konkordancia/*` diffje üres. Az éles `adat/jeloltek.tsv` nem változott. |
| ⛔ | OK | brief `:53-55` | Az M1 ⛔ teljesült (#393, 4832056d). Az E28/E29 a main-en van (#395, #397). Az M3 ⛔ (DT-F11a) érintetlen. |
| szintszűrés | OK (statikusan) | `general.py:1104-1256` | A `belso` szint kimarad az `olvasoi` és az `apparatus` nézetből. Hibát ad: a párosítatlan vagy ellentmondó `SZINT-*` pár, a `##`-en átnyúló pár és a régi `<!-- SZINT: x -->` alak. Ismeretlen `##` → `belso`. |
| soron belüli jelölő | **ELTÉRÉS (enyhe) → javítva** | `general.py` `FORRAS_CSAK_JELOLO_SOR` | Csak a sor eleji csak-forrásbeli jelölő esett ki. A soron belüli jelölő hiba nélkül átjutott a `--cel forras` nézetébe, ez ütközik a SEMA 3.10.4-gyel. Javítás: e67f352f (F11.M2.5), l. 2. szakasz. |
| kinyerés | OK (statikusan) | `general.py:1352-1476, 1561-1590` | Csak `--ir`-rel és hibátlan futásnál ír. `split('\t')`/`'\t'.join()`, `csv` nélkül. Írás előtt és után összevet, eltérésnél visszaállít. `dontes=nyitva`, `manual`. A lábjegyzetet nem olvassa, audit-sort nem ír (DT84 (2)). Az ADAT-HIV/ADAT-ÉRTÉK a DT-F11d-ig szándékosan hibát ad. UTF-8 wrapper: `general.py:71-74`. |
| DT-F11d | OK | `DONTESEK.md:272` | Helyőrző, végleges szám nélkül. 8 oszlop, 🟡, a Döntés oszlopban „—”. Nem dönt. |
| #114 átfedés | OK | — | A `lexikon_general.py`, a `sqlite_epit.py` és a `jeloltek.tsv` nem változott. Közös fájl csak a `DONTESEK.md`, ahol a két ág ugyanazon a helyen fűz hozzá, ezért triviális merge-konfliktus várható. |
| CI | OK | — | `futtat.py --valtozott … --diff-alap c74677aa` → rc=0, a változott fájlokra 0 találat. `futtat.py --teljes` → rc=0, E28=0, E29=0. |
| A1–A6 | OK / nem releváns | — | Minden állítás forrással áll. Tanulmány és nevesített tanító nincs a diffben. |

## 2. Az orkesztrátor futtatásai (az ellenőr parancskörén kívül)

| futtatás | állapot | eredmény |
|---|---|---|
| `PARDES_DATUM=2026-10-18 bash eszkozok/nulladiff.sh c74677aa`, `--csere` nélkül | c0b3bd6b és e67f352f | `nulladiff: RENDBEN`, rc=0, a teljes `lexikon/` azonos (HAMART-001-gyel együtt, N0) |
| `python eszkozok/feladatok.py ellenoriz` | e67f352f | 136 brief, 0 hiba, 0 figyelmeztetés |
| `python eszkozok/ellenorzes/futtat.py --teljes` | e67f352f | E28 0 találat („0 migrált nézet”), E29 0 találat |

A végrehajtó a commitüzenetekben rögzítette a saját méréseit. Ezek a 2. szakaszban felsoroltakkal egyeznek. A korábbi commitokból a mérés nyoma hiányzott, az e67f352f-ben már ott van.

## 3. Ítélet

**Zöld a javítás után.** Az egyetlen eltérés javítva (e67f352f). A javítás nem kapott újabb független ellenőrt; a mérései (N0, E28/E29, `ellenoriz`) az orkesztrátor futtatásában zöldek. Az M2 nincs kész: az `ADAT-HIV`/`ADAT-ÉRTÉK` ellenőrzés a DT-F11d döntésére vár (brief `allapot: dontesre_var`). Az M6 ezt a naplót bővíti.
