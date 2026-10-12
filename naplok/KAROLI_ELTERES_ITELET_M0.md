# F87 M0 — a #65 eltéréslistájának öt sora: újralevezetés és javaslat

*FELADATOK #87 · `F87_KAROLI_ELTERES_ITELET_BRIEF.md` M0 · 2026-10-12 · az adatsorok NEM változtak (⛔ előtt)*

proveniencia: scope=F87 M0, öt sor (KIRALY-001 2Móz 19:6; TEREMT-001 2Móz 15:5; ALVIL-001 Jób 17:13, Jób 17:16, Préd 9:10) | forras=konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, adat/karoli_strong/parok_{2Moz,Job,Pred}.tsv, adat/karoli_strong/szavak_{2Moz,Job,Pred}.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/*.tsv (ütközés, régi kulcs), naplok/KAROLI_ELLENORZES_elteresek.tsv, eszkozok/karoli_ellenorzes.py (`ellenoriz_sor`, írás nélkül) | ts=2026-10-12T06:42:35Z

A lekérdezés: a Károli-vers a régi kulcson és ±3 versen; a TAHOT-sorok a sor Strongjára (és a versben álló másik, versengő Strongra) szűrve; a `parok_<könyv>.tsv` sorai a releváns verseken (`bizonyossag`-gal) és a `szavak_<könyv>.tsv` nem párosított `hu` szavai; a két tábla sorai mezőnként; az új kulcs bármely `adat/*.tsv` mezőben (ütközés); a régi kulcs pontos mezőként és részsztringként minden `adat/*.tsv`-ben. A javasolt értékek ítéletét a #65 eszközének saját `ellenoriz_sor` függvénye adta, írás nélkül. A gépi párok modell-kimenetek (2Móz: Sonnet+C, `magas`; Jób, Préd: csak Sonnet, `alacsony`), javaslat, nem lekérdezés-eredmény (a `parok_*.tsv` proveniencia-sora).

## 1. Soronkénti levezetés (M0.1)

| # | Sor (`elofordulasok` / `jeloltek`) | Károli 1908 | TAHOT (Károli-kulcs) | Gépi pár | Ítélet ma → a javaslattal | A brief diagnózisa |
|---|---|---|---|---|---|---|
| 1 | KIRALY-001 2Móz 19:6 (5. / 21. sor), `strong` H3548+H4467, `karoli_szo` `papok` | „És lesztek ti nékem papok birodalma és szent nép…” | 19:6: H4467 מַמְלֶכֶת, H3548 כֹּהֲנִים | papok = H3548, birodalma = H4467 (mindkettő `magas`, S+C) | `elter` (hiányzik H4467) → `egyezik`, `magas`, nem részleges, frissíthető | **megerősítve** |
| 2 | TEREMT-001 2Móz 15:5 (45. / 61. sor), H8415, `a mélységbe` | „Elborították őket a hullámok, kő módjára merültek a mélységbe.” | 15:5: H8415 תְּהֹמֹת, H4688 מְצוֹלֹת | hullámok = H8415; mélységbe = H9003 + H4688 (mind `magas`, S+C) | `elter` (gépi H4688,H9003) → `egyezik`, `magas`, frissíthető | **megerősítve** |
| 3 | ALVIL-001 Jób 17:13 (97. / 113. sor), H7585, `A sírnak` | 17:12: „Ha reménykedem is, a sír már az én házam…”; 17:13: „A sírnak mondom: Te vagy az én atyám…” | 17:12: H7585 שְׁאוֹל; 17:13: H7845 שַׁחַת (H7585 nincs) | 17:12 sír = H7585 (`alacsony`); 17:13 sírnak = H7845 (`alacsony`) | `elter` (gépi H7845,H9005) → Jób 17:12-n `egyezik`, `alacsony` | **megerősítve**; a `kapcsolodas` („a Seól az én házam”) a 17:12 szövege |
| 4 | ALVIL-001 Jób 17:16 (98. / 114. sor), H7585, `a sír üregébe` | 17:16: **nincs Károli-vers** (a Károli Jób 17 a 15. versig tart); 17:15: „Leszáll az majd a sír üregébe…” | 17:15: H7585 שְׁאֹל | 17:15 sír = H7585, üregébe = H0905 בַּדֵּי (`alacsony`) | `nincs_par` („a vers/könyv nincs a gépi párosításban”) → Jób 17:15-n `egyezik`, `alacsony`, **részleges** (`mas_strong`: üregébe:H0905) | **megerősítve**; kiegészítés: a régi kulcs nem létező Károli-vers |
| 5 | ALVIL-001 Préd 9:10 (125. / 141. sor), H7585, `a Seolban` | 9:10: „A te ruháid mindenkor legyenek fejérek…”; 9:12: „… nincs a Seolban, a hová menendő vagy.” | 9:10: H7585 nincs; 9:12: H7585 שְׁאוֹל | 9:12 Seolban = H7585 (`alacsony`) | `nincs_par` („a karoli_szo egyetlen szava sincs a versben”) → Préd 9:12-n `egyezik`, `alacsony` | **megerősítve** |

Cáfolt diagnózis nincs. Eltérés a brief táblázatától csak kiegészítésként: (a) a 4. sor régi kulcsa (Jób 17:16) nem létezik a Károliban; (b) a 4. sor a javasolt kulccsal **részleges** egyezés (az „üregébe” gépi párja H0905), az ítélet ettől `egyezik` marad (DT-F65a (1)); (c) az 5. sor `nincs_par`-ja a szóhiányból ered (a vers létezik), nem a vers hiányából.

## 2. Ütközés és régi-kulcs hivatkozások (M0.2)

- **Ütközés:** a Jób 17:12, Jób 17:15, Préd 9:12 kulcs egyetlen `adat/*.tsv` mezőjében sem áll (egyik `id`-vel sem). Nincs ütközés.
- **A régi kulcsra hivatkozó adatsorok** (pontos mező-egyezés): a két tábla öt-öt sora (fent); `kapcsolatok.tsv` 3. és 7. sor (KIRALY-001, 2Móz 19:6 — a kulcs nem változik); `lxx_dontesek.tsv` 82. sor LD080 (2Móz 19:6) és 89. sor LD087 (2Móz 15:5) — a kulcs nem változik; **`lxx_dontesek.tsv` 10. sor LD008 (Préd 9:10)**, `bizonyossag` = `nyitott`, megjegyzése szerint „az előfordulás-sor igehelyének javításáig nyitott (DT23)” — ez a javítás után feloldható, de a brief szerint nincs benne (N-F87a). Jób 17:13/17:16 pontos mezőként máshol nem áll.
- **Részsztringként** (nem kulcs, a BDB-szócikk szövegében, MT-számozással): `forditasok.tsv` 80. (H7585), 112. (H1004), 316. (H905), 193. (H4672) sor. Szabad szöveg, nem változik (N-F87a: csak lista).

## 3. Javasolt változás mezőnként (M0.3, soronkénti elfogadás: DT107)

Minden más mező változatlan (`kapcsolodas`/`indoklas` szövege, `strong`, `gerinc_elem`, `azonositas_modja`, `megbizhatosag`, `proveniencia`, `datum`). Az `azonositas_modja`-t nem az M1, hanem az M2 `--frissit --ir` állítja (csak az 1–2. sor).

| # | `igehely` (mindkét tábla) | `karoli_szo` (mindkét tábla) | `igazolas` (`elofordulasok`) |
|---|---|---|---|
| 1 | marad (2Móz 19:6) | `papok` → `papok birodalma` | marad `nincs` (l. megjegyzés) |
| 2 | marad (2Móz 15:5) | `a mélységbe` → `a hullámok` | marad `TAHOT-igazolt` (15:5-ön H8415 áll) |
| 3 | Jób 17:13 → **Jób 17:12** | `A sírnak` → `a sír` | marad `TAHOT-igazolt` — **az új kulcson igazolt** (17:12: H7585); a régi kulcson ma nem volt az |
| 4 | Jób 17:16 → **Jób 17:15** | marad `a sír üregébe` | marad `TAHOT-igazolt` — az új kulcson igazolt (17:15: H7585) |
| 5 | Préd 9:10 → **Préd 9:12** | marad `a Seolban` | marad `TAHOT-igazolt` — az új kulcson igazolt (9:12: H7585) |

Megjegyzések, döntésre bocsátva (nem javaslat):
- **1. sor `igazolas`:** a TAHOT a 2Móz 19:6-on mindkét Strongot (H3548, H4467) hordozza, a mező mégis `nincs`. A brief hatóköre az `igazolas`-t csak az átkulcsolt sorokon ellenőrizteti; a `TAHOT-igazolt`-ra állítás külön döntés.
- **4. sor `karoli_szo`:** a `a sír üregébe` részleges egyezést ad (üregébe = H0905). Alternatíva: `a sír` (teljes egyezés). A brief javaslata szerint marad; a részlegesség az eltéréslistán `reszleges = igen`-ként jelenik meg.
- A 3–5. sor a javítás után is `tartalom-alapú` marad (`alacsony` pár, DT-M2); a lexikon- és a tanulmányfájlok a régi kulcsot mutatják (hatókörön kívül, M3-lista).

## 4. A javítás rögzítésének módja (M0.4, DT108)

A `jeloltek.tsv` `dontes` mezője zárt értékkészletű (`beépítve` | `elutasítva` | `nyitva`, SEMA 2.4), ezért a brief „`dontes`/`indoklas`” javaslatából csak az `indoklas` jöhet szóba. Az `indoklas` megjelenik a generált nézetekben (`eszkozok/lexikon_general.py`, `eszkozok/general.py`).

1. **(javaslat)** `proveniencia`, `megbizhatosag`, `datum` nem változik; a javítás ténye, oka és forráslekérdezése soronként a `naplok/KAROLI_ELTERES_ITELET_zaras.md`-be kerül; a `jeloltek.tsv` `indoklas` mezője a végén rövid hivatkozást kap: ` [F87: igehely/karoli_szo javítva, l. naplok/KAROLI_ELTERES_ITELET_zaras.md]`.
2. A hivatkozás csak a naplóban áll; a `jeloltek.tsv` `indoklas` mezője változatlan.
3. A hivatkozás a `forras_kereses` mezőbe kerül (a keresés forrását írja le), az `indoklas` változatlan.
