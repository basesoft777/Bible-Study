---
feladat: 41
cim: BSB-import kiegészítése — a küszöb alatti 8 ószövetségi könyv újramérése versszám-megfeleltetéssel, és az üres angol szavak jelölése
kod: BSB_UJRAMERES
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/f41-bsb-ujrameres
pr: https://github.com/basesoft777/Bible-Study/pull/135
lezarva_osszegzes: "36 ÓSZ-könyv ≥95% (278 125 sor), 7. oszlop Számozás mt 260 243 / kjv 223 / ellenorizetlen 17 659 (versszintű WLC-összevetés); DT-F41g ✅; nyitott: ELLENOR_F41_5 (F41.15), merge; a DT6 🟢 marad ((c), (d), (e), (g) nincs eldöntve)."
ad: a versszámozás miatt küszöb alatt maradt ószövetségi könyvek a 95%-os küszöbbel újramérve és importálva, a többinél igazolt ok; a BSB_Strongs.tsv-ben megkülönböztethető a „szándékosan nem fordított” és a „hiányzó” angol szó
kovetkezo: "Fő szál: fuggetlen-ellenor az F41.15 diffre, merge a felhasználótól; a DT6 🟢 marad, amíg a (c), (d), (e), (g) nyitott"
olvas: [eszkozok/fj2/, konkordancia/TAHOT_kivonat.tsv, konkordancia/Macula_heber_*.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, naplok/F16_bsb_lefedettseg.tsv, naplok/F16_bsb_verseltolas_diagnozis.tsv, naplok/F16_bsb_zsolt_megfeleltetes.tsv]
ir: [eszkozok/fj2/bsb_import.py, eszkozok/fj2/bsb_verseltolas_diag.py, eszkozok/fj2/wlc_versek.py, eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py, eszkozok/fj2/bsb_nulladiff.py, eszkozok/fj2/bsb_parameter_erzekenyseg.py, naplok/F41_parameter_erzekenyseg.tsv, naplok/F41_parameter_erzekenyseg.md, konkordancia/BSB_Strongs.tsv, konkordancia/README.md, naplok/F16_bsb_lefedettseg.tsv, naplok/F41_bsb_megfeleltetes.tsv, naplok/F41_nem_egyezo_versek.tsv, naplok/F41_nulladiff.txt, naplok/F41_wlc_versszam_ellenorzes.tsv, naplok/F41_wlc_hatar_ellenorzes.tsv, naplok/F41_zaras.md, adat/datasetek.tsv, adat/SEMA.md, adat/szotar_szerepek.tsv, DONTESEK.md, NYITOTT_FELADATOK.md, F41_BSB_UJRAMERES_BRIEF.md]
fugg: [16]
helyi_gep: nem
---

# F41_BSB_UJRAMERES_BRIEF.md — BSB-import kiegészítése: a küszöb alatti 8 ószövetségi könyv újramérése és az üres angol szavak jelölése

*FELADATOK #41 (várható szám, a `/befogad` véglegesíti) · Modell: sonnet · v1 · 2026.10.02 · a DT6 döntésének végrehajtása*

> **Javítás (F41 menet, 2026.10.02; a címsor változatlan):** a 2. szakasz „1Kir 4/5, Jóel 2/3, Neh 3/4” példái hibásak: a Strong-illeszkedés szerint (`naplok/F41_bsb_megfeleltetes.tsv`) ezekben a TAHOT_kivonat számozása a BSB-vel azonos, 0 eltolt verssel. A ténylegesen eltolt könyvek/fejezetek: 4Móz 12/13 és 29/30, 1Sám 23/24, 1Kir 22 (a 22:43 két MT-versre osztva), Jób 38–40, Préd 11/12, Ézs 2/3 és 9, Hós 11/12, Jón 1/2, Zsolt (62 fejezet). A 3.1 szövegében szereplő Jón 1:17 → 2:1 példa helyes. Részletek: N-F41d (`NYITOTT_FELADATOK.md`).

