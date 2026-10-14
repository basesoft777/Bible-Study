# Független ellenőrzés — #76 OLVASOI_KONKORDANCIA, M2b, 4. kör

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`, a kért `opus`-szal egyezik). Fájlíró eszköze nincs; a jelentést az orkesztrátor (Claude Sonnet 5.5) mentette az ellenőr szövege alapján, tömörítve. Tartomány: F76.32–F76.34 (`200d154c..69a88987`); kiemelten a hozzáférési szűrés. A felhasználó kérte ezt a kört. Tesztet nem futtatott, a renderelt DOM-ot nem látta: „nem ellenőrizve — eszköz-korlát”.*

**Eredmény: ELTÉRÉS, 8 tétel; a hozzáférési szűrés és a szintváltó biztonsági pontjai rendben.**

| # | Súly | Tétel | Hely |
|---|---|---|---|
| 3b | közepes | A próba-konfig, a README, a teszt docstringje és a zárónapló az angol forrástáblákat olvasó blokkokat (`szo.thayer`, `tbesg`, `lsj`, `tbesh`, `ubs_dntg`) „saját fordításként” (`forditasok`) írja le és a DT-F86c-re hivatkozik; valójában csak a `szo.bdb_magyar`, `szo.bdb_apparatus`, `szo.magyar_gorog` olvas a `forditasok`-ból. A DT-F86c (`F86_…_BRIEF.md:67`) szerint a BY-SA-eredetű tartalom (UBS_DNTG) nem zárható, a próba mégis zárja. A mechanizmus-próba működik, a leírás téves. | `hozzaferes_proba.toml:4-5`; `README.md:45`; `teszt_szintek.py:7-9`; `zaras.md` |
| 4b | közepes | A magyar-szivárgás teszt tautologikus: az „ablakot” az eredmény alapján választja (`not in lent_t and in fent_t`), majd ugyanezt állítja; részleges szivárgásra nem bukna. | `teszt_szintek.py:168-174` |
| 1h | alacsony–közepes | A `szo.ebben` UBS DBH-tartalma nem követi a `vers.ubs` láthatóságát; az Interlineáris csempék (`fejezet_eredeti`) semmilyen blokk-szűrésen nem mennek át. Ma nem szivárog, de a szűrés kikerülhető. | `blokkok.py:498-549,927`; `oldalak.py:244-250` |
| 1e | alacsony | A `szo.bdb_angol` szinttől függetlenül olvassa a `forditasok`-at (csak `d['en']`-t jeleníti meg); az `alapjelentes` docstringje („tiltott forrást nem olvas”) csak a kiadásra igaz; a blokk forrássora a fordítás-datasetet is listázza. | `blokkok.py:594-605,728-734,932,971` |
| 1f | alacsony | A héber fejléc a `strong_szotar`-ból jön `_latszik('szo.szotar')` nélkül (a görög ág ellenőriz). | `oldalak.py:186` |
| 7b | alacsony | A zárónapló „F76.34–F76.35”-öt ír, egyetlen commit van (F76.34), amely több tételt hozott egyben. | `zaras.md` |
| 5 | alacsony | A zárónapló szerint a pilot `mindNyit` „minden `details`-t” kinyit; a pilot `details:not(.forras):not(.sugo)`. A BDB-re nem számít; a szerver `fejezet-nave` blokkja zárt, a pilot kinyitná. | `sablon.html:1225-1226`; `blokkok.py:316` |
| 9a | alacsony | Az N-F76i (2) első fele elavult (nincs több `expectedFailure`), és két tesztkomment is. | `NYITOTT_FELADATOK.md`; `teszt_olvaso_szerver.py:168`; `teszt_pilot_aranymintaval.py:8` |

**OK (igazolva olvasással/grep-pel):** az alapjelentés, a „BDB magyarul” számláló, a bontott BDB (`kovet` lánc) és a görög fejléc (TBESG) átmegy a `kiadas_kizart` + `hozz.lathato` szűrésen; `/r/szo`, `/r/vers` és a szó-panel ugyanúgy szűr; a `/szint/<nev>` csak `belso` kiadásban él (egyébként 404, a süti és a `?szint=` figyelmen kívül); süti: HttpOnly, SameSite=Lax, Path=/, csak váltáskor, `Cache-Control: no-store`; a szintnév csak a konfig szintjei közül, nincs reflektálás/header-injection/open redirect; a szint a gyorsítótár-kulcs és az ETag része, 304 csak pontos egyezésre; `Vary: Cookie`; az éles konfig mindenki `kutato`, a próba-konfig csak a tesztekben; a „#86 határát nem dönti el” kimondva; a negatív teszt markerei valódi adatok (TBESG `G2316`, `arc, arcok is`); a BDB-ben nincs zárt `details` (kód); K3 és zárónapló rögzíti a felhasználói kérést (2026-10-14) és az M5 ellenőrzési pontot; fejléc rendben; a pilot kódja érintetlen; nincs végleges DT/N szám, DT133 érintetlen; CI-szkript 0 HIBA; `adat/`, `konkordancia/` Δ = 0; ⛔ M5–M7 érintetlen.

**Nem ellenőrizve — eszköz-korlát:** a tesztfutások (68 + 22 + 10, végrehajtói állítás; a 10 tesztmetódus száma egyezik); a renderelt DOM; végrehajtói CI-jelentés összevetése; az E27 elrejtett 32 tétele.
