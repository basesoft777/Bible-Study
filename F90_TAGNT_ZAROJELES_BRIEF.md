---
feladat: 90
kod: F90
cim: "A TAGNT-kivonat KJV- ([..]) és egyéb ({..}) versszámozású sorainak pótlása (48 csoport, 350 szó-sor)"
tipus: feladat
fazis: 1
modell: opus
allapot: megallt
ag: claude/f90-tagnt-zarojeles
ad: "Teljes `konkordancia/TAGNT_kivonat.tsv`: a nyers TAGNT minden szó-sora benne van, a [..]/{..} jelölésűek is, Károli-kulccsal; a 48 csoport Károli-döntése naplózva"
kovetkezo: "Te: a nyers TAGNT letöltésének engedélye és módja (DT-F90a). A nyers fájl a repóban és a gépen sincs meg (a F22.9 klónja a session scratchpadjével elveszett), az 1. lépés (rögzítés, eltérés-mérés) enélkül nem futhat; utána: 1. lépés mérése, majd ⛔ a Károli-döntési tábla jóváhagyása"
fugg: []
nem_fugg: [22, 38, 48]
olvas: [konkordancia/TAHOT_TAGNT_README.md, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, naplok/F22_TAGNT_zarojeles_sorok.md, NYITOTT_FELADATOK.md, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/sorrend_ellenoriz.py, F22_KAROLI_STRONG_BRIEF.md]
ir: [konkordancia/TAGNT_kivonat.tsv, konkordancia/TAHOT_TAGNT_README.md, eszkozok/tagnt_zarojeles_potlas.py, naplok/F90_jelentes.md, naplok/F90_karoli_dontesek.tsv, eszkozok/karoli_strong/sorrend_ellenoriz.py, NYITOTT_FELADATOK.md]
---

# A TAGNT-kivonat zárójeles sorainak pótlása

*Tervezet a /befogad-hoz (2026.10.12, a F22.9 ÚSZ-menet közben; a felhasználó döntése: külön feladat, most nem indul). Alap: N-F22c és N-F22d (`NYITOTT_FELADATOK.md`), a lelet: `naplok/F22_TAGNT_zarojeles_sorok.md`.*

## A tárgy

A nyers TAGNT (STEPBible-Data, `Translators Amalgamated OT+NT/TAGNT Mat-Jhn …`, `TAGNT Act-Rev …`) a versszámozás-eltérést a hivatkozás-mezőben jelöli. A fájl fejléce: *„Reference: Versification as used by NRSV. Differences are marked in square brackets for KJV, bround brackets for NA and curley brackets for others.”* A `konkordancia/TAGNT_kivonat.tsv` generátorának regexe (`konkordancia/TAHOT_TAGNT_README.md`, „Zárójeles kettős hivatkozás” szakasz) csak a kerek zárójelet (NA) ismeri; a **szögletes (KJV) és a kapcsos (egyéb) jelölésű szó-sorok kimaradtak.**

A F22.9 vizsgálata (2026.10.12, nyers fájl: `STEPBible-Data/aca7d691414e`, 2026.10.10): **48 csoport, 350 szó-sor.**

- **9 teljes vers** hiányzik a kivonatból: 2Kor 13:13 (`2Co.13.13[13.14]`), 3Ján 1:15 (`3Jn.1.15[1.14]`), Fil 1:16–17 (`Php.1.16[1.17]`, `Php.1.17[1.16]`), Jel 12:18 (`Rev.12.18[13.1]`), Ján 7:53 (`Jhn.7.53{8.1}`), Róm 16:25–27 (`Rom.16.25{14.24}` – `Rom.16.27{14.26}`).
- **39 vers részleges**: a kulcs megvan, de a vers szavainak egy része hiányzik (pl. `2Co.13.12[13.13]`: „Ἀσπάζονται ὑμᾶς οἱ ἅγιοι πάντες”, 5 szó).

A teljes lista: `naplok/F22_TAGNT_zarojeles_sorok.md`.

## Érintett

