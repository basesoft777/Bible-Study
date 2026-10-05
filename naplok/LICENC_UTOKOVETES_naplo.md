# F44 — Licenc-utókövetés napló

*Ág: `claude/licenc-utokovetes` · 2026.10.05 · végrehajtó: sonnet (Sonnet 5.5; a brief `modell: sonnet`-nel egyezik)*

## Kiinduló megállapítás

A brief (2026.10.02) óta a **DT-F33e** (felhasználói döntés, 2026.10.04) a Károli-részt tárgytalanná tette: a `Karoli_1908` és a `Karoli_KH` sor `kozkincs`, kiadói nyilatkozat nélkül. A `Versifikacios_tablak` sor már `tisztazott`, szó szerinti fejléc-idézettel és commit-tal (`b99716b`). Ezért az 1. és 3. lépés **ellenőrzés**, nem módosítás: az `adat/licencek.tsv` ebben a menetben **nem változott** (`git diff` üres rajta).

## 0. lépés (előfeltétel-fájlok, bent voltak)

- `adat/kulso/karoli_bible_hu_LICENC.txt`: HF `k-mktr/karoli_bible_hu` @ `b05136fd…` (2026-07-28). A YAML-fejlécben **nincs `license` mező**; a „License” szakasz: „Public domain (first published 1590, copyright expired).” A kártya címe: „Hungarian Károli Bible (1590)”, azaz az **1590-es vizsolyi kiadás, nem az 1908-as revízió**.
- `adat/kulso/openbible_crossrefs_LICENC.txt`: az oldal szó szerinti szövege (2026-10-04).

## 1. Károli 1908 — a két meglévő forrás (újraellenőrzés 2026-10-05)

| Forrás | Parancs | Eredmény |
|---|---|---|
| krisek/HunKar `hunkar.conf` @ `0e244494dd190e4a6b132c1afddfa307e73792f8` | `curl -sL https://raw.githubusercontent.com/krisek/HunKar/0e244494dd190e4a6b132c1afddfa307e73792f8/hunkar.conf`, majd `grep -n -i -E "license|about|source"` | 14. sor: `DistributionLicense=Public Domain`; 13. sor: `TextSource=https://github.com/krisek/HunKar`; 16. sor: `About=Revised version of the original translation by Károli Gáspár, first published in 1590 in Vizsoly, Hungary.`; 21. sor: a modul új forrásból (szentiras.hu kereszthivatkozások, abibliamindenkie.hu címek) épült újra |
| scrollmapper/bible_databases `LICENSE` @ `e1b254cef86d0e65b1a5d1a94b8b112d0f296a2c` | `curl -sL https://raw.githubusercontent.com/scrollmapper/bible_databases/e1b254cef86d0e65b1a5d1a94b8b112d0f296a2c/LICENSE`, `head -4` | „MIT License” / „Copyright (c) 2024 Scrollmapper” |

A `licencek.tsv` idézetei egyeznek. **Kinek az állítása:** a hunkar.conf a modulkészítőé (krisek), nem a szövegkiadóé. A DT-F33e miatt ez a `kozkincs` besoroláshoz nem hiányzik. Sor-állapot előtte = utána: `Karoli_1908` / `Karoli_KH`: `kozkincs`.

## 2. A HF-jelölt felmérése

- **Licenc:** a kártya saját állítása „Public domain”, de a YAML `license` mező hiányzik. A #33 mérce (jogtulajdonos szó szerinti nyilatkozata a saját adatára) szerint ez az adat készítőjének (k-mktr) önbesorolása, nem kiadói nyilatkozat; a kor-alapú közkincs (1590-es szöveg) áll mellette.
- **Kiadás:** **nem azonos az 1908-as revízióval**: az 1590-es Vizsoly. A hunkar.conf is megkülönbözteti („Revised version of the original translation … first published in 1590”). Az adatfájl (`data/data.parquet`) nincs letöltve.
- **20 verses szövegösszevetés: nem készült el.** Ok: (i) a DT-F33e a Károli-részt tárgytalanná tette; (ii) a kártya szerint eleve más kiadásról van szó (1590 vs. 1908: a helyesírás és a szöveg szükségszerűen eltér, az „egyezési arány” a kiadás azonosságát nem bizonyítaná); (iii) a brief D4 szerint a HF-szöveget a felhasználó másolná be, ez nem történt meg. A `naplok/LICENC_UTOKOVETES_karoli_diff.tsv` ezért **nem jött létre**. Ha a felvétel mégis kell (DT31), a mintavétel (rögzített seeddel) és az összevetés külön lépés.

## 3. Versifikációs táblák (újraellenőrzés)

A sor (`Versifikacios_tablak`) már tartalmazza: fájlnév `TVTMS - Translators Versification Traditions with Methodology for Standardisation for Eng+Heb+Lat+Grk+Others - STEPBible.org CC BY.txt`, STEPBible-Data @ `b99716b0cddb648ddb95cc786a197180f2f97d48`, 5 790 928 bájt. Ellenőrzés: `curl -sL -r 0-6000` a GitHub raw-ról ugyanezen a commiton (`Versification/` alatt). Az 1. sor és a fejléc-blokk szó szerint egyezik a sorban idézettel: „Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)”; „Include any part of this data in software or publications without requesting permission”; „Refer others to github.com/STEPBible as the source of the data. Please do not redistribute it yourself.” Állapot előtte = utána: `tisztazott` (a TVTMS-eredetű oszlopokra; a projekt saját hozzáadásai a `projekt_adat` sor tárgya). A commit rekonstruálható volt, hiány nincs.

