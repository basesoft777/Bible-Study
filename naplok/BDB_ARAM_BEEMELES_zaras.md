# BDB_ARAM_BEEMELES zárás (F72)

*scope=konkordancia/BDB_aram_potlas.tsv + BDB_teljes_unabridged.tsv + BDB_strong_alias.tsv | forras=eszkozok/bdb_aram_beemeles.py --m2 | ts=2026-10-07*

- Felhasználói jóváhagyás (chat, az orkesztrátor közvetítésével): 6 szöveges pótlás + 162 alias-sor; kizárva H2298 (kézi, kezi_elfogadott) és H5839 (téves testvér: BDB9760 Azarjá, H5665 Abed-Negó), indokolt kizárólistával a szkriptben.
- Végszámok: alias +162 (296 → 458 sor), szöveges +6 (8093 → 8099 sor, a végén), jelölt: 5 (H0004, H3769, H5013, H2298, H5839).
- Bájtazonosság: a régi tartalom prefixként azonos az origin/main-nel (a teszt ellenőrzi); az elvetett tábla bájtra változatlan.
- SHA-256 előtte → utána:
  - fő tábla `40d96e57…f3cf6` → `d4b15b2f…a7794`
  - alias `243c6bea…d375` → `6f9b86b6…a6f9`
  - elvetett `e66064b6…9f44` (változatlan)
- H6433 mérőszáma 0,07 (a többi pótlásé 0,73–0,79): a mérés a pótolt szöveg 12 karakteres szeleteit keresi a fő tábla egy olyan sorában, amely a címszó mássalhangzóit tartalmazza. A többi öt arámi szócikknek van héber testvérsora, amelyben a szöveg nagy része (részlegesen) ott áll. A H6433 (פֻּם, arámi pum, „mouth”, Dán 7:8) szócikke a héber peh (H6310) sorában csak mellékesen szerepel (más szerkezetben, a H6310 sora említi a Dán 7:8-at), ezért a szeletek nem egyeznek. A 0,07 tehát a szöveg hiányát jelzi, és helyes: a pum valódi arámi szócikk, nem a héber peh alpontja, így a szöveges pótlás indokolt.
- README: `konkordancia/BDB_teljes_unabridged_README.md` (új szakasz, SHA-256, figyelmeztetés: a `bdb_strong_potlas.py --alias` nulláról újraírná az alias-táblákat). Nyitott: N-F72a (helyőrző, `NYITOTT_FELADATOK.md`); N51 lezárása helyőrzővel: DT-F72/N51 lezárandó a main-en.
- A #38 sorrendjének újragenerálása NINCS elvégezve (külön jóváhagyás kell); a #38 7. adagjának `fugg` bővítése a befogadáskor.
- Teszt: `python eszkozok/teszt_bdb_aram_beemeles.py` zöld (beemelés utáni állapot). A független ellenőrzést nem én végzem.
