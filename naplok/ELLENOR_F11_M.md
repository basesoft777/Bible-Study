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
| ⛔ | OK | brief `:53-55` | Az M1 ⛔ teljesült (#393, 4832056d). Az E28/E29 a main-en van (#395, #397). Az M3 ⛔ (DT215) érintetlen. |
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
| ⛔ pontok | OK | brief `:53-55` | Az M1 a main-en van (#393). A DT215 nincs a `DONTESEK.md`-ben, az M3 nem indult. |
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

**Ítélet: zöld a javítások után.** Az öt eltérés javítva; a `karoli_variancia` kulcsa nyitva marad, mert a SEMA hiányát a #11 nem pótolja. A javító commitokat (080e39dd, c473c19a) újabb független ellenőr nem nézte, a méréseik zöldek. Az M2 kész, a brief `megallt`; az M3 a DT215 eldöntésére és külön jóváhagyásra vár.

## 7. Az R és az M3 ellenőrzése (89b30c2e..c8e0401f)

*A független ellenőr (`fuggetlen-ellenor`) jelentése, szó szerint; a fájlba az orkesztrátor fűzte, mert az ellenőrnek nincs írási eszköze.*

ELTÉRÉS: 9 tétel

*Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `89b30c2e..c8e0401f` (a 7205d9fb merge saját tartalma nem tárgy; a 89b30c2e = a main csúcsa) · ellenőr: claude-opus-5-5 (kért: opus).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | a tényleges modell claude-opus-5-5, a kért opus. Egyik adattábla sem kapott `modell` mezőt: a `jeloltek.tsv` fejléce `id…datum`, nincs `modell` oszlop. |
| 1 Hatókör (`ir`) | OK | `F11_MIGRACIO_BRIEF.md:15` | `git diff --numstat 89b30c2e..c8e0401f`: 22 fájl, mind az `ir` mezőben. A bővítések indokoltak: `archivum/ISTENTISZT-001/` (DT215), `adat/motivumok.tsv` (M3, forras_study), index és NYITOTT (generált blokk és hivatkozás-frissítés, CLAUDE.md), `szabalyok.py` és `test_szabalyok.py` (DT217 (2)), F70 brief és FELADATOK.md (CLAUDE.md hivatkozás-szabály), `teszt_lexikon_adatres.py` (R). Megjegyzés: az `ir` bővítéséhez külön felhasználói jóváhagyás nincs rögzítve; a bővítések a döntésekből következnek. |
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
| 3 T29/4 „jelölve” | **ELTÉRÉS (alacsony)** | `adat/kapcsolatok.tsv:14`; `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv:38` | A jóváhagyás szerint az „ApCsel 2:21 / Róm 10:13-ra szóló mondat jelölve” kerül az `1Móz 4:26 → Jóel 2:32` sorra. A cella jelölés nélkül áll, így ennek az ÓSZ–ÓSZ párhuzamnak a „Magas” bizonyosságát egy NT-idézés indokolja (A1). A DT217 (4) a két Jóel-sort pótolta, a jelölést nem írta felül. |
| 3 SECE `szoveg_en` | OK (G: vizuális) | `adat/lexikon_hivatkozasok.tsv:27-31` | SECE_H: a két részlet bájtra benne van a `konkordancia/SECE_H_teljes.tsv` 7122. és 8035. sorában (Grep szó szerinti mintával). SECE_G: Grep `-o` `LN: …Hebrew: [^\tD]+` mindkét fájlon (SECE_G 995, 1942, 2565 ↔ lexhiv 27–29), a karaktersor egyezik; a héber pontozás bájtszintű összevetése a parancskörben nem futtatható. |
| 4 M3.2 forrás-lefedettség | OK (kézi összevetés) | `motivumok/ISTENTISZT-001.md` | A leképezési tábla 211 sorából 97 forras, 38 generalt, 56 archivum, 20 adat (Grep count). `git diff -U0 c8e0401f:archivum/…/Segitsegul_hivni_az_Urat_tematikus.md c8e0401f:motivumok/ISTENTISZT-001.md` (52+/211−): minden törölt hunk nem-forras egység, vagy áthelyezett forras egység (RÉS-VÉGE miert_fontos → 110; RÉS-KEZDET modszertan → 340; T52 → 440; T67 → 442–444). A régi forrásréteg forras egységei a helyükön: sor 3 → 1, 13/6 → 258, 13/8 → 53, 24/6 → 141, 25/8 → 143 (Grep a régi forrásréteg 14., 25. és 26. sorára). A napló 72–74. sora → 334–336. Új kötőszöveg csak a megengedett helyeken: 3, 27, 344, 346, 428, 430, valamint ADAT-NÉZET/INAKTÍV/ADAT-HIV jelölők. |
| 4 T14/1, T20/1, T22/1 vágás | OK (megítélés) | `motivumok:33, 37, 49` | T20: a „, korábban elutasítva mint a motívumhoz nem tartozó zaj” rész kikerült; a mondat ép, az elutasítás az első tagmondatban megmaradt. T22: kikerült a „Példák: …” (adat) és a „Zsid 11:16 emiatt explicit kizárva…” (archív); a példák a `motivumok:403-405`-ben megmaradtak. T14/1: „kiszűrve)】”-nél vágva. A részegység-határok bájt-offszetje nincs a táblában, ezért ez szemrevételezés. |
| 4 A forrásréteg 24/6, 25/8 elhelyezése | **ELTÉRÉS (közepes)** | `motivumok/ISTENTISZT-001.md:141, 143`; `lexikon:1697, 1699` | A két részegység horgony nélkül áll a „Mit jelent ez a négy szint?” lista után, a **Peshat:** bekezdés előtt. Egyik sem nevezi meg az igehelyet (1Móz 13:4, ill. 21:33), a második kisbetűvel, csonka mondatként kezdődik („az egyetlen genezisi hely, ahol…”). Az olvasói lapon értelmezhetetlenek. A tábla javaslata a „Peshat-rész” volt. |
| 4 `--cel forras`/`kinyeres` | NEM ELLENŐRIZHETŐ | — | A `general.py` a parancskörön kívül esik. Az M3.2 commit-üzenete állítja, hogy „0 hiba”; ezt nem igazoltam. |
| 4 Generált jelölő a forrásban | OK | `motivumok/ISTENTISZT-001.md` | Grep `GENERÁLT\|ÜRES-` → 0. Megjegyzés: a 397. sor (forras egység, bájtra megőrzött) a már nem létező `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md` útra mutat. |
| 5 Archívum (DT215) | OK | `archivum/ISTENTISZT-001/*` | Glob: 3 fájl, lapos mappa, nincs `naplok` almappa. `git diff 89b30c2e:<eredeti> c8e0401f:archivum/…` mindhárom fájlra: egyetlen hozzáadott sor, az első (`<!-- ARCHÍV: <út> @ <commit> · F11 M3 · 2026-10-18 · nem forrás, nem szerkesztendő -->`). A fejléc commitjai (aa59df2b, 82f5c869, cd43a2fd) egyeznek a `git log -1 89b30c2e -- <út>` kimenetével. |
| 5 Fájlnév-ütközés | **ELTÉRÉS (alacsony)** | `generalt_proba/tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` | Glob: az archív napló alapneve megegyezik egy verziózott `generalt_proba/` fájléval. A `general.py --cel naplok` a régi `relativ` úttal ide ír tovább (`general.py:1986`). A DT215 kikötése szerint az alapnév nem ütközhet; az E27 alapnév szerint old fel. |
| 6 M3.3 `res_forras`, `forras_study` | OK | `adat/res_forras.tsv:10-16`; `adat/motivumok.tsv:4` | `git diff …`: 4 sor `tanulmany` → `motivumok/ISTENTISZT-001.md`, 3 sor `adat` üres mezővel; a forras_study első eleme átírva. A NYITOTT generált blokkja: 318 elutasítva (Grep count = 318), 259+50 (Grep `beépítve\|nyitva` = 309). |
| 6 Az index és a nyitott generált blokkja = generátor | NEM ELLENŐRIZHETŐ | — | Ehhez `general.py --ellenoriz` kellene. |
| 6 Hivatkozás-frissítés (A2) | **ELTÉRÉS (alacsony)** | `NYITOTT_FELADATOK.md:136` (N-F09h), `FELADATOK.md:82`, `NYITOTT_FELADATOK.md:327` (N17) | Az N-F09h és a FELADATOK-sor most az archív fájlt jelöli meg javítandó forrásként, pedig az archívum nem szerkesztendő. Közben a CC BY-SA 3.0 sor már sem az élő lapon, sem a forrásban nincs: Grep `CC BY-SA 3\.0` a két fájlban → 0, `git diff … lexikon/… \| grep -c '^-.*CC BY-SA 3\.0'` → 1. A tétel így félrevezetően „nyitott”; a `lexikonok_nyers/README` része valóban nyitott. Az N17 „(92. sor)” hivatkozása nem tolódott +1-gyel: az archív 93. sor a `LXX_kivonat` sor. Megjegyzés: a 2026.09.09-i és 09.23-i történeti bejegyzések útja is átírva („commit 8df6650” mellett). |
| 6 F70 és F11 brief-fejléc | **ELTÉRÉS (alacsony)** | `F70_SZOTAR_S26_BRIEF.md` `ir`; `F11_MIGRACIO_BRIEF.md:12` | Az F70 `ir` mezője a törölt `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`-re mutat, és a 2b rés célja `adat` lett. Az F11 `kovetkezo` mezője az M2-állapotot írja („az M3 a DT215 … után indul”). |
| 6 `general.py` naplok-tartalék | OK (megjegyzés) | `eszkozok/general.py:1988-1991` | Az `os.path.exists` tartalék minden motívumra él, nem csak a migráltra, így más motívum hiányzó naplója is csendben NAPLO_MD-sorvéget kapna. |
| 7 M3.5 E9-kivétel | OK (kód), NEM ELLENŐRIZHETŐ (futás) | `eszkozok/ellenorzes/szabalyok.py:552-568`; `tesztek/test_szabalyok.py:250-264` | `git diff … -- eszkozok/ellenorzes/`: útvonal-előtag szerinti kivétel. Egy teszt `archivum/` alatt 0 találatot, egy `tematikus_lezart/` alatt 1 HIBA-t vár. A kivétel az ARCHÍV fejlécet nem ellenőrzi (gyenge őr). A `unittest`-futás a parancskörön kívül esik. |
| 8 M3.6 éles lap = generátor | NEM ELLENŐRIZHETŐ | `lexikon/ISTENTISZT-001_TUDOMANYOS.md` | Az újragenerálás a parancskörön kívül esik. Ami ellenőrizhető: 0 【NAPLO】 a lapon (Grep). Tájékoztatásul: `git diff --stat c8e0401f:generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md c8e0401f:lexikon/ISTENTISZT-001_TUDOMANYOS.md` → 906+/292−, 97 hunk az aranymintához képest; ez az M4 mérésének tárgya. |
| 8 Kolofon napló-cella (ismert) | **ELTÉRÉS (közepes)** | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1987` | Az éles lap a már nem létező `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md`-re mutat (G.ID_NAPLO_TERKEP). A javítás helye a generátor, nem a lap. |
| 9 CI | OK (feltétellel) | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 89b30c2e..c8e0401f) --diff-alap 89b30c2e --diff-fej c8e0401f --commit-uzenet "$(git log --format=%B 89b30c2e..c8e0401f)"`: egyetlen HIBA az E16 („a cím nem [ELLENŐRZŐ] előtagú”); E11=1, E12=309, E13=101, E25=3, E27=40 JELENTÉS; E28 „0 migrált nézet”. Ugyanez `--pr-cim "[ELLENŐRZŐ] F11.M3: szétválasztás"` kapcsolóval: 0 HIBA. A PR címének tehát `[ELLENŐRZŐ]` előtaggal kell kezdődnie. A `--commit-uzenet-fajl <(…)` Windows-Pythonon nem nyílik meg (FileNotFoundError), ezért argumentumként adtam át. |
| 9 `ellenoriz.py`, `feladatok.py`, `unittest`, N0 | NEM ELLENŐRIZHETŐ | — | A parancskörön kívül esik. Az M3.3 commit-üzenete N0-t állít („csak a két ISTENTISZT-001 lexikonfájl tér el”); ezt nem igazoltam. |
| 10 DT215/e/f | OK (alak), NEM ELLENŐRIZHETŐ (szó szerinti idézet) | `DONTESEK.md` 3 új sor | `git diff … -- DONTESEK.md`: csak helyőrzők, 🟢, végleges DT-szám nincs. A „Felhasználó … (chat, a szülő session közvetítésével)” idézetek hitelessége a repóból nem igazolható. A DT216 javaslata A, a döntés B; ez a Javaslat oszlop, nem hiba. A sorrend rendben: DT215 (6c27b14a) az M3.1 előtt, DT216 (f8dc496c) az R.1 előtt, DT217 (53a20afb) az M3.4–M3.6 előtt. |
| Lista 1: törölt sorok | OK | `motivumok/ISTENTISZT-001.md` | `git diff --stat c8e0401f:archivum/…_tematikus.md c8e0401f:motivumok/ISTENTISZT-001.md`: 211 törölt / 52 új sor. Kategóriák a leképezési tábla szerint: generalt 38, archivum 56, adat 20 egység (a 20 adat egység = 10 jelölt + 24 kapcsolat-indoklás 15 cellából + 5 SECE-sor). |
| Lista 2: kulcstartomány | OK | — | Az adat egységek mind célba értek: T29/2–16 → 24 sor, T20/2 + T22/3 → 10, T56/T65/T66 → 5. |
| Lista 3: nulla-diff hatóköre | NEM ELLENŐRIZHETŐ | — | Az N0 a generált kimenetre vonatkozik (HAMART-001 és a többi motívum), a commitolt fájlokra nem. A commitolt `lexikon/` alatt csak az ISTENTISZT-001 TUDOMANYOS változott (`git diff --stat … -- lexikon/`). |
| Lista 4: TSV Δ (E17, DT3) | OK | — | `git diff --numstat 89b30c2e..c8e0401f`, fejléc nélkül: `adat/jeloltek.tsv` +10; `adat/lexikon_hivatkozasok.tsv` +5; `adat/kapcsolatok.tsv` 0 (24/24); `adat/res_forras.tsv` 0 (7/7); `adat/motivumok.tsv` 0 (1/1); minden más `adat/` és `konkordancia/` `.tsv` 0. A |Δ|≥10 a `jeloltek`-et érinti: bontás a leképezési tábla T20/2 (C-minta, 3) és T22/3 (D-minta, 7) sorában és az M3.1 commit-üzenetében; külön bontási napló nincs. |
| Lista 5: ⛔ pontok | OK | — | Az M3 ⛔ (DT215) a végrehajtás előtt eldőlt. A „merge csak zöld M4 után” (DT217) még nyitott: M4 nem futott. |
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
| 9 `ellenoriz.py` | OK | `RENDBEN: 12 \| SÉRTÉS: 0 \| KÉZI: 2 \| JELENTÉS: 3` (a 11. szabály a c8e0401f-en zöld; az 53a20afb–73613284 között SÉRTÉS volt, a DT217 (1) szerinti újragenerálásig) |
| 9 `feladatok.py ellenoriz` | OK | `137 brief, 0 hiba, 0 figyelmeztetés` |
| 9 `unittest discover` | OK | `python -m unittest discover -s eszkozok/ellenorzes/tesztek` → 187 teszt, OK |
| 9 CI | OK (feltétellel) | `futtat.py … --diff-alap origin/main --diff-fej HEAD --commit-uzenet-fajl <üzenetek>`: egyetlen HIBA az E16 (PR-cím `[ELLENŐRZŐ]` előtag); E28 „0 migrált nézet”, E29 0 |
| 9 N0 | OK | `bash eszkozok/nulladiff.sh origin/main 2026-10-18` (origin/main = 89b30c2e): eltér csak `lexikon/ISTENTISZT-001_TORZSCIKK.md` és `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (a migrált motívum, várt); a HAMART-001 és minden más motívum bájtra azonos. Ugyanez az R.1, M3.1 és M3.3 után is. |

**Az orkesztrátor összegzése.** A gépi ellenőrzések mind zöldek (az E16 a PR-cím dolga). Az ellenőr piros ítélete az éles lap három közepes eltérésén áll (2b rokon szavak, a két horgony nélküli töredék, a Kolofon napló-útja); ezek és az alacsony tételek a felhasználó döntésére várnak, javítás nélkül. A brief `megallt`; az M4 nem indult.

## 9. A javítókör újraellenőrzése (08f4eaed..252d9ce8)

*A független ellenőr (`fuggetlen-ellenor`) jelentése, szó szerint; a fájlba az orkesztrátor fűzte (az ellenőrnek nincs írási eszköze).*

ELTÉRÉS: 2 tétel

*Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `08f4eaed..252d9ce8` (F11.M3.8–M3.17, 10 commit, 14 fájl, +177/−41) · ellenőr: claude-opus-5-5 (kért: `opus`).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A tényleges modell claude-opus-5-5, a kért `opus`. A tartomány egyetlen adattáblába sem ír `modell` mezőt (`git diff 08f4eaed..252d9ce8 -- '*.tsv'`: `kapcsolatok`, `res_forras`, `F11_szetvalasztas`, egyikben sincs ilyen oszlop). |
| 1 (7./1.) 2b: mind az 5 SECE-sor | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1202-1238`; `eszkozok/lexikon_general.py` `adatres_2b_tokenek`, `_adatres_2b` | A `git diff … -- lexikon/` szerint a lapon G1941, H7121, H8034, G0994, G2564 áll, ebben a sorrendben. A Grep `\t(SECE_G\|SECE_H\|MCGED)\t` az `adat/lexikon_hivatkozasok.tsv`-ben pontosan ezt az 5 sort adja (27–31). Az új két részlet karaktersora egyezik a 28. és 29. sorral. A rokon tokenek a `rokon_szavak_strongok(sorai, tokenek)` kimenetéből jönnek, ismétlés nélkül. A lap „Rokon szavak” alszakasza (1154–) a G0994-gyel kezdődik. A forrás prózája változatlan: a `motivumok/ISTENTISZT-001.md` diffje csak a 141–153. sor körül mozdul, a „mindhárom ige” sor (`motivumok:73`) nincs a diffben. Más motívumra nem hat, mert a `_adatres_2b` csak `forras=adat` + üres `tanulmany` sorra fut, ilyen pedig csak az ISTENTISZT-001 három sora (`res_forras.tsv:11,13,14`). |
| 2 (7./2.) A 24/6 és 25/8 részlet horgonnyal | OK | `motivumok/ISTENTISZT-001.md:151-152`; `lexikon:1732-1733`; `archivum/ISTENTISZT-001/ISTENTISZT-001_forrasreteg_regi.md:25-26`; `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv:205,207` | A két sor a Peshat-bekezdés („…Beérseba).”) után, a **Remez:** előtt áll. Előtagjuk „- **1Móz 13:4** — ” és „- **1Móz 21:33** — ”, bájtra egyezik az archív 25. és 26. sor elejével (Read). A részletek szövege változatlan. A régi, horgony nélküli helyükről (a Peshat előtt) a két sor törölve van, a forrásban és a lapon is. A leképezési tábla M7/6 és M7/8 `cel` mezőjébe bekerült a „hely: …; horgony: …” tag. Szúrópróba: `python eszkozok/lekerdez.py karoli "1Móz 13:4"` → „…és segítségűl hívá ott Ábrám az Úrnak nevét.” (`scope=range:1Móz 13:4 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=1 \| ts=2026-10-18T15:38Z`). `karoli "1Móz 21:33"` → „…az örökkévaló Úr Istennek nevét.” (n=0 KH, `ts=2026-10-18T15:38Z`). `scan H7121 --szakasz "1Móz 13:4"` és `--szakasz "1Móz 21:33"` → 1-1 előfordulás (`forras=TAHOT_kivonat.tsv \| strong=H7121 \| n=1`). A 21:33 „egyetlen genezisi hely” állítását a `kollokacio H7121 H5769` támasztja alá: a Genezisből csak 1Móz 17:19 és 21:33 jön, és a 17:19 nem a formula (`scope=TAHOT-teljes+TAGNT-teljes \| strong=H7121+H5769 \| n=11 \| ts=2026-10-18T15:40Z`). |
| 3 (7./3.) Kolofon napló-cella | OK | `lexikon:2011`; `lexikon_general.py` `kolofon_naplo_cella` | A cella most: „generált (`adat/jeloltek.tsv`); a régi napló archívum: `archivum/ISTENTISZT-001/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md`”. A HAMART-001 és a többi térképezett motívum cellája nem változik. A `NAPLO_ID_TERKEP` 7 fájljából 6 megvan a `tematikus_lezart/naplok/` alatt (Glob), ezeknél a régi ág fut. A hetedik az ISTENTISZT-001-é, ez csak az `archivum/` alatt van (Glob). A `lexikon/HAMART-001*` nincs a diffben. A teszt 3 esete pozitív és negatív ágat is lefed (`teszt_lexikon_adatres.py` `KolofonNaploCella`). Mellékhatás, nem hiba: ha egy nem migrált motívum naplója hiányzik, a cella ezentúl „—”, és nem lóg az útja. |
| 4 (7./4.) A három generált rés | OK | `lexikon:1202,1204,1238` (2b); `1470,1472,1565` (minosites); `1668,1670,1695` (alatamasztas); `adat/res_forras.tsv:11,13,14`; `adat/SEMA.md:715` | Mindhárom résnél megvan a `<!-- GENERÁLT-RÉS: [rés] \| general.py --cel lexikon \| forrás: … -->` jelölő, a `*Proveniencia: \`scope=id:ISTENTISZT-001 \| forras=… \| ts=2026-10-18\`*` sor és a `*(generált)*` fejléc. A `res_forras.tsv` 3 sora `*(generált)*`, más motívum sora nem változott (numstat 3/3). A `_boundary_index` először a `*(kézi)*` alakot keresi tartalékként, csak utána a `_LEGACY_FEJLEC`-et; mindkettőre van pozitív és negatív teszt. A SEMA 2.12 `tanulmany` cellája átvezetve. Megjegyzés: a `ts` csak dátum (`G.TS`), időpont nincs benne. |
| 5 (7./5.) T29/4 „jelölve” | OK | `adat/kapcsolatok.tsv:14`; `lexikon:1678-1679` | `git diff --numstat … -- '*.tsv'`: `kapcsolatok.tsv` 1/1. A diffben egyetlen sor változik, az `1Móz 4:26 → Jóel 2:32` `indoklas` cellája, a végére fűzött zárójeles jelöléssel. A két Jóel→ÚSZ sor és minden más cella változatlan. Az Alátámasztás-táblában a sor ezért külön csoport lett. Ez várt hatás. |
| 6 (7./6.) N-F09h, FELADATOK, N17 | **ELTÉRÉS (alacsony)** | `FELADATOK.md:82`; `NYITOTT_FELADATOK.md:136,327`; `F70_SZOTAR_S26_BRIEF.md:28`; `lexikon/ISTENTISZT-001_TORZSCIKK.md:1091` | Ami rendben van: egyik hely sem jelöli javítandónak az archívumot. Az archív 233. sorban valóban CC BY-SA 3.0 áll (Read). Az N17 „93. sor”-a helyes, az archív napló 93. sora a `LXX_kivonat_Zsoltarok.tsv` sor (Read). Az eltérés: a FELADATOK:82 szerint „az ISTENTISZT-001-en a hiba megszűnt … az éles lapon … nincs CC BY-SA 3.0”, és az F70 állapot-megjegyzése szerint a sor „sem a forrásban, sem az éles lapon nincs”. Az éles `lexikon/ISTENTISZT-001_TORZSCIKK.md:1091` viszont ma is „LSJ … — CC BY-SA 3.0”-t ír (Grep `CC BY-SA 3\.0`). Az N-F09h saját korábbi mondata („az éles ISTENTISZT-001 törzscikk LSJ-címkéje a #36 felzárkóztatásában frissül”) ezt lefedi. A FELADATOK-sor és az F70 állapot-megjegyzése viszont a megszűnést mondja ki, a törzscikk kivétele nélkül. |
| 7 (7./7.) F70 `ir`/`olvas`, állapot-megjegyzés | OK (megjegyzés) | `F70_SZOTAR_S26_BRIEF.md:13-14,28` | Az `ir` mező `[motivumok/ISTENTISZT-001.md]`, az `olvas` az új forrással bővült, az állapot-megjegyzés kimondja, hogy a hatókör felülvizsgálata a felhasználóé. Megjegyzés: az `ir` átírása egy másik feladat írási hatókörét tette át az új kézi forrásra. Ezt a M3.12 a DT218 előtt tette meg, a DT218 pedig ezt mondja: „az F70 később”. Döntést nem sért, de az F70 hatóköre így már előre át van írva. |
| 7 (7./7.) F11 `kovetkezo` | **ELTÉRÉS (alacsony)** | `F11_MIGRACIO_BRIEF.md:12` | A fej állapotában a `kovetkezo` mező ezt írja: „az 1. … és a 2. pont … javaslattal döntésre vár; utána a végrehajtás”. Az 1. és a 2. pont a DT218 szerint eldőlt (7c3c9f47), és végre is van hajtva (ab77e7fa, 252d9ce8). A mezőt a M3.14 írta, a M3.15–M3.17 nem frissítette. A git log szerint a helyes állapot: a javítókör mind a 8 pontja kész, következik a független újraellenőrzés, utána az M4. |
| 8 (7./8.) `general.py --cel naplok` | OK (kód), NEM ELLENŐRIZHETŐ (futás) | `eszkozok/general.py:1984-1998` | Kódolvasás: ha a térképezett napló a `tematikus_lezart/naplok/` alatt nincs meg, az `archivum/[ID]/` alatt viszont igen, akkor a `celfajlnev=None` miatt az `else` ág fut. Ez `ISTENTISZT-001_kereszthivatkozas_naplo_GENERALT.md`-be ír, `forras_ut=NAPLO_MD` sorvég-méréssel. A többi 6 motívum naplója megvan (Glob), náluk a régi ág fut, változatlanul. Megszűnt a korábbi, minden motívumra élő `NAPLO_MD`-tartalék is (ELLENOR 7. szakasz 6/„naplok-tartalék” megjegyzés). A maradványt a jelentések kimondják: a 99c2d61f commit-üzenete („Marad: … generalt_proba/…/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md … jelentett maradvány, a felhasználó döntése”), a `DONTESEK.md` DT218 idézete („A generalt_proba névütközés kimondott maradványként marad”) és az F11 brief 5. szakaszának DT218 sora. A Glob mindkét fájlt mutatja: `generalt_proba/tematikus_lezart/naplok/…` és `archivum/ISTENTISZT-001/…`. Nem javítottam. A futtatás kívül esik a parancskörön. |
| 9 Hatókör (`ir`) | OK | `F11_MIGRACIO_BRIEF.md:22` | `git diff --stat 08f4eaed..252d9ce8`: 14 fájl. 12 az `ir` mezőben van. A maradék kettő a `DONTESEK.md` (a CLAUDE.md döntési szabálya szerint) és a saját brief fejléce. |
| 9 DT218 | OK (alak), NEM ELLENŐRIZHETŐ (idézet hitelessége) | `DONTESEK.md` (új sor a DT217 után) | Helyőrző, 🟢, végleges `DT<n>` nincs. A sorrend rendben: a 7c3c9f47 megelőzi az ab77e7fa-t és a 252d9ce8-at. |
| 9 Push | OK | — | `git log --remotes --oneline --grep="F11.M3"` → 0 sor: egyetlen távoli ref sem éri el az F11.M3 commitokat (az utolsó fetch szerint). |
| 10 CI | OK (feltétellel) | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 89b30c2e..252d9ce8) --diff-alap 89b30c2e --diff-fej 252d9ce8 --commit-uzenet "$(git log --format=%B 89b30c2e..252d9ce8)" --pr-cim "[ELLENŐRZŐ] F11.M3"` → kilépési kód 0, 0 HIBA. E11=1, E12=317 (a c8e0401f-en 309; a +8 az új jelölő-, proveniencia- és listasorokból várható), E13=101 (változatlan), E25=3, E27=40, E28 „0 migrált nézet”, E14/E15/E16/E26/E29=0. Ítélni nem kell: az ágon nincs E16-hiba a `[ELLENŐRZŐ]` PR-címmel. |
| 10 `teszt_lexikon_adatres.py`, `ellenoriz.py`, `feladatok.py ellenoriz`, `nulladiff.sh 89b30c2e 2026-10-18` | NEM ELLENŐRIZHETŐ | — | A parancskörön kívül esnek. A commit-üzenetek 17, ill. 18 tesztesetet állítanak. Grep `def test_`-tel a fájlban a 4 új eset megvan, futásuk nincs igazolva. Az N0 („csak a két ISTENTISZT-001 lexikonfájl tér el”) nincs igazolva. Megjegyzés: a commitolt `lexikon/ISTENTISZT-001_TORZSCIKK.md` nincs a tartományban; a generált törzscikk N0-eltérése a c8e0401f-en is várt volt (8. szakasz). |
| Lista 1: törölt sorok | OK | — | `git diff --stat`: −41 sor. Kategóriák: áthelyezett forrássor 2 (+2 üres) a `motivumok`-ban és ugyanennyi a lapon. Fejléc-csere 3 (`res_forras`) + 3 (lap). Cellacsere 1 (`kapcsolatok`), 2 (leképezési tábla), 1 (lap Kolofon), 1 (lap Alátámasztás-sor, kettéválik). Mezőcsere 2+1 (F70 `ir`/`olvas`, Csatolt tétel), 1 (F11 `kovetkezo`), 1+2 (FELADATOK, NYITOTT), 1 (SEMA). Kód: `general.py` 4, `lexikon_general.py` 9, teszt 1. Tartalomvesztés nincs. |
| Lista 2: kulcstartomány | OK | — | A 2b tokenhalmaza (3 saját + 2 rokon) = a `lexikon_hivatkozasok.tsv` SECE/MCGED sorainak teljes halmaza (5/5, Grep). |
| Lista 3: nulla-diff hatóköre | NEM ELLENŐRIZHETŐ | — | Az N0 a generált kimenetre vonatkozik, a commitolt fájlokra nem. A commitolt `lexikon/` alatt a tartományban csak az ISTENTISZT-001 TUDOMANYOS változott (`git diff --stat`). |
| Lista 4: TSV Δ (E17, DT3) | OK | — | A tartományban (`git diff --numstat 08f4eaed..252d9ce8 -- '*.tsv'`): `kapcsolatok` 0, `res_forras` 0, `naplok/F11_szetvalasztas` 0. A main-hez képest (`git diff --stat 89b30c2e..252d9ce8 -- adat/ konkordancia/`, fejléc nélkül): `jeloltek` +10, `lexikon_hivatkozasok` +5, `kapcsolatok` 0 (24/24), `res_forras` 0 (7/7), `motivumok` 0 (1/1), a többi 0. A \|Δ\|≥10 csak a `jeloltek`-et érinti; a bontása a 7. szakasz Lista 4 sora szerint nem változott. |
| Lista 5: ⛔ | OK | — | Merge nem volt, M4 nem futott; a „merge csak zöld M4 után” (DT217) érvényes. |
| A1 | OK | `kapcsolatok.tsv:14` | A T29/4 jelölése megvan. |
| A2 | ELTÉRÉS → 6. sor | — | A törzscikk CC BY-SA 3.0-ja. |
| A3 | OK | — | A tartomány nem hoz új tematikus vagy lexikai párhuzamot. |
| A4 | OK (megjegyzés) | `motivumok:151` | A Sod szövege nem változott. Az 1Móz 13:4 részlet („a hűtlenség … helyéről az imádat helyére”) értékelő olvasat, most a Peshat alatt áll. Ezt a felhasználó döntötte el (DT218 (2)), nem hiba. |
| A5 | nem érintett | — | A tanítói szakasz nincs a diffben. |
| A6 | OK | — | E13=101, E14=E15=0, változatlan. |
| Tanulmány-ellenőrzés (F37 T4) | nem él | — | A diff nem hoz `*_bovitett.md` / `*_tanulmany.md` fájlt. |
| Mellék: leképezési tábla audit-oszlopa | megjegyzés (régi) | `naplok/F11_szetvalasztas_ISTENTISZT-001.tsv:205,207` | Az utolsó oszlop `sed -n '24,24p' motivumok/ISTENTISZT-001.md` ma már az új kézi forrás 24. sorára mutat, nem a régi forrásréteg 24. sorára (archív helye: 25). Nem e javítókör hibája. |
| Parancskör | megjegyzés | — | A `lekerdez.py` és `futtat.py` kimenetét `head`/`tail`/`grep` csövekkel rövidítettem; ezek csak olvastak. |

**Az eltérések súlyosság szerint:**
1. Alacsony: a FELADATOK.md:82 és az F70 állapot-megjegyzése (`F70_SZOTAR_S26_BRIEF.md:28`) azt mondja, hogy az éles lapon megszűnt a CC BY-SA 3.0. Az éles `lexikon/ISTENTISZT-001_TORZSCIKK.md:1091` viszont ma is 3.0-t ír. Az N-F09h a törzscikket a #36-hoz rendeli; a két másik helyről ez a kivétel hiányzik.
2. Alacsony: az `F11_MIGRACIO_BRIEF.md:12` `kovetkezo` mezője szerint az 1–2. pont még döntésre vár, pedig a DT218 és a végrehajtás (M3.15–M3.17) megtörtént.

**Ítélet: zöld megjegyzésekkel.**
- A 7. szakasz 9 eltéréséből a három közepes kijavult: a 2b rés, a két horgony nélküli részlet és a Kolofon. A javításokat a lapon és a kódban igazoltam, mellékhatás nélkül a többi motívumra (statikusan).
- Az alacsony tételek is javultak, egy-egy szűk maradékkal: a törzscikk licenc-kivétele és a saját `kovetkezo` mező.
- A generalt_proba-névütközés kimondott maradvány, ahogy a felhasználó döntötte.
- A tesztek, az `ellenoriz.py`, a `feladatok.py` és az N0 futtatása a parancskörömön kívül esik, ezeket az orkesztrátornak kell futtatnia.

## 10. Az orkesztrátor futtatásai és a két maradék javítása (a 252d9ce8 után)

*Futtatta az orkesztrátor (claude-opus-5-5), 2026-10-18.*

| pont | eredmény | parancs / kimenet |
|---|---|---|
| 9. szakasz 1. eltérés (törzscikk-kivétel) | javítva | A `FELADATOK.md:82`, a `NYITOTT_FELADATOK.md` N-F09h sora és az `F70_SZOTAR_S26_BRIEF.md` állapot-megjegyzése kimondja a kivételt: az éles `lexikon/ISTENTISZT-001_TORZSCIKK.md:1091` LSJ-címkéje még CC BY-SA 3.0; a törzscikk az M5-ben megszűnik (D6), addig a #36 érinti. |
| 9. szakasz 2. eltérés (`kovetkezo`) | javítva | Az `F11_MIGRACIO_BRIEF.md` `kovetkezo` mezője: a javítókör mind a 8 pontja kész, az újraellenőrzés zöld megjegyzésekkel, következik az M4; merge csak zöld M4 után. |
| tesztek | OK | `teszt_lexikon_adatres.py` 18 eset OK; `teszt_general_forras.py`, `teszt_general_kinyeres.py`, `teszt_general_ellenorzo.py` OK; `python -m unittest discover -s eszkozok/ellenorzes/tesztek` 187 eset OK |
| `ellenoriz.py`, `feladatok.py ellenoriz` | OK | `RENDBEN: 12 \| SÉRTÉS: 0 \| KÉZI: 2 \| JELENTÉS: 3`; `137 brief, 0 hiba, 0 figyelmeztetés` |
| index / nyitott / naplo = generátor | OK | `general.py --cel naplo\|index\|nyitott --ellenoriz` → mind 0 |
| `--cel forras` / `--cel kinyeres`, lefedettség | OK | 0 figyelmeztetés; „0 új jelölt-sor, 0 ütközés, 0 ismétlés, 7 ellenőrző jelölő, 0 hiba”; a leképezési tábla 211 sorára 0 hiba |
| éles lap = generátor | OK, a 8. szakasz megjegyzésével | az egyetlen eltérés változatlanul a lap 3–4. sora (két üres sor a GENERÁLT-fejléc után, már a main-en is; az E28-listára vétel előtt rendezendő, M4/M5) |
| N0 (minden javítókör-commit után) | OK | `bash eszkozok/nulladiff.sh origin/main 2026-10-18`: eltér csak `lexikon/ISTENTISZT-001_TORZSCIKK.md` és `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (várt); a HAMART-001 és minden más motívum bájtra azonos |
| CI | OK | az ágon egyetlen HIBA az E16, amelyet a PR-cím `[ELLENŐRZŐ]` előtagja old fel (az ellenőr `--pr-cim`-mel 0 HIBA-t mért); E28 „0 migrált nézet”, E29 0 |

