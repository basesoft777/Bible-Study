---
feladat: 146
cim: Károli↔MT versmegfeleltetés javítása — a Jóel és a KJV-osztályú sorok MT-eltérései (VERSMEGF_MT_JAVITAS)
kod: VERSMEGF_MT_JAVITAS
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: nem_indult
ad: a `Karoli_versmegfeleltetes.tsv` Jóel-sorai helyes MT-megfeleltetést hordoznak (Károli 2:28–32 = MT 3:1–5, Károli 3:1–21 = MT 4:1–21), a KJV-osztályú sorok többi MT≠KJV eltérése mérve és jelentve, a #131 DBH-mérés 12 versének tételes jelentése proveniencia mellett
kovetkezo: "Te: a /kovetkezo-val indítás; első lépés a modell-ellenőrzés, majd a 2. szakasz mérése; ⛔ a javítandó halmaz jóváhagyása"
olvas: [konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_versmegfeleltetes_javitas.tsv, konkordancia/UBS_DBH_referenciak.tsv, konkordancia/Macula_heber_Joel.tsv, konkordancia/TAHOT_kivonat.tsv, eszkozok/lexikon_general.py, naplok/F117_mt_levezet.py, naplok/F117_mt_levezetes.tsv]
ir: [naplok/KAROLI_KK4_tabla_veglegesit.py, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_versmegfeleltetes_javitas.tsv, naplok/VERSMEGF_MT_JAVITAS_naplo.md]
fugg: [117, 131]
---

# VERSMEGF_MT_JAVITAS_BRIEF.md — Károli↔MT versmegfeleltetés javítása

*FELADATOK #146 · Modell: opus · v1 · 2026.10.28 · befogadva a felhasználó jóváhagyásával; a kiváltó megfigyelés a #131 (ág: `ccr-6dc5ac47-lksrko`, `naplok/F131_SZOTARI_GERINC_naplo.md` 5.2).*

## 1. Probléma

A `konkordancia/Karoli_versmegfeleltetes.tsv`-ben a Jóel 2:30–32 és 3:1–5 sora `osztaly=KJV`, `forras=szamlalas`, üres `igehely_mt`.
A fogyasztók (pl. `eszkozok/lexikon_general.py` `karoli_mt_vers`) az üres `igehely_mt`-t azonosságnak veszik.
A masszoréta szövegben viszont a KJV/Károli Jóel 2:28–32 = MT 3:1–5, a KJV/Károli Jóel 3:1–21 = MT 4:1–21.
Tanú: az `UBS_DBH_referenciak.tsv` (MT-számozás) H7121 és H8034 hivatkozása a `Jóel 3:5`-nél áll, a `Jóel 2:32`-nél nincs; az ISTENTISZT-001 lapja ezért „nincs DBH-hivatkozás”-t mutat a Jóel 2:32-re.

A hiba oka a tábla konvenciója (DT207): `KJV` és `KEZI` osztályú sorban az `igehely_mt` üres, tehát ahol az MT ≠ KJV és a tábla `KJV`-nak minősíti, a hiba néma. A Jóel ennek egy esete; más esetek valószínűek (Mal 3:19–24 / 4:1–6, az Ézs 9 az N-F85a szerint stb.).

## 2. Feladat

**2.1 Jóel — javítás.** A Jóel teljes Károli-tartományának `igehely_mt`-je a DT207 (c) módszerével: TAHOT (Károli-kulcs) ↔ Macula héber `ref` oszlop (MT-kulcs), Strong-Jaccard, monoton igazítás; a Macula `karoli` oszlopa tanúként kizárva. Független ellenőrzés: a KJV-pár (`KJV_Strongs_teljes.tsv`) és a szövegolvasás. Osztály a DT208 (c) szerint (`MT`, ha Károli = MT ≠ KJV; `KEZI` kitöltött `igehely_mt`-vel, ha Károli ≠ MT). A javítás **a DT204 (a) szerinti** verziózott bemenetben él (`konkordancia/Karoli_versmegfeleltetes_javitas.tsv`, halmaz-őrrel, `forras` a DT205 szerint); a generált táblát kézzel szerkeszteni tilos. A Jóel 2:28–29 sorát is vizsgáld (a tábla szerint a vers `KJV`, de a 2:28 az MT 3:1).

