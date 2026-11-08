ELTÉRÉS: 12 tétel

# ELLENOR_F123_HAMART-001: F123_MIGRACIO2_BRIEF.md (U2–U4, U3b, U7), `c6aa7b0c..3545baf7`

*A `fuggetlen-ellenor` subagent jelentése (2026-11-05). A subagentnek nincs fájlíró eszköze, ezért a szöveget a menet session-je (claude-opus-5-5) mentette, tartalmi változtatás nélkül, a két válaszát (az első jelentés és a CI-kiegészítés) egyesítve, tömörítve a parancssorokat. Az ellenőrzés közben a HEAD változott (`1f65c5eb` → `3545baf7`); az ellenőrzés a `3545baf7`-ig terjed. Egy összetett hívásban egy megengedetten kívüli, csak olvasó parancs (`head -3 adat/szotar_szakasz_cimke.tsv`) futott le.*

**Modell:** a session `claude-opus-5-5`, a kért `opus` — egyezik.

## Eredménytábla

| pont | eredmény | fájl | indok (röviden) |
|---|---|---|---|
| 1 Kivonat-számok (60 sor, 25/25/10, 86 vers, 7 tematikus) | OK | `motivumok/HAMART-001.md` | Grep, számlálás |
| 1 Scan-számok (H0779 52, H0127 211, H2555 59, H7843 135, H2403 271, G1944 2, G2671 5, G5356 8, G5351 8, G1311 5) | OK | | `lekerdez.py scan` |
| 1 Itzávón háromszor; kóc+dardar csak 1Móz 3:18, Hós 10:8; φθείρω+γῆ csak Jel 11:18, 19:2; málé/sámá+chámász 8/4 | OK | | `scan`, `kollokacio` |
| 1 Igealakok (H0779, H7843, 8:21 qalal) | OK | | `igealak` |
| 1 Károli-idézetek az 1/a-ban (60 sor) | OK | | `karoli` 65 versre |
| 1 Szótári mezők belső ellentmondása (1Móz 3:23, 4:14, 6:12, 8:21: a `jelentes_szam` új, a `jelentes_en`/`jelentes_hu` régi; a nyílt magba is exportálva) | **ELTÉRÉS (magas)** | `adat/elofordulasok.tsv`; `nyilt_mag/elofordulasok.tsv` | `git diff`, `bdb_szakaszok.tsv` |
| 1 „Négy sor több verset fog össze” — valójában 11 tartomány-sor | **ELTÉRÉS (alacsony)** | `motivumok/HAMART-001.md` 1. szakasz | |
| 1 Ez 12:19: a Kivonat „az erőszakkal megtelt föld”-et állítja; a versben a melóá (bőség) főnév áll, a málé+chámász kollokáció nem | **ELTÉRÉS (alacsony–közepes)** | Kivonat; `elofordulasok.tsv` | `scan H4393`, `kollokacio H4390 H2555` |
| 1 Nem szó szerinti alak idézőjelben („kezünk terhes fáradozását”, „megtelt erőszakkal”, „az Izráel vétkét”) | **ELTÉRÉS (alacsony)** | md; `jeloltek.tsv` (Hós 10:8); nyílt mag | `karoli` |
| 1 Zsolt 14:1 „ugyanaz a héber igealak” — azonos törzs, más személy/szám | megjegyzés | `elofordulasok.tsv` | `igealak H7843` |
| 1 Zsid 6:7-8: a Zsid 6:8-ban κατάρα áll, nem a LXX 3:17 ἐπικατάρατος-a | megjegyzés | `elofordulasok.tsv` | `lxx-hid` |
| 1 Gal 3:10, 3:13 LXX-állítások | OK | | `lxx-hid` |
| 1/G TR-mérce: Jel 22:3 — a Thayer szerint a TR (Rec.) κατανάθεμα, a lap a κατάθεμα alakot nevezi és „eltérés nincs”-et állít; a sor `strong` mezője üres | **ELTÉRÉS (közepes)** | `elofordulasok.tsv`; md | `TAGNT_kivonat.tsv`, Thayer G2652 |
| 2 Ján 7:49: az indok szerint „a motívum saját szava nem áll” (G6035); a Thayer G1944 szerint a TR-ben ἐπικατάρατοι áll — a rögzített indok hamis | **ELTÉRÉS (közepes)** | `jeloltek.tsv`; lap 1/b | Thayer G1944, TAGNT |
| 2 Belső jel hat renderelt indoklásban („(halo=karoli, blokk=tövis\|H7899)”: 4Móz 33:55, Ez 2:6, Jer 22:17, Ján 7:49, Mik 7:4, Mt 11:12) | **ELTÉRÉS (közepes)** | lap 1/b | `git diff \| grep halo=` |
| 2 Jer 51:25 a „katonai pusztítás” kizárással ütközik; az indoklás nem tér ki rá; a BDB nem idézi a verset a H7843-nál (a `Hif'íl 1` a menet besorolása) | **ELTÉRÉS (közepes, tartalmi)** | `jeloltek.tsv`; `motivumok.tsv` | `igealak H7843` |
| 2 Többi döntés (113 új / 109 régi sor; az okok sorrendje; „egyéb” 0) | OK | | |
| 3 Szótári gerinc (szakaszok és idézőhelyek) | OK | `szotar_szakasz_cimke.tsv`, `lexikon_hivatkozasok.tsv` | `bdb_szakaszok.tsv` |
| 4 `olvasoi_kapu.blokkok_1a` | OK, megjegyzéssel (tágít: egy próza előtti, nem Károli dőlt sor is bekerülne) | | |
| 4 `lexikon_general` (Siral → JSir; gyök-regex) | OK; mellékes: a `jeloltek.tsv`-ben „Sir 3:47” (Siralmak) igehely, a kapu a `Sir`-t deuterokanonikusnak veszi | | |
| 4 `nyilt_mag_export` | OK (a változott sorok mind HAMART-001-sorok) | | |
| 5 Nave (7/2/25) | OK, megjegyzéssel (BANISHMENT kiválasztva, miközben a kiűzetés-párhuzam nyitott tétel; FALL OF MAN kiválasztva, DEPRAVITY tiltva) | | |
| A1/A4 A Remez lezárja az 1Móz 8:21 vitáját („a föld átka mint állapot nem szűnt meg”; a 8:21 sora: „csak részben teljesíti”), miközben a vitatott pont szerint a lap „nem dönti el” | **ELTÉRÉS (közepes)** | md; `elofordulasok.tsv` | |
| A5, A2, L1, L5 | OK | | |
| L4/E17 A `lexikon_hivatkozasok` (+21) és a `szotar_szakasz_cimke` (+21) bontási napló nélkül | **ELTÉRÉS (alacsony)** | | `numstat` |
| CI E19: 7 HIBA (BDB H0127/1, /3, /4 és további 4) | **ELTÉRÉS (közepes)** | `lexikon_hivatkozasok.tsv` | `futtat.py` |
| CI E16 (a PR-cím „[ELLENŐRZŐ]” előtagja), E27 (5 HIBA, tételek nem látszanak) | NEM ELLENŐRIZHETŐ | | |
| L3 nulla-diff a többi lapon | NEM ELLENŐRIZHETŐ (generátort nem futtathat) | | |
| Kritérium-átírás: a negatív kritérium tartalmilag bővült (szópár, szövetségi kizárás, „név szerint”), a DT-F123ha ezt nem nevezi meg | megjegyzés | `motivumok.tsv` | |

