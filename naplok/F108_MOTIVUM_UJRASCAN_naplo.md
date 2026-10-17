# F108 napló — a motívumsorok újraellenőrzése az F84/F85 utáni TAHOT-on

*Futtatta: claude-sonnet-5-5 · 2026.10.17 · ág: `claude/f108-motivum-ujrascan` · a lekérdezések proveniencia-sorai: `naplok/F108_lekerdezesek.tsv` · részletes sorok: `naplok/F108_ujrascan_elteresek.tsv` (kulcs-összevetés: `tabla` = `elofordulasok` / `jeloltek:<dontes>`; újrascan-találatok: `tabla` = `ujrascan`).*

## 1. Gerinc-Strongok (1. lépés)

Forrás: az `elofordulasok.tsv` `gerinc_elem`/`strong` mezője; HAMART-001-nél kiegészítve a `motivumlog/PaRDeS_motivumok.md` 468. sorának gerincével (G2704) és a `jeloltek.tsv` `forras_kereses` mezőinek scan-jaival. A `manual` proveniencia: a lista kézi összeállítás, nem lekérdezés.

| Motívum | scan / kollokáció | Megjegyzés |
|---|---|---|
| KIRALY-001 | scan H3548; scan H8004; scan G5010 | |
| ISTENTISZT-001 | kollokacio H7121+H8034; scan G1941 | |
| TEREMT-001 | scan H8415; scan G0012 | |
| ALVIL-001 | scan H7585; scan G0086 | |
| MENNY-001 | kollokacio H1121+H0430; scan H5303 | |
| ANTROP-001 | kollokacio G4151+G5590; kollokacio H5315+H2416 | |
| HODIT-001 | scan H7497; scan H7496; scan H5303 | |
| HAMART-001 | scan H0127; scan H0779; scan H2403; scan H2555; scan H6093; scan H7843; scan H7043; scan H7451; scan G1311; scan G1944; scan G2671; scan G5351; scan G5356; scan G2704 | |
| TEREMT-002 | kollokacio H8414+H0922 | |

Nem futott külön scan: a H7121+H8034 (ISTENTISZT-001), G4151+G5590 és H5315+H2416 (ANTROP-001), H1121+H0430 (MENNY-001), H8414+H0922 (TEREMT-002) összetett gerinc, ezeknél a `kollokacio` parancs fut (egy versben). Az összetett gerinc egyes tagjára külön scan nem készült (H7121, H8034, H1121 stb. önmagukban a motívumot nem azonosítják).

## 2. Kulcs-összevetés (2. lépés) — mért számok