1. **A kivonat-generátor regexe.** A generátor a repóban nem található: a README leírja, de egyetlen `eszkozok/` szkript sem írja a `TAGNT_kivonat.tsv`-t. Ellenőrizendő, hogy van-e máshol, és ha nincs, akkor a javítás egy reprodukálható pótló szkript (`[javaslat: eszkozok/tagnt_zarojeles_potlas.py]`). A szkript a nyers fájl `[..]`/`{..}` sorait a meglévő kivonat mezőképzésével (README, „TAGNT_kivonat.tsv” oszlopok) állítja elő, és Károli-kulccsal illeszti be. Ugyanez a szűk regex él az `eszkozok/karoli_strong/sorrend_ellenoriz.py`-ban is (`SOR = …(?:\((\d+)\.(\d+)\))?#…`), azt is bővíteni kell.
2. **A README zárójeles szakasza.** Most úgy írja, hogy a zárójeles jelenség „négy helyen” fordul elő, és csak NA-eltérés. Bővíteni kell a `[..]` (KJV) és `{..}` (egyéb) jelöléssel, a 48 csoport számával és a Károli-döntés szabályával.
3. **A KJV/NRSV → Károli versmegfeleltetés.** A Károli hol a KJV-, hol az NRSV-számozást követi. Erre két példa van, mindkettő a csoportlista alapján:
   - a 3Ján 1:15 és a Jel 12:18 a Károliban önálló vers;
   - a Fil 1:16–17 a Károliban KJV-sorrendű.
   
   Ezért a kulcsot **csoportonként kell eldönteni** a Károli szövegének összevetésével, ahogy a README 4 NA-esetére (`KAROLI_DONTES`) és a TAHOT F85-átkulcsolására történt. A döntések naplója: `[javaslat: naplok/F<nn>_karoli_dontesek.tsv]` (nyers hivatkozás, Károli-kulcs, indok).

## Lépések

1. A nyers fájl rögzítése: commit-azonosító, és a 2026.08.24-i letöltéssel való eltérés mérése (a kivonat abból készült). Ha a két nyers változat a 48 csoporton kívül is eltér, ⛔ megállás, és jelentés.
2. A 48 csoport Károli-kulcsának döntése (értelmező lépés, szövegösszevetés). ⛔ A döntési táblát a felhasználó hagyja jóvá.
3. A pótlás: szkripttel, a kivonat meglévő sorainak bájtazonos megtartásával. Csak sor beszúrása történik; a sorrend a README szerinti kulcs-sorrend.
4. Igazolás:
   - a kulcs-összevetés újrafuttatása: a 9 csak-Károli kulcs megszűnik, a részleges versek szószáma kiegészül;
   - a `tokenek.py` `[nem TR]` és sorszám-logikája változatlanul fut;
   - az F22 eredeti nélküli listája (`eszkozok/karoli_strong/eredeti_nelkuli_lista.py`) újragenerálva.
5. README- és NYITOTT-frissítés. Az N-F22c és az N-F22d lezárása vagy pontosítása.

## Kész, ha

- **K1:** a nyers TAGNT minden szó-sora (a `[..]`/`{..}` jelölésűek is) a kivonatban van, Károli-kulccsal; a 350 sor beszúrása szkriptből, újrafuttatható.
- **K2:** a kivonat meglévő sorai bájtazonosak.
- **K3:** a Károli-döntési tábla jóváhagyva, minden csoporthoz indokkal.
- **K4:** a README zárójeles szakasza és a `sorrend_ellenoriz.py` regexe frissítve.
- **K5:** független ellenőr TISZTA, CI zöld.

## Mi nincs benne

- **Az érintett, már párosított F22-versek újrapárosítása.** A A csomag és a B (Gal, Ef, Zsid) érintett verseit a F22.9 `kezi`/`fuggoben` állapotba tette. Az újrapárosításuk és a 2Kor futtatása a F22 brief dolga, e feladat után.
- **A Károli-dataset versösszevonásai** (Róm 3:30–31, Róm 8:38–39, 1Kor 3:22–23). Ez külön jelenség, a nyers TAGNT-ben mind a hat vers megvan, ezért ez a F22 `versosszevonas.tsv`-ének tárgya.
- **Az ÓSZ (TAHOT):** a zárójeles sorait az F85 már kezelte.
