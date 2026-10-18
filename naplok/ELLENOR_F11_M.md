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
| DT202 | OK | `DONTESEK.md:272` | Helyőrző, végleges szám nélkül. 8 oszlop, 🟡, a Döntés oszlopban „—”. Nem dönt. |
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

**Zöld a javítás után.** Az egyetlen eltérés javítva (e67f352f). A javítás nem kapott újabb független ellenőrt; a mérései (N0, E28/E29, `ellenoriz`) az orkesztrátor futtatásában zöldek. Az M2 nincs kész: az `ADAT-HIV`/`ADAT-ÉRTÉK` ellenőrzés a DT202 döntésére vár (brief `allapot: dontesre_var`). Az M6 ezt a naplót bővíti.

*Utólag: a DT-F11d-t a felhasználó 2026-10-18-án eldöntötte (mind a négy alpontban az (a) változat). Az M2 befejezését a 4–6. szakasz rögzíti.*

## 4. Az M2 végső ellenőrzése (origin/main..7f27631e)

Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `origin/main..HEAD`, a merge-bázis `49dd711e`, a fej `7f27631e` (a `claude/f11-m2` ág az origin/main összefésülése után) · ellenőr: `fuggetlen-ellenor`, `claude-opus-5-5` (kért: `opus`, egyezik). *Ezt a szakaszt is az orkesztrátor írta ki az ellenőr jelentéséből.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | Adattábla `modell` mezőjét a menet nem írta. |
| hatókör (`ir`) | OK | — | `git diff --numstat origin/main..HEAD`: 6 fájl változott, `DONTESEK.md`, brief, `adat/SEMA.md`, `eszkozok/general.py`, `naplok/ELLENOR_F11_M.md`, sablon 9. Mind az `ir` mezőben van, vagy a CLAUDE.md engedi. |
| M3 érintetlen | OK | — | A `motivumok`, `lexikon` és `tematikus_lezart` diffje üres. |
| törölt sorok | OK | — | 9 sor: a brief fejléce 2, SEMA 3.10.5 2, sablon 9 6. pont 3, `general.py` 2. Mind cserélt sor, adatsor nem tűnt el. |
| kulcstartomány | ELTÉRÉS (enyhe) | `general.py:1350-1366` | A `SEMA_KULCSOK` 7 olyan táblát kihagy, amelynek van „Kulcs:” sora; ezekre hamis „nincs SEMA-kulcsa” hiba jön. |
| nulla-diff | OK (átvett adat) | — | Az orkesztrátor futtatta: `nulladiff.sh origin/main` RENDBEN. |
| TSV Δ | OK | — | Az `adat/*.tsv` és a `konkordancia/*.tsv` diffje üres, csak a `SEMA.md` változott. |
| ⛔ pontok | OK | brief `:53-55` | Az M1 a main-en van (#393). A DT-F11a nincs a `DONTESEK.md`-ben, az M3 nem indult. |
| (a) szakasz-felismerés | OK | `general.py:1041-1056,1129-1139` | A `##` címsor eleje szerint ismer fel. Ismeretlen `##` → `belso`, figyelmeztetéssel. Egyezik a sablon 9 4. pontjával és a SEMA 3.10.2-vel. |
| (a) P-lépés-figyelmeztetés | OK | `general.py:1060,1190-1195` | Feltétel: 1. szakasz, `###` alcím, `\bP[1-7]\b`, és nem `belso` szint (a `SZINT-KEZDET` vermét is figyeli). |
| (b) ADAT-HIV | OK (a kulcslistán kívül) | `general.py:1398-1449` | Az elírt mezőnév hiba, nem néma nem-találat. Hiányos kulcs és kulcson kívüli mező hiba. `n != 1` hiba. |
| (c) eval | OK | `general.py:1344,1452-1474` | `eval`, `exec`, `csv` és `ast` nincs a kódban, a kifejezést regex illeszti. |
| (c) egész érték | ELTÉRÉS (közepes) | `general.py:1343,1566` | A `(\d+)$` csak a záró számjegysort nézi, így a `2.5`, a `-3` és a `P3` „rendben”, ha a záró számjegy egyezik. Ez csendes elfogadás. |
| (c) zárt készlet | ELTÉRÉS (enyhe) | `general.py:1344` | A mohó `.*` miatt a `count(…)+count(…)` nem „ismeretlen függvény” hibát ad, hanem 0 találatos szűrőt. |
| (d) gerinc-alak | OK | `general.py:1507-1547` | `gerinc: X — …`, a szakasz-mutató a `##` címsor. |
| sablon 9 ↔ SEMA ↔ kód | OK, a fenti 3 pont kivételével | sablon `:91,150-155`; SEMA `:1324-1327,1383-1385` | Régebbi, nem e diffből eredő ellentmondás: a SEMA 1. táblája (`:21`) és a 2.5 (`:349`) mást ad a `lexikon_hivatkozasok` kulcsára. |
| DT202 sor | OK; a forrás oszlop ELTÉRÉS (enyhe) | `DONTESEK.md:277` | Helyőrző, 8 oszlop, ✅ az alkalmazó commitokkal. A „(a #12 véglegesítésekor)” zárójel ellentmond a ✅-nak. |
| felhasználói idézetek | NEM ELLENŐRIZHETŐ | — | A chat a repóból nem érhető el. |
| merge-feloldás | OK | `DONTESEK.md:274-276` | `DONTESEK.md`: 1 sor beszúrva, törlés nincs. A DT197–201 bájtra egyezik a main-nel. |
| brief fejléc | OK; a `pr` ELTÉRÉS (enyhe) | brief `:8,12,13` | `megallt`, a `kovetkezo` „Te:” kezdetű és a tényeknek megfelel. A `pr: #393` a mergelt M1-PR-re mutat. |
| `csv` modul | OK | `general.py:244-262` | `split('\t')`, oszlopszám-ellenőrzéssel. |
| tesztek | NEM ELLENŐRIZHETŐ | — | A tesztek a scratchpadben futottak, a repóban nincsenek. |
| CI | OK | — | `futtat.py --valtozott … --diff-alap origin/main` rc=0. Az E2–E16, E19, E20, E26, E28 és E29 0 találat. |
| A1–A6 | OK / nem releváns | — | — |

## 5. A végső ellenőrzés eltéréseinek javítása

| eltérés | javítás | commit |
|---|---|---|
| (c) egész érték (közepes) | A szám előtt nem állhat számjegy, betű, `.`, `,` vagy `-`. A `2.5`, `1,5`, `-4` és `P4` mostantól hiba. | 080e39dd F11.M2.11 |
| kulcslista (enyhe) | A kulcsokat a kód a SEMA 2. szakaszának „Kulcs:” soraiból vezeti le, 21 táblára. A felsorolt hétből hat kapott kulcsot; a `karoli_variancia.tsv`-nek a SEMA 2.24-ben nincs „Kulcs:” sora, ezért arra az `ADAT-HIV` továbbra is hibát ad. | 080e39dd F11.M2.11 |
| zárt készlet (enyhe) | Az argumentumban nem lehet zárójel. A `count(…)+count(…)` „ismeretlen kifejezés” hibát ad. | 080e39dd F11.M2.11 |
| DT202 forrás oszlop (enyhe) | A tény került a helyére: sablon 9 v0.2 (4. és 6. pont), SEMA 3.10.2 és 3.10.5. | c473c19a F11.M2.12 |
| brief `pr` (enyhe) | `pr: —` (a `feladatok.py` ezt a mezőt nem ellenőrzi). | c473c19a F11.M2.12 |

A végrehajtó a tesztjeit a scratchpadben, a repón kívül futtatta: a `teszt_ellenorzo` 22 negatív esettel, valamint a `teszt_kinyeres` és a `teszt_forras` zöld.

## 6. Az orkesztrátor futtatásai a c473c19a-n

| futtatás | eredmény |
|---|---|
| `PARDES_DATUM=2026-10-18 bash eszkozok/nulladiff.sh origin/main`, `--csere` nélkül | `nulladiff: RENDBEN`, a teljes `lexikon/` azonos, a HAMART-001-gyel együtt (N0) |
| `python eszkozok/feladatok.py ellenoriz` | 136 brief, 0 hiba, 0 figyelmeztetés |
| `python eszkozok/ellenorzes/futtat.py --teljes` | E28 0 találat, E29 0 találat |
| `git diff --stat origin/main..HEAD -- adat/*.tsv` | üres: az ág egyetlen adattáblát sem változtat |

**Ítélet: zöld a javítások után.** Az öt eltérés javítva; a `karoli_variancia` kulcsa nyitva marad, mert a SEMA hiányát a #11 nem pótolja. A javító commitokat (080e39dd, c473c19a) újabb független ellenőr nem nézte, a méréseik zöldek. Az M2 kész, a brief `megallt`; az M3 a DT-F11a eldöntésére és külön jóváhagyásra vár.
