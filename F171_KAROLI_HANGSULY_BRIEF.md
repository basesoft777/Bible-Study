---
feladat: 171
cim: A Károli-réteg mint vizsgálati tárgy a közleményekben és a nyílt mag olvasói fájljaiban
kod: KAROLI_HANGSULY
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ad: a data paper két kéziratának újrahasznosítás-szakaszában és a nyílt mag olvasói fájljaiban (generátorsablonból) egy-egy bekezdés a népnyelvi protestáns fordításról mint vizsgálati tárgyról, a nyílt mag soronkénti Károli-adatára hivatkozva
kovetkezo: A kézirat-rész kész (F171.1 mérés, F171.2 kéziratok; draft PR, a felhasználó átolvasására vár). A 4. lépés (generátorsablon, nyilt_mag OLVASSEL/README) a #170 merge-e után, frissített ágon; a független ellenőr a teljes tétel végén
munka: folyamat
olvas: [nyilt_mag/, adat/elofordulasok.tsv, kozlemeny/data_paper/vazlat.md, kozlemeny/data_paper/folyoirat_kovetelmenyek.md, kozlemeny/data_paper/szamok.py]
ir: [kozlemeny/data_paper/kezirat_hu.md, kozlemeny/data_paper/kezirat_en.md, eszkozok/nyilt_mag_export.py, nyilt_mag/OLVASSEL.md, nyilt_mag/README.md, nyilt_mag/ELLENORZO_OSSZEG.sha256]
fugg: []
nem_fugg: [123]
---

# F171_KAROLI_HANGSULY_BRIEF.md — A Károli-réteg mint vizsgálati tárgy

*FELADATOK #171 · Modell: opus · effort: high · v1 · 2026.11.05*

*Befogadva a felhasználó jóváhagyásával („nem kellene akkor ezt jobban hangsúlyozni?”, majd „mehet”, 2026-11-05). A futtató sessiont **magas erőfeszítéssel** (`effort: high`) kell indítani: a feladat nyilvános, tudományos szöveg, ahol a megfogalmazás minősége maga a kimenet.*

## 1. Cél

A nyílt adatmag minden előfordulás-sora kimondja, **melyik Károli-szó** adja vissza a motívum héber vagy görög szavát, a párosítás módjával és bizonyosságával. Ez nemcsak olvasói segédlet: a népnyelvi protestáns fordítás (Károli, 1590/1908) mint **vizsgálati tárgy** — fordítástudomány, recepciótörténet, a magyar bibliai nyelv kialakulása — ebben az adatkészletben soronként, motívumszavanként látszik. A mai kéziratok ezt egy mondatban érintik („supports Hungarian reception history”); a feladat önálló bekezdéssé emeli, mindkét kéziratban és a nyílt mag olvasói fájljaiban.

## 2. Hatókör

**Benne van:**

1. `kozlemeny/data_paper/kezirat_hu.md` „6. Újrahasznosítás” és `kezirat_en.md` „(4) Reuse potential” szakaszába egy-egy bekezdés: (a) a Károli mint népnyelvi protestáns fordítás, vizsgálati tárgyként; (b) mit mutat a nyílt mag ebből soronként (a motívumszó Károli-megfelelője, a párosítás módja és bizonyossága, a változatok — pl. ugyanaz a héber szó több magyar alakkal); (c) milyen kérdésekhez használható (fordítói következetesség, terminológiai egységesítés vagy annak hiánya, recepció); (d) korlát: a gépi párosítás része modell-kimenet, jelölve. Számok **csak mérésből** (`kozlemeny/data_paper/szamok.py` vagy a nyílt mag kimenete), a „A számok forrása” / „Number provenance” szakaszba felvezetve.
2. A meglévő „Károli-szó … reception history” mondat a bekezdésbe olvad (nem marad kettős állítás).
3. A nyílt mag `OLVASSEL.md` és `README.md` fájljába (a **generátor sablonjában**, `eszkozok/nyilt_mag_export.py`; a kimenet generált, kézzel nem szerkeszthető) ugyanez röviden, 2–4 mondatban, mindkét nyelven; újragenerálás, `ELLENORZO_OSSZEG.sha256` frissül, E35 zöld.
4. Nyelvi szabályok: nyilvános szövegben **„termék” / „product” szó nincs**; a pár: *nyílt adatmag* ↔ *a lexikon* (*open data core* ↔ *the lexicon*). A magyar szöveg a kézirat meglévő regiszterét követi (Digitális Bölcsészet, „Labor”), az angol a JDMDH/JOHD rövid cikk regiszterét. Felekezeti értékítélet nincs; a Károli tárgy, nem mérce.

