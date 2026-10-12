# BDB_KAROLI_POTLAS_M0.md — F80 M0 felmérés (csak olvas)

*FELADATOK #80 · 2026-10-12 · ág: claude/f80-karoli-potlas · az adatot nem módosítja; a mérőszkriptek a repón kívül futottak.*

## 1. Lefedettség (K1)

- `adat/karoli_strong/` alatt **43** `parok_*.tsv` (és 43 `szavak_*.tsv`) van; ebből **39 ószövetségi** (1–5Móz, Józs, Bír, Ruth, 1–2Sám, 1–2Kir, 1–2Krón, Ezsd, Neh, Eszt, Jób, Zsolt, Péld, Préd, Én, Ézs, Jer, JSir [`Sir`], Ez, Dán, Hós, Jóel, Ámós, Abd, Jón, Mik, Náh, Hab, Zof, Hag, Zak, Mal), 4 újszövetségi (2Ján, 3Ján, Filem, Júd). A 39/39 ÓSZ-könyv megvan, mind nem üres (a legkisebb: Abd 446 sor, a legnagyobb: Jer 32 797).
- Sorok: ÓSZ 466 785, ÚSZ 1 219 (összesen 468 004). Fejléc mindenütt 8 oszlop.
- **Strong-normalizálás egységes:** az ÓSZ-fájlok `strong` oszlopa 466 785/466 785 sorban `H` + 4 jegyre kitöltött szám (`H0853`), homográf-betűs vagy rövid (`H853`) alak 0; a G-alak (1 219 sor) kizárólag a négy ÚSZ-fájlban áll. A `forditasok.tsv` BDB-kulcsai (674) mind `H` + 4 jegy; a `bdb_adatblokk.strong_norm` mindkét oldalt azonos számra hozza. Néma nem-találat kockázata: nincs.
- A BDB ószövetségi szótár, a #22 ÚSZ-csomagjai (köztük a 22.9) nem érintik. A brief `fugg: []` helyes.

## 2. Érintett szócikkek

- `forditasok.tsv`: BDB `teljes` sor **674** (674 egyedi Strong; `sonnet` 648, `opus` 20, `kezi` 6; mind `mezo=forditas_hu`).
- **A mostani `bdb_adatblokk.py` mind a 674-hez ad Károli-alakot** (0 `[NINCS KÁROLI-ALAK]`; az ÓSZ-párosítás teljes).
- **Fordításkori állapot — részben rekonstruálható** (módszer: a szócikk első megjelenése a `forditasok.tsv` git-történetében; az akkor a fán álló `parok_*` fájlok, mai tartalmukkal). Három csoport:

| Csoport | Szócikk | Megjegyzés |
|---|---|---|
| **A.** a `bdb_adatblokk.py` létrejötte előtt fordítva (F56.1, 2026-10-06 08:10 +02:00) | **432** (sonnet 406, opus 20, kézi 6) | adatblokk akkor nem volt, tehát sem Károli-szakasz, sem `[NINCS…]` jelzés; a fordításkori Károli-támasz **0** |
| **B.** blokkal fordítva, a Strongnak volt Károli-párja (akkor 6 könyv: 1–5Móz, Józs) | **214** | a blokk már akkor adott Károli-alakot (csak a 6 könyvből) |
| **C.** blokkal fordítva, `[NINCS KÁROLI-ALAK]` | **28** | mind a 6 könyves állapotban (28/242 = 11,6%) |

- Összegzés: a 674-ből **460** (A + C) kapott kevesebb Károli-támaszt, mint amit ma kapna (432 semmit, 28 jelzett üreset); a B-nél (214) a szakasz a 6 könyvről a teljes ÓSZ-re bővül (alakok, számok, példaversek változnak). A teljes kész halmaz tehát érintett, az A/C az a rész, ahol a fordításkor a támasz hiányzott. **Korlát:** az „első megjelenés” a commit-idő, nem a fordító futásának ideje; a `parok` fájlokat mai tartalmukkal vettem (azok az egyesítés óta nem változtak lényegesen, nem ellenőriztem soronként). Az A csoportot ez nem érinti (a generátor nem létezett). A `naplok/BDB_FORDITAS_naplo.md` csak adagszintű arányt ad (DT54/M6c: a 7. adag 86%-a, a kész 1–648. sor 94%-a kapott párt, ami a *mai* kifutású mérés); szócikkenkénti `NINCS` jelzést a napló nem tárol.

