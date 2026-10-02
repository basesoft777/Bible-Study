# F33 — zárójelentés (megállt: két ⛔, döntésre vár)

*Ág: `claude/f33-licenc-rendezes` · 2026.10.02 · végrehajtó: sonnet · független ellenőrzés még nem futott.*
- **L0:** a `licencek.tsv` kiinduló állása 39 sor, 15 `tisztazott` / 24 `tisztazatlan` (egyezik a briefel). A README-re épülő `tisztazott` sorok: SDBH, SDGNT, UBS_DBH, UBS_DNTG, SDBH_SDGNT_segedtablak, OSHL, Strong_szotar. A `LXX_kivonat` olvasói a DT-F33b-ben (kód: `lekerdez.py` 469., `lxx_osszevetes.py` 93., `kockazat_szures_18_tanulmany.py` 137.; adat: `datasetek.tsv` 4 sor; a többi történeti/dokumentáció).
- **L1–L2 kész (F33.1):** szó szerinti idézet + URL (GitHubnál commit) + 2026-10-02 dátum a forrás saját LICENSE-fájljából/licencoldalából/fejlécéből. Végső állapot a táblából: **22 `tisztazott` / 17 `tisztazatlan`**; `kereskedelmi`: 18 igen, 4 feltetelesen, 17 tisztazatlan; `share_alike`: 6 igen, 16 nem, 17 tisztazatlan.
- **Újonnan `tisztazott` (7):** BDB, TAGNT, TAHOT, TIPNR, TSK, Macula_gorog, LXX_OS. A többi 15 sor idézete szó szerinti forrás-idézetre cserélve.
- **Marad `tisztazatlan`, mit kerestem:** LSJ (két forrás ellentmond: marvel.bible CC BY-SA 3.0, PerseusDL/lexica CC BY-SA 4.0), SECE_G/H (a forrás `<rights>Public Domain</rights>`; a GPL 3.0 jelzés nem igazolódott; az „enhanced” réteg licence nincs kimondva), Thayer („used with permission”), Nave_basokant, KJV_ASV_Strongs, LXX_kivonat (nincs licencnyilatkozat), Cremer_nyers/Girdlestone (nincs forrásfájl), származtatott/projekt-sorok.
- **MCGED:** bajtazonos (K3).
- **L3 (rögzítés):** TBESH/TBESG fejlécidézetek és az Online Bible-záradék a sorokban; a nyers TBESH/TBESG fájlok **követettek** (`TBESH.txt`, `TBESG.txt`, két `.lexicon`, `TBESH_konszolidalt.tsv`). ⛔ **DT-F33a** (nyitott, fájl nem mozdult). TAGNT/TAHOT/TIPNR: kereskedelmi korlátozás a fejlécben nincs.
- **L4 ⛔ DT-F33b:** az `LXX_kivonat`-nak van kód- és adat-olvasója, nem töröltem semmit.
- **L5 nincs elvégezve:** a DT-F24 állapota 🟢 marad, amíg a DT-F33a/b nem dől el (K6 nyitott, K4 ⛔ jelentés).
- **Értelmezési pont (orkesztrátornak):** a „forrás saját LICENSE-fájlja vagy licencoldala” mércét a source-repók saját README-jére is alkalmaztam, ha nincs külön LICENSE (HebrewLexicon, GreekResources, STEPBible-Data, BDB, HunKar); ezeknél a megjegyzés jelzi. A `adat/SEMA.md` 2.19 2. szabálya (repó-README is elég) az új mércével ellentétes, de a SEMA.md nem az `ir` listán van, ezért nem módosítottam.
- **Maradék:** DT-F33a, DT-F33b, L5, `fuggetlen-ellenor` (legfeljebb 2 kör), `lexikon_general.py` N9-átállás (külön kód-tétel), a szoros hatókör miatt a SEMA.md-igazítás.
