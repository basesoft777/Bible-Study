# ELLENOR_F91 — F91_ZSOLT_FELIRAT_SZAMOZAS_BRIEF.md · 25e39a1a..3c3779b8 (F91.0–F91.12)

*A független ellenőr (`fuggetlen-ellenor`, tényleges modell: `claude-opus-5-5`, kért: `opus`, egyezik) jelentése; a fájlba az orkesztrátor írta ki, mert az ellenőr nem kapott Write eszközt. Az ellenőr az ág saját változásait a merge-base-től (`25e39a1a`) vette; az `origin/main` közben az F95 merge-dzsel előrébb jár.*

**Eredmény: ELTÉRÉS, 6 tétel.** Nem ellenőrizhető (az ellenőr parancsköre nem engedte): a `teszt_sqlite_epit.py`, az `ellenoriz.py`, a KK4-generátor ideiglenes kimenetre futtatása, az f92 várt számai új építésen.

## Eltérések súlyossági sorrendben

1. **E1 (magas): reprodukálhatóság, körkörös függés.** Az A-tábla generátora (`KAROLI_KK4_tabla_veglegesit.py` → `f91_versmegf_javit.py:58`) az LXX_OS-ből olvas. Az LXX_OS generátora (`eszkozok/lxx_os_import.py:464–477, 573–593, 1312`) viszont az A-táblából veszi a felirat-kulcsot (`tk = tabla.get(ig)`, `:573`), és a `zsolt_felirat_eltolas` szabály (`:584–593`) csak akkor tüzel, ha az A-tábla felirat-sorának van KJV-értéke. Az A1 után ez üres, tehát az LXX_OS újragenerálásakor a felirat-szabály nem tüzelhet (valószínűleg `sorrend_beagyazas`, `:603`; ez kódolvasásból következtetés, nem futtatás). Ekkor a builder és az `f92` `zsolt_felirat_eltolas`-szűrése néma marad, és az etalon maga is változik. Az M0b nem vizsgálta, napló nem rögzíti. Merge előtt döntést kíván.
2. **E2 (közepes): hiányos builder-szűrés.** A `zsolt_felirat_eltolas` jelölés 66 Károli-verset fed le (58 zsoltár `:1` + Zsolt 51/52/54/60 `:1–2`; mind valóban felirat-vers, nem felirat sort nem zár ki). A 67. felirat-vers, a **Zsolt 13:1** (A-tábla: `felirat`) az LXX_OS-ben `karoli_ok` üres, `igehely_kjv=13:1` (`psalms-lxx.tsv:2070`), ezért a térképsor (`LXX_versificacios_terkep.tsv:3691`) a 13:1 felirat-versre is ráteszi a `terkep_ertek`-et. Az `f92_db_igazolas.py` ellenőrzése ugyanígy vak rá.
3. **E3 (közepes-alacsony): a brief `ir` mezője** nem fedi 8 módosított fájlt: `NYITOTT_FELADATOK.md`, `adat/SEMA.md`, `eszkozok/sqlite_epit.py`, `eszkozok/teszt_sqlite_epit.py`, `eszkozok/f92_db_igazolas.py`, `eszkozok/zsolt_felirat_felmeres.py`, `eszkozok/olvaso_pilot/README.md`, `eszkozok/olvaso_pilot/felmeres.py`.
4. **E4 (alacsony): a DT143 sor** 7 cellás a 8 oszlopos `DONTESEK.md` táblában (a Javaslat cellában `🟡`, a Napló cella hiányzik).
5. **E5 (alacsony): az N-F91a szövege elavult**: a B3-at (átnevezés) még teendőként írja, pedig az F91.12 elvégezte; hiányzik belőle, amit a DT142 rendelt hozzá (Zsolt 1 → Psa 151, Zsolt 37 dupla sor, hiányzó Zsolt 2 és 148–150 sorok) és az M2c §2 mérése (203 Károli-vers nélküli KJV-kulcs).
6. **E6 (alacsony): `ZSOLT_FELIRAT_SZAMOZAS_M2a.md:20`** (§1) még a Zsolt 13:6 `;`-os alakját mondja, a §6 (DT144) és a tábla ezt felülírta; a mondat nincs elavultként jelölve.

## Rendben (ellenőrizve)

- Elfogadás 1: a felmérés proveniencia-sorral (`M0.md:13`).
- Elfogadás 2: Zsolt 22 — a 22:2–22:32 mind a 31 versen az A-tábla = LXX_OS `igehely_kjv` (v−1); a 22:1 (felirat) a DT142 szerint üres, nem összevetés. Hatókör: a „0 eltérés” a v > d versekre áll.
- DT142: csak `Zsolt` sorok és 1 jegyzetsor változott, pontosan 63 fejezet, 1055 sor (`lxx_os_etalon_f91`), 67 felirat-sor; a Nave nem változott. B3: a térképben csak a fejléc (`KJV_igehely`) változott, Δ = 0.
- DT144: Zsolt 13:6 = `13:5` + megjegyzés; `;` 0 sorban; N-F91b felvéve. Hatókör: a nem `Zsolt` sorok és a nem fejléc sorok bájtra azonosak.
- DT-szám/E26: csak helyőrzők; commit-üzenetek `F91.n:` előtaggal; E2–E16, E19, E20, E26, E12–E15 0 találat; E25 (3) és E27 (34) nem F91-es.
- Pilot kód: az `olvaso_pilot/` alatt csak 2 egysoros szövegcsere (README, `felmeres.py` leíró sztring), olvasó logika nem változott.
- TSV-sorszám Δ = 0 mindkét táblán, bontási napló nem kell (<10).
- A brief ⛔-pontjain a menet megállt (M1, N2).
- A „0 Macula-sor” (M2b) és a `pardes.db`-ben mért 1 344 `terkep_ertek`-változás ideiglenes építésekre áll, a repó `pardes.db`-jére nem.

## Teendők

- Futtatandó a hívónak: `python eszkozok/teszt_sqlite_epit.py`; `python eszkozok/ellenoriz.py`; a KK4-generátor `KK4_KIMENET=<temp>`-mel, bájt-összevetés; az f92 várt számai új építésen (merge után).