## 3. Tárolási lehetőségek

Méret (a mostani generátor szerint, a 674 szócikkre): 61 852 különböző kisbetűs Károli-szóalak; példavers-hivatkozás alakonként legfeljebb 3-mal 96 694 db; a blokk-keretbe (≤2 500 karakter) illeszkedő Károli-szakasz összesen ~1,49 MB (átlag 2,2 KB/szócikk); a korlátlan példa-szakasz 11,6 MB, tehát nem érdemes minden példát szövegesen tárolni.

| | (a) új mező a `forditasok.tsv`-ben | (b) külön tábla az `adat/`-ban |
|---|---|---|
| SEMA | a 2.14 bővül egy mezővel (pl. `karoli_adat`); a `FORDITASOK_FEJLEC`, a `fordit.py` `KIMENET_FEJLEC`-egyezés (a SEMA szerint azonos) és az `ellenoriz.py` 13. szabálya is módosul | új SEMA-szakasz (pl. 2.25), kulcs `strong`+`szoalak` (+ példa-hivatkozás), proveniencia-oszlop; a 2.14 nem változik |
| Méret | a 3,70 MB-os fájl +~1,5 MB (+40%); a 65 nem-BDB sor üres mezővel | ~62 k alaksor (+ példa-hivatkozások), becsült 4–8 MB, csak hivatkozásokkal (vers+sorszám) kisebb; a `forditasok.tsv` marad |
| K3 (bájtra változatlan) | minden sor végére kerülne az új mező: **mind a 739 sor átíródik**, a „bájtra egyező” állítás csak az eredeti oszlopokra igaz | a `forditasok.tsv` egyáltalán nem íródik: K3 triviálisan teljesül |
| Ütközés `emeles.py` | **közvetlen:** `emeles.py` (657. sor) `assert fejlec == FORDITASOK_FEJLEC`, és a `cmd_beir` a mezőlistából ír sort; új mező nélküli sort újraírna/elutasítana | nincs |
| Ütközés #38 | a #38 és a #80 ugyanazt a fájlt írja; a brief szerint kizárják egymást, a #38 megy előre, tehát a #80 addig nem indulhat; fejléc-váltás futó adag közben | nincs fájl-ütközés; a #80 a #38-tól függetlenül futhat, új sorokra (#38 új szócikkei) a pótlás újrafuttatható |
| Egyéb | a `lexikon_general.py` fejléc szerint olvas (tűri) | a kimenet a `strong` kulccsal join-olható; a szakasz újragenerálható a `bdb_adatblokk.py`-ból (a generált/adat réteg-szabály tisztán marad) |

## 4. Javaslat és ⛔

**Javaslat: (b) külön tábla**, `adat/bdb_karoli.tsv` (név a döntésé), soronként egy (`strong`, kisbetűs szóalak) pár magas/egyéb számmal és a példavers-hivatkozásokkal (`vers`+`sorszám`, a szöveg nem másolódik), szócikkenkénti proveniencia-sorral; üres forrásnál (jelenleg nincs ilyen) kifejezett jelzés. Indok: a (a) minden meglévő sort átír és az `emeles.py` fejlécellenőrzésével, valamint a futó #38-cal ütközik; a (b) K3-at triviálisan teljesíti, és nem várja a #38-at. Döntési pontok a felhasználónak: 1. (a) vagy (b); 2. példák tárolása hivatkozásként (javasolt) vagy szövegesen; 3. a B csoport (214) frissítése is kell-e, vagy csak A + C (460), vagy a teljes 674 (javasolt: teljes, mert a szakasz a teljes ÓSZ-ből egységes).

*Proveniencia: scope=manual (git-történet-rekonstrukció, a Károli-támasz fordításkori állapotára közelítés) | forras=adat/karoli_strong/parok_*.tsv, adat/forditasok.tsv, eszkozok/bdb_adatblokk.py, eszkozok/emeles.py, git log | ts=2026-10-12.*
