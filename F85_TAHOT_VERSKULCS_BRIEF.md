---
feladat: 85
cim: "TAHOT_kivonat: versszintű Károli-kulcs a maradék eltérésekre (Jób 40 és a fejezethatár-eltolások)"
kod: TAHOT_VERSKULCS
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: dontesre_var
ag: claude/tahot-verskulcs
ad: "A TAHOT_kivonat.tsv minden ÓSZ-sorának kulcsa a Károli-vers, amelynek a héber szövegét hordozza (Jób 40 és a fejezethatár-eltolások), így a Károli-kulcs szerinti lekérdezés nem ad üres vagy eltolt eredményt; a DT90 mért adattal eldönthető"
kovetkezo: "Te: a független ellenőr az F85.8–F85.10-en (a 4 sort külön vizsgálva), majd az 5–7. tétel engedélye"
fugg: [84]
olvas: [konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/Macula_heber_Job.tsv, f22/versmegfeleltetes.tsv, f22/versmegfeleltetes_kezi.tsv, f22/versosszevonas.tsv, eszkozok/karoli_strong/versbeosztas.py, eszkozok/tahot_karoli_kulcs_generalas.py, eszkozok/tahot_lefedettseg_ellenoriz.py, naplok/F83_Job_versbeosztas_jelentes.md, naplok/F84_jelentes.md, naplok/F22_Job_jelentes.md, adat/SEMA.md]
ir: [eszkozok/tahot_verskulcs_esetlista.py, eszkozok/tahot_verskulcs_finomit.py, naplok/F85_esetlista.tsv, naplok/F85_jelentes.md, naplok/F85_macula_elvetve.tsv, naplok/F85_b_ellenorzes.tsv, naplok/F85_kulcsvaltas.tsv, eszkozok/karoli_strong/tokenek.py, eszkozok/tahot_verskulcs_kivezetes.py, eszkozok/tahot_verskulcs_igazolas.py, naplok/F85_kivezetett_sorok.tsv, naplok/F85_igazolas.tsv, naplok/F85_igazolas.md, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAHOT_TAGNT_README.md, konkordancia/README.md, eszkozok/tahot_karoli_kulcs_generalas.py, eszkozok/tahot_verskulcs_atkulcsolas.py, f22/versmegfeleltetes_kezi.tsv, f22/versmegfeleltetes.tsv, naplok/F22_versbeosztas.md, CLAUDE.md, adat/SEMA.md, NYITOTT_FELADATOK.md, DONTESEK.md, f22/versosszevonas.tsv]
---

# TAHOT_VERSKULCS — a TAHOT_kivonat versszintű Károli-kulcsa a maradék eltérésekre

*Beérkező brief · 2026-10-09 · forrás: a KONZISZTENCIA_20261009 utáni chat-menet (DT90 előkészítése) · a fejléc mezői javaslatok; a végleges számot, fejlécet és a `kizar`/`fugg` viszonyt a `/befogad` adja*

## Mit ad, ha kész

