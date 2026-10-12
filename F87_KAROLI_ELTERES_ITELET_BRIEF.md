---
feladat: 87
cim: A #65 eltéréslistájának kézi ítélete — három eltérő sor (KIRALY-001 2Móz 19:6, TEREMT-001 2Móz 15:5, ALVIL-001 Jób 17:13) és két verskulcs-hibás sor (ALVIL-001 Jób 17:16, Préd 9:10)
kod: KAROLI_ELTERES_ITELET
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: lezarva
ag: claude/f87-karoli-elteres-itelet
ad: a #65 eltéréslistáján kézi ítéletre váró öt sor soronként eldöntve és javítva az elofordulasok.tsv-ben és a jeloltek.tsv-ben (Károli-szó, illetve Károli-verskulcs), a két 2Móz-sor szó-szintű-gépi azonosítással, az eltéréslista újragenerálva
kovetkezo: "merge a felhasználótól; nyitott: N-F87a (LD008 feloldható), N-F87b, N-F87c (NYITOTT_FELADATOK.md)"
olvas: [naplok/KAROLI_ELLENORZES_elteresek.tsv, naplok/KAROLI_ELLENORZES_zaras.md, adat/karoli_strong/, adat/karoli_variancia.tsv, adat/SEMA.md, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, eszkozok/karoli_ellenorzes.py, F65_KAROLI_ELLENORZES_BRIEF.md]
ir: [adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/karoli_variancia.tsv, naplok/KAROLI_ELLENORZES_elteresek.tsv]
fugg: [65]
lezarva_osszegzes: öt sor javítva (3 karoli_szo, 3 Károli-verskulcs; KIRALY-001 2Móz 19:6 és TEREMT-001 2Móz 15:5 szó-szintű-gépi), eltéréslista és variancia újragenerálva; zárás: naplok/KAROLI_ELTERES_ITELET_zaras.md, ellenőr: naplok/ELLENOR_KAROLI_ELTERES_ITELET.md (2. kör TISZTA)
---

# F87_KAROLI_ELTERES_ITELET_BRIEF.md — A #65 eltéréslistájának kézi ítélete

*FELADATOK #87 · Modell: opus · v1 · 2026.10.11 · forrás: a #65 (KAROLI_ELLENORZES, PR #287) eltéréslistája és zárójelentése · döntés: DT104, DT105 (a #65 illesztési és frissítési szabálya)*

## 1. Cél

A #65 a régi `tartalom-alapú` Károli–Strong párokat a #22 gépi párosítása ellen ellenőrizte. Az eltérő sorokat szándékosan nem javította (F65 2. szakasz: „a feloldás értelmező döntés, külön tétel”). Ez a feladat az a tétel: az eltéréslistán kézi ítéletre váró sorokat soronként eldönti, és a döntést a kanonikus sorokon végrehajtja.

A befogadáskori előzetes vizsgálat (2026-10-11; `Karoli_1908.tsv`, `parok_2Moz.tsv`, `parok_Job.tsv`, `parok_Pred.tsv`, `TAHOT_kivonat.tsv`) szerint **egyik eltérés sem Strong-hiba**. Kettő hiányos vagy rossz Károli-szó, három pedig régi (KJV/MT-számozású) igehely, amely nem Károli-kulcs:

| # | Motívum | Régi igehely | Strong | Régi `karoli_szo` | Károli-szöveg (a lényeges rész) | Gépi pár | Diagnózis | Javaslat |
|---|---|---|---|---|---|---|---|---|
| 1 | KIRALY-001 | 2Móz 19:6 | H3548+H4467 | `papok` | „papok birodalma” | papok = H3548, birodalma = H4467 (`magas`) | a `karoli_szo` csak a lánc első tagját fedi | `karoli_szo` → `papok birodalma` |
| 2 | TEREMT-001 | 2Móz 15:5 | H8415 | `a mélységbe` | „Elborították őket a hullámok … merültek a mélységbe” | hullámok = H8415; mélységbe = H4688 + H9003 (`magas`) | a `karoli_szo` másik héber szóé (מְצוֹלֹת); a תְּהֹמֹת-ot Károli itt „hullámok”-nak fordítja | `karoli_szo` → `a hullámok` |
| 3 | ALVIL-001 | Jób 17:13 | H7585 | `A sírnak` | Jób 17:12: „a sír már az én házam” (a 17:13 „sírnak”-ja H7845) | Jób 17:12 sír = H7585 (`alacsony`) | verseltolás; a `kapcsolodas` idézete („a Seól az én házam”) a 17:12 | `igehely` → `Jób 17:12`, `karoli_szo` → `a sír` |
| 4 | ALVIL-001 | Jób 17:16 | H7585 | `a sír üregébe` | Jób 17:15: „Leszáll az majd a sír üregébe” | Jób 17:15 sír = H7585 (`alacsony`) | verseltolás (`nincs_par`) | `igehely` → `Jób 17:15` |
| 5 | ALVIL-001 | Préd 9:10 | H7585 | `a Seolban` | Préd 9:12: „… nincs a Seolban, a hová menendő vagy” | Préd 9:12 Seolban = H7585 (`alacsony`) | verseltolás (`nincs_par`) | `igehely` → `Préd 9:12` |

