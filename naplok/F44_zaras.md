# F44 — zárójelentés (Licenc-utókövetés; DT-F44a–d eldöntve)

*Ág: `claude/licenc-utokovetes` · 2026.10.05 · végrehajtó: sonnet (Sonnet 5.5) · napló: `naplok/LICENC_UTOKOVETES_naplo.md`*
- **Károli 1908 / KH:** a DT-F33e (2026.10.04) tárgytalanná tette; a `licencek.tsv` nem változott (`kozkincs`), idézetek ma újraellenőrizve (hunkar.conf @ 0e24449, scrollmapper LICENSE @ e1b254c).
- **Versifikacios_tablak:** már `tisztazott`; a TVTMS fájl neve és a STEPBible-Data @ b99716b rögzítve, a fejléc-idézet ma újraellenőrizve.
- **Nem teljesült: a 20 verses szövegösszevetés** (és a `LICENC_UTOKOVETES_karoli_diff.tsv`). Ok: a `k-mktr/karoli_bible_hu` kártya az 1590-es vizsolyi kiadás, nem az 1908-as revízió, így az egyezési arány semmit nem bizonyítana; a Károli-rész a DT-F33e miatt tárgytalan; a HF-szöveget senki nem másolta be. Elvetve (DT-F44a).
- **DT-F44a ✅ elvetés:** a karoli_bible_hu-nak nincs `license` mezője a kártyán, és az 1590-es kiadás, nem az 1908-as. Nincs `datasetek.tsv`-sor.
- **openbible.info:** 4 új `datasetek.tsv`-sor (`openbible_crossrefs`, `hianyzik` + JELÖLT, NEM IMPORTÁLT), CC BY az oldal szó szerinti lábléce szerint; adat nem letöltve, `licencek.tsv`-sor nincs (DT-F44c: nincs `jelolt` érték a SEMA-ban). Import külön feladat, `/befogad` útján (DT-F44d).
- **bible-mcp:** README @ 4388b38 szó szerint a naplóban (kód PolyForm NC, származtatott rétegek CC BY-NC 4.0); a használati szabály a DT-M5-tel együtt döntendő (DT-F44b); a DT-M5 sor érintetlen.
- **Módosított fájlok:** `adat/datasetek.tsv` (+4), `DONTESEK.md` (+4 saját sor), a napló és ez a zárójelentés, a brief fejléce. A `licencek.tsv` diffje üres.
- **Nyitott:** az openbible import `/befogad`-ja; DT-M5. PR és ellenőrzés a zárás szerint (az orkesztrátor).
