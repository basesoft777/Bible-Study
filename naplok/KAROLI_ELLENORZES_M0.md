# KAROLI_ELLENORZES M0 — felmérés (F65.1)

*2026-10-11 · mérőeszköz: `eszkozok/karoli_ellenorzes.py --meres` · proveniencia: scope=manual | forras=adat/karoli_strong/parok_*.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv | ts=manual (nem lekérdezés)*

## 1. A `parok_<könyv>.tsv` szerkezete és a `bizonyossag` újramérése

Fejléc: `vers  hu_sorszam  hu_szo  er_sorszam  er_szo  strong  bizonyossag  forras`. Az első sor `# proveniencia: …`. A `vers` Károli-kulcs, `1Móz 1:1` alakú (a magyar rövidítés megegyezik az `igehely`-ével, normalizálás nem kell). A `hu_szo` egyetlen szóalak (írásjel nélkül, a Károli-szöveg betűivel); többszavas kifejezés nincs, egy héber szó több magyar sorban, egy magyar szó több Strongon is állhat (pl. `színén` = H5921 + H6440). A `strong` egyetlen, négyjegyű (`H0776`), nincs `+` lánc; a `+` a `szavak_<könyv>.tsv`-ben van (`H9003+H7225`).

**Újramérés (a brief 2026-10-05-i táblája elavult a `magas` oszlopban nem, a könyvek számában igen):** 27 könyv kész, de a `magas` bizonyosság továbbra is **csak az 1Móz (29 579 magas / 2 034 alacsony) és a 2Móz (23 265 / 1 222)**. A többi 25 könyv (3Móz, 4Móz, 5Móz, Józs, Bír, Ruth, 1–2Sám, 1–2Kir, 1–2Krón, Ezsd, Neh, Eszt, Jób, Zsolt, Péld, Préd, Ézs, Jer, Ez, Dán, Jón, Náh) **mind `alacsony`** (csak Sonnet, DT-F22c).

## 2. A régi sorok

| tábla | `tartalom-alapú` sor | ebből 1Móz | 2Móz |
|---|---|---|---|
| `adat/jeloltek.tsv` | 221 (8 motívum) | 20 | 5 |
| `adat/elofordulasok.tsv` | 205 | 20 | 5 |
| `konkordancia/Karoli_Strong_kivonat.tsv` | 383 | 194 (Gen) | 6 (Exo) |

A `jeloltek.tsv`-nek **nincs `strong` oszlopa**: a 221 sorból 205 az `elofordulasok.tsv` (id + igehely) sorához kapcsolható, ott van a Strong. A maradék 16 sor mind TEREMT-002, az `elofordulasok.tsv`-ben nincs párja → ezekre Strong híján ellenőrzés nem futtatható (`nincs_strong`).

## 3. Az illesztés szabálya (az eszköz ezt valósítja meg)

1. Az `igehely` versekre bontva (`1Móz 14:18-20` → 18, 19, 20; fejezethatárt átlépő tartomány: nincs bontva, `nincs_par`).
2. A `karoli_szo` szavakra bontva (kisbetűsítve, írásjel nélkül); azok a `parok` sorok „találtak”, amelyek `hu_szo`-ja ezek egyike a megfelelő versekben.
3. A sor Strongjai (`H7121+H8034` → külön-külön, négyjegyűre normálva) mind szerepeljenek a találtak Strongjai között → `egyezik`; ha a szavak megvannak, de valamelyik Strong hiányzik → `elter` (a gépi Strongok és a hiányzó listázva); ha egy szó sincs meg → `nincs_par`.
4. `magas` ítélet: az `egyezik` sor pár-bizonyossága a megfelelő (a Strongot igazoló) párokon; csak ha mind `magas`, frissíthető.

*Korlát (nyíltan):* a szó-egyezés laza (bármelyik szó elég), tehát `egyezik` azt jelenti: a sor Strongját a gépi párosítás is ugyanezen szavak valamelyikéhez rendeli ugyanazon a versen. Nem azt, hogy a teljes kifejezés minden szava ellenőrzött. A többszavas `karoli_szo` ítélete így erősebb a Strongok oldaláról (mind megvan), gyengébb a szavak oldaláról.

## 4. Mérés (`naplok/KAROLI_ELLENORZES_elteresek.tsv` előzetes, M2-ben végleges)

