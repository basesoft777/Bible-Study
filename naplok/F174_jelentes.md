# F174_jelentes.md — a modernizált Károli – Strong nyílt mag (F174, FELADATOK #174)

*`F174_KAROLI_MODERN_STRONG_BRIEF.md` · ág: `claude/serene-kirch-e9dd90` · PR #707 · végrehajtó modell: `claude-opus-5-5`*

## Zárás

- **Kész (F174.1–9):** a modernizált Károli (#96) és a Károli–Strong párok (#22) összekapcsolása kulcs szerint (igehely, token-sorszám), modell nélkül (`eszkozok/karoli_modern_export.py`). A `nyilt_karoli_modern/` 66 könyvenkénti TSV-t tartalmaz (709 423 sor: 598 715 pár, 599 367 token), mellette a versszöveget, a kétnyelvű kódkönyvet, a MODSZER/METHODS leírást, az ISMERT_HIBAK/KNOWN_ISSUES listát, az attribúciót, a LICENSE-t, a CITATION.cff-et (DOI 10.5281/zenodo.24141950), a KIADAS/RELEASE fájlt és az ellenőrző összeget. A `kozlemeny/` hu/en tervezet export-ignore-ral kimarad a kiadásból.
- **Kapu** (`eszkozok/karoli_modern_kapu.py`): 0 BUKÁS. Teljesség: mind a 598 715 pár átkerült, és mind a 488 659 Strongos token megvan; a #96 lezárásakori 61 könyvön 418 633 / 418 633. Az újrafuttatás bájtazonos, a `nyilt_mag/` és a gyökérbeli `CITATION.cff` változatlan. Teszt (`teszt_karoli_modern_export.py`): 15/15 OK.
- **Szerkesztői átnézés (2026-11-12), átvezetve:** pontos mért számok a közleményben és a MODSZER 4.4-ben (Wilson 95%, korpuszbecslés), az előfizetésre utaló mondat kikerült, a két Strongos tokenszám (488 659 / 418 633) magyarázata bekerült a MODSZER 6.-ba. A szövegeket a szerkesztő jóváhagyta („Jóváhagyom”).
- **A forrás javítása (F174.8):** a három E/1 → T/3 személyhiba (1Móz 39:15 *kezdtem*, Dán 7:16 *kértem*, Ez 22:30 *kerestem*) az `igealak.py` `TOKEN_KIVETEL` táblájában javult, a modern réteg újragenerálva (K2/K3/K3b átment). F174.9: a generált fejléc útvonala platformfüggetlen (`/`).
- **Eltérés a brieftől:** a brief 418 633-as teljességi száma a 61 könyvé; a kapu a mai 66 könyvön mér, és a 61 könyvön a régi számot is igazolja. Az `ir` két lépésben bővült (`eszkozok/karoli_modern/igealak.py`, `karoli_modern.py`, `adat/karoli_modern/`), az orkesztrátor jóváhagyásával. A mintatáblák változatlanok maradtak. Független ellenőri kör (`fuggetlen-ellenor`) nem futott; a szövegeket a szerkesztő nézte át.
- **Nyitott:** N-F174a (az `adat/licencek.tsv` `karoli_modern` sora a CC BY 4.0 kiadáshoz; átadva az F208-nak, #710, a `nyilt_mag/` újragenerálásával együtt); N-F174b (a kapu és a teszt felvétele a CI-ba).
- **Következő:** a merge az orkesztrátoré; a Zenodo-feltöltés a felhasználó lépése; a #175 erre épül.
