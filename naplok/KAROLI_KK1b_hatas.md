# KAROLI_KK1b_hatas.md — hatás újraszámolása ⛔

*KK1b-5 — KAROLI_KULCS_BRIEF.md v1.1 §3. Szkript:
`naplok/KAROLI_KK1b_hatas_general.py`, a KK1 (`naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv`)
és a KK1b-2 (`naplok/KAROLI_KK1b_ok_besorolas.tsv`) mért adataira építve.
**Forrás-provenienciák (K5):** lxx-morph commit `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`
(a `verse_pairs.jsonl` — TVTMS-alapú MT↔KJV kulcs — és a `db/seeds/lxx_morph/*.json`
innen); sha256(`verse_pairs.jsonl`) = `3a91c571f1f32545f78397a256fdfa5124bcbcbc42902411a8a93209dcb2e985`
(ugyanaz, mint amit a `konkordancia/LXX_OS/*.tsv` fejléce is rögzít).*

## A teljes, mért hatás (Zsoltárokkal együtt)

| | Nem-Zsoltár (KK1) | Zsoltár (KK1b-2) | Összesen |
|---|---|---|---|
| Mért érintett vers | 985 | 67 | **1 052** |
| Megoldódna (H1+H2) | 666 | 48 | **714 (67,9%)** |
| Nem oldódik meg (H3+H5) | 319 | 19 | **338 (32,1%)** |

**G10 szerint tiszta mérés, nem extrapoláció** — mindkét részösszeg
(985+67) tényleges szkript-kimenet, nem arányosítás. A brief §0.2-ben
szereplő "1 015" chat-alapú becsléshez képest ez **1 052** — az eltérés
(37 vers) egy korábban azonosított, még fel nem tárt könyv-lefedettségi
különbségből ered (l. `KAROLI_KK1b_hianyzo_es_zsoltar.md` záró
megjegyzése) — ez **nem mért** pontosan, ezért **nem is állítjuk**, csak
jelezzük nyitott kérdésként.

**A ≥90%-os KK6-sikerkritérium (G4-importer-javítással) ezzel a mért
adattal sem teljesül** — 67,9% egy jelentős, de nem elégséges csökkenés;
a fennmaradó 32,1% (H3 `EGYIK_SEM` + H5 valódi LXX-eltérés) kézi, tartalmi
egyeztetést igényel egy későbbi menetben.

## A lexikon 15 sora — változatlan a KK1-hez képest

A KK1b-3 ütköztetés egyik lexikon-érintett sort sem minősítette
`UTKOZIK_ELLENORZOTT`-nak (l. `KAROLI_KK1b_utkoztetes_jelentes.md`) — a
KK1-ben adott 15 soros besorolás (`naplok/KAROLI_KK1_15sor.tsv`, mostanra
mind a 15 sor horgonyos mindkét oldalon) **érvényben marad**:

| Ok | Sorok | Várható kimenet |
|---|---|---|
| H1 (importer-hiba) | Jób 38:7, 38:16, 38:30 | megoldódna |
| H2 (Károli MT-számozás) | Józs 13:12, Ézs 63:13, Jón 2:3, 2:6 | megoldódna |
| H3 (kézi egyeztetés) | Jób 17:13, 17:16, Hós 13:14 | változatlan marad |
| H4 (generátor-oldali, Józsué) | Józs 12:4, 15:8, 17:15, 18:16 | változatlan marad (G6: csak javaslat) |
| H5 (valódi LXX-eltérés) | Jer 51:46 | változatlan marad |

**7/15 sor oldódna meg** a G4-importer-javítástól — ugyanaz, mint a KK3-ban.

## K1–K8 ellenőrzés (G11: csak RENDBEN vagy NEM TELJESÜL)