Módszer: a sor `strong`-ja (összetettnél minden tag) a mai `TAHOT_kivonat.tsv` (H) / `TAGNT_kivonat.tsv` (G) ugyanazon igehelyén (tartománynál a tartomány bármely versén) áll-e; ha nem, a ±1–2. vers és a fejezethatár vizsgálata. A `jeloltek.tsv` sorainak nincs `strong` mezője: itt a `forras_kereses`-ben említett Strong(ok) szolgálnak (ha nincs, `nincs_strong` — TSK/frázis/kézi találat). A `zsoltar_55` osztály minden Zsolt-sort felvesz (csak osztályozás, a #55-re utalva; a „mért osztály” a megjegyzésben). **E** = `elofordulasok.tsv`, **J** = `jeloltek.tsv`.

| Motívum | tábla | összes | rendben | kulcs_eltolodott | hianyzik | osszetett_resz | zsoltar_55 | nincs_strong |
|---|---|---|---|---|---|---|---|---|
| KIRALY-001 | E | 9 | 6 | 0 | 0 | 1 | 2 | 0 |
| KIRALY-001 | J | 23 | 6 | 0 | 0 | 0 | 2 | 15 |
| ISTENTISZT-001 | E | 32 | 27 | 0 | 0 | 0 | 5 | 0 |
| ISTENTISZT-001 | J | 92 | 1 | 0 | 0 | 0 | 21 | 70 |
| TEREMT-001 | E | 41 | 30 | 0 | 0 | 0 | 11 | 0 |
| TEREMT-001 | J | 43 | 0 | 0 | 0 | 0 | 11 | 32 |
| ALVIL-001 | E | 72 | 57 | 0 | 0 | 0 | 15 | 0 |
| ALVIL-001 | J | 74 | 0 | 0 | 0 | 0 | 15 | 59 |
| MENNY-001 | E | 9 | 6 | 0 | 0 | 0 | 0 | 3 |
| MENNY-001 | J | 12 | 0 | 0 | 0 | 0 | 0 | 12 |
| ANTROP-001 | E | 8 | 4 | 0 | 1 | 3 | 0 | 0 |
| ANTROP-001 | J | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| HODIT-001 | E | 33 | 32 | 0 | 0 | 0 | 1 | 0 |
| HODIT-001 | J | 51 | 0 | 0 | 0 | 0 | 5 | 46 |
| HAMART-001 | E | 52 | 44 | 0 | 0 | 0 | 3 | 5 |
| HAMART-001 | J | 222 | 70 | 0 | 0 | 0 | 17 | 135 |
| TEREMT-002 | E | 3 | 3 | 0 | 0 | 0 | 0 | 0 |
| TEREMT-002 | J | 66 | 18 | 0 | 0 | 0 | 4 | 44 |
| **ÖSSZESEN** | E | 259 | 209 | 0 | 1 | 4 | 37 | 8 |
| **ÖSSZESEN** | J | 592 | 95 | 0 | 0 | 0 | 75 | 422 |

Egyéb osztály: nincs.

**Eredmény:** az `elofordulasok.tsv` 259 sorából **egyetlen sem `kulcs_eltolodott`, és egyetlen ÓSZ-sor sem `hianyzik`** (egy ÚSZ-sor `hianyzik`: ANTROP-001 `1Kor 2:15`; javítva F108.7, `naplok/ELLENOR_F108.md` 1.) (az F85.6-os átkulcsolás és az F87.3 utáni állapotban az ÓSZ-sorok Strongjai a mai TAHOT-on a helyükön állnak). Az eltérések mind ÚSZ-oldaliak és tartalmi természetűek (nem kulcshibák):

- KIRALY-001 `Zsid 7:1-28` (G5010+G0813+G0282): **osszetett_resz** — jelen: G5010+G0282
- ANTROP-001 `Luk 1:46` (G4151+G5590): **osszetett_resz** — jelen: G5590
- ANTROP-001 `Luk 1:47` (G4151+G5590): **osszetett_resz** — jelen: G4151
- ANTROP-001 `1Kor 2:14` (G4151+G5590): **osszetett_resz** — jelen: G4151
- ANTROP-001 `1Kor 2:15` (G4151+G5590): **hianyzik** — jelen: G4152 (melléknév)

(Az ANTROP-001 `1Kor 2:15`-ön a G4151 és a G5590 nem áll, csak a G4152 πνευματικός; a G5590 az 1Kor 2-ben sehol nincs (a 2:14-en a G5591 ψυχικός és a G4151, a 2:13-on a G4151 és a G4152). Ez nem F85-típusú kulcsolás-hiba — a TAGNT-kulcs szerves ÚSZ-kulcs —, hanem a sor szótári alakjának kérdése: a melléknévi G4152/G5591 helyén a főnévi G4151/G5590 áll. Az eredeti `kulcs_eltolodott` osztály tévesen azt állította, hogy a Strongok a 2:14-en/2:13-on állnak; F108.7 javította, `naplok/ELLENOR_F108.md` 1. A KIRALY-001 `Zsid 7:1-28` összetett Strongjából a G0813 hiányzik a tartományon. Mindkettő a motívum saját menetében bírálandó el, nem kulcsjavítás.)

A `nincs_strong` E-sorok (8): HAMART-001 5 (tematikus: hivatkozás), MENNY-001 3 (Júd 1:6, 1:14-15, 2Pét 2:4-5: apokrif/formula-hivatkozás). Nincs Strongjuk, így a kulcs nem ellenőrizhető; nem hiba.

**Korlát (J-sorok):** a `jeloltek.tsv` 592 sorából 422-nél nincs a `forras_kereses`-ben Strong (TSK/frázis/kézi forrás), ezeknél a Strong-alapú kulcs-ellenőrzés nem végezhető (`nincs_strong`); a 95 `rendben` és 75 `zsoltar_55` sor ellenőrizhető. Egyetlen ellenőrizhető J-sor sem `kulcs_eltolodott`/`hianyzik`.

## 3. Újrascan (3. lépés)

A lekérdezések proveniencia-sorai: `naplok/F108_lekerdezesek.tsv`. „Új” = a találat igehelye sem az `elofordulasok.tsv`-ben, sem a `jeloltek.tsv`-ben (azonos motívum-ID alatt, tartományokat versre bontva) nem szerepel.

| Motívum | parancs | találat | már E-ben | csak J-ben | **új** |
|---|---|---|---|---|---|
| KIRALY-001 | scan H3548 | 653 | 4 | 6 | 643 |
| KIRALY-001 | scan H8004 | 2 | 2 | 0 | 0 |
| KIRALY-001 | scan G5010 | 9 | 6 | 3 | 0 |
| ISTENTISZT-001 | kollokacio H7121+H8034 | 196 | 22 | 2 | 172 |
| ISTENTISZT-001 | scan G1941 | 31 | 10 | 0 | 21 |
| TEREMT-001 | scan H8415 | 35 | 34 | 0 | 1 |
| TEREMT-001 | scan G0012 | 9 | 9 | 0 | 0 |
| ALVIL-001 | scan H7585 | 64 | 64 | 0 | 0 |
| ALVIL-001 | scan G0086 | 10 | 9 | 1 | 0 |
| MENNY-001 | kollokacio H1121+H0430 | 279 | 5 | 0 | 274 |
| MENNY-001 | scan H5303 | 2 | 2 | 0 | 0 |
| ANTROP-001 | kollokacio G4151+G5590 | 6 | 3 | 1 | 2 |
| ANTROP-001 | kollokacio H5315+H2416 | 61 | 1 | 0 | 60 |
| HODIT-001 | scan H7497 | 24 | 24 | 0 | 0 |
| HODIT-001 | scan H7496 | 8 | 8 | 0 | 0 |
| HODIT-001 | scan H5303 | 2 | 1 | 1 | 0 |
| TEREMT-002 | kollokacio H8414+H0922 | 3 | 3 | 0 | 0 |
| HAMART-001 | scan H0127 | 211 | 14 | 11 | 186 |
| HAMART-001 | scan H0779 | 52 | 23 | 29 | 0 |
| HAMART-001 | scan H2403 | 271 | 1 | 1 | 269 |
| HAMART-001 | scan H2555 | 59 | 15 | 3 | 41 |
| HAMART-001 | scan H6093 | 3 | 3 | 0 | 0 |
| HAMART-001 | scan H7843 | 135 | 8 | 10 | 117 |
| HAMART-001 | scan H7043 | 79 | 3 | 3 | 73 |
| HAMART-001 | scan H7451 | 621 | 4 | 8 | 609 |
| HAMART-001 | scan G1311 | 5 | 1 | 4 | 0 |
| HAMART-001 | scan G1944 | 2 | 2 | 0 | 0 |
| HAMART-001 | scan G2671 | 5 | 3 | 2 | 0 |
| HAMART-001 | scan G5351 | 8 | 1 | 7 | 0 |
| HAMART-001 | scan G5356 | 8 | 1 | 7 | 0 |
| HAMART-001 | scan G2704 | 1 | 0 | 0 | 1 |

**Írási szabály (az én operatív döntésem, a DT-F108a-ban visszakérdezve):** csak a szűk, ≤25 új találatú scan-ek új helyei kerültek a `jeloltek.tsv`-be (`nyitva`); a tág gerinc-Strongoknál (H3548 643, H7451 609, H2403 269, H0127 186, H1121+H0430 274, H7121+H8034 172, H7843 117, H7043 73, H5315+H2416 60, H2555 41) az új helyek **nem** íródtak a `jeloltek.tsv`-be (az ISTENTISZT/HAMART korábbi menetek a hits-ből szűk, naplózatlan szűrővel válogattak), hanem a `F108_ujrascan_elteresek.tsv`-ben `uj_talalat_nem_irva_tul_tag` osztállyal állnak. A Zsolt-találatok (126) sehol nem íródtak, `zsoltar_55_uj_talalat_nem_irva` osztállyal a #55-re utalva.

**Új sorok a `jeloltek.tsv`-ben (25, mind `nyitva`):** TEREMT-001 `Jób 41:32` (H8415 — a brief 4. pontjának ismert esete: **megtalálva, `nyitva`**); ISTENTISZT-001 21 hely (G1941 ἐπικαλέω); ANTROP-001 `1Pét 1:22`, `Mt 12:18` (G4151+G5590 kollokáció); HAMART-001 `2Tim 3:8` (G2704 kataftheiró).

**Üres/zéró eredmények (explicit):** ALVIL-001 (H7585, G0086), HODIT-001 (H7497, H7496, H5303), MENNY-001 (H5303), TEREMT-002 (H8414+H0922 kollokáció), KIRALY-001 (H8004, G5010), HAMART-001 (H0779, H6093, G1311, G1944, G2671, G5351, G5356): **0 új hely**, vagyis a régi scan ezeken teljes volt. Az F84 (Jób 41) hatása az egyetlen H8415-ön látszik (Jób 41:32); a HAMART/ALVIL/HODIT scanekben nem járt új Jób-hellyel az adott Strongokon.

## 4. Ellenőrzések

- `elofordulasok.tsv`: **nem módosult** (git diff üres rá).
- `jeloltek.tsv`: csak 25 új sor, a meglévő sorok bájtra változatlanok (a szkript `startswith(eredeti)` és sor-egyenlőség ellenőrzéssel írt).
- `eszkozok/`: nem változott; a szkriptek a scratchpadben maradtak.
- A bible-mcp-t nem használtam (DT32).

## 5. Nyitott: DT-F108a (a `DONTESEK.md`-ben)

A kérdés a `DONTESEK.md` `DT-F108a` tételében áll: (1) a tág gerinc-Strongoknál (kb. 2 400 új találat) kerüljenek-e a helyek a `jeloltek.tsv`-be, vagy marad a mostani szűk szabály; (2) a 25 új `nyitva` jelölt elbírálása (a motívumok saját menetében vagy közös tételben); (3) `kulcs_eltolodott` ÓSZ-sor nincs, tehát kulcsjavító tétel nem kell — csak az ANTROP-001 `1Kor 2:15` tartalmi kérdése marad.
