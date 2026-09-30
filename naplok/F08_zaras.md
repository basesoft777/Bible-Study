# F08 zárójelentés (FELADATOK #8; ág: `claude/lxx-dontesek`)

**Elkészült:** a 87 függő hely (`naplok/F17_87_hely.tsv`) 86 sort kapott az `adat/lxx_dontesek.tsv`-ben (LD005–LD090; a 4Móz 13:34 a HODIT-001 és a MENNY-001 közös sora); a régi LD001–LD004 változatlan (4 → 90 adatsor). Bizonyosság: **biztos 71** (63 `eltero_forditas`, 8 `nincs_heber_kulcsszo`), **valószínű 9**, **nyitott 6**. Bemenet: `naplok/F08_bemenet.txt` (Macula-vers illesztéssel + `LXX_OS`-vers + FJ1-jelölt), szkriptek: `eszkozok/f08/`.

**Módszer:** független forrás csak a Macula szó-szintű illesztése és az `LXX_OS` KK-kötésű verse; az FJ1-jelölt Macula-származék, nem számít külön. A Macula 38 gépi megfelelőjéből 36 megerősítve, 2 ellentmondó (1Móz 8:21 ἔτι, Mik 6:12 szócsere → nyitott); a Strong nélküli Macula-alakok Strong-ja az `LXX_OS`-ből.

**Sémaeltérés a brieftől (DT23 (d)):** új `bizonyossag` oszlop és `nincs_heber_kulcsszo` típus (SEMA 2.11); `ellenoriz.py` 10. szabálya és a `lexikon_general.py` megjelenítési szűrője módosult (csak `biztos`/régi sor jelenik meg). Próbagenerálás a repón kívül: 64 lexikonsor függőből eltérő, 23 függő marad. `ellenoriz.py`: RENDBEN 11, SÉRTÉS 0. A lexikonoldalak nincsenek újragenerálva.

**Leletek:** a Préd 9:10 előfordulás-sor igehelye MT-számozású (Károli 9:12; DT7 (g) válasza); a HODIT-001 2Sám 21 / 1Krón 20 soraiban a szó H7498, a sor H7497; a Macula βόθρος → G0999 a Strong-szótárban βόθυνος; a DT7 (a) nem hat ki.

**Nyitott (DONTESEK `DT23`, 🟡, (a)–(g)):** 9 valószínű és 6 nyitott sor, a Préd 9:10 igehely-javítása, a sémabővítés elfogadása, a `nincs_heber_kulcsszo` megjelenítése, H7497/H7498.

**Ellenőrzés:** a `fuggetlen-ellenor` feladata (nem futott ebben a menetben).
