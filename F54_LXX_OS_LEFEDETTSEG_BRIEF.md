---
feladat: 54
cim: Az LXX_OS lefedetlen versei — valódi görög hiány vagy versszámozási rés
kod: LXX_OS_LEFEDETTSEG
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: az 503 Károli-vers mindegyikéről (az lxx-hid az LXX_OS-ből n=0-t ad, a régi LXX_kivonat adott) dokumentált ítélet: kulcsolási rés (pótolva az lxx_os_import.py besorolásában) vagy valódi görög hiány (explicit üres eredmény); idegen vagy kettős Károli-kulcs nem keletkezik
kovetkezo: /kovetkezo; ⛔ az M0 felmérés után
olvas: ["konkordancia/LXX_OS/*.tsv", konkordancia/LXX_OS/README.md, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/Karoli_1908.tsv, konkordancia/Verzifikacios_elteres_tabla.tsv, naplok/FORRASKIVEZETES_M5_M7.md, naplok/FORRASKIVEZETES_M5_eltereslista.tsv, eszkozok/lekerdez.py]
ir: [eszkozok/lxx_os_import.py, "konkordancia/LXX_OS/*.tsv", konkordancia/LXX_OS/README.md, eszkozok/teszt_lekerdez_sir.py]
fugg: [42]
---

# F54_LXX_OS_LEFEDETTSEG_BRIEF.md — Az LXX_OS lefedetlen versei

*FELADATOK #54 · Modell: sonnet · v1 · 2026.10.05 · forrás: a #42 (FORRASKIVEZETES, PR #176) nyitott tétele, `naplok/FORRASKIVEZETES_M5_M7.md` (f3)*

## 1. Cél

A #42 kivezette a régi `LXX_kivonat`-ot; a CLAUDE.md 6. kutatási lépése (`lekerdez.py lxx-hid`) azóta az `LXX_OS`-ből olvas. Az átállás eltéréslistája (`naplok/FORRASKIVEZETES_M5_eltereslista.tsv`, `kategoria = csak_regi_vers`) szerint **503 Károli-versre** a régi forrás adott LXX-szöveget, az új n=0-t ad:

| Könyv | db | Könyv | db |
|---|---|---|---|
| Jób | 78 | 1Sám | 34 |
| Zsolt | 66 | Dán | 30 |
| Jer | 59 | Én | 28 |
| Hós | 57 | Józs | 27 |
| Péld | 50 | Ézs | 24 |
| 2Móz | 46 | Jón 2, 4Móz 1, 1Kir 1 | 4 |

A feladat minden versről eldönti és dokumentálja, melyik esetbe tartozik, és a kulcsolási réseket pótolja.

**Előfelmérés (a befogadáskor, `manual`, nem lekerdez.py-kimenet; ts=2026-10-05):** a rések nagy része **nem görög hiány**. Több esetben egész fejezet hiányzik (Jób 17, 37, 38; Hós 2, 11, 13, 14; Péld 12, 18; 2Móz 35; 1Sám 17; Ézs 56; Jer 33, 48), és az `LXX_OS`-ben ezekhez **megvan a görög szöveg**, csak üres a Károli-kulcs, `karoli_ok = szamozas_elteres` jelöléssel. Ellenőrizve:
- `job-lxx.tsv` „Job (LXX) 17:” 176 szó, mind `szamozas_elteres`;
- `hosea.tsv` „Hosea 11:” 219 szó, ugyanígy;
- `proverbs.tsv` „Proverbs 12:” 301 szó;
- `exodus.tsv` „Exodus 35:” 553 szó.

A zsoltároknál a rés zsoltáronként egy vers (66 zsoltár, egyenként 1, illetve az 51., 52. és 60. zsoltárban 2). Ez feliratszámozási eltolódásra utal, nem hiányra. A hipotézist az M0 igazolja vagy cáfolja; a brief nem feltételezi az eredményt.

## 2. Hatókör

**Benne van:**
- az 503 vers osztályozása (M0);
- a kulcsolási rések pótlása az `lxx_os_import.py` besorolási logikájában, offline (`--ujrabesorol`), letöltés nélkül (M1);
- a `konkordancia/LXX_OS/*.tsv` újragenerálása és a README frissítése;
- a `teszt_lekerdez_sir.py` rögzített számainak frissítése, ha az M1 megváltoztatja őket.

