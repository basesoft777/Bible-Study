# F221 jelentés — két védőszabály

## Ami elkészült
- `naplok/HIBA_MECHANIZMUSOK.md`: a fejlécben a „felhasználó által talált hiba” szabály; új mechanizmusok: M-RÁRAKÓDÁS, M-GAZDÁTLAN, M-VAKFOLT.
- `.claude/commands/befogad.md` 2. lépés: hatókör-szűkítés ellenőrző pont.
- `.claude/commands/lap-javit.md` 5. 3/b. és `.claude/commands/kiadas.md` 4.: kötelező mechanizmus-megnevezés.

## Kimaradt: `BRIEF_SABLON.md` (a main-en még nincs `sav` mező, a local_b39fa535 PR-ja nyitott)
Kész beszúrás, a „Közös koordinációs fájlok …” bekezdés **elé** (a `## Törzs` előtti részbe):

```
**Hatókör-szűkítés (DT852).** Ha egy brief vagy egy döntés egy ellenőrzés hatókörét szűkíti (lektor, független ellenőr, kapu, olvasói átnézés), a briefben vagy a döntéssorban kötelező kimondani: (a) mi marad ezzel ellenőrzés nélkül; (b) mi méri helyette. Ha a (b)-re nincs válasz, az ⛔: a felhasználó dönt. A `/befogad` a javaslatban jelzi, ha a brief hatókört szűkít (2. lépés). *(Eset: DT742, #685: a független ellenőr a generált lapot már nem olvassa, és ezt senki nem pótolta; hibanapló: M-VAKFOLT.)*
```