`elofordulasok.tsv` 205 sor: **153 egyezik · 3 elter · 49 nincs_par**.
- `nincs_par` 49: mind újszövetségi (G-Strong, a #22 csak az ÓSZ-t párosítja: 1Kor, Jel, ApCsel, Luk, Zsid, Róm, …) vagy még nem párosított ószövetségi könyv (Hab, Hós, Jóel, Ámós, Zak, Sof, Én); Jób 17:16 és Préd 9:10 (**javítva az ellenőri jelentés után**: a régi igehely nem Károli-kulcs, KJV/MT-számozás; a Károli-kulcs Jób 17:15, ill. Préd 9:12 — a Károli-Jób 17 a 17:15-nél véget ér, a Préd 9:10 a Károli-szövegben más vers; tehát nem szóalak-eltérés, hanem verseltolás; az ítélet változatlan). A harmadik, `elter` ítéletű sor (ALVIL-001 Jób 17:13) is verseltolásból ered (Károli-kulcs Jób 17:12, ott a H7585 megvan).
- **1Móz/2Móz (25 sor): 23 egyezik + `magas`, 2 elter.** Ez a ma frissíthető halmaz (a többi 130 `egyezik` sor `alacsony` párokon áll: nem frissíthető).
- A két 1Móz/2Móz eltérés valódi:
  - KIRALY-001, 2Móz 19:6, `papok` (H3548+H4467): a gépi pár `papok` → H3548, a H4467 (`birodalma`) külön szóhoz tartozik; a régi sor a kifejezés két szavát egy `karoli_szo`-ba vonta.
  - TEREMT-001, 2Móz 15:5, `a mélységbe` (H8415): a gépi párosítás szerint H8415 a `hullámok` (`תְּהֹמֹת`), a `mélységbe` H9003 + H4688 (`מְצוֹלֹת`). A régi sor `karoli_szo`-ja valószínűleg rossz szóra mutat (a H8415 szava itt `hullámok`). Értelmező feloldás, külön tétel (brief 2. szakasz „Nincs benne”).

## 5. A tematikus táblák

A tematikus táblák (`tematikus_lezart/*.md`) Igehely + Strong-számok + Kapcsolódás szöveg oszlopokat hordoznak, **Károli-idézet-oszlop nincs** (pl. `Segitsegul_hivni_az_Urat_tematikus.md`: `Igehely | Kapcsolódás | Strong-szám(ok) | BDB-entry-id | …`). Gépi Károli-szó + Strong pár ezekből nem nyerhető ki; az 1.1 ellenőrzés ezért **csak a `jeloltek.tsv`/`elofordulasok.tsv` sorain át fut** (a brief 3. M0/4. pontja szerinti alapeset).

## 6. A `Karoli_Strong_kivonat.tsv`

Az `ATALAKITASI_TERV.md.md` 83. sora szerint generált nézet (`elofordulasok`-ból). Az eszköz nem írja (brief 2. szakasz). *Megjegyzés:* 383 sora van, az `elofordulasok.tsv`-nek 205 `tartalom-alapú` sora; a 194 Gen-sor nagy része (a `1Moz_1v1_bovitett.md` forrás) nincs `elofordulasok`-sorban, tehát a kivonat nem tisztán az `elofordulasok` nézete. A kivonat frissítését a generátor gazdája végzi; a #65 csak jelzi.

## 7. Javaslat a megerősített sor kezelésére

- `azonositas_modja`: `tartalom-alapú` → `szó-szintű-gépi` (DT-M2).
- `karoli_szo`: **marad** (a régi, kézzel adott alak; a gépi párosítás szavai a variancia-táblában és az eltéréslistában visszakereshetők).
- `megbizhatosag`: **marad** (a `magas`/`közepes` a régi kutatói minősítés; az ellenőrzés nem a kutatói minősítést cseréli). Ha a felhasználó a `közepes` sorokat is frissíteni kívánja `szó-szintű-gépi`-re, a `megbizhatosag` külön marad (a mód és a minősítés két külön mező).
- A `jeloltek.tsv` sor az `elofordulasok`-ítélettel együtt frissül (id + igehely kulcs).
- A `proveniencia`-mező (elofordulasok) nem változik (a proveniencia az állítás eredetét mondja; az újraazonosítás a `azonositas_modja`-ban látszik). A frissítés tényét az F65-napló (`naplok/KAROLI_ELLENORZES_zaras.md`) rögzíti.

## 8. Az M3 mintához

ANTROP-001-nek **egyetlen** 1Móz/2Móz sora van (1Móz 2:7 `élő lélekké`, H5315+H2416; gépi: H2416, H5315, H9005, `magas` → egyezik): a brief szerinti ≥3 triplet-sor nincs. Javaslat: az M3 mintája **ANTROP-001 (1 sor) + ISTENTISZT-001 (7 sor 1Móz/2Móz, mind egyezik+magas)**; ha a felhasználó a mintát egy motívumra akarja, az ISTENTISZT-001 (aranyminta, lásd az „Aranyminta előbb” elvet) a megfelelőbb. Az ANTROP-001 NT-sorai (7) `nincs_par`.

## 9. Döntési kérdések (⛔, `DONTESEK.md`: DT-F65a)

1. Az illesztés szabálya (3. szakasz) elfogadható-e?
2. A frissítés szabálya (7. szakasz): csak `azonositas_modja` vált, `karoli_szo` és `megbizhatosag` marad?
3. Tudomásul veszi-e a „magas” lefedettséget: ma **csak 25 sor** (23 frissíthető) esik 1Móz/2Móz-re, a többi 180 régi sor nem frissül (a 3Móz–Ez könyvekre ma 130 `egyezik` sor van, de `alacsony` párokon; a #22 kétmodelles futása után újrafuttatható)?
4. M3-minta: ANTROP-001 + ISTENTISZT-001?
