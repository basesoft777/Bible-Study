# F85_zaras.md — #85 TAHOT_VERSKULCS zárójelentés

*2026.10.09 · ág: `claude/tahot-verskulcs` · modell: sonnet (`vegrehajto-sonnet`) · jelentés: `naplok/F85_jelentes.md` · ellenőrzés: `naplok/ELLENOR_F85*.md` (6 kör, záró: `ELLENOR_F85_zaro.md`)*

**Eredmény.** A `TAHOT_kivonat.tsv` Igehely-kulcsa 337 versen (6330 sor) Károli-kulcsra váltott (328 eltolás + 9 összevonás-kulcs; 2Móz 38, 4Móz 17, Jób 59, Péld 28, Préd 66, Én 13, Ézs 31, Dán 37, Hós 48). Soronkénti napló: `naplok/F85_kulcsvaltas.tsv`. A sorszám (469 301) és az Igehely mezőn kívüli tartalom bájtazonos; a fájlsorrend nem változott (a 4Móz 29:39 + 30:1 és Hós 11:11 + 12:1 pár a fájl áthelyezett blokkja miatt nem szomszédos).

**Kulcs-összevetés (ÓSZ).** Károli-vers nélküli TAHOT-kulcs 0, TAHOT-sor nélküli ÓSZ-Károli-vers 0 (23 204 kulcs); 9 közös kulcs két-két TAHOT-verssel (`f22/versosszevonas.tsv`). Napló: `naplok/F85_kulcsosszevetes.md`.

**Döntések** (felhasználó, chat, 2026.10.09): DT-F85a — mind a 337 vers; a 3 egykori hiány-sor tárgytalan (összevonás); a 4 bizonytalan sor azonos kulcson; a 17 összevonásnál közös Károli-kulcs; az 5–7. tétel külön engedéllyel.

**Kimenet.** `f22/`: a kézi tábla 97 és az összevonás-fájl 7 kompenzáló sora kivezetve (a `versosszevonas.tsv` új `er_tol`/`er_ig` oszloppal 9 sor), a detektor-lista 290 → 12 (ÚSZ). `tokenek.py`: összevonás-kezelés az új kulcsokon; `versbeosztas.py` önteszt; generátor-őr (`--felulir-atkulcsolt`). Dokumentáció: CLAUDE.md TAHOT-mondat, SEMA 4, README-k.

**Igazolás.** 17 747 vers bemenete és 19 táblapár (`parok_*`/`szavak_*`) reprodukálása bájtazonos; 5 könyvnél (2Móz, 4Móz, Ézs, Jób, Péld) csak a proveniencia-sor tér el (elfogadva). `adat/karoli_strong` az `origin/main`-nel azonos.

**Nyitott.** N-F85a (Karoli_versmegfeleltetes Ézs 9 MT-oszlop), N-F85b (Macula `karoli`), N-F85c (ALVIL-001 három régi kulcsú sora), N-F85e (generátor nyers bemenetei), N-F85f (más TAHOT-kulcsú táblák). **A záró ellenőr 3 eltérése nyitva marad:** (1) a DT90 szövege hamis premisszát hordoz (a felhasználó döntése); (2) elavult „maradó korlát” állítások az `ADATVAGYON_TERV.md:766`, `ATALAKITASI_TERV.md.md:845`, `NYITOTT_FELADATOK.md:590/592` sorban; (3) `F85_kivezetett_sorok.tsv:7` hivatkozás hiánya. Az `OT-full` címke (DT90) a felhasználó döntése.
