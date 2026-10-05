---
feladat: 44
cim: Licenc-utókövetés — a Károli 1908 és a versifikációs táblák forrásának tisztázása
kod: LICENC_UTOKOVETES
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/licenc-utokovetes
ad: az adat/licencek.tsv Karoli_1908, Karoli_KH és Versifikacios_tablak sora tisztázott vagy dokumentáltan tisztázatlan marad, szó szerinti licencidézettel és rögzített commit-tal; a k-mktr/karoli_bible_hu nyílt Károli-jelölt felmérve; a TVTMS fájl neve és commitja rögzítve; az openbible.info kereszthivatkozás-tábla forrásjelöltként felvéve licencidézettel; a bible-mcp connector használati szabálya döntési javaslatként
kovetkezo: "Lezárás: fuggetlen-ellenor (naplok/ELLENOR_LICENC_UTOKOVETES.md), draft PR; zárójelentés: naplok/F44_zaras.md"
olvas: [adat/licencek.tsv, adat/datasetek.tsv, adat/SEMA.md, naplok/LICENC_RENDEZES_zaras.md, konkordancia/Validacios_naplo.md, konkordancia/LXX_versificacios_terkep.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, F01_KAROLI_KULCS_BRIEF.md, adat/kulso/karoli_bible_hu_LICENC.txt, adat/kulso/openbible_crossrefs_LICENC.txt]
ir: [adat/licencek.tsv, naplok/LICENC_UTOKOVETES_naplo.md, naplok/LICENC_UTOKOVETES_karoli_diff.tsv, adat/datasetek.tsv]
fugg: [33, 42]
helyi_gep: nem
lezarva_osszegzes: "Károli-rész tárgytalan (DT-F33e), licencek.tsv változatlan; karoli_bible_hu elvetve (nincs license mező, 1590-es kiadás; DT-F44a), 20 verses összevetés elmaradt; openbible_crossrefs 4 sor hianyzik+JELÖLT (import külön feladat); bible-mcp a DT-M5-tel döntendő; PR: orkesztrátor"
---

# F44_LICENC_UTOKOVETES_BRIEF.md — Licenc-utókövetés (Károli 1908, versifikációs táblák)

*FELADATOK #44 (a számot a `/befogad` adja) · Modell: sonnet · v1.1 · 2026.10.02 · openbible.info + bible-mcp · a #33 (LICENC_RENDEZES, lezárva, PR #123) utófeladata; az N-F33 tételt ez váltja ki vagy egészíti ki*

## 1. Cél

A #33 leltárában három sor maradt `tisztázatlan`, amelyek a publikálást közvetlenül érintik:
- `Karoli_1908` — scrollmapper/bible_databases `HunKar.json` (a repó MIT, a tartalomra a hunkar.conf közkincs-állítása);
- `Karoli_KH` — krisek/HunKar OSIS (a hunkar.conf „DistributionLicense=Public Domain” állítása);
- `Versifikacios_tablak` — TVTMS-alapú, de a TVTMS fájl neve és commitja nincs rögzítve, licencfejléce nincs idézve.

A feladat ezeket a sorokat tisztázza, és felméri a `k-mktr/karoli_bible_hu` HF-datasetet mint független, nyílt Károli 1908 forrásjelöltet.

Két további tétel (kiegészítés 2026.10.02): az **openbible.info kereszthivatkozás-tábla** (~345 000 vers→vers hivatkozás, közösségi szavazatos rangsorral; a szerző CC BY licencet jelöl) felvétele forrásjelöltként a `datasetek.tsv`-be, licencidézettel; és a **`nirajagarwal/bible-mcp`** MCP-szerver (hostolt végpont, kód PolyForm Noncommercial, származtatott rétegei CC BY-NC 4.0) használati szabályának rögzítése: chat-oldali ellenőrző eszköz, nem forrás.

## 2. Hatókör

**Benne van:** licencidézetek, commit-rögzítés, a HF-jelölt szöveg-összevetése 20 versen, a `licencek.tsv` három sorának frissítése, napló.
**Nincs benne:** Károli-forrás cseréje a repóban; a KK vagy a versifikációs táblák módosítása; bármely gated (NuBerea) dataset; a Bible-Discovery zárt Károli (DT: kizárva, l. 5. szakasz D3).

## 3. Lépések

**0. (Te)** A HF `k-mktr/karoli_bible_hu` kártyájáról a `license` mező és a README szövege szó szerint az `adat/kulso/karoli_bible_hu_LICENC.txt`-be, a letöltés dátumával és a dataset commit-hashével (Files → History). Ha a kártyán nincs licenc, ezt a tényt írd a fájlba. (A HF a cloud proxyn nem elérhető, ezért ez kézi lépés.)

**1. Károli 1908 — a meglévő két forrás.** A `hunkar.conf` és a scrollmapper `LICENSE` szó szerinti idézete (GitHub raw, commit rögzítve) a `licencek.tsv` megfelelő mezőibe; a mérce a #33 L2 lépése szerint. Ha a közkincs-állítás csak a modulkészítőé (nem a szövegkiadóé), a sor `tisztázatlan` marad, de a napló rögzíti, kinek az állítása, és mi hiányzik.

**2. A HF-jelölt felmérése.** A 0. lépés fájljából a licenc besorolása a #33 mércéjével. Szövegösszevetés: 20 vers (10 ÓSZ, 10 ÚSZ, a `Karoli_1908`-ból véletlen minta, seed a naplóban) a `karoli_bible_hu` megfelelő soraival — ehhez a 20 vers szövegét Te másolod be a `naplok/LICENC_UTOKOVETES_karoli_diff.tsv` `hf_szoveg` oszlopába (a dataset-viewerből), a script a diffet és az egyezési arányt számolja. Kimenet: azonos kiadás-e (1908-as revízió), eltérések jellege (helyesírás, versszámozás).