A `konkordancia/TAHOT_kivonat.tsv` minden ÓSZ-sorának kulcsa a Károli-vers, amelynek a héber szövegét hordozza — fejezethatáron és fejezeten belül is. A Károli-kulcs szerinti lekérdezés (`lekerdez.py`, a `jelolt.py`, a #22 bemenete) így nem ad üres vagy eltolt eredményt. A #22 kézi versmegfeleltetésének azok a sorai, amelyek csak a kulcs-eltolást kompenzálták, kivezethetők. Ezzel a DT90 (`OT-full` scope-címke) érdemben eldönthetővé válik.

## Háttér (mérés, 2026-10-09, `main` `6e312832`; ellenőrizendő, nem kimondandó)

- **Jób 40:** a TAHOT kulcsai 40:6–24 (MT-számozás), a Károli versei 40:1–19. Szövegösszevetéssel: a TAHOT 40:6 (`and he answered Yahweh <obj.> Job from a tempest`) = Károli 40:1 („Ekkor szóla az Úr Jóbnak a forgószélből”); a TAHOT 39:34–38 a Károli 39:34–38-cal egyezik. Egyenletes eltolás: TAHOT 40:(n+5) = Károli 40:n, 19 vers. (`CLAUDE.md` „Adat-tár”: maradó korlát; `naplok/F83_Job_versbeosztas_jelentes.md`, N-F41g.)
- **Kulcs-szintű eltérés az egész ÓSZ-ben** (TAHOT-kulcs ↔ `Karoli_1908.tsv`-kulcs): 27 TAHOT-kulcs Károli-vers nélkül 16 fejezetben (2Móz 36:38; 4Móz 30:17; Dán 4:35–37; Hós 2:23, 12:15, 13:16; Jób 17:16, 37:24, 40:20–24; Préd 1:18, 8:16–17, 10:18–20; Péld 12:28; Én 6:11–13; Ézs 8:23, 64:12), és 18 Károli-vers TAHOT-sor nélkül 6 fejezetben (2Móz 35:36; Dán 3:31–33; Hós 14:10; Jób 40:1–5; Préd 9:19–23; Én 5:17–19).
- **Fejezeten belüli eltolás** is van, amelyet a kulcs-összevetés nem lát: a `f22/versmegfeleltetes_kezi.tsv` 97 sora közül Péld 12 (27), Jób 37 (23), Jób 40 (19), Jób 17 (15), Ézs 9 (3), Ézs 64 (1). A teljes kép a versbeosztás-detektorból (`eszkozok/karoli_strong/versbeosztas.py`, `f22/versmegfeleltetes.tsv`) jön, nem a kulcsokból.
- A #22 párosítása (`adat/karoli_strong/parok_*.tsv`) már Károli-kulcsú: a Jób 40 szúrópróbája (40:1 → H6030/H3068/H0347/H5591; 40:6 → H6327/H0639/H5678) helyes. A párosítás-táblák ezért **nem változhatnak** e feladattól.

## Hatókör

**Benne van:** a TAHOT_kivonat azon sorainak átkulcsolása, ahol a kulcs és a tartalom Károli-verse igazoltan eltér (eltolás), a sorok tartalmának változtatása nélkül; a #22 kézi táblájának és detektor-listájának ehhez igazítása; a kulcsgenerátor felülbírálásainak és a dokumentációnak (`CLAUDE.md` TAHOT-mondat, SEMA 4. szakasz kb. 1229. sora, `TAHOT_TAGNT_README.md`, `konkordancia/README.md`) a mért állapotra hozása.

**Nincs benne:** valódi hiány pótlása (ha egy eset nem eltolás, hanem hiányzó szöveg: külön tétel); a `parok_*`/`szavak_*` táblák módosítása; az `OT-full` címke kiadása és a `lekerdez.py` címkéinek változtatása (az a DT90 döntése után külön lépés); a BSB `Számozás` oszlopa (N-F41g).

## Tételek

1. **Esetlista.** Minden eltérő fejezetre (kulcs-szint és a detektor `eltolt`/`nincs_karoli`/`nincs_eredeti` sorai) eset-tábla: `fejezet | TAHOT-kulcs | Károli-vers | típus (eltolás / összevonás / valódi hiány / bizonytalan) | igazolás`. Az igazolás gépi: Strong-halmaz-illeszkedés a Károli-szöveg Strong-kivonatához (`Karoli_Strong_kivonat.tsv`, STEPBible-alak, a `Konyv_normalizalo_tabla.tsv`-vel), ahol van, a WLC-hez (Macula) is; a kézi szövegösszevetés csak megerősítés. Napló: `naplok/<F nn>_esetlista.tsv` + jelentés.
2. **⛔ 1 — megállás a táblaírás előtt.** A felhasználó jóváhagyja az esetlistát: mely esetek kerülnek átkulcsolásra, mi történik a `bizonytalan` és a `valódi hiány` esetekkel, és a 1:2 / 2:1 összevonásoknál (ha vannak) a kulcs formája.
3. **Átkulcsolás.** Szkript (`eszkozok/tahot_verskulcs_atkulcsolas.py`): csak az első oszlop (Igehely) változik a jóváhagyott sorokon; a sorrend Károli-sorrend. Írás előtt összevetés az eredetivel: minden nem érintett sor bájtazonos, az érintett sorok a kulcs kivételével bájtazonosak, a sorszám nem változik. Eltérésnél leáll. TSV-olvasás `split('\t')`, írás `'\t'.join()` (a `csv` modul tilos).
4. **A #22 kézi táblája.** A `f22/versmegfeleltetes_kezi.tsv` azon sorai, amelyek csak az átkulcsolt eltolást kompenzálták, kikerülnek (különben kétszeres eltolás). A detektor újragenerálása (`versbeosztas.py`) után igazolás: a már elkészült könyvekre (`adat/karoli_strong/parok_*.tsv`) a párosítás bemenete (vers → héber szavak) változatlan — ahol nem, ott leáll, és jelent.
5. **Kulcsgenerátor.** A `tahot_karoli_kulcs_generalas.py` felülbírálásai úgy, hogy újrafuttatva ugyanezt a kulcsolást adják (vagy indokolt megjegyzés, ha a generátor ezt nem tudja kifejezni).
6. **Dokumentáció.** `CLAUDE.md` „Adat-tár” TAHOT-mondata (a „maradó korlát” a mért állapotra), SEMA 4. szakasz (a Jób 40:1–5 / Jób 41 „hiányzik” állítás — ma is ott áll, a #52 3. futásának ⛔-ja), `TAHOT_TAGNT_README.md`, `konkordancia/README.md`; N-tételek a `NYITOTT_FELADATOK.md`-ben.
7. **Zárás.** Ellenőrzés: `tahot_lefedettseg_ellenoriz.py` és egy versszintű kulcs-összevetés (Károli-vers ↔ TAHOT-kulcs) a teljes ÓSZ-re, eredménnyel a jelentésben; független ellenőr; a DT90-hez mért adat (a tételt nem zárja le).

## Elfogadási pontok

1. A versszintű kulcs-összevetésben csak a ⛔ 1-ben jóváhagyott kivételek maradnak, mindegyik indokolva.
2. A `TAHOT_kivonat.tsv` sorainak száma és a sorok tartalma (a kulcs kivételével) változatlan; a diff csak az Igehely oszlopot érinti.
3. A `parok_*.tsv` / `szavak_*.tsv` táblák bájtazonosak; a már futott könyvek detektor-bemenete változatlan.
4. A kézi tábla kivezetett sorai listázva, mindegyiknél az átkulcsolt eset hivatkozásával.
5. A dokumentáció (CLAUDE.md, SEMA 4, README-k) a mért állapotot írja; régi állítás nem marad.

## Kapcsolatok

- **#84** (lezárva): a Jób 41 pótlása — ennek a folytatása.
- **#22** (fut, könyvenként): a kézi tábla és a detektor közös; a két feladat egyszerre nem futhat (`kizar`). A Péld még hátra van a #22-ben — a befogadáskor eldöntendő, hogy ez a feladat a Péld-menet előtt vagy után fusson.
- **DT90** (🟡): az `OT-full` címke — e feladat mérése után dönthető érdemben.
- **N-F41g**: a BSB Jób-számozása — nem része, de a mért esetlista bemenete lehet.
