# F241 átadó — F241.5b, 1. menet → F241.5b, 2. menet

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet), PR #841 · a döntések: `naplok/F241_dontesek.md` (D1–D16); előbb azt olvasd, és a fájl aktuális állapotát hajtsd végre. **A két ⛔ megválaszolva: D15 (a 91 MINTA-hely) és D16 (sablonszövegek, szakszavak, sorrend); a lent álló javaslatoknál a D15/D16 szövege az irányadó** (pl. a „jelöltek közé” zárómondat elmarad; „A szócikk teljességmérése”; a „szónézet” nem „szócikk”; a LISTA_NEVELO kivétele cellatípusból).*

## Állapot

- **Kész:** KONYV („Zef” → „Sof”, `51bd1fa1`), a mérce B63/B21 hash-sora (`e7d93251`); a HAMART-001 regressziója RENDBEN.
- **Mérve, javításra vár (a mérés és a javaslat: `side-session-notes/local_5140778b…/F241.5b_MINTA91_meres.md`, 1. és 2. rész; munkalista: `F241.5b_szokincs_munkalista.tsv`):**
  1. a 91 MINTA-hely (⛔ 1, elküldve 2026-11-24): külön olvasói-indoklás tábla hash-kulccsal (`adat/olvasoi_indoklasok.tsv`); a 61 kereszthivatkozásos sor kettőzése (3. és 6. szakasz); a B56 két `megjegyzes`-e és a `kiadasok.tsv` egy szava helyben; a BDB „arab,;” technikai (a `bdb_jelolt/forras_javit.py` szabálya);
  2. LISTA_NEVELO, MUNKASZO, a D11-kapuk szakszavai (⛔ 2, elküldve 2026-11-24): a Kolofon „A lap elején áll (…)”, az Irodalom „A keresések versszámainak mérése”, a LISTA_NEVELO oszlop-hatóköre (Kulcsszó, Funkció), „lánc” → „a motívum szava”, „szónézet” → „szócikk”.
- **Az `ellenoriz` 11. szabálya:** a régi generátor fogyasztója; az új generátor lapján SÉRTÉST ad, tartalmi veszteség nélkül. **Az F241.7 első lépése** az átkötés (nem marad gazdátlanul).

## Következő (a D15 és a D16 szerint; a (4) sablonsorai még ⛔ az integrátorhoz, soronként, egyben)

1. A ⛔ 1 válasza szerint: az olvasói-indoklás tábla (séma: `adat/SEMA.md`, új szakasz; `lapgen_bemenetek.tsv` új B-sor; a `vizsgalt.py` és a `kereszthiv.py` Indok cellája; a mezőtípus-jegyzék része), a kettőzés, a helyben javítások; a MINTA-kapu az ISTENTISZT-001 lapján 0.
2. A ⛔ 2 válasza szerint: a sablon- és névtábla-sorok cseréje, a szókincs-kapu (statikus teszt a B65/B66 minden során, D12) és a névtábla-identitás kapu (a `pardes_szint` stb. valódi nevei indokolt kivétellel; az `ok_cella`-másolat megszüntetése), egy commitban a javítással.
3. A D11 többi pontja: mezőtípus-jegyzék (a B04 `indoklas` két típusa, a B02 `sablon_verzio`), az adattábla-prózamező festékkategóriája, a (b2) idézet-minőség kapu (B14/B18/B39), a (d) ág javításai; a forrásmérés tételenkénti táblája a munkalista.
4. Minden lépés után: a célzott tesztek, az ISTENTISZT-001 mérése, a HAMART-001 regressziója; a mérce hash-sora külön commitban.

## Szabályok (az előző átadóból, változatlanul)

- Helyi ág: `git checkout -B <helyi> origin/claude/f241a-kiadasi-ut` (az `f241a-helyi` név más worktree-ben foglalt); push: `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Egyszerre egy lapgen-futás; előtte `python.exe`-lista; más session folyamatát soha nem állítod le.
- Célzott tesztek (`futtat.py <név>`), nem a teljes készlet; a HAMART-001 regressziója: `PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívül>`, `regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --teljes`.
- A normalizáló tábla vagy más rögzített hash-ű bemenet változása után a rá hivatkozó generált tábla fejléce elavul (pl. `thayer_vers_jelentes.tsv`): az előállító szkriptet újra kell futtatni, és ellenőrizni, hogy csak a fejléc változik.
- Kontextus-plafon kb. 150 ezer token; lépéshatáron átadó.