## Az ELTÉRÉS-ek súlyossági sorrendben

1. Négy előfordulás-sorban a szótári mezők ellentmondanak egymásnak, a nyílt magban is (1Móz 3:23, 4:14, 6:12, 8:21).
2. A Ján 7:49 elutasítási indoka a TR-mérce szerint hamis.
3. CI E19: hét BDB-hivatkozásnak nincs fordítása.
4. A Jel 22:3 a nem-TR alakot nevezi, „eltérés nincs”.
5. Hat renderelt indoklásban belső jel (`halo=`, `blokk=`).
6. A Remez lezárja az 1Móz 8:21 vitáját.
7. A Jer 51:25 beépítése ütközik a „katonai pusztítás” kizárással.
8. Az Ez 12:19 Kivonat-állítása túlzó.
9. Bontási napló hiányzik a két +21 soros táblához.
10. A „négy tartomány-sor” állítás hibás (11).
11. Nem szó szerinti alakok idézőjelben.
12. (E19 a CI-ből, l. 3.)

## A javítókör (F123.HAMART3.13; a menet session-je, egy kör)

| # | Tétel | Javítás |
|---|---|---|
| 1 | Szótári mezők | a 60 HAMART-001 sor `jelentes_en` / `jelentes_hu` mezője üres: a lap és a nyílt mag a szakaszcímkéből (`szotar_szakasz_cimke.tsv`) dolgozik, mint az ALVIL-001 és az ANTROP-001 új cikkén; a nyílt mag újragenerálva |
| 2 | Ján 7:49 | az indoklás: a farizeusok átkozódása; a TR-ben ἐπικατάρατος, a kritikai kiadásban ἐπάρατος; emberi átkozódás (elutasítási ok: „emberi átkozódás, nem a genezisi lánc folytatása”); a módszertan „Melyik görög szöveg” bekezdése megnevezi |
| 3 | CI E19 | **a 7-ből 6 kulcsolási hiba volt, nem fordításhiány:** a `forditasok.tsv` a háromjegyű Strongok szócikk-azonosítóját nullázás nélkül tárolja (H127, H779, H56, H423), a hivatkozás nullázva (H0127…); az E19 csak a Strongot normalizálta, a szócikk-azonosítót nem → `eszkozok/ellenorzes/szabalyok.py` E19: a szócikk-azonosító is normalizálva. A 7. valódi hiány: a Thayer G2652 (Jel 22:3) — fordítva (a Thayer-lánc, Sonnet, 2 sor; más kulccsal nem volt sora). E19 utána: 0. |
| 4 | Jel 22:3 | a sor és a módszertan: a kritikai kiadásokban κατάθεμα, a TR egyes kiadásaiban κατανάθεμα, a jelentés azonos; „eltérés nincs” helyett az alakváltozat kimondva. A `strong` mező üres marad: a tematikus sorokon nincs a kritériumhoz tartozó Strong (a szótári mezőkben a G2652 áll). |
| 5 | Belső jel | a hat indoklás „(halo=…, blokk=…): N vers, a versek listája …” mondata: „Ugyanez a vers a teljesség-mérés egy másik csoportjában is szerepel.” A `halo=` csak a lábjegyzetek forrás-nyomában maradt (mint a kiadott lapokon). |
| 6 | 8:21 vitája | a Remez Pál mondatát idézi, a 3:17 átkának folytatását a vitatott pontokra hagyja; az 1Móz 8:21 sora: „hogy Lámek vigasztalás-várását teljesíti-e, azt a lap vitatott pontként tárgyalja”; a Róm 8:20-22 sora ugyanígy |
| 7 | Jer 51:25 | az 1/a és az indoklás kimondja: nem egy hadjárat pusztítása (a katonai pusztítás kizárva), hanem egy birodalom vádja, amely az egész földet rontotta meg (a Jel 19:2 ugyanezt mondja); a `Hif'íl 1` a menet besorolása (a BDB a verset nem idézi), a menetnaplóban rögzítve |
| 8 | Ez 12:19 | a Kivonat: „a föld a lakói erőszaka miatt üresedik ki teljességéből” |
| 9 | Bontási napló | a menetnapló U3-ában: `szotar_szakasz_cimke.tsv` +21 = BDB 13 (H0127 3, H0779 1, H6975 1, H2403 1, H7843 4, H7451 1, H0423 1, H0056 1) + Thayer 8 (G5356, G1944, G2671, G1311, G5351, G2652, G1261, G2626); `lexikon_hivatkozasok.tsv` +21 ugyanezek kulcssorai |
| 10 | Tartomány-sorok | „Tizenegy sor”, felsorolva |
| 11 | Idézőjel | „kezünk terhes fáradozásában”; a „megtelt erőszakkal” idézőjel nélkül; „az Izráel vétke” |
| — | Zsolt 14:1, Zsid 6:8 (megjegyzések) | „ugyanannak az igének ugyanaz a törzse (hif'íl)”; a Zsid 6:8 átok-szava „a Genezis átok-szavának rokona” |
| — | CI E16 | a PR címe „[ELLENŐRZŐ]” előtagot kap (a PR ellenőrzőt is módosít) |
| — | E2, E4 (a saját CI-futásból) | E2: az `archivum/` alatti fájl kimarad (mint az E9-ben); E4: a teljes-scan napló az archivált motívum régi naplója is lehet (`archivum/<ID>/`). Mindkettő `eszkozok/ellenorzes/szabalyok.py`. A `test_szabalyok.py` 26 hibája a main szabályfájljával is ugyanígy jelentkezik (E27-tesztek, környezetfüggő). |

Nem javított, csak rögzített: a Nave két megjegyzése (a döntés az orkesztrátoré volt, DT-F123hb); a „Sir 3:47” kulcs és a kapu `Sir`-kezelése (külön tétel, nem a cikké); a negatív kritérium bővülése (a DT-F123ha a szövegét nem nevezi meg; a javasolt szöveg az U2-javaslat E pontjának következménye) — az orkesztrátornak jelezve.
