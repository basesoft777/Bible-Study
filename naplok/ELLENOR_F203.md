ELTÉRÉS: 3 tétel

# ELLENOR_F203 — `F203_THAYER_FORDITAS_BRIEF.md` · `9926ae542445fcf0d304a415ac31ee70a823de9a..03068b60`

*A `fuggetlen-ellenor` (claude-opus-5-5) jelentése, a végrehajtó mentette szó szerint (az ellenőrnek nincs fájlíró eszköze). A HEAD a megbízás után egy committal (`03068b60`, csak a brief `kovetkezo`) előrébb lépett; a tartomány ezt is fedi.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | tényleges `claude-opus-5-5`, kért `opus`; a végrehajtó commitjai `Co-Authored-By: Claude Opus 5.5`, a jelentés fejléce `claude-opus-5-5` |
| 0 `modell` mezők | NEM ELLENŐRIZHETŐ | `adat/forditasok.tsv:8053`, `:18965…` | a G2671 sz2 és a 68 TBESG-sor `modell` = `claude-sonnet-5-5` (subagent); a subagent tényleges modellje a repóból nem igazolható |
| G/D pontok | — | brief | a briefben nincs G/D szakasz; a Határok és a Tételek „Kész, ha” oszlopa szerint ellenőrizve |
| Határ: tiltott fájlok | OK | — | `git diff --stat base..HEAD -- lexikon/ eszkozok/lexikon_general.py …olvasoi_kapu.py …olvasoi_kovetkeztetes.py …allitas_adat.py …ellenoriz.py …karoli_kh_epseg.py eszkozok/visszhang eszkozok/bdb_jelolt adat/bdb_* adat/elofordulasok.tsv adat/jeloltek.tsv adat/motivumok.tsv generalt_proba/` → üres |
| Határ: helyőrzők | OK | `dontesek/uj/…`, `nyitott/uj/…` | DT-F203a, N-F203a–e; végleges szám az ágon nincs |
| F203.1 aranyminta 787 → 795 | NEM ELLENŐRIZHETŐ | `teszt_vers_jelentes.py` | futtatás kellene; statikusan a `NEM_JAVITOTT` {K3,K4,K1e,K5} + U014 = 5 maradék = 800 − 795, egyezik |
| F203.1 korpusz-változás (1. kérdés) | OK | `adat/thayer_szakaszok.tsv` | a `bont.szerkezet`-et nem futtathattam; a régi ↔ új tábla (a bontó kimenete) összevetése: `git diff … \| grep '^[-+]G' \| cut -f1-5 \| sort \| uniq -u \| cut -f1 \| sort -u` → **64 Strong**. A régi táblából eltűnt összes fej-sor (≈90 sor, mind az 54 K2c/K2d-Strong) átnézve: mind hivatkozás-töredék („c. 142 (and in…”, „d. Zeitschr.…”, „c. 6, p. 397{b}”), zárójeles etimológia (G0329, G0536, G2585, G2855) vagy átnevezés; valódi fej nem nyelődött el (G0812 a/b/c, G3986, G4190, G4183 valódi fejei megmaradtak). K1d: 10 Strongban valódi pont nyílik (G1209 d., G2632 b., G3768 b., G5547 b. …). A korpusz Grep-je (`<p><b>[a-z].</b>` + szám / „and x.”): 26 találat, mind töredék |
| F203.1 `--ellenoriz` azonos | NEM ELLENŐRIZHETŐ | — | csak futtatással |
| F203.1 átkulcsolás (2. kérdés) | OK | `adat/forditasok.tsv` | `git diff … \| grep -E '^[-+][^-+]' \| cut -f1 \| uniq -c` → −75/+75 Thayer, +68 TBESG, egyéb sor nem; 18 Strong; 38+7+10+10+7+3 = 75 = jelentés. Kulcsütközés az írás előtt kiszűrve (`ellenoriz_iras`, első 5 mező; `forditas_atkulcsol.py:452`). Megjegyzés: a `Mai` teszt első állítása (`terv_tabla(…, TB.szakaszok, TB.szakaszok) == []`) triviális (azonos táblánál `continue`, `:293`); a valódi védelem a második fele (hash = kulcsszakasz) |
| N124 `nem_bibliai` (3. kérdés) | OK | `adat/thayer_vers_jelentes.tsv:336-338` | Grep `nem_bibliai` → 3 sor, mind G0027 #12–14; a vers-diffben csak `szakasz`/`utvonal`-átszámozás és ez a 3 `karoli_vers`-ürítés; forrás-Grep: „Ascensio” egyetlen helyen; `python eszkozok/lekerdez.py karoli "Luk 8:18"` → a vers létezik (a régi kitöltés tévesen sikerült) |
| `lista` (4. kérdés) | OK, megjegyzéssel | `eszkozok/glossza_lexikon_forditas.py:214-229, 232-288` | a jelölő `⟦GLF:n⟧` egyedi (előtag-ütközés nincs: a zárójel lezár); alapból repón kívül ír; render nélkül megáll. Kockázat: a jelölő nem üres, így a generátor ágválasztását megváltoztathatja (pl. `lexikon_general.py:6070`: a valódi lapon angol szöveg magyar nélkül áll — ott a jelölő látszik, ez valódi hiány). A „42 → 24” futtatás nélkül NEM ELLENŐRIZHETŐ |
| B4 lapdiff (5. kérdés) | OK, megjegyzéssel | `eszkozok/lapdiff_blokk.py`, `muhely_allapot.py:466-477` | a HAMART/ALVIL-lapon minden kézi próza (Kivonat, „Miért fontos”, Minősítés, Értelmezés) generált blokkon kívül, `kivul:*` néven áll → változása érvénytelenít; a szótári blokkban csak generált olvasói mondat. Rések: a sorvégi szóköz nem számít (`_normal`; Markdownban a két sorvégi szóköz sortörés); a (c) és a „gépi” jelleg nincs gépileg ellenőrizve (a SEMA kimondja). `git diff --stat 05c05743..HEAD -- lexikon/ALVIL-001…` → a Kivonat (19.) és a Jelmagyarázat is változott: a 0 → 0 érvényes átnézés helyes |
| G2671 sz2 (6. kérdés) | OK, megjegyzéssel | `adat/forditasok.tsv:8053-8054` | a proveniencia teljes (subagent, adag 9203, kapu); a beírás alakja = a `beir` szabványos felülírásáé (`forditas.py:229-234`). Az egyedi írószkript nincs a repóban: a „bájtőrző, hash-ellenőrzéssel” NEM ELLENŐRIZHETŐ. `lekerdez.py scan G2671` → 5 hely, mind a fordításban |
| 68 TBESG-sor (6. kérdés) | **ELTÉRÉS** | `adat/forditasok.tsv:18965…` (68 sor) | Grep TBESG rövid → 269 = 201 + 68, törlés nincs. De a `megjegyzes` **„F161 (glossza-lánc, …, G001-p1 …)”**: a `MENETJEL` beégetett menetjelölés (`glossza_api_koteg.py:724`) — az F203-as sorok F161-esnek látszanak, és a `custom_id` (G001-p1 …) menetek között nem egyedi |
| „Ádám” (6. kérdés) | OK, megjegyzéssel | `adat/forditasok.tsv:18967` | a javítás jelölve („F203: kézi javítás … ádám → Ádám”); a „kapuk átmentek” a javítás előtti alakra szól; `allapot` = `sonnet` |
| Tesztek (7. kérdés) | NEM ELLENŐRIZHETŐ | — | tesztet nem futtathatok. Statikusan: a `Sigla`-bukás az F186 jelentés 273./441. sorában korábbról dokumentált (66 ≠ 60) → OK; a `TeljesUt` G4151/G0444-et használ, nem TIPNR-Strongot, a tulajdonnév-jelzés valószínűleg nem okozza; a `TesztHatarFrissesseg` és a 4 olvasó-szerver BDB-teszt függetlensége nem igazolható |
| F203.5 „Kész, ha” | **ELTÉRÉS** | brief 42. sor | a feltétel: „`teszt_futtat.py --gyors` és a saját tesztek zöldek”; a jelentés 5. pontja szerint 4 + 1 + 1 + 1 bukás/hiba; a „korábban is bukott” ellenőrizetlen (7. kérdés) |
| F203.4 ⛔ költség | NEM ELLENŐRIZHETŐ | jelentés 4. | a becslés megvan (9 161 Strong, 87 442 karakter); a felhasználói idézetek („mehet előfizetésből”, „Csak az olvasó-fázisban döntsünk”) csak a végrehajtó állításai |
| A1 | OK | jelentés | proveniencia-sorok vannak; a „más nem bibliai műnél nincs `bcv`” állításból csak az Ascensio-rész igazolt |
| A2 | OK | `NYITOTT_FELADATOK.md` | N-F12e, N-F184a, N124 lezárása a kódban teljesül; N125/N126 részben, N123 nyitva; N-F203a–e valóban nyitott |
| A3–A5 | nem alkalmazható | — | nincs tanulmány, párhuzam vagy tanító |
| A6, CI-egyezés | NEM ELLENŐRIZHETŐ | — | CI-jelentést nem kaptam; a saját `futtat.py` futás a lezárásig nem adott kimenetet; az E1-et (`ellenoriz.py`, 13. szabály) a `futtat.py` nem futtatja |
| 1.6 E28 | NEM ELLENŐRIZHETŐ | jelentés 1.6 | repón kívüli render kellene; a mai HAMART-lap 1413–1415. során a hamis „c (hivatkozás nélkül)” pont valóban áll. A brief új `kovetkezo` terve (lapok újragenerálása) a mostani `ir`-en kívül esik (`lexikon/*`): határ-módosítás kell hozzá |
| L1 törölt sorok | OK | — | szakaszok −52 (K2c/K2d, 48 Strong) / +11 (K1d, 10 Strong); forditasok 0 törölt, 75 módosított, +68; vers 0 törölt, 3 `karoli_vers` üres; forras_javitas csak `ts` |
| L2 kulcslefedés | OK, megjegyzéssel | — | új fordítatlan Thayer-szakaszok lapon kívül (G5547 sz5, G4160 sz23, G1538 sz3 …; N-F203b); TBESG-lefedettség 269 / 9 362 |
| L3 „nulla-diff” hatóköre | OK | — | forras_javitas: 0 nem párosuló sor (csak `ts`); vers_jelentes: tartalmilag csak a 3 G0027-sor; „a mai táblán üres terv” csak azonos táblára igaz (2. kérdés) |
| L4 Δ táblánként | **ELTÉRÉS** | `naplok/F203_jelentes.md` 1. | `thayer_szakaszok.tsv` **−41**; `forditasok.tsv` **+68** (bontás a 4. pontban, OK); vers 0; forras_javitas 0; `konkordancia/` 0. A −41-hez a jelentés csak Strong-szintű bontást ad (54/10), a sorszintű −52/+11 egyeztetés hiányzik |
| L5 ⛔ | OK / NEM ELLENŐRIZHETŐ | — | lap nem generálódott újra; a felhasználói döntés valódisága: l. F203.4 |

ELTÉRÉS-ek súlyossági sorrendben: (1) F203.5: a kész-feltétel (zöld tesztek) nem teljesül, a bukások függetlensége nem igazolt; (2) a 68 TBESG-sor provenienciája F161-es menetjelölést és nem egyedi `custom_id`-t visel; (3) E17/DT3: a `thayer_szakaszok.tsv` −41 sorának nincs sorszintű bontása (−52/+11).

## Az ellenőr kiegészítése (a saját `futtat.py`-futása után)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| A6, E12–E15 | OK | — | `futtat.py --valtozott <25 fájl> --diff-alap 9926ae54… --diff-fej HEAD`: E12–E15 0 találat |
| CI-egyezés / 1.6 E28 | OK (merge-feltétel) | `lexikon/ISTENTISZT-001…:866`, `ALVIL-001…:1114`, `TEREMT-002…:423` + 2 | E28 5 HIBA („5 migrált nézet”), az LXX-blokk tooltipjeiben: egyezik a jelentés 1.6 pontjával |
| a CI egyéb találatai | OK | — | E25, E27, E34, E36 korábbi sorokra; E32 a `muhely_allapot.py:829` régi során; E30 (3 FIGYELMEZTETÉS) ékezet nélküli blokk-/függvénynév a `da6590fa`, `f217a636` üzenetében |
| E1 / 13. szabály | NEM ELLENŐRIZHETŐ | — | a `futtat.py` nem futtatja |

Az ELTÉRÉS-ek száma és sorrendje változatlan (3).

## Javítókör 1 (a végrehajtó, 2026-11-11)

A végrehajtó válasza és javításai: `naplok/F203_jelentes.md` 7. pont.