**Kimondott maradványok** (a felhasználó döntése szerint, nem javítva): (1) a befagyasztott `generalt_proba/tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` alapneve egyezik az `archivum/ISTENTISZT-001/` alatti archív naplóéval (DT218; a `generalt_proba/` nem törölhető, az archív név a DT215 szerint az eredeti); (2) az F70 hatókörének felülvizsgálata később (DT218); (3) az éles lap fejlécének két üres sora (M4/M5, az E28-felvétel előtt); (4) a leképezési tábla `forras_parancs` oszlopa a régi fájlútra mutat (a fájlok azóta archívumban).

**Ítélet: zöld megjegyzésekkel.** Az M3 és a javítóköre kész; a brief `megallt`, az M4 nem indult; merge csak zöld M4 után (DT217).

## 11. Az M5 ellenőrzése (3fbb927a..bb1a1052)

ELTÉRÉS: 2 tétel

*Brief: `F11_MIGRACIO_BRIEF.md` · tartomány: `3fbb927abdbe..bb1a10527d84` (F11.M5.0–M5.4, 5 commit, 8 fájl, +17/−10, ebből 1 átnevezés) · ellenőr: claude-opus-5-5 (kért: `opus`) · 2026-10-19. A szakaszt a hívó fűzte a fájlhoz, mert az ellenőrnek nincs írási eszköze.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A tényleges modell claude-opus-5-5, a kért `opus`. A tartomány egyetlen adattáblába sem ír `modell` mezőt: `git diff --numstat -M 3fbb927a..bb1a1052` szerint az `adat/` és a `konkordancia/` alatt nincs változás, az egyetlen TSV az `e28_migralt_nezetek.tsv`, és annak nincs `modell` oszlopa. |
| Tartomány | OK | — | `git log --oneline 3fbb927a..bb1a1052` → 5 commit (ef83773c, bfc5b79e, 760f674a, bfd0ed9b, bb1a1052). `git log --oneline 3fbb927a..main` üres, tehát a base = main. |
| 1a Archív fejléc (DT215 alak) | OK | `archivum/ISTENTISZT-001/ISTENTISZT-001_TORZSCIKK.md:1` | Az 1. sor: `<!-- ARCHÍV: lexikon/ISTENTISZT-001_TORZSCIKK.md @ 300ce93e · F11 M5 · 2026-10-19 · nem forrás, nem szerkesztendő -->`. Ugyanaz az alak, mint a három M3-as archív fájlé (Grep `^<!-- ARCHÍV` az `archivum/ISTENTISZT-001/` alatt). A DT215 szövegében álló „F11 M3” itt a lépés neve szerint „F11 M5”. Ez a mező értelme szerint helyes. |
| 1b Bájtazonosság | OK | ua. | `git diff --numstat 3fbb927a:lexikon/ISTENTISZT-001_TORZSCIKK.md bb1a1052:archivum/ISTENTISZT-001/ISTENTISZT-001_TORZSCIKK.md` → `1 0`. A diff egyetlen hunkja (`@@ -1,3 +1,4 @@`) csak a fejlécsort adja hozzá, a tartalom bájtra azonos. |
| 1c Commit-hash | OK | ua. | `git log --format="%H %s" 3fbb927a -- lexikon/ISTENTISZT-001_TORZSCIKK.md` → egyetlen commit: `300ce93ec17c… R1.7: kereszthivatkozási törzscikk`. Ez a fájl létrehozó és egyben utolsó módosító commitja. |
| 1d Archív példány belső linkje | megjegyzés | `archivum/ISTENTISZT-001/ISTENTISZT-001_TORZSCIKK.md:4` | A `[tudományos lexikonoldal](ISTENTISZT-001_TUDOMANYOS.md)` relatív link az archív helyen nem létező fájlra mutat. A bájtazonosság (DT215) miatt helyesen maradt így. Nem hiba. |
| 2a Élő hivatkozás a megszűnt útra | OK | — | Grep `lexikon/ISTENTISZT-001_TORZSCIKK` (rejtett `.claude/`, `.github/` is) → a `naplok/` és az `archivum/` sorain kívül csak az `F11_MIGRACIO_BRIEF.md:58,92` (az M5 leírása és az N-F11e, jogos) és a `NYITOTT_FELADATOK.md:126` (ez a `generalt_proba/F78_…/lexikon/…` útjának része). A `render_diff_osztalyoz.py` és a tesztje csak alapnévvel hivatkozik, a próba-diffek osztályozására. A briefek `olvas`/`ir` mezőiben (Grep `^(olvas\|ir):.*TORZSCIKK` a `*BRIEF*.md`-ken) csak a `F114:15` `lexikon/ALVIL-001_TORZSCIKK.md` és az F11 `ir` mezője fordul elő. |
| 2b Frissített mondatok igazsága | OK | `FELADATOK.md:83`; `NYITOTT_FELADATOK.md:153,171`; `F70_SZOTAR_S26_BRIEF.md:28` | A „CC BY-SA 3.0 LSJ-címke csak ott áll” állítás: Grep `CC BY-SA 3\.0` → `lexikon/` 0 találat, `motivumok/ISTENTISZT-001.md` 0 találat, az archív törzscikk 1092. sora 1 találat. A „7 törzscikk marad” állítás: Glob `lexikon/*_TORZSCIKK.md` → 7 fájl (ALVIL, ANTROP, HAMART, HODIT, KIRALY, MENNY, TEREMT-001). A „nyitva marad a README:18” állítás: `konkordancia/lexikonok_nyers/README.md:18` ma is `CC BY-SA 3.0`. A `FELADATOK.md` módosított sora (83) a generált blokkokon kívül áll (a jelölők: 13–35, 39–51, 55–67, 71–73, 117–174). |
| 2c (A2) N-F09h: elavult mondat | **ELTÉRÉS (alacsony)** | `NYITOTT_FELADATOK.md:153` | A tétel közepén változatlanul áll: „Az éles ISTENTISZT-001 törzscikk LSJ-címkéje a #36 felzárkóztatásában frissül (l. az F42 utótételt).” Ugyanennek a tételnek a végét az M5.1 átírta („az éles törzscikk … megszűnt … az archívum nem javítandó”), így a tétel saját magának ellentmond. A korábbi mondat már nem igaz. |
| 2d DT215 alapnév-kényszer | **ELTÉRÉS (alacsony)** | `archivum/ISTENTISZT-001/ISTENTISZT-001_TORZSCIKK.md` | A DT215 kimondja: „az E27 alapnév szerint is feloldja a hivatkozást, ezért az archív fájlnév nem ütközhet élő fájléval”. Glob `**/ISTENTISZT-001_TORZSCIKK*` szerint az archív alapnév egyezik három nem archív fájléval: `motivumlog/lexikon_pilot/ISTENTISZT-001_TORZSCIKK.md`, `generalt_proba/F09_szotar_s2_proba/lexikon/…` és `generalt_proba/F78_szerepmatrix_proba/lexikon/…`. A DT218 csak a `generalt_proba` napló-ütközését mondta ki maradványnak. Ezt az ütközést (főleg a `motivumlog/lexikon_pilot/`-ét) a diff sehol nem jelöli maradványnak. Hatás: az E27 a megszűnt `lexikon/ISTENTISZT-001_TORZSCIKK.md` útra mutató elavult hivatkozást alapnév szerint feloldaná, tehát nem venné észre. Ezért a 2a pontot kézi Greppel igazoltam (élő elavult hivatkozás nincs). |
| 2e Az F11 `ir` mezője | megjegyzés | `F11_MIGRACIO_BRIEF.md:15` | Az M5.1 a `lexikon/ISTENTISZT-001_TORZSCIKK.md` utat kicserélte az archív útra. A fej `ir` mezője így nem tartalmazza azt az utat, amelyet a diff töröl (átnevez). A CI ezt nem jelzi. Hibának nem minősítem, csak jelzem. |
| 3a A lap diffje = 3 sor | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1314,1386,1387` | `git diff --numstat` → `3 1`. A hunkok: a 1314. sorban „104 találat” → „106 találat”, és két új sor (1386–1387): `TSK: Hós 2:20 (Votes: 27)`, `TSK: Hós 2:22 (Votes: 27)`. Más változás nincs. |
| 3b Visszavezetés az adatra/generátorra | OK | `konkordancia/TSK_kereszthivatkozasok.tsv:286362-286363` | Grep `^Zak 13:9\tHós` → `Hós 2:21 … 27`, `Hós 2:23 … 27` (KJV-számozás). `python eszkozok/lekerdez.py tsk "Zak 13:9"` → 52 sor, köztük `Hós 2,20 Votes=27` és `Hós 2,22 Votes=27` (`scope=range:Zak 13:9 \| forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv (tsk_kulcs, KJV->Károli) \| n=52 \| ts=2026-10-19T06:23Z`). A Votes ≥ 15 sorok száma 46, a lap 1365–1410. sora szintén 46, sorrendre egyezik. A szöveg is ellenőrizve: `karoli "Hós 2:20"` → „…meghallgatom az egeket…” (= KJV 2:21), `karoli "Hós 2:22"` → „…Én népem vagy te; ő pedig ezt mondja: Én Istenem!” (= KJV 2:23), mindkettő `forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| ts=2026-10-19T06:23Z`. `karoli "Hós 2:23"` → nincs Károli-szöveg. Az összesítő is stimmel: Grep `^- (TSK\|Károli-KH): ` a lapon → 106. Az ok: `git log 4a6fc763..b3651664 -- eszkozok/tsk_kulcs.py` → `3b7fa508 F117.4` (nem őse a lap utolsó commitjának, a `4a6fc763`-nak, és a b3651664 merge hozta be). A b3651664..3fbb927a között a generátor-bemeneteken csak a ff1bbdc5 számkiosztás változtat: egy 【NAPLO】 sort a `motivumok/ISTENTISZT-001.md`-ben, amely a lapon nem jelenik meg (Grep `DT-F11a\|DT215\|szétválasztásával készült` a lapon: 0). |
| 3c Reprodukálhatóság | OK | — | Az E28 maga generál a repón kívül (`szabalyok.py:2027` `tempfile.mkdtemp`, `PARDES_DATUM` = a commitolt lap első `ts=` dátuma, bájt-összevetés a HEAD blobbal), a worktree HEAD-je = bb1a1052. A saját `futtat.py` futásom: „E28 (0 talalat) — E28: 1 migrált nézet”. Az újragenerált lap tehát bájtra egyezik a commitolttal. Külön `general.py --kimenet` futtatást nem végeztem, mert a parancskörön kívül esik. |
| 4a E28-sor oszlopai | OK | `eszkozok/ellenorzes/e28_migralt_nezetek.tsv:2` | A sor: `ISTENTISZT-001 · lexikon/ISTENTISZT-001_TUDOMANYOS.md · lexikon · apparatus · 11 · 2026-10-19`. Az F116 brief 4. pontja (`F116_GENERALT_NEZET_CI_BRIEF.md:108-111`: `id`, `fajl`, `cel`, `melyseg` ∈ {apparatus, olvasoi}, `feladat`, `datum`) és a `szabalyok.py:1819-1829, 2013-2029` szerint (a `cel` a `general.py --cel`-hez, az `id` a `--id`-hez megy) mind a hat oszlop helyes. |
| 4b E28 / E29 a head-en | OK | — | `python eszkozok/ellenorzes/futtat.py --valtozott DONTESEK.md F11_MIGRACIO_BRIEF.md F70_SZOTAR_S26_BRIEF.md FELADATOK.md NYITOTT_FELADATOK.md archivum/ISTENTISZT-001/ISTENTISZT-001_TORZSCIKK.md lexikon/ISTENTISZT-001_TORZSCIKK.md eszkozok/ellenorzes/e28_migralt_nezetek.tsv lexikon/ISTENTISZT-001_TUDOMANYOS.md --diff-alap 3fbb927a… --diff-fej bb1a1052… --esemeny pull_request` → E28 0 („1 migrált nézet”), E29 0. Egyetlen HIBA az E16 (üres PR-cím, a lista az ellenőrző könyvtárban van). Ugyanez `--pr-cim "[ELLENŐRZŐ] F11 M5"`-tel: E16 0, E28 0, E29 0, HIBA nincs. A teljes PR-nek tehát `[ELLENŐRZŐ]` előtag kell (E16). |
| 4c `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | — | A parancskörön kívül esik. Az orkesztrátornak kell futtatnia. |
| 5a DT243 tényszerűsége | OK | `DONTESEK.md:318`; `F11_MIGRACIO_BRIEF.md:91` | `git log -2 3fbb927a -- lexikon/ISTENTISZT-001_TUDOMANYOS.md` → `4a6fc763 F11.M4.5` ✓. A 3b7fa508 (17:34) és a b3651664 (20:22, „Merge branch 'main' into claude/f11-m3b”) ✓. A sorszámok (1314, 1386–1387) ✓, a numstat 3/1 ✓. A javasolt opció (a) egyezik az alkalmazottal. |
| 5b DT243 (b) opció számadata | NEM ELLENŐRIZHETŐ (pontatlan) | `DONTESEK.md:318` | A „24 `GENERÁLT … ts=` sor dátuma is változik” mondatot a lapon mértem. Grep `GENERÁLT.*ts=2026-10-18` → 10, `ts=2026-10-18` → 23, `2026-10-18` → 24. A 24 a dátumot tartalmazó sorok száma, nem a GENERÁLT-jelölőké. Hogy a 2026-10-19 pontosan hány sort írna át, azt generálás nélkül nem tudom eldönteni. Csak a nem választott opció leírását érinti. |
| 5c DT243 jóváhagyás | NEM ELLENŐRIZHETŐ | ua. | A 🟢 és az idézet a chatből jön („a szülő session közvetítésével”). A repóból a hitelessége nem igazolható. |
| 5d N-F11e tényszerűsége | OK | `eszkozok/torzscikk_general.py:454-503` | A `run` minden `motivumok` elemre fut, amelynek van előfordulás-sora. Az egyetlen kihagyási ok a hiányzó `_TUDOMANYOS.md`. `--ir` esetén ír a `lexikon/[ID]_TORZSCIKK.md`-be, a migráltságot nem nézi. Ezt a 10. szakasz N0-mérése is mutatja („eltér … `lexikon/ISTENTISZT-001_TORZSCIKK.md`”). Az állítás igaz. |
| 5e Helyőrző-szabály | OK | — | A diffben új döntés-azonosító csak a `DT243` és az `N-F11e`, végleges `DT<n>`/`N<n>` nincs. Az előző betűk foglaltak: N-F11d a `DONTESEK.md:297`-ben, DT-F11i az `ellenoriz.py:530`-ban, tehát a j és az e a következő szabad betű. Az N-F11e a `NYITOTT_FELADATOK.md`-be nem került be („a merge után, `/befogad` útján”). |
| 6 A brief fejléce | OK (a PR-szám NEM ELLENŐRIZHETŐ) | `F11_MIGRACIO_BRIEF.md:8-13` | `allapot: megallt`, `ag: claude/f11-m5` (= a worktree aktuális ága), a `kovetkezo` szerint az M5 kész és az M6 jóváhagyásra vár, az M7 külön kérésre. Ez egyezik a commit-sorral: az M6-jelentés nincs a diffben, az M7 nem futott. A `pr: "#408, #417"` mezőben a #417 létezését `gh` nélkül nem tudom igazolni. |
| M5 „ugyanabban a commitban” | OK | — | `git diff --numstat -M bfc5b79e~1 bfc5b79e` → az átnevezés, a `FELADATOK.md`, a `NYITOTT_FELADATOK.md`, az F70 és az F11 brief egyetlen commitban van. |
| M5 törlés → archiválás | OK | `F11_MIGRACIO_BRIEF.md:58` | A brief „törlést” ír. Az archiválás a felhasználó állandó szabálya (a felhasználói memória „Régi fájl: archiválás” bejegyzése), és a brief M5 sora kimondja. A repó adatából ez nem igazolható, a felhasználó szabálya a forrása. |
| ⛔ pontok | OK | — | Az M6 ⛔: a végrehajtó előtte megállt (nincs ELLENOR-szakasz a diffben). A DT74 (3) befagyasztás: a lap az M6 előtt csak a DT243 (a) jóváhagyásával változott, a 3 sorra korlátozva (3a). |
| Elfogadási feltétel 6 (E27) | OK | — | Az E27-ben 42 JELENTES/FIGYELMEZTETÉS van, HIBA nincs. A kimenet csak az első 3-at mutatja (távoli ágak hiánya). A megszűnt útra az E27 az alapnév-feloldás miatt amúgy sem jelezne (2d), ezért a 2a kézi Grep a döntő. |
| Lista 1: törölt sorok | OK | — | `git diff --numstat -M`: −10 sor. Kategóriák: a brief fejlécmezői 4 (`ag`, `kovetkezo`, `pr`, `ir`), a brief M5 sora 1, az F70 állapot-megjegyzése 1, a `FELADATOK.md` 1, a `NYITOTT_FELADATOK.md` 2, a lap TSK-összesítője 1. Mindegyik soron belüli csere. Az átnevezés 0 tartalmi sort veszít (1b). |
| Lista 2: kulcstartomány | OK | — | A Zak 13:9 TSK ≥ 15 halmaza a lapon 46/46 egyezik a `lekerdez.py tsk` kimenetével (3b). Más kulcstartományt a diff nem érint. |
| Lista 3: a nulla-diff hatóköre | OK (szűk) | — | A „3 sor” állítás csak a commitolt lapra vonatkozik (base ↔ head blob), és az E28 szerint a head-lap = az újragenerált lap. A többi motívum kimenetére (HAMART-001 N0) nem vonatkozik: a diff nem érint adatot, generátort vagy más motívum fájlját, de N0-t nem futtattam (parancskörön kívül). |
| Lista 4: TSV Δ (E17, DT3) | OK | — | `git diff --numstat -M 3fbb927a..bb1a1052`: az `adat/` és a `konkordancia/` alatt egyetlen `.tsv` sem változott, minden táblán Δ = 0. A körön kívül: `eszkozok/ellenorzes/e28_migralt_nezetek.tsv` +1. Küszöb alatt, bontási napló nem kell. |
| Lista 5: ⛔ | OK | — | Lásd a „⛔ pontok” sort. |
| A1 | OK | `DONTESEK.md:318` | A DT243 lekérdezési állítása proveniencia-sort kap (`scope=lexikon/… \| forras=eszkozok/general.py … --kimenet <tmp> \| ts=2026-10-19`). A NYITOTT/FELADATOK állapotmondatai tényállítások, a fenti Grepekkel igazolva. |
| A2 | ELTÉRÉS → 2c | — | — |
| A3 | nem érintett | — | A diff nem hoz tematikus vagy lexikai párhuzamot. |
| A4 | nem érintett | — | A Remez/Sod szöveg nem változott (`motivumok/` nincs a diffben). |
| A5 | nem érintett | — | Nincs tanítói szakasz a diffben. |
| A6 | OK | — | E12 = 312, E13 = 101 (azonos a 9. szakasz értékével), E14 = E15 = 0. A lap E12/E13 jelentései a már elfogadott állapotból jönnek, a 3 új sor nem ad újat. |
| Tanulmány-ellenőrzés (F37 T4) | nem él | — | A diff nem hoz `*_bovitett.md` / `*_tanulmany.md` fájlt. |
| Parancskör | megjegyzés | — | Két Bash-hívásban a `git`/`futtat.py` kimenetét `head`/`grep` csővel rövidítettem, egyben `for` ciklust használtam a commitonkénti `git diff --numstat`-hoz. Ezek csak olvastak. |

