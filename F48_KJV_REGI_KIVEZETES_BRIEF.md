---
feladat: 48
cim: A régi studybible.info KJV/ASV fájlok kivezetése: minden az eBible KJV-forrásra (KJV_Strongs_teljes), az ASV kiesik
kod: KJV_REGI_KIVEZETES
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: a KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv és az ASV_Strongs_{Genesis,Exodus,Proverbs}.tsv (studybible.info, tisztázatlan licenc) kikerül a repóból; a kód, a tesztek és a dokumentáció egyetlen KJV-forrást (konkordancia/KJV_Strongs_teljes.tsv, eBible) használ; a KJV_ASV_Strongs licenc- és dataset-sor kivezetve
kovetkezo: "futtatható az F22 (#22) lezárása és mergelése után; a 2. lépés ⛔ pontján (a mérés eredménye) a felhasználó dönt"
olvas: [adat/licencek.tsv, adat/datasetek.tsv, adat/SEMA.md, konkordancia/README.md, konkordancia/TAHOT_TAGNT_README.md, konkordancia/KJV_Strongs_Genesis.tsv, konkordancia/KJV_Strongs_Exodus.tsv, konkordancia/KJV_Strongs_Proverbs.tsv, konkordancia/KJV_Strongs_teljes.tsv, konkordancia/ASV_Strongs_Genesis.tsv, konkordancia/ASV_Strongs_Exodus.tsv, konkordancia/ASV_Strongs_Proverbs.tsv, eszkozok/f19_ebible_import.py, eszkozok/f19_ellenorzes.py, eszkozok/karoli_strong/, naplok/F19_hianyok.tsv]
ir: [eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/bemenet.py, eszkozok/karoli_strong/futtat.py, eszkozok/karoli_strong/elopar_kjv.py, eszkozok/karoli_strong/kjv_osszevet.py, eszkozok/f19_ebible_import.py, eszkozok/f19_ellenorzes.py, adat/licencek.tsv, adat/datasetek.tsv, adat/SEMA.md, konkordancia/README.md, konkordancia/TAHOT_TAGNT_README.md, konkordancia/KJV_Strongs_Genesis.tsv, konkordancia/KJV_Strongs_Exodus.tsv, konkordancia/KJV_Strongs_Proverbs.tsv, konkordancia/ASV_Strongs_Genesis.tsv, konkordancia/ASV_Strongs_Exodus.tsv, konkordancia/ASV_Strongs_Proverbs.tsv, naplok/KJV_REGI_KIVEZETES_naplo.md]
fugg: [19, 21, 22]
helyi_gep: nem
---

# Fnn_KJV_REGI_KIVEZETES_BRIEF.md — A régi KJV/ASV fájlok kivezetése

*FELADATOK #nn (a számot a `/befogad` adja) · Modell: sonnet · v1 · 2026.10.04*

## 1. Cél

A `KJV_ASV_Strongs` adatkészlet (studybible.info, 3 könyv: 1Móz, 2Móz, Péld) licence tisztázatlan (`adat/licencek.tsv`; a studybible.info-n nincs licencnyilatkozat, a Strong-címkézés három forrása: Bible Foundation, CrossWire KJV2003, Cross Word Project). A KJV azóta az eBible-ból (`konkordancia/KJV_Strongs_teljes.tsv`, 66 könyv, Public Domain, `kozkincs`) folytatódik; az ASV kiesett (az eBible-ASV címkézése forráshibás, DT19 (b)). **Felhasználói döntés (2026.10.04):** minden az új KJV-forrásra vezetendő át, az ASV kiesik, a régi hat fájl törlődik a repóból.

## 2. Hatókör

**Benne van**
- a `KJV_Strongs_{Genesis,Exodus,Proverbs}.tsv` és az `ASV_Strongs_{Genesis,Exodus,Proverbs}.tsv` törlése (a git-történetben megmaradnak);
- a `eszkozok/karoli_strong/` KJV-támpontja: a `tokenek.KJV_FAJLOK` / `kjv_tamapont()` ág megszüntetése, a `bemenet.py` `kjv_forras` alapértelmezése `'teljes'`, a `'regi'` ág törlése (`futtat.py` 1528. sora körül, az önteszt 2469. sora körül, `elopar_kjv.py` 293. sora, `kjv_osszevet.py`);
- a `f19_ebible_import.py` és a `f19_ellenorzes.py` fejléc-/összevetés-hivatkozásai a régi fájlokra;
- a `licencek.tsv` `KJV_ASV_Strongs` sora és a `datasetek.tsv` négy sora (`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`) kivezetve; a SEMA és a két README hivatkozásai javítva.