**Nincs benne:** a kéziratok más szakaszainak átírása; új hivatkozás felvétele ellenőrizetlen forrásból (új irodalmi tétel csak ⛔-vel, a szerzőnek javasolva, l. 3. lépés); a nyílt mag adat-oszlopainak módosítása (az a #170); a lexikonlapok.

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md): `opus`. Olvasd végig mindkét kéziratot (az értelmező próza egy kézben, aki belenyúl, az egészet olvassa — KONTEXTUS K1), a `vazlat.md`-t és a `folyoirat_kovetelmenyek.md`-t, és a nyílt mag `OLVASSEL.md`/`README.md`-jét.
1. Mérés: a bekezdés számai (hány előfordulás-sorban van Károli-szó, hány különböző Károli-alak motívumszavanként, a párosítás módjának megoszlása) a `szamok.py` bővítésével **vagy** a nyílt mag fájljaiból egy rögzített paranccsal; a parancs és a kimenet a kézirat „A számok forrása” szakaszába.
2. A két bekezdés megírása (hu, en). Nem fordítás egymásból: mindkettő a saját folyóirata olvasójának szól, ugyanazzal a tartalommal.
3. ⛔ Ha a bekezdéshez irodalmi hivatkozás kellene (pl. Károli-recepció, bibliafordítás-történet), a jelöltet nem írod be: a kézirat „Kitöltendő helyőrzők (a szerző)” listájába kerül `[HIVATKOZÁS: …]` helyőrzővel, és a szerzőé.
4. Generátorsablon: a rövid bekezdés az `OLVASSEL.md`/`README.md` megfelelő szakaszába; újragenerálás; `python eszkozok/nyilt_mag_kapu.py` 0 BUKÁS.
5. Commitok tételenként (`F171.1` mérés, `F171.2` kéziratok, `F171.3` nyílt mag). Független ellenőr (`fuggetlen-ellenor`), majd draft PR; a felhasználó a renderelt szöveget olvassa át merge előtt.

## 4. Elfogadási feltételek

- Mindkét kézirat újrahasznosítás-szakaszában egy önálló bekezdés áll a fenti (a)–(d) tartalommal; a régi egymondatos állítás nem ismétlődik.
- Minden szám mért, a forrása a kézirat számforrás-szakaszában szerepel; `grep` szerint a bekezdésben nincs `{{N:` helyőrző.
- `grep -i "termék\|product"` a két kéziraton és a nyílt mag olvasói fájljain: 0 találat a nyilvános szövegben.
- A nyílt mag `OLVASSEL.md` és `README.md` generált kimenetében a rövid bekezdés mindkét nyelven ott van; `nyilt_mag_kapu.py` 0 BUKÁS; E35 zöld.
- Új irodalmi tétel csak helyőrzőként, a szerzőnek.

## 5. Döntésnapló

- `nem_fugg: [123]` (befogadás, 2026-11-05): a #123 az `elofordulasok.tsv`-t írja; ez a feladat csak a mai állapot számait olvassa, a számok a kiadott export állapotához kötöttek.
- Ütközés a #170-nel (`eszkozok/nyilt_mag_export.py`, `nyilt_mag/`): a 4. lépés (generátorsablon) nem fut a #170-nel egyszerre. A kézirat-rész (1–3. lépés) független; ha a #170 fut, a 4. lépés a #170 merge-e után, frissített ágon jön.