**Az eltérések súlyosság szerint:**
1. Alacsony: a `NYITOTT_FELADATOK.md:153` (N-F09h) közepén megmaradt a mondat, hogy „az éles ISTENTISZT-001 törzscikk LSJ-címkéje a #36 felzárkóztatásában frissül”. Ez az M5 óta nem igaz, és ellentmond a tétel végén frissített mondatnak.
2. Alacsony: az archív `ISTENTISZT-001_TORZSCIKK.md` alapneve ütközik három nem archív fájléval: `motivumlog/lexikon_pilot/` és két `generalt_proba/…/lexikon/` példány. Ez a DT215 „nem ütközhet élő fájléval” kényszerébe ütközik, és maradványként sincs jelölve. Hatása: az E27 a megszűnt útra mutató hivatkozást alapnév szerint feloldaná, ezért nem jelezné. Ma ilyen élő hivatkozás nincs (kézi Grep).

Megjegyzések, nem eltérés: a DT243 (b) opció „24 GENERÁLT … ts= sor” száma a mért 10 / 23 / 24 közül csak a dátumos sorok számával egyezik. A `feladatok.py ellenoriz`, az N0 és a PR #417 létezése nem ellenőrizhető a parancskörömből, ezeket az orkesztrátornak kell igazolnia. A PR címének `[ELLENŐRZŐ]` előtag kell (E16).

**Ítélet: ELTÉRÉS, 2 alacsony tétellel.** A gépi pontok (archív bájtazonosság és hash, a 3 soros lapdiff és annak eredete, E28/E29, az E28-sor oszlopai, a DT243 és az N-F11e tényei, a helyőrzők, a brief fejléce) mind rendben vannak. A merge a felhasználó döntése.

*Az orkesztrátor kiegészítése (2026-10-19, a bb1a1052-n): `python eszkozok/feladatok.py ellenoriz` → 141 brief, 0 hiba, 0 figyelmeztetés; a PR #417 létezik (draft, cím `[ELLENŐRZŐ] F11 M5: …`, E16 rendben). Az N0 (HAMART-001) nem futott: a diff nem érint adatot, generátort vagy HAMART-001-fájlt.*