## 3b. openbible.info kereszthivatkozások

- Szó szerinti idézet: `adat/kulso/openbible_crossrefs_LICENC.txt`: „Unless otherwise indicated, all content is licensed under a Creative Commons Attribution License.” (link: CC BY 4.0). Az oldal szerint az adat főleg a közkincs Treasury of Scripture Knowledge-ből ered.
- **`datasetek.tsv`: 4 új sor** (egy study-típusonként, mint a többi dataset): dataset `openbible_crossrefs`, `fajl` üres, `kotelezoseg=ajanlott`, `allapot=hianyzik`. **Eltérés a briefhez:** a brief `jelölt` állapotot kér, de az SEMA 2.6 értékkészlete (`elerheto|korlatos|hianyzik|generalt_nezet`) nem ismeri; a `hianyzik` a még nem importált datasetek helye (SEMA 2.6), a megjegyzés „JELÖLT, NEM IMPORTÁLT”-ként jelöli. Új `allapot`-érték bevezetése SEMA-módosítás, nem az `ir` hatóköre: DT33.
- `licencek.tsv`-sor nem került fel (a brief szerint import előtt nincs). Adat nem lett letöltve.

## 3c. bible-mcp (`nirajagarwal/bible-mcp`)

README @ `4388b3844e7cffb19bc1351eb4f8979ae885bcec` (`master` ág, 2026-09-28; az alapértelmezett ág `master`, nem `main`), „Public edition” szakasz, szó szerint:

> This is a **non-commercial public resource**. Licensing is layered — sources keep their own licenses (all PD / CC BY / CC BY-SA); the code is PolyForm Noncommercial 1.0.0; the compilation and derived data (versemap, citation graph, embeddings, outputs layer) are CC BY-NC 4.0. Full details: `LICENSE.md`, attributions in `NOTICE.md`.

Ugyanott: az openbible-réteg „~345,000 ranked cross-references | openbible.info | CC BY”; a Theographic Bible Metadata CC BY-SA 4.0; a provenancia-szintek: „A=free, B=share-alike, C=non-commercial, D=closed — we are non-commercial, so C is usable”. (A `LICENSE.md` és `NOTICE.md` nem lett olvasva; az idézet a README-é.) A MACULA-réteg és az openbible mögöttes forrás közvetlenül elérhető, tisztázott forrásból.

## 5. ⛔ Döntési javaslatok (tételként a DONTESEK.md-ben, nincs alkalmazva)

- **(a) `Karoli_1908`:** tárgytalan, a DT-F33e már döntött: `kozkincs`. Nincs teendő. (A hunkar.conf modulkészítői állítás; a kiadói nyilatkozat hiánya a DT-F33e szerint nem akadály.)
- **(b) `karoli_bible_hu`:** javaslat: **elvetés** (nincs `datasetek.tsv`-sor). Indok: az 1590-es vizsolyi kiadás, nem az 1908-as revízió, tehát nem helyettesíti a `Karoli_1908`-at; a Károli-forrás cseréje nincs napirenden (D5); a kártya `license` mezője hiányzik. Alternatíva: `hianyzik`+JELÖLT felvétel, ha az 1590-es szöveg külön célra (történeti összevetés) kell. → DT31
- **(c) `Versifikacios_tablak`:** javaslat: a besorolás marad `tisztazott` (TVTMS-eredetű oszlopokra); a projekt-hozzáadások a `projekt_adat` sorban `tisztazatlan`. Nincs új teendő.
- **(d) bible-mcp:** a brief szövege: „NC-licencű MCP-szerver (pl. bible-mcp) connectorként használható a chatben ellenőrzésre és tájékozódásra (szókeresés, interlineáris, kereszthivatkozás), de a kimenete nem kerül adatfájlba, briefbe vagy tanulmányba; minden adatot a saját, tisztázott forrásból (MACULA, BDB, TAHOT stb.) kell újra kinyerni és arra hivatkozni. A tool csak rámutat, hol nézzünk.” Opciók: elfogadás / elvetés (nem kötjük be). **Ütközik a már nyitott DT-M5-tel** (javaslat: elvetés egyelőre, a provenienciája nem ellenőrizhető); a két tétel együtt döntendő, a DT-M7 (2026-10-05) is érinti. Javaslat: a szabály csak a használat esetére érvényes, a DT-M5 a használat kérdése. → DT32
- **(e) openbible.info:** import külön feladatként; a licenc a szerző szó szerinti nyilatkozata (az oldal lábléce, mint a TSK-soré) alapján CC BY. A „kapcsolódó igehelyek” rangsor-megjelenítése a study-rules döntése. → DT34

## Elfogadási feltételek állapota

- `licencek.tsv` három sora: szó szerinti idézet + commit megvan (korábbi menetekből, ma újraellenőrizve); a többi sor diffje üres (a fájl egyáltalán nem módosult).
- 20 verses összevetés: **nem készült** (indoklás fent); eltérés a briefhez.
- Nem került új Károli-szöveg a `konkordancia/` alá.
