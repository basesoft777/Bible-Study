# BDB_ARAM_BEEMELES — szárazfutás kivonata (F72, M0)

*Generálta: `python eszkozok/bdb_aram_beemeles.py --m0` · scope=konkordancia/BDB_aram_potlas.tsv + konkordancia/BDB_teljes_unabridged.tsv + konkordancia/BDB_strong_alias.tsv | forras=eszkozok/bdb_aram_beemeles.py --m0 | ts=2026-10-07*

A repó fájljai nem változtak. A jóváhagyás előtt semmi sem íródik élesben.

- Alias-jelölt (mérőszám >= 0,8): **162**; szöveges pótlás: **6** (ebből részleges 0,5–0,8: 5); jelölt marad: 5 (H0004 (cimke_reszleges), H2298 (kizárt: kézzel a BDB9285-höz rendelt (kezi_elfogadott)), H3769 (csonk), H5013 (csonk), H5839 (kizárt: téves testvér: BDB9760 = Azarjá, a H5665 pedig Abed-Negó)).
- Ütközés / hiba: nincs.
- Minden alias-sor testvérkulcsa létezik a fő táblában: igen.
- Az alias-sorok testvére szerepel a #57 elvetett táblájának `testver_strong` oszlopában: 161/162.
- Ahol nem (kézi ellenőrzésre): H3606 -> H3605 (elvetett-tábla testvére: H6903).

## A 6 szöveges pótlás (a fő tábla végére)

- **H1753** (BDB9431, mérőszám 0.73): H1753. dur [דּוּר] verb dwell (see Biblical Hebrew); — Pe`al Imperfect 3 feminine singular of beasts תְּדוּר Dan 4:18 3 masculine plural birds יְדֻרוּן v. Dan 4:9 (Qr feminine יְדוּרָן, f. subject, צִ … *(511 karakter)*
- **H3367** (BDB9591, mérőszám 0.79): H3367. yeqar [יְקָר] noun masculine^Dan 2:6 honour (see Biblical Hebrew); — absolute וִיקָר) Dan 2:6; Dan 7:14 construct id. Dan 4:27, לִיקַר v. Dan 4:33 (K^§ 57. Anm. Str קָר-); emphatic וִיקָרָא Dan … *(232 karakter)*
- **H3848** (BDB9637, mérőszám 0.79): H3848. lebesh [לְבֵשׁ] verb be clothed (see Biblical Hebrew); — Pe`al Imperfect accusative אַרְנְּוָנָא: 3 masculine singular יִלְבַּשׁ. Dan 5:7, 2 masculine singular תִּלְבַּשׁ v Dan 5:16. Haph`el Pe … *(282 karakter)*
- **H6433** (BDB9814, mérőszám 0.07): H6433. pum פֻּם noun masculine^Dan 7:8 mouth (compare Biblical Hebrew פֶּה; on form see K^§ 61, 2) M^§ 76f.); — ׳פ absolute Dan 7:8; Dan 7:20, construct Dan 4:28 +, suffix פֻּמֵּהּ (on form see K^l.c. … *(447 karakter)*
- **H7560** (BDB9910, mérőszám 0.78): H7560. resham רְשַׁם verb inscribe, sign (ᵑ7 Syr.; see Biblical Hebrew (once, late)); — Pe`al Perfect 3 masculine singular ׳ר Dan 6:10 2 masculine singular רְשַׁ֫מְתָּ v. Dan 6:13 רְשַׁ֑מְתָּ v. Dan 6 … *(508 karakter)*
- **H8065** (BDB9965, mérőszám 0.79): H8065. shamayin [שְׁמַ֫יִן] noun masculine plural heavens (Biblical Hebrew [שָׁמַי], שָׁמַיִם, √ שׁמה); — always emphatic שְׁמַיָּא: 1. visible sky Jer 10:11; Dan 4:8; Dan 4:10; Dan 4:17; Dan 4:19; Da … *(884 karakter)*

## Az alias-sorok mintája (első 6 és az elvetett táblában nem szereplő testvérű sor)

| masodlagos_strong | tabla_strong | bdb_id | nyelv | szoveg_hasonlosag |
|---|---|---|---|---|
| H0007 | H0006 | BDB9265 | aram | 0.831 |
| H0069 | H0068 | BDB9268 | aram | 0.848 |
| H0144 | H0143 | BDB9271 | aram | 1.000 |
| H0236 | H0235 | BDB9281 | aram | 0.810 |
| H0399 | H0398 | BDB9297 | aram | 0.826 |
| H0506 | H0505 | BDB9305 | aram | 0.909 |
| H3606 | H3605 | BDB9612 | aram | 0.908 |

Teljes lista: a `--kimenet` mappa `alias_uj_sorok.tsv` fájlja (a repón kívül). Proveniencia-sablon: `scope=konkordancia/BDB_aram_potlas.tsv + konkordancia/BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_aram_beemeles.py --m2 (arami masodlagos Strong; a szocikk szovege mar a heber testversor sorveegen all: ujjlenyomat-meres >= 0,8, eszkozok/bdb_aram_potlas.py --duplikacio modszere; N51, felhasznaloi dontes 2026-10-06) | ts=2026-10-07`