**2.2 Felmérés — csak jelent.** A tábla minden `KJV` és `KEZI` osztályú sorára (üres `igehely_mt`) ugyanezzel a módszerrel mérd, hol MT ≠ Károli. Kimenet: `naplok/VERSMEGF_MT_JAVITAS_naplo.md` és tételes TSV (könyv, fejezet, vers, mért MT-vers, Jaccard, osztály-javaslat, proveniencia). Ide tartozik az Ézs 9 (N-F85a). **Ezt a halmazt nem javítod**; a 2.1-en kívüli javítás külön döntés.

**2.3 A #131 12 verse — jelentés.** Tételesen, soronként proveniencia-sorral (`scope=… | forras=… | ts=…`, vagy `manual`): a `naplok/F131_dbh_meres.py` által DBH-találat nélkül listázott ÓSZ-versek (Ézs 7:11, 1Móz 4:10, 1Krón 20:6, 20:8, 1Móz 14:19, 14:20, Jób 41:32), és az MT nélküli KEZI-sorok (Préd 9:12, 4Móz 13:34, Jób 38:7, 38:16, 38:30). Mindegyiknél: a táblabeli MT-megfeleltetés helyes-e (Macula `ref` mint tanú); ha igen, a DBH-hiány valódi (a szónak ott nincs DBH-hivatkozása, üres eredmény nem negatív lelet), ha nem, a tábla hibás. Hiányt gyenge anyaggal kitölteni tilos.

## 3. Pontok

- ⛔ **3.1** A 2.2 felmérés után megállás: a javítandó halmaz (a Jóel, és ami a felméréből igazoltan hibás) a felhasználó jóváhagyása után kerül a javító bemenetbe; a nem egyértelmű (Jaccard-kétség, 1-2 / 2-1 lépés, összevonás) sorok tételes lista, nem találgatás.
- **3.2** Halmaz-őr: a javító kulcsokon kívül a tábla egyetlen sora sem változhat (a KK4 kétszeri futása bájtazonos).
- **3.3** Fogyasztók: a `lexikon_general.karoli_mt_vers` a kitöltött `igehely_mt`-t használja (DT209: a `bsb_import` és a `sqlite_epit` az új kombinációra az N-F117a / #120 hatóköre; itt nem javítod, de ha az új sorok a #120 őrét kiváltanák, jelezd). Ellenőrizd: a Jóel 2:32 sora az ISTENTISZT-001 lapján megkapja a `Jóel 3:5` DBH-hivatkozásait (a lap újragenerálása a #131 / a lexikon dolga, itt csak a mérés).
- **3.4** Proveniencia minden lekérdezésből származó állításhoz; TSV olvasása `split('\t')`, írása `'\t'.join()` (nem `csv`); kódot fájlba, nem inline shellbe.
- **3.5** Commit tétel-szintű (`F146.0:`, `F146.1:` …), UTF-8 fájlból; push csak kérésre; merge csak a felhasználótól.

## 4. Kész, ha

1. A Jóel minden Károli-versének `igehely_mt`-je igazoltan helyes, a javító bemenetben, a KK4 újrafuttatása bájtazonos a halmazon kívül.
2. A 2.2 felmérés tételes táblája és összegzése megvan (hány sor, mely könyvek).
3. A 2.3 12 verse mindegyikére van ítélet proveniencia-sorral.
4. A hiányok és a bizonytalan sorok explicit jelölve; új nyitott tétel csak helyőrzővel (`N-F146a` …).
