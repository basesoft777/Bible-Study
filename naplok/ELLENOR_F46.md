# Független ellenőrzés: F46 BDB_KONYVFELOLDAS · origin/main..3b4cb1f (claude/bdb-konyvfeloldas)

*A fuggetlen-ellenor subagent jelentésének összefoglalója (az ellenőr nem tud fájlt írni; az orkesztrátor rögzítette). Verdikt: ELTÉRÉS: 6 tétel, mind nem blokkoló. Az ellenőr nem ellenőrizhetett: külső forrás idézetét (D2), a #38 előfeltételét (D5), a modellt (D6), a kapuk és tesztek futtatását (nincs futtatási joga); ezekre a végrehajtó jelentése és a saját `ellenoriz.py`/CI-futás az irányadó.*

## OK (lekérdezéssel igazolva)
- D1 egy ⛔ megállás a csere előtt (az adat-táblákat csak a F46.6 írja, a ⛔ és a döntés után).
- D3 N-F34/N-F34c lezárva (141 + 12 = 153 sor); D4 a fordításban csak igehely-token (55) és 2 névhiba változott, 42 forras_hash.
- DT-F46 (1)b kiválasztás: 269 csere sor (266 + 3 névhiba); >500 előfordulású Strong: 18 sor kézin; 6 Strong MT→Károli átváltása (7 alak) rendben; F46.6 kapu csak szigorít; (5) a H8034 védett sora nem változott.
- A forrás 269 token-cseréje, sorvesztés nélkül; TSV-kezelés `csv` nélkül; CI-futtató E2–E16, E19: 0 találat.

## ELTÉRÉS
1. **MT-számozású javasolt Károli-alak a 6 megnevezett Stronggon kívül is** (H2204, H7871, H2938, H7138 2Sám 19; H3940 Náh 2:5; H1932 Dán 6:27): a cél a Károliban egy verssel eltolt. A létezés-kapu nem fogja meg. Fordításba nem került; a lefordított BDB-szöveg igehelyei MT-számozásúak, ezért a konvenció kérdése a felhasználóra tartozik → **nyitott tétel a PR-ban** (l. N-F46a).
2. Az `OSHL_BDB_igehelyek.tsv` (+4053 sor) E17/DT3 bontási naplója hiányzik (120 többlet bdb_id, 397 Strong nélküli sor).
3. A `DONTESEK.md` DT-F46 sorában eltolódtak az oszlopok.
4. Az N-F46a „299 + 55 javaslattal” helyesen 296 + 55 = 351.
5. A csere.tsv névhiba-sorainak `ok` mezője ellentmond a DT-F46 (3)-nak („Pharaoh” a független forrásban).
6. A `konkordancia/BDB_teljes_unabridged_README.md` sha256-sora elavult (nincs az `ir` listán; a végrehajtó jelezte).
