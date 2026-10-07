# Olvasói pilot — „csak adat” ellenőrzőlista (F60, M1)

*Kézi lista; a gépi része a `eszkozok/olvaso_pilot/teszt_olvaso_pilot.py` `CsakAdat` osztálya. A független ellenőr külön ellenőrzi.*

**Mérce (brief M1):** a sablon minden szövege vagy **(a)** felületi utasítás / jelmagyarázat (mire lehet kattintani, mit jelent egy jelölés), vagy **(b)** adatból jön (számolt érték, adatállapot-jelzés, a forrástábla szövege). Ami egyik sem, kikerül. Három szöveg határeset (**c**: a jelleg vagy a módszer közlése); ezeket a felhasználói átnézésnél (M3) érdemes eldönteni.

## 1. Blokkok és jelleg-címkék (gépi teszt: minden blokk-cím egyezik egy címkézett forrásbejegyzéssel)

| Blokk (cím) | Hol | Jelleg | Adatforrás (`?` jel) |
|---|---|---|---|
| Károli-szöveg | vers-lap | forrásadat + modell-kimenet | Karoli_1908; adat/karoli_strong/parok_*.tsv (az aláhúzás) |
| Versszámozás | vers-lap | forrásadat | Karoli_versmegfeleltetes; LXX_OS |
| Héber szöveg | vers-lap | forrásadat + gépi feldolgozás | TAHOT; Macula_heber; LXX_OS |
| Septuaginta (LXX, Rahlfs) | vers-lap | forrásadat | LXX_OS |
| Kereszthivatkozások (TSK) | vers-lap | forrásadat | TSK |
| Károli-kereszthivatkozások | vers-lap | forrásadat | Karoli_KH |
| Szó adatai (héber) | szó-lap | forrásadat + gépi feldolgozás (számolás) + modell-kimenet (Károli-párok) | Strong_szotar; TAHOT; parok_*.tsv |
| Ebben a versben | szó-lap | forrásadat + gépi feldolgozás + modell-kimenet („Károli itt”) | Macula_heber; UBS_DBH; LXX_OS; parok_*.tsv |
| Így fordítja Károli | szó-lap | modell-kimenet | parok_*.tsv |
| BDB-szócikk apparátusokra bontva / Jelentés (BDB…) | szó-lap | forrásadat + modell-kimenet (a magyar) + gépi feldolgozás (a bontás) | BDB (forditasok.tsv; BDB_teljes_unabridged.tsv) |
| Görög megfelelő a Septuagintában | szó-lap | forrásadat | lxx_bridge |
| Szó adatai (görög) | görög szó-lap | forrásadat + gépi feldolgozás (számolás) | TBESG; TAGNT; lxx_bridge |
| Jelentés magyarul | görög szó-lap | modell-kimenet | Thayer; UBS_DNTG (forditasok.tsv) |
| Jelentés | görög szó-lap | forrásadat | TBESG |
| Héber háttér | görög szó-lap | forrásadat | lxx_bridge |
| Az Újszövetségben | görög szó-lap | forrásadat | TAGNT; Karoli_1908 |
| Szótári szöveg (angol) | görög szó-lap | forrásadat | TBESG; Thayer |

Javított hiba (F60.1): a héber lap „Jelentés (BDB…)” címe korábban a görög lap „Jelentés” (TBESG) bejegyzéséhez illeszkedett, tehát hibás forrást jelzett. A blokk saját bejegyzést kapott (BDB; forrásadat + modell-kimenet).

## 2. Statikus szövegek

**(a) felületi utasítás / jelmagyarázat:** a „Hogyan olvasd ezt az oldalt?” lista (5 pont); „Kapcsolt szavak jelölése”; fülek (Szó, Vers részletei, Bezárás); a lábléc „Aláhúzott szó …” és „Arany jelölés …” sora; a „Jobbról balra. Szavanként: …” és a „A keretes, aláhúzott görög szavakra kattintva …” segédsor; „Lenyit/Rövidebben/A teljes szócikk elrejtése” gombok; „Forrás” nyitó.

**(b) adatból jön / adatállapot-jelzés:** fejléc-címkék (versek száma, szó-lapok száma, „BDB magyarul: x/y”, „Károli–Strong: n könyv”: számolás); „Magyar fordítás nincs · az angol eredeti áll” és társai (a `bdb_hu` mező üres); „Nincs TSK-hivatkozás”, „Ehhez a vershez a Károli-kiadás nem ad kereszthivatkozást”, „Nincs Károli-pár a feldolgozott könyvekben”, „A lxx_bridge nem ad párt (kevesebb mint 3 egyezés)”, „A szó az Újszövetségben nem fordul elő (vagy a TAGNT-kivonatban nincs)”; „A szó az Újszövetség Károli-szövegében nincs kiemelve (a párosítás könyvei: …)” (a könyvlistát a párosítás-fájlok adják); „A UBS-szótár ehhez az előforduláshoz nem ad jelentés-besorolást” (üres `ubs` mező); a számok („előfordulás az ÓSZ-ben”, „Károli-pár (n magas)”, „az első n a m-ből”); a versszám-sor („a számozás egyezik / eltér / a két tábla ellentmond”: a két tábla összevetése).

**(c) határesetek (felhasználói átnézésre):**
1. *„Gépi szeletelés (próba): a határokat a szócikk saját jelölői adják …; hibás határ előfordulhat.”* — a gépi feldolgozás jellegének közlése a lapon; a „?” súgóba is átkerülhetne.
2. *Lábléc: „Az előfordulásszám a TAHOT-kivonatból jön, amely nem teljes (pl. a Zsolt 88/89/140/142 hiányzik).”* — adatminőségi jelzés a `CLAUDE.md`-ből (kézi állítás, nem a pilot méri).
3. *Lábléc: „… a Macula-illesztés pontossága az F17 napló szerint kb. 78% (átvett szám, naplok/F17_import_naplo.md)”* — átvett szám (a napló 78,3%-ot ad); nem a pilot méri.
   Ide tartozik még a lábléc „Igealak: a Macula nyers kódja … a kód jelkulcsa nincs a repóban” (adatlefedettségi jelzés) és a „UBS … CC BY-SA 4.0” sor (licenc-közlés).

**Kikerült szöveg (F60.0–F60.1):** a feladatszámok (#22, #38, #7), „folyamatban”, „halasztva”, a „teremtéstörténet” és az „1Mózes 1:1–2:3” rögzített felirat, a „1–5Móz, Józs” rögzített felsorolás. A teszt (`test_nincs_feladatszam_es_szakaszra_rogzitett_szoveg`) őrzi.

## 3. Ami nem kerül a lapra
Magyarázó szöveg (szószedet), motívum, értelmezés: a #59 jóváhagyott szószedetén át jöhet később.
