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

## 7. Az R és az M3 ellenőrzése (89b30c2e..c8e0401f)

*A független ellenőr (`fuggetlen-ellenor`) jelentése, szó szerint; a fájlba az orkesztrátor fűzte, mert az ellenőrnek nincs írási eszköze.*

ELTÉRÉS: 9 tétel

*Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `89b30c2e..c8e0401f` (a 7205d9fb merge saját tartalma nem tárgy; a 89b30c2e = a main csúcsa) · ellenőr: claude-opus-5-5 (kért: opus).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | a tényleges modell claude-opus-5-5, a kért opus. Egyik adattábla sem kapott `modell` mezőt: a `jeloltek.tsv` fejléce `id…datum`, nincs `modell` oszlop. |
| 1 Hatókör (`ir`) | OK | `F11_MIGRACIO_BRIEF.md:15` | `git diff --numstat 89b30c2e..c8e0401f`: 22 fájl, mind az `ir` mezőben. A bővítések indokoltak: `archivum/ISTENTISZT-001/` (DT-F11a), `adat/motivumok.tsv` (M3, forras_study), index és NYITOTT (generált blokk és hivatkozás-frissítés, CLAUDE.md), `szabalyok.py` és `test_szabalyok.py` (DT-F11f (2)), F70 brief és FELADATOK.md (CLAUDE.md hivatkozás-szabály), `teszt_lexikon_adatres.py` (R). Megjegyzés: az `ir` bővítéséhez külön felhasználói jóváhagyás nincs rögzítve; a bővítések a döntésekből következnek. |
| 1 Push | OK | — | `git log --remotes --oneline` szűrve „F11.M3\|F11.R”-re: 0 találat. A `git branch -r --contains c8e0401f` és a `… be54e5ef` kimenete üres. |
| 2 R: `forras=adat` + üres `tanulmany` | OK | `eszkozok/lexikon_general.py` `res_torzs` | `git diff … -- eszkozok/lexikon_general.py`: nem üres mezőnél `return mondat` (G16 változatlan), üres mezőnél `ADAT_RES_RENDEREK[res]`, más résnél `ValueError`. A `res_forras.tsv`-ben üres `tanulmany`-ú `adat` sor csak az ISTENTISZT-001 11., 13. és 14. sora (Grep `\tadat\t$`); a KIRALY-001 alatamasztas sora (G16) nem üres. |
| 2 R: KIEGESZITO kizárása | OK | `lexikon_general.py` `_szotar_reszek`, `rokon_szavak_strongok` | Szűrés `r['szotar'] not in KIEGESZITO_SZOTARAK`. SECE/MCGED sor csak az 5 új sor (H7121, H8034, G1941, G2564, G0994). Más motívum `elofordulasok.tsv`-sora egyiket sem hordozza: Grep `^[A-HJ-Z][A-Z]*-[0-9]+\t.*\b(H7121\|H8034\|G1941\|G2564\|G0994\|G994)\b` → 0. |
| 2 R: apparatus nézet | OK | `lexikon_general.py` `_tanulmany_szoveg` | Csak a `motivumok/` előtagra fut `G.forras_nezet(…,'apparatus')`. `res_forras.tsv`-ben `motivumok/` csak az ISTENTISZT-001 4 sora (Grep). |
| 2 R: HAMART-001 érintetlen | OK (statikus) | — | A fenti három ág nem ér el HAMART-001-sort, és `lexikon/HAMART-001*` nincs a diffben. A gépi N0-t lásd a 9. pontnál. |
| 2 R: tesztek | NEM ELLENŐRIZHETŐ | `eszkozok/teszt_lexikon_adatres.py` | A futtatás kívül esik a parancskörön. A fájlban 13 eset van, pozitív és negatív is (Grep `def test_`). |
| 2 R: 2b renderelő (szélső eset) | **ELTÉRÉS (közepes)** | `lexikon_general.py` `adatres_2b`; `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1204-1222, 1238` | Az `adatres_2b` csak a motívum saját tokenjeire renderel. Az 5 felvett SECE-sorból ezért 3 jelenik meg (G1941, H7121, H8034); a G2564 és a G0994 holt adat: Grep `33\.129\|GK: G1066` a lapon → 0. Közben a lapon maradt próza (1238, forrás: `motivumok/ISTENTISZT-001.md:73`) „mindhárom ige SECE-listájára” hivatkozik, és a régi éles lap ezt a háromigés táblát mutatta. Ez tartalomvesztés az éles lapon. |
| 2 R: minősítés-adat szúrópróba | OK | `lexikon:1460-1479` | `lekerdez.py tsk "Zak 13:9"`: ApCsel 2:21 Votes=83, Róm 10:12=18, Róm 10:14=18, Jóel 2:32=15 (`scope=range:Zak 13:9 \| forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv … \| n=50 \| ts=2026-10-18T14:41Z`). `lekerdez.py karoli "Jer 10:25"` → Zsolt 79,6, `karoli "Zsolt 79:6"` → Jer 10,25 (`n=1 \| ts=2026-10-18T14:37Z`). A jelöltszám 61: Grep `^ISTENTISZT-001\t[^\t]*\t(TSK\|Károli-KH)` → 61; a lapon „61 sor”. |
| 2 R / CLAUDE.md 1. szabály | **ELTÉRÉS (közepes-alacsony)** | `adat/res_forras.tsv:11,13,14`; `lexikon:1202, 1454, 1648` | A három generált rés fejléce továbbra is „*(kézi)*”. A lekérdezésből származó „Független megerősítés”-listának nincs `scope=…\|forras=…\|ts=…` sora, és GENERÁLT-jelölője sincs, csak egy leíró dőlt sor. |
| 3 M3.1 jeloltek | OK | `adat/jeloltek.tsv` (+10) | `git diff … -- adat/jeloltek.tsv`: 10 új `elutasítva` sor (C-minta: Ézs 43:1, 44:5, 45:3; D-minta: 2Sám 6:2, 1Krón 13:6, Jer 7:10, 7:11, 7:14, 7:30, 5Móz 28:10), proveniencia `scope=manual \| forras=… \| ts=2026-10-18`. `lekerdez.py kollokacio H7121 H8034`: mind a 10 vers benne van (`scope=TAHOT-teljes+TAGNT-teljes \| … \| strong=H7121+H8034 \| n=196 \| ts=2026-10-18T14:36Z`). A Jer 7:30 forrása: `archivum/…/Segitsegul_hivni_az_Urat_tematikus.md:88` („Jer 7:10-11,14,30”). |
| 3 M3.1/M3.4 kapcsolatok `indoklas` | OK | `adat/kapcsolatok.tsv:12-36` | `git diff --word-diff=porcelain … -- adat/kapcsolatok.tsv`: csak hozzáadás, más cella nem változott. `awk -F'\t'` szerint NF=8 maradt. A 25 ISTENTISZT-001 sorból 24 kitöltve, a 2Móz 33:19 → 34:5 (25. sor) üres. Az archív 107–121. sor cellái szó szerint egyeznek, két jóváhagyott levágással: T29/12 („2026.09.06: Károli-KH…”, archívum) és T29/13 („— TSK-eredetű lelet, 2026.09.06”, archívum). |
| 3 T29/4 „jelölve” | **ELTÉRÉS (alacsony)** | `adat/kapcsolatok.tsv:14`; `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv:38` | A jóváhagyás szerint az „ApCsel 2:21 / Róm 10:13-ra szóló mondat jelölve” kerül az `1Móz 4:26 → Jóel 2:32` sorra. A cella jelölés nélkül áll, így ennek az ÓSZ–ÓSZ párhuzamnak a „Magas” bizonyosságát egy NT-idézés indokolja (A1). A DT-F11f (4) a két Jóel-sort pótolta, a jelölést nem írta felül. |
| 3 SECE `szoveg_en` | OK (G: vizuális) | `adat/lexikon_hivatkozasok.tsv:27-31` | SECE_H: a két részlet bájtra benne van a `konkordancia/SECE_H_teljes.tsv` 7122. és 8035. sorában (Grep szó szerinti mintával). SECE_G: Grep `-o` `LN: …Hebrew: [^\tD]+` mindkét fájlon (SECE_G 995, 1942, 2565 ↔ lexhiv 27–29), a karaktersor egyezik; a héber pontozás bájtszintű összevetése a parancskörben nem futtatható. |
| 4 M3.2 forrás-lefedettség | OK (kézi összevetés) | `motivumok/ISTENTISZT-001.md` | A leképezési tábla 211 sorából 97 forras, 38 generalt, 56 archivum, 20 adat (Grep count). `git diff -U0 c8e0401f:archivum/…/Segitsegul_hivni_az_Urat_tematikus.md c8e0401f:motivumok/ISTENTISZT-001.md` (52+/211−): minden törölt hunk nem-forras egység, vagy áthelyezett forras egység (RÉS-VÉGE miert_fontos → 110; RÉS-KEZDET modszertan → 340; T52 → 440; T67 → 442–444). A régi forrásréteg forras egységei a helyükön: sor 3 → 1, 13/6 → 258, 13/8 → 53, 24/6 → 141, 25/8 → 143 (Grep a régi forrásréteg 14., 25. és 26. sorára). A napló 72–74. sora → 334–336. Új kötőszöveg csak a megengedett helyeken: 3, 27, 344, 346, 428, 430, valamint ADAT-NÉZET/INAKTÍV/ADAT-HIV jelölők. |
| 4 T14/1, T20/1, T22/1 vágás | OK (megítélés) | `motivumok:33, 37, 49` | T20: a „, korábban elutasítva mint a motívumhoz nem tartozó zaj” rész kikerült; a mondat ép, az elutasítás az első tagmondatban megmaradt. T22: kikerült a „Példák: …” (adat) és a „Zsid 11:16 emiatt explicit kizárva…” (archív); a példák a `motivumok:403-405`-ben megmaradtak. T14/1: „kiszűrve)】”-nél vágva. A részegység-határok bájt-offszetje nincs a táblában, ezért ez szemrevételezés. |
| 4 A forrásréteg 24/6, 25/8 elhelyezése | **ELTÉRÉS (közepes)** | `motivumok/ISTENTISZT-001.md:141, 143`; `lexikon:1697, 1699` | A két részegység horgony nélkül áll a „Mit jelent ez a négy szint?” lista után, a **Peshat:** bekezdés előtt. Egyik sem nevezi meg az igehelyet (1Móz 13:4, ill. 21:33), a második kisbetűvel, csonka mondatként kezdődik („az egyetlen genezisi hely, ahol…”). Az olvasói lapon értelmezhetetlenek. A tábla javaslata a „Peshat-rész” volt. |
| 4 `--cel forras`/`kinyeres` | NEM ELLENŐRIZHETŐ | — | A `general.py` a parancskörön kívül esik. Az M3.2 commit-üzenete állítja, hogy „0 hiba”; ezt nem igazoltam. |
| 4 Generált jelölő a forrásban | OK | `motivumok/ISTENTISZT-001.md` | Grep `GENERÁLT\|ÜRES-` → 0. Megjegyzés: a 397. sor (forras egység, bájtra megőrzött) a már nem létező `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md` útra mutat. |
| 5 Archívum (DT-F11a) | OK | `archivum/ISTENTISZT-001/*` | Glob: 3 fájl, lapos mappa, nincs `naplok` almappa. `git diff 89b30c2e:<eredeti> c8e0401f:archivum/…` mindhárom fájlra: egyetlen hozzáadott sor, az első (`<!-- ARCHÍV: <út> @ <commit> · F11 M3 · 2026-10-18 · nem forrás, nem szerkesztendő -->`). A fejléc commitjai (aa59df2b, 82f5c869, cd43a2fd) egyeznek a `git log -1 89b30c2e -- <út>` kimenetével. |
| 5 Fájlnév-ütközés | **ELTÉRÉS (alacsony)** | `generalt_proba/tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` | Glob: az archív napló alapneve megegyezik egy verziózott `generalt_proba/` fájléval. A `general.py --cel naplok` a régi `relativ` úttal ide ír tovább (`general.py:1986`). A DT-F11a kikötése szerint az alapnév nem ütközhet; az E27 alapnév szerint old fel. |
| 6 M3.3 `res_forras`, `forras_study` | OK | `adat/res_forras.tsv:10-16`; `adat/motivumok.tsv:4` | `git diff …`: 4 sor `tanulmany` → `motivumok/ISTENTISZT-001.md`, 3 sor `adat` üres mezővel; a forras_study első eleme átírva. A NYITOTT generált blokkja: 318 elutasítva (Grep count = 318), 259+50 (Grep `beépítve\|nyitva` = 309). |
| 6 Az index és a nyitott generált blokkja = generátor | NEM ELLENŐRIZHETŐ | — | Ehhez `general.py --ellenoriz` kellene. |
| 6 Hivatkozás-frissítés (A2) | **ELTÉRÉS (alacsony)** | `NYITOTT_FELADATOK.md:136` (N-F09h), `FELADATOK.md:82`, `NYITOTT_FELADATOK.md:327` (N17) | Az N-F09h és a FELADATOK-sor most az archív fájlt jelöli meg javítandó forrásként, pedig az archívum nem szerkesztendő. Közben a CC BY-SA 3.0 sor már sem az élő lapon, sem a forrásban nincs: Grep `CC BY-SA 3\.0` a két fájlban → 0, `git diff … lexikon/… \| grep -c '^-.*CC BY-SA 3\.0'` → 1. A tétel így félrevezetően „nyitott”; a `lexikonok_nyers/README` része valóban nyitott. Az N17 „(92. sor)” hivatkozása nem tolódott +1-gyel: az archív 93. sor a `LXX_kivonat` sor. Megjegyzés: a 2026.09.09-i és 09.23-i történeti bejegyzések útja is átírva („commit 8df6650” mellett). |
| 6 F70 és F11 brief-fejléc | **ELTÉRÉS (alacsony)** | `F70_SZOTAR_S26_BRIEF.md` `ir`; `F11_MIGRACIO_BRIEF.md:12` | Az F70 `ir` mezője a törölt `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`-re mutat, és a 2b rés célja `adat` lett. Az F11 `kovetkezo` mezője az M2-állapotot írja („az M3 a DT-F11a … után indul”). |
| 6 `general.py` naplok-tartalék | OK (megjegyzés) | `eszkozok/general.py:1988-1991` | Az `os.path.exists` tartalék minden motívumra él, nem csak a migráltra, így más motívum hiányzó naplója is csendben NAPLO_MD-sorvéget kapna. |
| 7 M3.5 E9-kivétel | OK (kód), NEM ELLENŐRIZHETŐ (futás) | `eszkozok/ellenorzes/szabalyok.py:552-568`; `tesztek/test_szabalyok.py:250-264` | `git diff … -- eszkozok/ellenorzes/`: útvonal-előtag szerinti kivétel. Egy teszt `archivum/` alatt 0 találatot, egy `tematikus_lezart/` alatt 1 HIBA-t vár. A kivétel az ARCHÍV fejlécet nem ellenőrzi (gyenge őr). A `unittest`-futás a parancskörön kívül esik. |
| 8 M3.6 éles lap = generátor | NEM ELLENŐRIZHETŐ | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` | Az újragenerálás a parancskörön kívül esik. Ami ellenőrizhető: 0 【NAPLO】 a lapon (Grep). Tájékoztatásul: `git diff --stat c8e0401f:generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md c8e0401f:lexikon/ISTENTISZT-001_TUDOMANYOS.md` → 906+/292−, 97 hunk az aranymintához képest; ez az M4 mérésének tárgya. |
| 8 Kolofon napló-cella (ismert) | **ELTÉRÉS (közepes)** | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1987` | Az éles lap a már nem létező `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md`-re mutat (G.ID_NAPLO_TERKEP). A javítás helye a generátor, nem a lap. |
| 9 CI | OK (feltétellel) | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 89b30c2e..c8e0401f) --diff-alap 89b30c2e --diff-fej c8e0401f --commit-uzenet "$(git log --format=%B 89b30c2e..c8e0401f)"`: egyetlen HIBA az E16 („a cím nem [ELLENŐRZŐ] előtagú”); E11=1, E12=309, E13=101, E25=3, E27=40 JELENTÉS; E28 „0 migrált nézet”. Ugyanez `--pr-cim "[ELLENŐRZŐ] F11.M3: szétválasztás"` kapcsolóval: 0 HIBA. A PR címének tehát `[ELLENŐRZŐ]` előtaggal kell kezdődnie. A `--commit-uzenet-fajl <(…)` Windows-Pythonon nem nyílik meg (FileNotFoundError), ezért argumentumként adtam át. |
| 9 `ellenoriz.py`, `feladatok.py`, `unittest`, N0 | NEM ELLENŐRIZHETŐ | — | A parancskörön kívül esik. Az M3.3 commit-üzenete N0-t állít („csak a két ISTENTISZT-001 lexikonfájl tér el”); ezt nem igazoltam. |
| 10 DT-F11a/e/f | OK (alak), NEM ELLENŐRIZHETŐ (szó szerinti idézet) | `DONTESEK.md` 3 új sor | `git diff … -- DONTESEK.md`: csak helyőrzők, 🟢, végleges DT-szám nincs. A „Felhasználó … (chat, a szülő session közvetítésével)” idézetek hitelessége a repóból nem igazolható. A DT-F11e javaslata A, a döntés B; ez a Javaslat oszlop, nem hiba. A sorrend rendben: DT-F11a (6c27b14a) az M3.1 előtt, DT-F11e (f8dc496c) az R.1 előtt, DT-F11f (53a20afb) az M3.4–M3.6 előtt. |
| Lista 1: törölt sorok | OK | `motivumok/ISTENTISZT-001.md` | `git diff --stat c8e0401f:archivum/…_tematikus.md c8e0401f:motivumok/ISTENTISZT-001.md`: 211 törölt / 52 új sor. Kategóriák a leképezési tábla szerint: generalt 38, archivum 56, adat 20 egység (a 20 adat egység = 10 jelölt + 24 kapcsolat-indoklás 15 cellából + 5 SECE-sor). |
| Lista 2: kulcstartomány | OK | — | Az adat egységek mind célba értek: T29/2–16 → 24 sor, T20/2 + T22/3 → 10, T56/T65/T66 → 5. |
| Lista 3: nulla-diff hatóköre | NEM ELLENŐRIZHETŐ | — | Az N0 a generált kimenetre vonatkozik (HAMART-001 és a többi motívum), a commitolt fájlokra nem. A commitolt `lexikon/` alatt csak az ISTENTISZT-001 TUDOMANYOS változott (`git diff --stat … -- lexikon/`). |
| Lista 4: TSV Δ (E17, DT3) | OK | — | `git diff --numstat 89b30c2e..c8e0401f`, fejléc nélkül: `adat/jeloltek.tsv` +10; `adat/lexikon_hivatkozasok.tsv` +5; `adat/kapcsolatok.tsv` 0 (24/24); `adat/res_forras.tsv` 0 (7/7); `adat/motivumok.tsv` 0 (1/1); minden más `adat/` és `konkordancia/` `.tsv` 0. A |Δ|≥10 a `jeloltek`-et érinti: bontás a leképezési tábla T20/2 (C-minta, 3) és T22/3 (D-minta, 7) sorában és az M3.1 commit-üzenetében; külön bontási napló nincs. |
| Lista 5: ⛔ pontok | OK | — | Az M3 ⛔ (DT-F11a) a végrehajtás előtt eldőlt. A „merge csak zöld M4 után” (DT-F11f) még nyitott: M4 nem futott. |
| A1 | ELTÉRÉS → T29/4 sor | — | Lásd a T29/4 sort. |
| A2 | ELTÉRÉS → N-F09h/N17 sor | — | Lásd a hivatkozás-frissítés sorát. |
| A3 | OK | `motivumok:53` | A σῴζω-jegyzet „nem lexikai kapocs-bővítés” jelöléssel áll; új tematikus/lexikai címke nem keletkezett. |
| A4 | OK (megjegyzés) | `motivumok:141-143, 251-258` | Az új ⚠️ (5/6) a Sod után áll, a Sod-szöveg bájtra változatlan. A 141/143 töredékek szintcímke nélkül állnak (lásd fent). |
| A5 | NEM ELLENŐRIZHETŐ | `motivumok:311-326` | A tanítói szakasz bájtra változatlan forras egység; az 5/7 összefoglaló archívumba került. A jóváhagyott lista és forrás vizsgálata az M7 tárgya. |
| A6 | OK (megjegyzés) | `lexikon:338-339, 1208` | E13: kiejtés nélküli görög/héber a minősítés jelölt-indoklásában és a 2b SECE-részletben. A régi 2/b tábla átírást adott, a generált nem. Az E14 és az E15 0. |
| Tanulmány-ellenőrzés (F37 T4) | nem él | — | A diff nem hoz `*_bovitett.md` / `*_tanulmany.md` fájlt (az archív fájl `_tematikus.md`, a forrás `motivumok/`). |

**Az eltérések súlyosság szerint:**
1. Közepes — a 2b rés csak 3 SECE-sort renderel az 5-ből, a lapon maradt próza a hiányzó kettőre hivatkozik (`lexikon_general.py` `adatres_2b`; `lexikon:1204-1238`).
2. Közepes — a forrásréteg 24/6 és 25/8 részegysége horgony nélkül áll az Értelmezésben (`motivumok:141,143` → `lexikon:1697,1699`).
3. Közepes — a Kolofon a törölt napló-útra mutat (`lexikon:1987`, ismert).
4. Közepes-alacsony — a generált rések „*(kézi)*” fejléccel állnak, és a TSK/Károli-KH-ból származó megerősítésnek nincs proveniencia-sora (`res_forras.tsv:11,13,14`).
5. Alacsony — a T29/4 cellájáról hiányzik a „jelölve” (`kapcsolatok.tsv:14`).
6. Alacsony — az N-F09h / FELADATOK / N17 hivatkozások az archívumot jelölik meg javítandónak, a sorszám pedig elcsúszott.
7. Alacsony — az F70 `ir` mezője és az F11 `kovetkezo` mezője elavult.
8. Alacsony — az archív napló alapneve ütközik egy `generalt_proba/` fájléval.
9. Alacsony — a fenti 4–8. mellett az E16-ot a PR-cím `[ELLENŐRZŐ]` előtagja oldja fel; ez nem a diff hibája, de a merge feltétele.

**Ítélet: piros.** Szűkebben:
- Az adatréteg (jeloltek, kapcsolatok, SECE) és az archívum az ellenőrzött pontokon rendben van; ez a rész zöld lenne megjegyzésekkel.
- Az éles lexikonoldal (M3.6) a 1., 2. és 3. közepes eltérés miatt piros.

Mindhárom a forrásban vagy a generátorban javítható. A merge egyébként is csak zöld M4 után lehetséges.

## 8. Az orkesztrátor futtatásai a c8e0401f-en (az ellenőr parancskörén kívül)

*Az ellenőr „NEM ELLENŐRIZHETŐ” pontjai; futtatta az orkesztrátor (claude-opus-5-5), 2026-10-18.*

| pont | eredmény | parancs / kimenet |
|---|---|---|
| 2 R tesztek | OK | `python eszkozok/teszt_lexikon_adatres.py` → 13 teszt, OK; `teszt_general_forras.py`, `teszt_general_kinyeres.py`, `teszt_general_ellenorzo.py` → OK |
| 4 `--cel forras` / `--cel kinyeres` | OK | `general.py --cel forras --id ISTENTISZT-001 --kimenet <repón kívül>`: 0 figyelmeztetés (olvasoi 198, apparatus 360, belso 445 sor); `--cel kinyeres`: „0 új jelölt-sor, 0 ütközés, 0 ismétlés, 7 ellenőrző jelölő, 0 hiba”. Lefedettség-szkript (a leképezési tábla 211 sora): 97 forras bent bájtra, a 114 nem-forras egység egyetlen ≥ 25 karakteres sora sem maradt a forrásban, 0 hiba. |
| 6 index / nyitott / naplo = generátor | OK | `general.py --cel naplo\|index\|nyitott --ellenoriz` → mind 0 kilépési kód |
| 8 éles lap = generátor | OK, egy megjegyzéssel | `PARDES_DATUM=2026-10-18 general.py --cel lexikon --id ISTENTISZT-001 --kimenet <repón kívül>` ↔ `git show HEAD:lexikon/ISTENTISZT-001_TUDOMANYOS.md`: egyetlen eltérés, a commitolt lap 3–4. sora két üres sor a GENERÁLT-fejléc után. Ez a main-en (`origin/main`) is megvan: a helyben frissítés (`frissit_meglevo_fajlt`) a lap fejléc-szerkezetét megőrzi, az új-fájl ág (`epit_uj_fajl`) egy üres sort ír. Az E28-listára vétel (M4/M5) előtt a két ágnak egyeznie kell, különben az E28 piros. |
| 9 `ellenoriz.py` | OK | `RENDBEN: 12 \| SÉRTÉS: 0 \| KÉZI: 2 \| JELENTÉS: 3` (a 11. szabály a c8e0401f-en zöld; az 53a20afb–73613284 között SÉRTÉS volt, a DT-F11f (1) szerinti újragenerálásig) |
| 9 `feladatok.py ellenoriz` | OK | `137 brief, 0 hiba, 0 figyelmeztetés` |
| 9 `unittest discover` | OK | `python -m unittest discover -s eszkozok/ellenorzes/tesztek` → 187 teszt, OK |
| 9 CI | OK (feltétellel) | `futtat.py … --diff-alap origin/main --diff-fej HEAD --commit-uzenet-fajl <üzenetek>`: egyetlen HIBA az E16 (PR-cím `[ELLENŐRZŐ]` előtag); E28 „0 migrált nézet”, E29 0 |
| 9 N0 | OK | `bash eszkozok/nulladiff.sh origin/main 2026-10-18` (origin/main = 89b30c2e): eltér csak `lexikon/ISTENTISZT-001_TORZSCIKK.md` és `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (a migrált motívum, várt); a HAMART-001 és minden más motívum bájtra azonos. Ugyanez az R.1, M3.1 és M3.3 után is. |

**Az orkesztrátor összegzése.** A gépi ellenőrzések mind zöldek (az E16 a PR-cím dolga). Az ellenőr piros ítélete az éles lap három közepes eltérésén áll (2b rokon szavak, a két horgony nélküli töredék, a Kolofon napló-útja); ezek és az alacsony tételek a felhasználó döntésére várnak, javítás nélkül. A brief `megallt`; az M4 nem indult.