> **Javítás (F41.7, 2026.10.02; felhasználói döntés: DT-F41c (a), DT-F41b lezárva, DT-F41d, DT-F41e):** a célszámozás MT (WLC). A 3.4 „6. oszlopa” mellé a `BSB_Strongs.tsv` 7. oszlopot kapott: `Számozás` (`tahot_szamozas` / `kjv_szamozas`); a Jób 38–41 a main KJV-számozásán maradt (jelölve), a Préd 11/12 és Ézs 2/3 átszámozása visszavonva (a WLC szerint KJV = MT: `naplok/F41_wlc_hatar_ellenorzes.tsv`); a 4Móz, 1Sám, Hós, Jón átszámozás és az 1Kir 22:43 osztás marad. A nulla-diff (`naplok/F41_nulladiff.txt`) commitolt szkripttel készül (`eszkozok/fj2/bsb_nulladiff.py`); a WLC-összevetés: `eszkozok/fj2/bsb_wlc_versszam_ellenorzes.py` → `naplok/F41_wlc_versszam_ellenorzes.tsv`.

> **Javítás (F41.10, 2026.10.02; felhasználói döntés: DT-F41f):** a 4Móz 12/13 átszámozása visszavonva (a WLC szerint KJV = MT; main szerinti számozás); a 4Móz 29/30 marad (WLC: KJV ≠ MT). A 7. oszlop (`Számozás`) értékei `mt` / `kjv` / `ellenorizetlen` (a `tahot_szamozas` / `kjv_szamozas` megszűnt), versszintű WLC-összevetésből (`eszkozok/fj2/wlc_versek.py`); az N-F41h a teljes MT-átszámozásról szól. Részletek: `naplok/F41_zaras.md`, `DONTESEK.md` DT-F41f.

> **Javítás (F41.12, 2026.10.02; a harmadik független ellenőrzés nyomán, DT-F41g):** a `Számozás` kritériuma szigorítva (`wlc_versek.vers_igazolt`: környezet-egyértelműség, részvers- és szomszéd-szűrő; döntetlen → `ellenorizetlen`); a WLC-szkript konzisztencia-ellenőrzés + független Jaccard-ellenőrzés. Részletek: `naplok/F41_zaras.md`, `DONTESEK.md` DT-F41g.

<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Olvasd be a csatolt briefet és a `CLAUDE.md`-t, majd hajtsd végre a 3. szakasz lépéseit sorrendben. Az 1. lépés végén ⛔ állj meg, és a jelentést add vissza; a 2–5. lépés csak jóváhagyás után fut. A küszöböt (`eszkozok/fj2/kuszob.txt`) nem módosíthatod. Ha egy fejezet megfeleltetése nem igazolható, a fejezet kimarad, jelölve. Csendes közelítést nem alkalmazhatsz. A menetet a `CLAUDE.md` menetzárási szabálya szerint zárd.
<!-- /KOZVETLEN_FUTTATAS -->

## 1. Cél

A #16 (BSB-import) 31 ószövetségi könyvet importált. 8 könyv a 95%-os küszöb alatt maradt: 1Sám 94,56; 2Sám 94,96; Ezsd 94,64; Préd 90,91; Ézs 94,73; Dán 89,64; Hós 89,80; Jón 78,72. A `naplok/F16_bsb_verseltolas_diagnozis.tsv` szerint ötnél a versszámozás az ok: fejezetenkénti eltolással a Jón 100,00, a Préd 96,82, a Hós 96,94, az Ézs 98,06, az 1Sám 96,91 lenne. A 2Sám, az Ezsd és a Dán értékét az eltolás nem javítja, az okuk vizsgálatlan.

Ez a feladat a következőket végzi el:

1. a Zsoltárokon már működő BSB→MT megfeleltetést általánosítja a többi eltolt fejezetre, majd ugyanazzal a küszöbbel újramér és importál;
2. a 2Sám, Ezsd és Dán nem egyező verseiből igazolja az eltérés okát;
3. az üres „Angol szó” mezőket (elided span) jelöli.