**Nincs benne:**
- a 256 `csak_uj_vers` és a `strong_eltero` / `nagy_eltero` kategóriák (Strong-konvenció). Ezeket csak akkor kell érinteni, ha az M1 javítása mellékesen megváltoztatja őket; ekkor a jelentés felsorolja;
- a régi, eltolt zsoltár-kivonatra épülő állítások tartalmi újraellenőrzése (ez a #55);
- lexikonoldal- vagy törzscikk-render (ez a #36);
- új adatforrás letöltése vagy importja.

## 3. Lépések

### M0 — Osztályozás (csak olvas) és ⛔

Jelentés: `naplok/LXX_OS_LEFEDETTSEG_M0.md`, és versenkénti tábla: `naplok/LXX_OS_LEFEDETTSEG_osztalyozas.tsv`.

Mind az 503 versre (a lista az eltéréslistából, `kategoria = csak_regi_vers`):

1. **A osztály — kulcsolási rés:** a görög vers megvan az `LXX_OS`-ben, de nincs Károli-kulcsa (vagy rossz versre kulcsolt). Rögzítendő: az LXX-igehely, a `karoli_ok` értéke, és a javasolt Károli-kulcs forrása:
   - a `Karoli_versmegfeleltetes.tsv` sora (`osztaly`: KJV / MT / KEZI);
   - a `Verzifikacios_elteres_tabla.tsv`;
   - a `karoli_fejezet_dontes.tsv` vagy a `karoli_vers_felulbiralas.tsv`.

   Ha egyik tábla sem ad kulcsot, az ok is rögzítendő.
2. **B osztály — valódi görög hiány:** az LXX-szöveg ezt a verset nem tartalmazza (pl. az LXX rövidebb Jób- és Jeremiás-szövegében). A bizonyíték: az `LXX_OS` szomszédos versei és a vers tartalmának hiánya.
3. **C osztály — a régi kivonat volt hibás:** a régi forrás olyan szöveget adott, amely nem ehhez a vershez tartozik (pl. eltolódás, kiegészítő forrásból töltött sor). A bizonyíték: a régi Strong-halmaz (eltéréslista `csak_regi_strong`) és a Károli-vers tartalma.

Összesítés könyvenként és osztályonként, minden számhoz proveniencia-sorral (`scope=… | forras=… | ts=…`). **Üres osztály elfogadható eredmény**; bizonytalan esetet nem szabad A-ba sorolni, az `bizonytalan` jelölést kap.

**⛔ Megállás.** A kérdések egy csokorban, mindegyiknél javaslattal és alternatívával. Várható kérdések:
- **(a)** Az A osztály javításának módja: a meglévő megfeleltető táblák általános alkalmazása a `szamozas_elteres` jelölésű fejezetekre, vagy fejezetenkénti kézi felülbírálat (`karoli_vers_felulbiralas.tsv`).
- **(b)** A zsoltár-feliratok kulcsolása (ha a rés oka ez): melyik versszámozás az irányadó.
- **(c)** A `bizonytalan` sorok sorsa: maradjanak üresek (javaslat) vagy kapjanak kézi döntést.

### M1 — A kulcsolási rések pótlása

- A javítás az `lxx_os_import.py` besorolási logikájában történik (a #42-ben bevezetett `--ujrabesorol` mód mintájára), az M0 (a) döntése szerint. **Kézi kitöltés emlékezetből nem lehet**; minden új kulcs egy megfeleltető tábla során lóg, és ez a sor visszakereshető.
- Az `LXX_OS` újragenerálása előtt és után a sorok összevetése (CLAUDE.md, TSV-írás): csak a `igehely_karoli` és a `karoli_ok` oszlop változhat; ha más is változik, állj meg.
- A `csv` modul tilos: olvasás `split('\t')`, írás `'\t'.join()`.

### M2 — Ellenőrzés

- **Kettős kulcs nincs:** egy Károli-vershez egy szövegváltozaton belül legfeljebb egy LXX-vers tartozik, kivéve, ahol a megfeleltető tábla kifejezetten összevonást ír.
- **Idegen kulcs nincs:** minden új `igehely_karoli` létezik a `Karoli_1908.tsv`-ben.
- **Könyvenkénti lefedettség:** a kulcsolt versek száma könyvenként az M1 előtt és után, a Károli-versszámmal összevetve.
- **Mintavétel:** legalább 10 A osztályú versen a `lekerdez.py lxx-hid` kimenete (proveniencia-sorral), és a görög szöveg tartalmi egyezése a Károli-verssel. Ebből legalább 3 Jób-, 2 Hóseás- és 2 zsoltárvers legyen.
- A `teszt_lekerdez_sir.py` zöld; ha egy rögzített szám változik, az indokkal együtt frissül.

### M3 — Zárás

- `naplok/LXX_OS_LEFEDETTSEG_zaras.md` (≤20 sor): osztályonkénti végszámok, a maradék B és `bizonytalan` sorok listájára mutató hivatkozás.
- A `fuggetlen-ellenor` jelentése: `naplok/ELLENOR_LXX_OS_LEFEDETTSEG.md`.
- A brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Mind az 503 vers szerepel az osztályozó táblában, A / B / C / `bizonytalan` jelöléssel, indokkal és forrással.
- **K2.** Minden A osztályú vers az M1 után kulcsolt, és az `lxx-hid` nem üres eredményt ad rá; a kulcs forrása a táblában visszakereshető.
- **K3.** A B és a `bizonytalan` versekre az `lxx-hid` explicit üres eredményt ad (CLAUDE.md 3. szabály: nincs kitöltés).
- **K4.** Nincs kettős és nincs idegen Károli-kulcs (M2).
- **K5.** Az `LXX_OS` újragenerálásakor csak az `igehely_karoli` és a `karoli_ok` oszlop változott.
- **K6.** A `teszt_lekerdez_sir.py` zöld; a CI zöld; a független ellenőr eltérés nélkül zár, vagy az eltérései javítva vannak.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A feladat a #42 nyitott tétele; csonkként befogadva (PR #177). | #42 zárás, felhasználó |
| v1 | 2026-10-05 | Az előfelmérés szerint a rés nagy része kulcsolási hiba, nem görög hiány; ezt az M0 igazolja, a brief nem feltételezi. | befogadási előfelmérés |
| v1 | 2026-10-05 | Egyetlen ⛔ (M0 után); a javítás csak megfeleltető táblán lógó kulccsal, emlékezetből nem. | CLAUDE.md 2–3. szabály |