Az új kulcsokon (Jób 17:12, Jób 17:15, Préd 9:12) ma nincs ALVIL-001 sor, és a `TAHOT_kivonat.tsv` mindhármon H7585-öt ad. **A táblázat javaslat, nem döntés:** az M0 saját lekérdezéssel újra levezeti, és a felhasználó soronként fogadja el.

A 4. és az 5. sor az eltéréslistán `nincs_par` ítéletű, de a zárójelentés (`naplok/KAROLI_ELLENORZES_zaras.md`, „Versszám-javítás”) ugyanabba a hibaosztályba sorolja, mint a 3. sort. Ezért kerül ebbe a feladatba.

## 2. Hatókör

**Benne van:**
- a fenti öt sor kézi ítélete és javítása az `elofordulasok.tsv`-ben és a `jeloltek.tsv`-ben, a két táblában egyezően;
- az átkulcsolt sorok `igazolas` mezőjének újraellenőrzése a `TAHOT_kivonat.tsv` ellen, az új kulcson (az F85 óta a TAHOT kulcsa a Károli-vers);
- a #65 eszközének újrafuttatása (`eszkozok/karoli_ellenorzes.py`): az 1. és a 2. sor a javítás után várhatóan `egyezik` és `magas`, így a DT104/DT105 szabálya szerint `szó-szintű-gépi` lesz; a 3–5. sor `alacsony` páron áll (Jób, Préd: csak Sonnet), ezért `tartalom-alapú` marad (DT-M2);
- az eltéréslista (`naplok/KAROLI_ELLENORZES_elteresek.tsv`) és az `adat/karoli_variancia.tsv` `megerosites`-sorainak újragenerálása.

**Nincs benne:**
- tanulmány, motívumfájl és motívumnapló javítása: `tematikus_lezart/Hadesz_Seol_tematikus.md`, `Tehom_tematikus.md`, `Melkizedek_tematikus.md` és a kereszthivatkozás-naplók, `motivumok/KIRALY-001.md`, `motivumok/TEREMT-001.md`, `motivumlog/PaRDeS_motivumok.md`. Ezek a régi igehelyeket és szóalakokat használják; a feladat csak listázza őket (forrás-réteg, kézi);
- a `lexikon/` (generált nézet, DT28): az ALVIL-001, a KIRALY-001 és a TEREMT-001 lexikonoldala a régi kulcsokat mutatja, amíg újra nem generálódik;
- más adattáblák régi kulcsai (`adat/lxx_dontesek.tsv` Préd 9:10, `adat/forditasok.tsv`): csak jelentés, nyitott tételként (`N-F87a`);
- a `kapcsolodas` mező szövege (a KIRALY-001 idézete „papok királysága”, nem Károli-szöveg): értelmező próza, nem változik;
- a #22 párosításának javítása, `alacsony` párból `szó-szintű-gépi`, a `Karoli_Strong_kivonat.tsv` (N-F65a), a #22 régi aranymintája (`f21p/regi_arany_hibas.tsv`);
- a #65 eltéréslistájának többi sora (46 további `nincs_par`): csak a fenti öt.

## 3. Lépések

### M0 — Levezetés és ⛔

Jelentés: `naplok/KAROLI_ELTERES_ITELET_M0.md`, a proveniencia-sorral.
1. Soronként saját lekérdezéssel: a Károli-vers (`Karoli_1908.tsv`), a gépi párok (`parok_<könyv>.tsv`, `bizonyossag`-gal) és a TAHOT-sor (`TAHOT_kivonat.tsv`) a régi és az új kulcson. A fenti táblázat diagnózisát megerősíti vagy cáfolja; ha cáfolja, az eltérés a jelentésbe kerül, javaslat nélkül.
2. Az új kulcson nincs-e már ugyanolyan `id` + `igehely` sor (ütközés), és melyik `adat/*.tsv` hivatkozik a régi kulcsra (sor + fájl).
3. Soronként a javasolt változás mezőnként (`igehely`, `karoli_szo`, `igazolas`), a többi mező változatlan.
4. A javítás rögzítésének módja (`DT-F87a`). Javaslat: a `proveniencia` és a `megbizhatosag` nem változik; a javítás ténye, oka és a forráslekérdezés a feladat naplójába (`naplok/KAROLI_ELTERES_ITELET_zaras.md`) kerül soronként, a `jeloltek.tsv` sorában pedig a `dontes`/`indoklas` mező [javaslat] egy rövid hivatkozást kap a naplóra. Alternatíva: a hivatkozás csak a naplóban áll.