**Nincs benne**
- az F19 és F21 brief, valamint a lezárt zárójelentések és az `f21p/` mérési kimenetek szövege (történeti dokumentum, nem szerkesztendő);
- a `adat/karoli_strong/` már kész párosítási kimenetei (nem újragenerálandók);
- az eBible-ASV pótlása vagy bármilyen új ASV-forrás.

## 3. Lépések

**0. Leltár.** `grep -rn "KJV_Strongs_Genesis\|KJV_Strongs_Exodus\|KJV_Strongs_Proverbs\|ASV_Strongs_\|KJV_FAJLOK\|kjv_tamapont(\|'regi'\|KJV_ASV_Strongs"` a kódra, tesztre, adatra és dokumentációra (a `naplok/` és az `f21p/` történeti kimenetei nélkül). A találati lista a napló első szakasza. A régi hat fájl sha256-ja a naplóba kerül (a F21/F22 bizonyítékok azonosításához).

**1. Mérés a törlés előtt (csak olvas).** A `konkordancia/KJV_Strongs_teljes.tsv` a `Karoli_versmegfeleltetes.tsv` KJV-oszlopával (`tokenek.kjv_tamapont_teljes`) adja-e ugyanazt a Strong-halmazt, mint a régi fájl, a 3 könyv minden versére? Verses eltérés-tábla `naplok/KJV_REGI_KIVEZETES_egyezes.tsv` (a tartalmi eltérés a nem egyező versek száma és jellege). A 1. lépés a F19 meglévő mérését (`eszkozok/f19_ellenorzes.py`, `F19_hianyok.tsv`) ismétli, nem helyettesíti.

**2. ⛔ A mérés eredménye.** Ha a nem egyező versek száma > 0, a felhasználó dönt: (a) a törlés mehet, és az F21/F22 mérési kimenetek „régi támpont" eredményei történeti adatként maradnak; (b) a nem egyező versekre javítás kell a `teljes` oldalon. Ha 0 az eltérés, a ⛔ pont nem áll meg. A napló rögzíti, mely F21/F22 futások használták a régi támpontot (a `bemenet.py` alapértelmezése `'regi'`, ezért valószínűleg az 1Móz/2Móz futások; a leltár a futási parancsokból és a kimenetek proveniencia-sorából igazolja vagy cáfolja), mert ezek újrafuttatása a törlés után más támpontot használna.

**3. Kód.** A `'regi'` ág és a `KJV_FAJLOK` eltávolítása; az alapértelmezés `'teljes'`; a `futtat.py` önteszt átírása (a „régi alapértelmezés" ellenőrzések törlése, a `teljes` ág tesztjei maradnak); a `f19_*` szkriptek hivatkozásai javítva. A `python eszkozok/karoli_strong/futtat.py --onteszt` (vagy a meglévő önteszt-belépő) zöld.

**4. Adat és dokumentáció.** A hat fájl törlése (`git rm`); a `licencek.tsv` `KJV_ASV_Strongs` sora és a `datasetek.tsv` négy sora a rend szerint kivezetve (törlés, a megjegyzés a naplóban); a `SEMA.md` és a két README hivatkozásai javítva. A `lexikon_general.py` licenc-konstansához és a `TISZTAZATLAN_SZOTARAK` halmazhoz nem nyúl (N9).

**5. Ellenőrzés.** `python eszkozok/feladatok.py ellenoriz`, a CI-ellenőrzők a változott fájlokra, `grep` a leltár mintáira: nulla találat a kódban és az adatban.

## 4. Elfogadási feltételek

- A hat régi fájl nincs a repóban; a kódban és az adatban nincs hivatkozás rájuk.
- A KJV-támpont egyetlen forrásból jön (`KJV_Strongs_teljes.tsv`); az önteszt zöld.
- A 1. lépés eltérés-táblája a repóban van, és a ⛔ pont eredménye a naplóban.
- A `licencek.tsv` és a `datasetek.tsv` nem hivatkozik a `KJV_ASV_Strongs`-ra.
- Az F21/F22 történeti kimenetei és a briefek változatlanok.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | A régi hat fájl törlése, nem `_nyers/`-be mozgatása | felhasználói döntés (2026.10.04): a studybible.info licence tisztázatlan, az új forrás elegendő | áthelyezés a gitignore-olt `_nyers/` alá |
| D2 | Az ASV kiesik | az eBible-ASV forráshibás (DT19 (b)); a régi ASV-fájlok csak referenciák voltak | új ASV-forrás keresése |
| D3 | A feladat az F22 lezárása után fut | a `futtat.py` mindkét feladat `ir` listáján szerepel; az F22 (és az F21 pilot) futásai alapértelmezésben a régi támponttal készülhettek | párhuzamos futás a futó F22 mellett |