## 2. Hatókör

**Benne van:**
- a megfeleltetés általánosítása versszintre, fejezethatáron átnyúló esetekkel (pl. Jón: BSB 1:17 → MT 2:1, BSB 2:1–10 → MT 2:2–11);
- a diagnózis kiterjesztése mind a 39 ószövetségi könyvre, mert a már importált 31 könyvben is lehetnek eltolt fejezetek (pl. 1Kir 4/5, Jóel 2/3, Neh 3/4);
- a nem egyező versek listája okkategóriával;
- újramérés és import;
- az `elided` jelölés a `BSB_Strongs.tsv`-ben.

**Nincs benne:**
- a küszöb módosítása (DT6 (d), döntésre vár; nem része ennek a feladatnak);
- a hiányzó 117 első vers pótlása a `hebrew-tsv/`-ből (DT6 (c), a licenc tisztázásáig halasztva, a #33 utánra);
- a Zsolt 13 kézi megfeleltetése (DT6 (g), külön döntés, l. 3.0);
- az újszövetségi könyvek (DT6 (f): nincs BSB-import, a görög réteg forrása a Macula, #87);
- a `KJV_Strongs_*.tsv` / ASV fájlok hasonló jelölése (ha kell, külön N-tétel).

## 3. Lépések

### 3.0 Döntések átvezetése (a menet első commitja)

A `DONTESEK.md` DT6-sorának „Döntés” cellája:

> (a)+(b)+(f) elfogadva ((a), (f): a mostani tényállapot rögzítése; felhasználó, chat, 2026.10.02). (b): a BSB→MT megfeleltetés általánosítása versszintre, ugyanazzal a 95%-kal, az F41-ben. (c): a licenc tisztázásáig halasztva (#33), nincs eldöntve. (d), (e): döntésre vár. (g): kiválik `DT-F41a` néven. (2026.10.02)

Állapota 🟢. A menet a DT6-ot nem állítja ✅-ra: az marad 🟢, amíg a (c)–(e), (g) nyitott.

A (g) új sorba kerül `DT-F41a` helyőrzővel. A kérdés és az opciók szó szerint a DT6-ból jönnek (kézi megfeleltetés: BSB 2→MT 3, 3→4, 4→5, 5+6→6, vagy kimaradás), az állapot 🟡.

### 3.1 Megfeleltetés és diagnózis mind a 39 ószövetségi könyvre — ⛔ megállás

- Az eltolás-modell versszintű. Minden BSB-vershez egy MT-vers tartozik (`fej:vers`), a fejezethatáron átnyúló esetekkel együtt. Egy vershez több MT-vers vagy egy MT-vershez több BSB-vers csak jelölve fordulhat elő (belső versosztás-eltérés, mint a Zsolt 13-ban), és az ilyen fejezet nem importálható.
- **A megfeleltetés forrása a Strong-illeszkedés**, a `bsb_verseltolas_diag.py` módszere szerint, kiterjesztve. Az MT-oldali fejezet-maxot a Károli-kulcs `igehely_mt` oszlopa és a TAHOT-max ellenőrzi.
- **Figyelem:** a Károli-kulcs `igehely_kjv` oszlopa nem használható közvetlenül. Egy jelzett példa: a `Jón 2:1` sorban `igehely_kjv` = `2:1`, holott a Károli Jón 2:1 a KJV 1:17-e. Ezt a lépés ellenőrizze, és ha igazolódik, vegye fel N-tételként (`N-F41a`). Javítani nem ennek a menetnek a dolga.
- Fejezetenként igazolni kell, hogy minden BSB-vers a megfeleltetett MT-versre illeszkedik, és nem a szomszédosra (az F16.11 próbája).
- Kimenet: `naplok/F41_bsb_megfeleltetes.tsv`, a következő oszlopokkal: `konyv`, `bsb_vers`, `mt_vers`, `modell` (`azonos` / `eltolt` / `illesztetlen`), `ok`.

**⛔ Jelentés (legfeljebb 20 sor):**
- könyvenként a régi és az új egyezési százalék;
- a 31 már importált könyv közül melyikben van eltolt fejezet, és hány sort érintene az újraimport;
- az illesztetlen fejezetek listája;
- a KK `igehely_kjv` ellenőrzésének eredménye.

**Döntésre vár:** a 31 importált könyv eltolt fejezeteinek átszámozása is megtörténjen-e. Javaslat: igen, hogy a `BSB_Strongs.tsv` Igehely-oszlopa egységesen MT-számozású legyen, ahogy a Zsoltároknál már az.

### 3.2 Nem egyező versek okkategóriával

`naplok/F41_nem_egyezo_versek.tsv` mind a 39 ószövetségi könyvre, a 3.1 megfeleltetése után. Oszlopai: `konyv`, `bsb_vers`, `mt_vers`, `tahot_nincs_bsbben`, `bsb_tobblet`, `okkategoria`.

Az okkategória értékei:
- `szamozas` — maradék, a modell által nem kezelt eset;
- `arami` — a vers arámi szakaszba esik: Dán 2:4b–7:28, Ezsd 4:8–6:18 és 7:12–26, Jer 10:11; ezt a TAHOT nyelvjelöléséből kell venni, ha van;
- `cimkezes` — eltérő Strong-szám ugyanarra a szóra (pl. H3068/H3069, betűs utótag);
- `egyeb`.

A 2Sám, az Ezsd és a Dán okát könyvenként egy mondatban kell összefoglalni. **Feltevés, nem igazolt:** a Dán és az Ezsd eltérése az arámi szakaszok Strong-címkézéséből jön. Ezt a lépés igazolja vagy cáfolja.

### 3.3 Újramérés és import

- A `bsb_import.py` a 3.1 versszintű megfeleltetését használja. A küszöb, a definíció és a nevező változatlan (`kuszob.txt`).
- Az új egyezési oszlop a megfeleltetéssel mért érték. Az eltolás nélküli érték (az F06-módszer) tájékoztatóként marad, ahogy a Zsoltároknál.
- Import: minden ószövetségi könyv, amely a küszöböt eléri. Az illesztetlen fejezetek kimaradnak, jelölve.
- A 31 korábbi könyv importja a 3.1 döntése szerint változik. Ha az átszámozást nem hagyod jóvá, ezeknek a soroknak bájtazonosnak kell maradniuk (nulla-diff: `naplok/F41_nulladiff.txt`).

### 3.4 Az üres „Angol szó” jelölése (DT6 (e) — döntésre vár)

⛔ A DT6 (e) pontja nincs eldöntve (felhasználó, 2026.10.02): ha a menet ide ér, megállás. Az `Angol szó állapota` oszlop, amely ennek a lépésnek már elkészült eredménye (PR #135), előkészítő jellegű, és a DT6 (e) eldöntéséig nem tekinthető végleges, elfogadott kimenetnek; a lépést e szerint kell feltételesnek olvasni.

- Új, 6. oszlop: `Angol szó állapota`, a következő értékekkel:
  - `forditva` — az „Angol szó” nem üres;
  - `elhagyva` — a forrás-span `elided` jelzőt hordoz (a `vers_sorok()` ezt ma csak számolja);
  - `ures_jelzo_nelkul` — üres „Angol szó”, `elided` jelző nélkül. Várhatóan 0; ha nem, a jelentésbe kerül.
- Az „Angol szó” mező üres marad, helyőrző szöveg nem kerül bele.
- **Előtte ellenőrizni kell, ki olvassa a `BSB_Strongs.tsv`-t** (`grep -rn BSB_Strongs`, a CI-szabályokkal együtt). Ha valamelyik olvasó oszlopsorszámmal dolgozik, és egy 6. oszloptól eltörne, ⛔ megállás.
- Az import-szkript a végén gépi ellenőrzést végez: üres „Angol szó” csak `elhagyva` vagy `ures_jelzo_nelkul` állapottal fordulhat elő, a darabszámok pedig egyezzenek a napló `szurt sorok` számlálóival. CI-szabályt ez a menet nem ír; ha kell, `N-F41b` javaslatként kerül a `NYITOTT_FELADATOK.md`-be.

### 3.5 Menetzárás

A `CLAUDE.md` szerint: `fuggetlen-ellenor` (`naplok/ELLENOR_F41.md`), push, draft PR, a `FELADATOK.md` saját sora, és a DT6 sora (🟢 marad; ✅ nem a zárócommitban). A záró összefoglaló első sora a PR linkje és a CI állapota.

## 4. Elfogadási feltételek

1. A `kuszob.txt` változatlan; minden importált ószövetségi könyv ≥ 95% a megfeleltetéssel mért értéken.
2. Minden importált fejezet megfeleltetése igazolt (`modell` ≠ `illesztetlen`); az illesztetlen fejezetek jelölve kimaradnak.
3. A Jón, Préd, Hós, Ézs, 1Sám új értéke legalább a diagnózisban mért érték (100,00 / 96,82 / 96,94 / 98,06 / 96,91), vagy az eltérés soronként indokolt.
4. A 2Sám, Ezsd és Dán eltérésének oka a nem egyező versek listájából igazolt (könyvenként egy mondat, okkategória-számokkal).
5. (Feltételes: csak ha a DT6 (e) eldőlt.) A `BSB_Strongs.tsv` minden sorában van `Angol szó állapota`; `ures_jelzo_nelkul` = 0, vagy a sorok listázva vannak.
6. Ha a 31 korábbi könyv átszámozását nem hagyod jóvá, az érintetlen sorok nulla-diffje igazolt.
7. A CI zöld, és az ellenőri jelentés eltérés nélkül zárul (vagy az eltérések itt döntésként szerepelnek).

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | A DT6-ban (a)+(b)+(f); a (d) döntésre vár, nem része a feladatnak | a D15 küszöbe mérés előtt rögzített; a diagnózis szerint öt könyvben a számozás az ok, nem a BSB címkéi | a küszöb lazítása; a 8 könyv végleges kihagyása |
| D2 | A megfeleltetés versszintű, Strong-illeszkedéssel igazolva; a KK `igehely_mt` csak ellenőrzés | a fejezetenként állandó k (Zsoltár-modell) a fejezethatáron átnyúló eseteket (Jón 1:17 → MT 2:1) nem kezeli; a KK `igehely_kjv` oszlopa legalább egy helyen hibásnak látszik | a Zsoltár-szkript változatlan kiterjesztése; a KK `igehely_kjv` közvetlen használata |
| D3 | A diagnózis mind a 39 ószövetségi könyvre fut, az átszámozásról ⛔ döntés | egységes MT-számozás kell a `BSB_Strongs.tsv`-ben; a 31 importált könyv adatait csak jóváhagyással szabad megváltoztatni | csak a 8 könyv |
| D4 | (e) — döntésre vár (DT6); előkészítőként: külön `Angol szó állapota` oszlop a forrás `elided` jelzőjéből | az üres mező ma nem különbözteti meg a „nem fordította” és a „nem jött át” esetet; a Károli–Strong párosításnak ez információ; helyőrző szöveg beszivárogna a renderbe és a keresésbe | helyőrző az „Angol szó” mezőben; „elided” a Morfológiai kód oszlopban (eltérne a KJV-formátumtól) |
| D5 | A (g) Zsolt 13 külön döntés (`DT-F41a`) | nem része a jóváhagyott javaslatnak | a menetben eldönteni |
| D6 | (c) a #33 (licenc rendezése) utánra | a `hebrew-tsv/` licence nincs kimondva | pótlás most |