**⛔ Megállás:** a felhasználó soronként elfogadja, módosítja vagy elveti a javítást, és dönt a `DT-F87a`-ról.

### M1 — Javítás

- Csak az M0-ban elfogadott sorok és mezők. Írás előtt soronkénti összevetés az eredetivel, és megállás, ha más is változna (minta: `eszkozok/igazolas_migracio.py`). TSV-írás `'\t'.join()`, a `csv` modul tilos (CLAUDE.md).
- Az `elofordulasok.tsv` és a `jeloltek.tsv` ugyanazon sora egy commitban.
- Commit: `F87.<n>: …`.

### M2 — Újraellenőrzés

- `karoli_ellenorzes.py --ellenorzes`, majd `--frissit` szárazon, utána `--frissit --ir`: csak a `magas` + `egyezik` sorok váltanak `szó-szintű-gépi`-re. A második futás 0 sort ír.
- Az eltéréslista és a `karoli_variancia.tsv` újragenerálva. Az öt sor várható új ítélete: 1–2. `egyezik` (`magas`), 3–5. `egyezik` (`alacsony`). Ha más jön ki, megállás és jelentés.

### M3 — Zárás

`naplok/KAROLI_ELTERES_ITELET_zaras.md` (≤20 sor: soronként régi → új érték és a forráslekérdezés; a tanulmányok, a motívumfájlok és a lexikon régi hivatkozásainak listája; a nyitott tételek), `fuggetlen-ellenor` (`naplok/ELLENOR_KAROLI_ELTERES_ITELET.md`, mind az öt soron), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Mind az öt sor ítélete a naplóban, saját lekérdezéssel levezetve; elvetett javaslatnál a sor változatlan, az ok rögzítve.
- **K2.** Csak az M0-ban elfogadott mezők változtak; az `elofordulasok.tsv` és a `jeloltek.tsv` megfelelő sora egyezik.
- **K3.** `szó-szintű-gépi` csak `magas` + `egyezik` soron áll (DT-M2, DT104, DT105); a Jób és a Préd sorai `tartalom-alapú`-k maradnak.
- **K4.** Tanulmány-, motívum- és lexikonfájl változatlan; a régi hivatkozásaik listája a zárójelentésben; az `ellenoriz.py` és a CI zöld.
- **K5.** A független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-11 | A feladat a #65 három `elter` sora mellett a két verskulcs-hibás `nincs_par` sort is tartalmazza (azonos hibaosztály). | befogadás, `naplok/KAROLI_ELLENORZES_zaras.md` |
| v1 | 2026-10-11 | A befogadáskori előzetes vizsgálat szerint egyik eltérés sem Strong-hiba; a javaslat csak `karoli_szo` és `igehely` változást tartalmaz. | befogadás, előzetes lekérdezés (Károli 1908, `parok_*`, TAHOT) |
| v1 | 2026-10-12 | DT-F87b: mind az öt sor javítása elfogadva az M0 szerint; a 4. sor `karoli_szo`-ja marad (`a sír üregébe`); az 1. sor `igazolas`-a marad (N-F87b). | felhasználó (chat), `naplok/KAROLI_ELTERES_ITELET_M0.md` |
| v1 | 2026-10-12 | DT-F87a: a javítás ténye a `naplok/KAROLI_ELTERES_ITELET_zaras.md`-ben, a `jeloltek.tsv` `indoklas` végén rövid hivatkozással; `proveniencia`, `megbizhatosag`, `datum` változatlan (a `dontes` zárt mező, SEMA 2.4). | felhasználó (chat), `naplok/KAROLI_ELTERES_ITELET_M0.md` 4. pont |
| v1 | 2026-10-12 | Az `adat/karoli_variancia.tsv` teljes újragenerálással, egyetlen ts-sel (az ellenőr 1. eltérése: a két beszúrt sor vegyes ts-t adott); a ts-en kívül a tábla az előző változattal azonos. | `naplok/ELLENOR_KAROLI_ELTERES_ITELET.md` |

Nyitott tétel: **N-F87a** — a régi KJV/MT-kulcsú igehelyek más adattáblákban (`lxx_dontesek.tsv` Préd 9:10, `forditasok.tsv`); a feladat csak listázza őket.
