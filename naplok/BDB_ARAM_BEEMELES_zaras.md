# BDB_ARAM_BEEMELES zárás (F72)

*scope=konkordancia/BDB_aram_potlas.tsv + BDB_teljes_unabridged.tsv + BDB_strong_alias.tsv | forras=eszkozok/bdb_aram_beemeles.py --m2 | ts=2026-10-07*

- Jóváhagyás (felhasználó, chat, az orkesztrátor közvetítésével): a ⛔ 2. pont; később a H2298/H5839 kizárásának visszavonása (ELLENOR_F72 alapján). **A két korábbi kizárás téves alapon állt:** a szöveg mindkét esetben a testvérsor végén van; a `kezi_elfogadott` (H2298 → BDB9285) döntés a szócikk-azonosításról szólt, nem a táblasorról. H5839 → H5838 (BDB9760): indokolt felülírás (`TABLA_FELULIR`), mert a legjobb mérőszámú sor a H5665 (Abed-Negó) volt.
- Végszámok: alias +164 (296 → 460 sor), szöveges +6 (8093 → 8099 sor, a végén), jelölt 3 (H0004, H3769, H5013).
- Bájtazonosság: a nem-F72 alias-sorok és a fő tábla régi része bájtra azonos az origin/main-nel (a szkript és a teszt ellenőrzi); az elvetett tábla változatlan. A korábbi 162 F72-sor oszlopai (a proveniencia kivételével) azonosak maradtak; a proveniencia `forras` mezője a brief szerint a `bdb_aram_potlas.py --duplikacio`-t is nevezi.
- SHA-256 előtte → utána: fő tábla `40d96e57…f3cf6` → `d4b15b2f…a7794`; alias `243c6bea…d375` → `71e40bc8…cc04`; elvetett `e66064b6…9f44` (változatlan).
- H3606 → H3605 kézi ellenőrzése: elfogadva (arámi–héber kol, ugyanaz a lemma).
- H6433 mérőszáma 0,07 (a többi pótlásé 0,73–0,79): a mérés a szöveg 12 karakteres szeleteit keresi a fő tábla egy sorában. A többi öt arámi szócikknek a héber testvérsorban nagyrészt ott a szövege; a H6433 (פֻּם, arámi pum, „mouth”, Dán 7:8) a héber peh (H6310) sorában csak mellékesen szerepel, más szerkezetben. A 0,07 valódi hiányt jelez: a pum önálló arámi szócikk, a pótlás helyes.
- README, N-F72a (az `--alias` őrizze meg az arámi sorokat; helyőrző), N51 lezárása (helyőrző DT-F72): kész.
- Teszt: `python eszkozok/teszt_bdb_aram_beemeles.py` zöld. A #38 sorrendjének újragenerálása: l. a következő commit. A független ellenőrzést nem én végzem.