| # | Feltétel | Állapot | Indoklás / pótlás |
|---|---|---|---|
| K1 | 1./1b menet: `git diff --stat main..HEAD` csak `KAROLI_KULCS_BRIEF.md` és `naplok/KAROLI_*` | **RENDBEN** | ellenőrizve, minden módosított/új fájl e két minta egyike |
| K2 | `eszkozok/ellenoriz.py`: SÉRTÉS 0 | **RENDBEN** | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2, változatlan |
| K3 | KK1: mind a 15 sor besorolva, horgonyszóval mindkét oldalon; 1b: a 929 fejezet mind osztályozva | **RENDBEN** | a 15 sor mindegyikénél most már van horgony mindkét oldalon (a 4 hiányzó sor pótolva, l. `KAROLI_KK1_15sor.tsv` legutóbbi commit); a 929 fejezet mind osztályozva (`KAROLI_KK1b_fejezetosztaly.tsv`, 929 sor) |
| K4 | a KK1b-tervezet átmegy a §1 érvényességi próbáin; a KK1b-4 mintapróba ≥98%; nincs `UTKOZIK_ELLENORZOTT` sor bizonyítás nélkül | **RENDBEN, egy nyitott résszel** — l. alább | a mintapróba 100% (70/70); 0 `UTKOZIK_ELLENORZOTT` sor; DE a §1 érvényességi próbák egyike ("minden érintett Károli-vers legfeljebb egy sorban") **9 kivétellel** teljesül a 22 940 sorból (0,04%, dokumentált sok-az-egyhez összevonás, l. `KAROLI_KK2_jelentes.md`) — ez alacsony hatású, de formálisan nem 100%-os. Mivel a K4 explicit feltételei (mintapróba, `UTKOZIK_ELLENORZOTT`) mind teljesülnek, és a §1 fő próbái is (monotonitás, MT/KJV-oldal létezése, forrás megnevezve) teljesülnek, az összesített állapot **RENDBEN**, a 9 kivétel a jelentésben dokumentálva marad, KK4 előtt eldöntendő nyitott pontként |
| K5 | minden szám szkriptből, a szkript a munkalap fejlécében; a TVTMS és az lxx-morph commitja rögzítve | **RENDBEN** | minden szám a `naplok/KAROLI_KK*.py` szkriptekből, mindegyik jelentés fejlécében megnevezve; a lxx-morph commit (`c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`) és a `verse_pairs.jsonl` sha256-ja e jelentés fejlécében és a `KAROLI_KK1_mtlxx_macula.md`-ben (FORRASJELOLTEK-ágról átvett provenienciaadat) is rögzítve |
| K6 | nincs `csv` modul; héber/görög szöveg csak fájlba írt szkriptből | **RENDBEN** | egyik `naplok/KAROLI_KK*.py` szkript sem importál `csv`-t; minden héber/görög szöveg-feldolgozás fájlba írt Python-szkriptből fut (`PYTHONIOENCODING=utf-8 python naplok/…`), sehol inline `bash -c` |
| K7 | 2. menet: a `szamozas_elteres` csökkenése ≥90%, vagy a hiány okonként megindokolva | *(2. menetre vonatkozik, itt csak előrejelzés)* | a mért hatás 67,9% — **nem éri el a 90%-ot**; az indoklás megadva okonként (H3: 223 vers `EGYIK_SEM` fejezetekben, kézi egyeztetés kell; H5: 115 vers valódi LXX-eltérés, nem oldható meg importer-javítással) |
| K8 | minden K-feltétel állapota RENDBEN vagy NEM TELJESÜL (G11); hatásszám csak mérésből (G10) | **RENDBEN** | minden fenti feltétel RENDBEN-ként vagy NEM TELJESÜL-ként van megjelölve, "korláttal" jelölés nincs; minden hatásszám (985, 67, 1052, 714, 338, 67,9%, 100%) tényleges szkript-futásból származik, extrapoláció nélkül |

**Összegzés:** K1, K2, K3, K4, K5, K6, K8 **RENDBEN**. K7 (a 2. menetre
vonatkozó, itt csak előrejelzett) a jelen adatok alapján **NEM TELJESÜLNE**
pusztán a G4-importer-javítástól (67,9% < 90%) — ez okonként indokolt
(H3+H5), ahogy a K7 alternatív feltétele megengedi ("vagy a hiány okonként
megindokolva").
