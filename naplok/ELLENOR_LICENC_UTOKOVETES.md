# Független ellenőrzés: F44 (LICENC_UTOKOVETES)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze (tartomány `bd39b91..cfe4325`, 4 commit); a fájlba az orkesztrátor írta át, mert az ügynöknek ebben a sessionben nem volt Write eszköze, és nem commitolhat. Az ügynök egyik lekérdezése sem írt fájlt. Verdikt: **ELTÉRÉS, 4 tétel** (a javított tételek az 1. kör után lent).*

## Eredmény pontonként
- **EF1, EF2 (licencek.tsv három sora, a többi sor):** OK. `git diff bd39b91..cfe4325 -- adat/licencek.tsv` üres; a pinelt commit-azonosítók és a „Please do not redistribute” a 9., 10., 19. sorban megvannak.
- **EF3 (20 verses összevetés):** ELTÉRÉS, nem teljesült. Nincs `karoli_diff.tsv`; az ok dokumentált (1590-es kiadás, DT-F33e), a DT-F44a lefedi.
- **EF4 (nincs új Károli-szöveg a `konkordancia/` alatt):** OK, a diff üres.
- **Idézetek a pinelt commitokon (0e24449, e1b254c, b99716b, bible-mcp 4388b38):** NEM ELLENŐRIZHETŐ az ügynök korlátozott eszközeivel (GitHub raw nem érhető el). Az ügynök a repón belüli egyezést igazolta.
- **⛔ 5.:** ELTÉRÉS. A brief „nem beírva a DONTESEK.md-be” kéri a javaslatot, a DT-F44a–d mégis bekerült a `DONTESEK.md`-be (`DONTESEK.md:103-106`), és a fájl nincs az `ir` listán. A CLAUDE.md/`/kovetkezo` 7. lépése a tételeket a `DONTESEK.md`-be kéri; az ütközésről a felhasználó dönt.
- **DT-F44a–d 🟢:** formailag OK. A DT-F44b tartalma halasztás a 🟡 DT-M5-re, mégis „🟢”: ELTÉRÉS (a felhasználó döntése: a DT-M5-tel együtt, a szabály csak használatra szól). A DT-M5 sora nem módosult (OK).
- **openbible sorok (`adat/datasetek.tsv:101-104`):** szerkezet, SEMA 2.6 `hianyzik`, kulcsütközés nincs: OK. **ELTÉRÉS:** a sorok a nem létező „DT-F44e”-re hivatkoztak (helyesen DT-F44d), és az „értékkészlet-bővítés külön döntés” szöveg elavult (a DT-F44c már döntött).
- **Nyers külső adat nincs a repóban:** OK (5 fájl változott, `konkordancia/` és `adat/kulso/` diff üres).
- **D1–D7, A1–A2, A6:** OK. A3–A5 nem alkalmazható. E2–E16, E19, E12–E15: 0 találat; E25: 1 JELENTES + 2 FIGYELMEZTETES a diffen kívül, a base-ben is fennáll (F26#D34).
- **Listák:** törölt sor csak a brief fejlécében (2), táblasor-Δ: `datasetek.tsv` +4, minden más 0.

## Eltérések súlyossági sorrendben, és állapotuk
1. A ⛔ 5. pont sérülése (DT-F44a–d a `DONTESEK.md`-ben): **nyitott, a felhasználó dönt.**
2. A DT-F44b „🟢” halasztásnál: **nyitott, a felhasználó dönt** (a tétel szövege a DT-M5-tel együtt döntést rögzíti).
3. EF3 nem teljesült: dokumentált (DT-F44a), **a zárójelentésben szerepel.**
4. Hivatkozás (DT-F44e→DT-F44d) és elavult szöveg a `datasetek.tsv` 101–104. sorában: **javítva** az orkesztrátor commitjában.
