# N-F156a — a Károli-KH tábla másolat-mintázata: ok, kezelés, mérés

*scope=konkordancia/Karoli_kereszthivatkozasok.tsv | forras=krisek/HunKar `hunkaroli_rev.osis.xml` (commit 0e244494dd190e4a6b132c1afddfa307e73792f8, 10 497 338 bájt, Public Domain, `hunkar.conf`) + eszkozok/karoli_kh_osis_konverzio.py + eszkozok/karoli_kh_gyanus_general.py | ts=2026-11-02*

## Az ok, a teljes láncon

1. **Nyers forrás.** A tábla a HunKar OSIS XML-ből készült (commit 1a4d46a8, 2026-08-24, chat-menet; a szkript nem került a repóba). A nyers XML nincs a repóban; a mostani vizsgálathoz a krisek/HunKar nyilvános repó sekély klónját töltöttük le (az orkesztrátor jóváhagyásával, a felhasználó „Letöltheti" engedélyére), a repón kívüli scratchpadbe; a repóba nem került, adatként kezelve (semmit nem futtattunk belőle).
2. **Konverzió.** A README módszere szerint újraírva: `eszkozok/karoli_kh_osis_konverzio.py`. `--osszevet`: 32 407 kinyert sor, a meglévő tábla 32 407 sora, **0 eltérő sor**, a fejléc azonos. A konverzió tehát nem okozza a hibát, a tábla a forráshoz hű.
3. **A másolat a forrásban keletkezik.** A forrás XML `<verse>` elemeiben a `<note type="crossReference" osisRef="Acts.2.27">` jegyzet tartalma másik versé. Minta: `Acts.2.18`–`2.47` jegyzetei szó szerint az `Acts.7.5`–`7.34` jegyzetei (2:27 = „1Móz 46,27; 2Móz 1,5; 5Móz 10,22", ami ApCsel 7:14 helyes listája; 2:25, Zsolt 16:8–11, helyes). A HunKar `hunkar.conf` History_2.0 szerint a kereszthivatkozások a szentiras.hu/KG-ből jöttek; a hiba innen örökölt kulcsolási hiba, a forrás-XML-ben van. Az ApCsel 2:26–47 eredeti listája ebből a forrásból **nem nyerhető vissza**.
4. **Szisztematikus, nem véletlen.** A gyanús listák többsége konstans verssorszám-eltolású blokkban áll (a `Karoli_1908.tsv` kanonikus sorrendjében), a gazda ugyanabban a könyvben; az eltolások néhány közös értékből jönnek (−154, −117, −271, −406, −405, −523). A mechanizmus pontos magyarázata (feltevés: a jegyzet-folyam rögzített számú elemmel el van csúszva) nem igazolt; erre nem építünk.

## Mérés (a gyanú-szabály: `karoli_kh_epseg.py`, RITKA_STRONG = 150, kis mintán kalibrált)

| | előtte | utána |
|---|---|---|
| gyanús forrásvers a főtáblán | **5 078** (7 971 KH-sor) | a fogyasztók mindet kihagyják; a szűrt táblán a szabály 1 versre ad találatot (a csoportok összetétele változott) |
| fogyasztott forrásvers / KH-sor | 19 817 / 32 407 | 14 739 / 24 436 |
| ebből **blokk-tag** (≥3 gyanús vers, azonos könyvpár és eltolás) | — | **4 410** (86,8%) — a legerősebb bizonyíték, 165 blokk, a lista: `naplok/KAROLI_KH_blokkok.md` |
| **nem blokk-tag** (`egyedi`) | — | **668** (13,2%) — **nagyobb a hamis-pozitív kockázat** |

*(A PR #598 idején mért 5 471 az olvasói kapu előtti, lexikai kivétel nélküli szabály értéke; a mai 5 078 a pontosított szabályé.)*

- **A 3 hamis pozitív** (Péld 1:12, 1Krón 20:4, Zsolt 76:3): a pontosított szabály szerint nem gyanúsak; a `gyanus.tsv`-ben nincsenek (a `teszt_karoli_kh_gyanus.py` őrzi).
- **A 2 bizonytalan** (Hab 2:17 → Ézs 33:1, Zsolt 49:15 → Jób 27:17): `egyedi` osztályú gyanús versek maradnak. A nyers forrás ezt **nem dönti el**: a XML-ben ott a lista, de a gazdájuk (Ézs 21:2, Péld 13:22) listájával azonos, vagyis ugyanaz a másolat-mintázat; blokk-bizonyíték nincs. Kezelésük: marad a kihagyás, a (d) próba/emberi átnézés dönthet.
- **Hány ma elrejtett lista lesz helyes?** **Egy sem.** A helyes lista a másolt helyeken ebből a forrásból nincs; a gyanús versek listája nem javul, csak kimarad. A nem gyanús versek (a lapokon ma is megjelenők) listái változatlanok.
- **A gyanú-szabály okafogyottá válik-e?** Nem: a karantén-fájl pontosan ennek a szabálynak a kimenete, a szabály most a *forrás* hibájának kezelése. Ha a (d) út (szentiras.hu/KG, N-F156d) helyes adatot ad, a karantén kiürül, és a szabály okafogyottá válik; a generátorból most nem vettünk ki semmit.

## Kezelés (DT-F156q, (a))

- Főtábla nyers-hű, változatlan. Új: `konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv` (forrásvers, osztály, blokk-eltolás, ok, a gazda, a lista, proveniencia).
- Fogyasztók (`eszkozok/karoli_kh_szuro.py`): `sqlite_epit.py`, `lekerdez.py` (`karoli`: kiírja, hány sort hagyott ki), `olvaso_pilot/adat.py`. Nem módosítva (a feladat szerint): `lexikon_general.py` (N-F156c, a gépi kör merge-e után), `lexikon/`. Szűrve még: `olvaso_mockup/nav_kinyer.py` (csak Jóel 2, 7 gyanús vers). Szűrés nélkül: `f110_ir2.py` (csak proveniencia-szöveg), `olvaso_pilot/felmeres.py`/`db_meres.py` (mérések, nem fogyasztók).
- Tesztek: `eszkozok/teszt_karoli_kh_gyanus.py`; a `teszt_sqlite_epit.py` és a `teszt_olvaso_pilot.py` futása lent.

## Nyitott

- **N-F156c** `lexikon_general.py` → `karoli_kh_szuro` (a gépi kör merge-e után), lapok újragenerálása.
- **N-F156d — lezárva:** a szentiras.hu KG ugyanazt a hibát hordozza, onnan nem javítható. Az orkesztrátor kézi oldalmegnyitása (ts=2026-11-02, `https://szentiras.hu/biblia/kg/csel/2,1`; slug: `csel`): Csel 2:27 → „1Móz. 46,27. 2Móz. 1,5. 5Móz. 10,22.”; 2:25 helyes; 2:18–2:21, 2:26, 2:28, 2:31 a Csel 7-es blokk listáit hordozza. A session két lekérése (`/KG/ApCsel2,27`, `/biblia/kg/apcsel/2,27`) rossz slug miatt 404 volt (nyers válasz a scratchpadben, nem a repóban).
- A szabály a nem duplikált hibás listát nem fogja meg (ApCsel 22:16 → Jón 1:5): korlát, nem negatív lelet.