**3. Versifikációs táblák.** A `konkordancia/Validacios_naplo.md` és az `F01_KAROLI_KULCS_BRIEF.md` (G2, K5) alapján a használt TVTMS fájl neve és a STEPBible-Data commit azonosítása; a fájl licencfejlécének szó szerinti idézete (GitHub raw). A `licencek.tsv` `Versifikacios_tablak` sorának frissítése; ha a commit nem rekonstruálható, a sor `tisztázatlan` marad, a hiány megnevezve.

**3b. openbible.info kereszthivatkozások.** A `https://www.openbible.info/labs/cross-references/` oldal licencnyilatkozatának szó szerinti idézete (a cloud proxy a domaint nem engedi: ha a letöltés nem megy, Te másolod be az `adat/kulso/openbible_crossrefs_LICENC.txt`-be, dátummal). Az adat maga **nem** kerül letöltésre ebben a menetben. A `datasetek.tsv`-be új sor `jelölt` állapottal: név `openbible_crossrefs`, forrás-URL, méret (~345 000 sor a szerző szerint), licenc a #33 mércéjével besorolva, tervezett szerep: a tanulmányok „kapcsolódó igehelyek” szakaszának rangsorolt jelöltlistája a Nave mellett (nem helyette). A `licencek.tsv`-be nem kerül sor, amíg nincs import.

**3c. bible-mcp használati szabály (nem letöltés, nem bekötés).** A szerver GitHub-README-jének licenc-szakasza (PolyForm NC a kódra, CC BY-NC 4.0 a kompilációra és a származtatott rétegekre) szó szerint a naplóba, commit-tal. Az 5. lépés döntési javaslata kap egy (d) pontot, l. lent. A connector bekötése a felhasználó kézi lépése a Claude.ai beállításaiban, ha a (d) elfogadva.

**4. Napló** (`naplok/LICENC_UTOKOVETES_naplo.md`): parancsok, idézetek forrása (URL + commit), a 20 vers egyezési aránya, a három sor előtte/utána állapota.

**5. ⛔ Döntési javaslat** a napló végén (nem beírva a DONTESEK.md-be):
- (a) a `Karoli_1908` sor végleges besorolása (tisztázott / tisztázatlan, mi hiányzik);
- (b) a `karoli_bible_hu` mint tartalék forrás: felvétel az `adat/datasetek.tsv`-be `jelölt` állapottal, vagy elvetés;
- (c) a `Versifikacios_tablak` sor besorolása.
- (d) **bible-mcp mint chat-oldali ellenőrző eszköz.** Javasolt szabály a DONTESEK.md-be: „NC-licencű MCP-szerver (pl. bible-mcp) connectorként használható a chatben ellenőrzésre és tájékozódásra (szókeresés, interlineáris, kereszthivatkozás), de a kimenete nem kerül adatfájlba, briefbe vagy tanulmányba; minden adatot a saját, tisztázott forrásból (MACULA, BDB, TAHOT stb.) kell újra kinyerni és arra hivatkozni. A tool csak rámutat, hol nézzünk.” Opciók: elfogadás / elvetés (nem kötjük be).
- (e) **openbible.info kereszthivatkozások** importja külön feladatként, ha a licenc tisztázott; a tanulmánysablon „kapcsolódó igehelyek” szakaszának szabálya (study-rules) dönt arról, hogy a rangsor megjelenik-e.

**6. Zárás** a menetzárási szabály szerint (`fuggetlen-ellenor`, `naplok/ELLENOR_LICENC_UTOKOVETES.md`, push, draft PR; az összefoglaló első sora a PR-link és a CI-állapot).

## 4. Elfogadási feltételek

- A `licencek.tsv` három érintett sorában a licenc-mező szó szerinti idézetet és forrás-commitot tartalmaz, vagy a `tisztázatlan` státusz indoka a sorban áll.
- A többi sor `git diff`-je üres.
- A 20 verses összevetés táblája és aránya a naplóban, reprodukálható parancs mellett.
- Nem kerül új Károli-szöveg a `konkordancia/` alá.

## 5. Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Külön utófeladat, nem a #33 újranyitása | a #33 lezárt (PR #123); a `kovetkezo` mezője maga kéri az N-F33 befogadását |
| D2 | A NuBerea `stepbible` (TVTMS parquet) nem kell | a KK a TVTMS-t a STEPBible-Data GitHub-repóból már használja (F01 G2); a NuBerea ugyanazt adja gated formában, regisztráció nélkül is rendezhető |
| D3 | A Bible-Discovery Károli (zárt licenc, csak másolás) nem forrásjelölt | a felhasználó döntése 2026.10.02; NC/zárt forrás nem kerül a repóba |
| D4 | A HF-jelölt szövegét a felhasználó másolja (20 vers), a script csak összevet | a HF a cloud proxyn nem elérhető; 20 vers kézi másolása elfogadható ár |
| D5 | Forráscsere nincs ebben a menetben | előbb a licenc-státusz, a csere külön döntés |
| D6 | openbible.info kereszthivatkozás: forrásjelölt, import nélkül; licenc előbb | CC BY a szerző jelölése szerint, de a nyilatkozat szó szerinti idézete hiányzik; nincs a leltárban; a Nave mellé rangsort ad, nem helyettesíti |
| D7 | bible-mcp: eszköz, nem forrás; az NC-forráspolitika (F43 3. szakasz, 5. lépés (d)) alól a connector-használat kivétel, az adatátvétel nem | a mögöttes források (MACULA, BDB, openbible.info) tisztázottak és közvetlenül elérhetők; a szerver származtatott rétegei NC, ezért onnan semmi nem kerül a repóba |
