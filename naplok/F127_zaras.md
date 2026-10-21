# LEXIKON_HALO_RES zárójelentés (FELADATOK #127; ág: `claude/lexikon-halo-res`)

**Elkészült:** két új rés (`alkalmazas`, `tanitoi`; DT-F127a) a 8 lexikonoldalon „6/b.” szakaszként, `res_forras.tsv` 56 → 72; motívumközi jelölt-út (DT-F127b, d): `jeloltek.tsv` kulcsbővítés (627 → 634), új `motivum_kapcsolatok.tsv` (3 sor, DT-F127e), generált „5/b. Kapcsolódó motívumok” blokk (DT-F127f). Bontás: `naplok/F127_bontas.md`.

**Ellenőrzés:** `naplok/ELLENOR_F127.md` ELTÉRÉS 5 → 1. kör (F127.19–25) → `ELLENOR_F127_2.md` ELTÉRÉS 2 → 2. kör (F127.26–30) → `ELLENOR_F127_3.md` ELTÉRÉS 2 (alacsony súlyú; a zárást ezekkel a felhasználó hagyta jóvá).

**Bizonyíték:** a generátor nulla-diffjére és a tesztekre **egyedül a végrehajtó saját futása** a bizonyíték (az ellenőr ezeket nem futtathatja): `f127_res_eles.py --kimenet` 8/8 lap bájtra azonos; `general.py --cel lexikon --id ISTENTISZT-001` azonos; a törzscikkben nincs 5/b./6/b.; `ellenoriz.py`, `feladatok.py ellenoriz`, `futtat.py` (`[ELLENŐRZŐ]` PR-címmel) exit 0; 9 érintett teszt exit 0.

**Eltérések (brief 7. szakasz):**
- `eszkozok/torzscikk_general.py` módosítása (DT-F127c); a hat eszköz (`jelolt`, `nem_vizsgalt`, `betolt`, `karoli_ellenorzes`, `ellenorzes/szabalyok`, `sqlite_epit`) `ir`-bővítése (DT-F127d);
- az F127.9 azonosító kétszer (`7e35612c`, `120f2cef`); az `eszkozok/olvaso_mockup/kinyer.py` szűretlen (DT-F127d (b));
- N-F127a (a tanítói és az `alkalmazas` rés belső utalásai) és N-F127b (az E18/K3.2 fájlra nem illeszkedő `olvas`-minta) nyitva;
- az ELLENOR_F127_3 két maradéka: elavult `kovetkezo` (F127.30 rendezte); az F127.27/28 ELLENOR-hivatkozása a jóváhagyó üzenet 1/2/3 tagolását követi.

**Tesztek:** a `teszt_nem_vizsgalt.py` `teszt_lelet` a base-en (`9d602794`) is piros. A `teszt_olvaso_szerver` és a `teszt_pilot_aranymintaval` (`teszt_futtat.py`, WSL `pardes.db`) **ellenőrizetlen**: a régi adatbázist olvasták, az ág viszont a sémát módosította.

**Merge-feltétel:** a `pardes.db` helyi újraépítése (nem a /mnt/c-ről), majd `python eszkozok/teszt_futtat.py` újrafuttatása a merge előtt.
