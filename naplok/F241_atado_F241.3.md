# F241 átadó — F241.3 → F241.4

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet), PR #841 · a döntések: `naplok/F241_dontesek.md` (D1–D12), előbb azt olvasd, és a fájl aktuális állapotát hajtsd végre.*

## Állapot

- **D9–D12 a döntésfájlban** (`a894f9af`, `ce69c7fb`). A D11 új lépést ad: **F241.5b** (a TEREMT-001 forrásmérésének gépi kapui és generátor-javításai) az F241.5 után, az F241.6 előtt; a D12 szerint a kapuk az `adat/lapgen_sablonok.tsv` és az `adat/olvasoi_nevtabla.tsv` minden során futnak. A D10: a szerkesztői nézés formája (C-v, #847) az F241.7-ben és az F241.10-ben.
- **F241.3 kész** (`57ba097f`, `88e6caa5`): a lapszöveg-kapuk a lapmodell szakaszazonosítóján (`lapgen/lapszakasz.py`; `olvasoi_kapu.py`, `proza_1a.py`); HN-17 és N-F239b zárva, gépi teszttel. Közben az F241.1 Kolofon-kapujának három szerkezeti tesztbukása (GK-01, GK-08a) javítva. Részletek, mérés: `naplok/F241_jelentes.md`, „F241.3”.
- Push: `88e6caa5` (és ez az átadó). A PR első sora frissítve.

## Nyitott, a jelentésben kimondva

- `teszt_muhely_allapot.py` `test_hamart_a_valos_adaton_hatardontessel_lezart`: a main-en is bukik (a HAMART-001 határ-frissessége „elavult”), nem ettől az ágtól; nem javítottam (a motívum határa a szerkesztőé), az integrátornak jelezve.
- Az új generátoros ISTENTISZT-001 lapon 103 BUKÁS (MINTA 91: a „jelölt”/„fölérendelt fogalom” a `jeloltek.tsv` kézi indoklásaiban; LISTA_NEVELO 9; KONYV 2 „Zef”; MUNKASZO 1 „Lap teljesség-mérése”), a HAMART-001-en 2 — tartalmi leletek, az F241.5b és az F241.7 bemenete. A „jelölt”-indoklások adatból jönnek: ha a javításuk adatot érint, az a DT933 (1) szerint új nézést kér (⛔ az F241.7-ben).
- A `test_szabalyok.py` 26 E27-hibája környezeti (C:/E: meghajtó); a CI-ben nem áll elő.

## Következő: F241.4 — licenckapu (N223)

A brief 4. pontja szerint: minden licencleltár-forrás, amelynek adata a lapon látszik és `kotelezo_megjeloles`-e nem üres, szerepel a Kolofon forrásmegjelölésében; kapu és teszt. ⛔ a megjelölendő halmaz bővítése (DT911 3. (b)): mérés → lista (forrás, licenc, látszik-e a lapon) → az integrátor dönt. Utána F241.5 (34 fordítás, N244), F241.5b (D11–D12), F241.6 (független ellenőr), F241.7.

## Szabályok, amelyek ezen a szeleten élnek

- A `claude/f241a-kiadasi-ut` ág egy korábbi worktree-ben (`xenodochial-tesla-3c2679`) ki van csekkolva: helyi ágon dolgozz (`git checkout -B <helyi> origin/claude/f241a-kiadasi-ut`), push: `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Egyszerre egy lapgen-futás; futtatás előtt `python.exe`-lista; más session folyamatát soha nem állítod le. Egy lap új generátoros generálása repón kívülre kb. 45 s.
- A felmérés szkriptjei (repón kívül, a régi session scratchpadjében; nem kellenek): a regresszió mintája a jelentésben.
- A `teszt_olvasoi_kapu.py`-ban két lapépítő segéd van: `uj_lap(torzs, cimek)` (a MunkaszoSzakaszHiv-é) és `modell_lap(...)` (a ModellSzakasz-é) — új segédnek új nevet adj.
- Kontextus-plafon: kb. 150 ezer token; lépéshatáron átadó.
