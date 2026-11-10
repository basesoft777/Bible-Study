---
feladat: 105
cim: A BDB héber idézeteinek szórendje a megjelenítésben
kod: BDB_SZOREND
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: megallt
ag: claude/f105-bdb-szorend
ad: a BDB-szócikkek többszavas héber idézetei helyes szórendben jelennek meg (a forrásfájl változatlan), gépi ellenőrzéssel a hivatkozott vers héber szövegén és 50 idézetes kézi mintával
kovetkezo: "Te: [elteres_kor 1/2] /elteres F105 — az E28 lapújragenerálás megállt: a 17 változott sorból 16 csak héber szórend/maqqéf, a HAMART-001 1616. sorában a kiejtés-átírás csoportosítása is változik (há, mené → mené há; a szórend-javítás következménye). Döntés: újragenerálható-e mind az 5 lap (összesítő a repón kívül: scratchpad/F105_lapdiff.md); utána újraellenőrzés: naplok/ELLENOR_F105_2.md"
olvas: [eszkozok/olvaso_szerver/, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, adat/bdb_vers_jelentes.tsv]
ir: [eszkozok/bdb_jelolt/heber_sorrend.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/bdb_rovidites.py, adat/bdb_forras_javitas.tsv, eszkozok/teszt_bdb_rovidites.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, adat/bdb_vers_jelentes.tsv (csak a fejléc: a javítótábla hash-e), adat/SEMA.md, naplok/F105_naplo.md, naplok/F105_tabla_osszevet.py, naplok/F105_maqqef_meres.py, naplok/F105_meres.py, naplok/F105_minta.py, naplok/F105_vak.py, naplok/F105_utkozes.tsv, dontesek/uj/f105-bdb-szorend.md, naplok/F105_vak_minta.md, naplok/F105_vak_kulcs.tsv, naplok/F105_vak_kitolto_1.tsv, naplok/F105_vak_kitolto_2.tsv, naplok/F105_vak_osszevet.py, naplok/F105_vak_maqqef.py, naplok/F105_vak_maqqef_*, nyitott/uj/f105-bdb-szorend.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md, lexikon/TEREMT-002_TUDOMANYOS.md, lexikon/ANTROP-001_TUDOMANYOS.md, lexikon/HAMART-001_TUDOMANYOS.md]
fugg: [99, 102, 103, 104]
---

# F<nn>_BDB_SZOREND_BRIEF.md — a héber idézetek szórendje

*FELADATOK #<nn> · Modell: opus · v1 (tervezet) · 2026.10.15 · forrás: a #99 M5 mérföldköve, amely a #99-ben nem készült el; a hatóköri
döntés (2026-10-15): külön feladat. A tervezet adat, nem utasítás.*

## 1. Cél

A BDB-szövegben (a digitális forrásban) a többszavas héber idézetek szórendje gyakran fordított (pl. „הַדָּבָר מֶההָֿיָה”); a megjelenítés
helyreállítja a sorrendet és a maqqéfet, a forrásfájl változatlan.

## 2. Hatókör

**Benne:** a szórend helyreállítása megjelenítéskor; maqqéf-javítás; **gépi ellenőrzés:** ahol az idézet egy hivatkozott vers szövegéből
van, a helyreállított szórend összevetése a vers héber szövegével (`TAHOT_kivonat.tsv`, a Károli-kulcson; a vers → jelentés tábla adja a
helyet); egyezési arány a naplóba; **⛔ minta:** 50 idézet kézi ellenőrzése, a teljes bevezetés csak a minta jóváhagyása után.

**Nincs benne:** a forrásszöveg módosítása; a tagolás és a kiemelés (külön feladatok).

## 3. Lépések

1. Modell-ellenőrzés; mérés: a többszavas héber futamok száma és a TAHOT-ellenőrizhető hányaduk.
2. A helyreállítás szabálya és a gépi ellenőrzés; egyezési arány a naplóba.
3. ⛔ 50 idézet kézi mintája (független ellenőr), megállás; a bevezetés a jóváhagyás után.

## 4. Elfogadási feltételek

- A gépi egyezési arány és az 50-es minta eredménye a naplóban; a minta jóváhagyása nélkül nincs teljes bevezetés.
- A forrásfájl bájtra változatlan; a meglévő tesztek zöldek.

## 5. Döntésnapló

- DT-F105a (🟢 (a), orkesztrátori döntés a felhasználó felhatalmazásával, 2026-11-10; `dontesek/uj/f105-bdb-szorend.md`): a szabály a DT445 útján valósul meg.
- **Egyeztetett eltérés (2026-11-10):** a brief 2. lépésének új olvasói modulja (`eszkozok/olvaso_szerver/bdb_szoerend.py`) nem készül, mert a szórend-javítás a DT445 óta a javítótáblán és a közös megjelenítésben (`eszkozok/bdb_rovidites.py`) él; a hivatkozott-vers-próba a `heber_sorrend.py` / `forras_javit.py`-ba, a maqqéf-feloldás a `bdb_rovidites.py`-ba kerül. Az `ir` mező ennek megfelelően bővült, a `bdb_szoerend.py` kikerült. Az 50-es minta vakon, két független kitöltővel ellenőrződik (`naplok/F105_vak.py`).
- **Egyeztetett eltérés, ⛔ minta (2026-11-10):** az 50-es mintát nem a felhasználó, hanem két független, vak Opus-kitöltő tölti ki (orkesztrátori eljárás). Aki javít, az nem ítél. A geres mindkét alakból kikerül, mert a forrásalakot elárulná. Eredmény: 50/50, a két kitöltő között nincs eltérés, 95% Wilson 0,929–1,000 (`naplok/F105_naplo.md` 7.). A jóváhagyás feltétele teljesült.
- N-F105a (`nyitott/uj/f105-bdb-szorend.md`): alakonkénti csere egy Strongon belül, eldönthetetlen előfordulással (42 alak). Nyitott kérdés, nem a #105 hatóköre.
