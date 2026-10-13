# ELLENOR_F94_4 — szűkített negyedik ellenőrzés

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`; kért: `opus`, egyezik). Tartomány: e9083945..1dc8ca65 (a31417df F94.9a, 1dc8ca65 F94.9b). A jelentés összefoglalóját az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze).*

**Eredmény: TISZTA, eltérés nincs.**

- A *megevék* jegye üres (`karoli_szotari_alak.tsv:40329`); a 4 vers (2Krón 30:18, Ezsd 6:21, Mk 4:4, Luk 8:5) T/3 tárgyas. Az *Evék/evék/ivék* `mult.E3` változatlan; az *ivék* mind a 9 helyén E/3, az *evék* 24 előfordulásából 2 T/3 tárgyas (2Móz 16:35, Ján 6:58).
- Bájtazonosság: a táblában 2 sor változott (a `# GENERÁLT` sor hibrid-sha256-ja és ts-e; a *megevék* `regies_jegy`-e `mult.E3` → üres); minden nem-jegy oszlop, a sorrend és a 66 824 sor azonos.
- `hibrid.py`: csak a `JEGY['megevék']=''` és az igekötős ág elsőbbsége; más igekötős alak jegye nem változott (a táblazdiff igazolja).
- SEMA 2.27: a `mult.E1` „nem -ik-es igén”, az *eszik* -ik-es, tehát a (d) nem támasztható alá, a (b) SEMA-kompatibilis. Megjegyzés: az *evék* `mult.E3` / *megevék* üres különbség a felhasználó döntése, az N-F94h dokumentálja.
- Dokumentumok (napló 18.2 és 18.6, N-F94e, N-F94h, DT140 🟢 pontosítás, zárójelentés 12 sor): következetesek, érvényes „megevék E/3” állítás nem maradt.
- CI exit 0 (E25/E27 régi, az ág fájljain kívül); a hozzáadott sorokban nincs abszolút útvonal, `csv` modul, Bible Discovery, emMorph; sorszám-Δ 0, törölt sor 0.

**Nem ellenőrizhető az ellenőr szerepéből:** a két sha256, a `ts` valódi futásidő volta (a commit-idővel összhangban: 17:14Z, commit 17:15:51Z), a végrehajtó tényleges modellje, K2/K3 (a körben nem változott a szótári alak). *Az orkesztrátor utólag újraszámolta a két sha256-ot (`sha256sum`): `hibrid.py` `60e1c215…`, tábla `c3fc23c9…`, egyezik a naplóval.*
