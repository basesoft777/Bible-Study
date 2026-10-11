# ELLENOR_F22_Zak — F22_KAROLI_STRONG_BRIEF.md (D41, v2.35), `ebe8c417..c02aa600`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-zak` (külön worktree); commitok: `b875700e`, `5107bf86`, `c02aa600`.*

ELTÉRÉS: 2 tétel

## Igazolt (saját lekérdezéssel)

- **211/211 vers, 14 fejezet:** a `Karoli_1908.tsv` `^Zak ` sorai 211 (az utolsó `Zak 14:1`); minden versnek van hu 1 és er 1 sora.
- **parok_Zak 4 701:** 4 703 sor = proveniencia + fejléc + 4 701; mind `alacsony / S`, mindegyiknek van H-Strongja.
- **szavak_Zak 9 510:** hu 4 723 (3 855 `parositva`, 868 `betoldas`), er 4 787 (4 375 `parositva`, 412 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^Zak ` sorai; `kezi` / `fuggoben` / `magas` 0.
- **Kapuhiba 2/211 → 0:** Zak 11:6 (k16) és Zak 14:8 (k20); a javító kör `kapuhiba_db` 0 / `igen`. Tartalmi megjegyzés (nem eltérés): a Zak 11:6-ban az אָנֹכִי (H0595) a javítás után `forditatlan`, `alacsony` bizonyosságú modelldöntés.
- **Költség:** 1. kör 1,292199, 2. kör 0,042307, összesen 1,334506 USD; tokenek 240 514 / 210 337 és 26 987 / 3 064; plafon 2,34; versenként 0,006325. Kumulatív 80,563594 USD: a 24 sor `futo_osszeg_usd` értéke az Abd utolsó sorától (79,229088) indul, mind = előző + a sor költsége.
- **Régebbi sorok bájtra változatlanok:** futásnapló 24/0, batchek 2/0; a D40 igazítása nem kellett. **Prompt-hash:** mind az 1 548 `api_termeles/` sor `84f12ca7aafb`.
- **Versbeosztás:** a `versmegfeleltetes*.tsv`, `versosszevonas.tsv` fájlokban 0 Zak-sor; a jóváhagyási naplósor a diffben. **Jóváhagyó commit:** 17:22:26Z, 12 másodperccel az 1. batch (17:22:38Z) előtt.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere), `adat/SEMA.md` 2.20; a korábbi könyvek megmaradtak, duplázás nincs. **`tokenek.py`:** `…, 'Náh', 'Préd', 'Abd', 'Zak')`.
- **A 10 megmaradt kis könyv:** 992 vers; parok-fájl egyiknek sincs; beolvasztás csak a Hós 1:11 és 11:11.
- **Régi arany 2/3:** a `Zec.6.13` (pap H3548, székében H3678) és a `Zec.13.9` (H7121 + H8034) hármas a párosításban megvan (`parok_Zak.tsv`, `scan` n=1). A „műtermék” indoklás tényszerű: az `f22_elemzes.py` `kifejezes_helyek` függvénye egybefüggő tokensorozatot keres; a Károli-szövegben „segítségül hívja **az én** nevemet” áll, ezért a „segítségül hívja ... nevemet” nem található, a nevezőben marad (2/3), a tájékoztató sor számlálója nem számolja (2/2). Pontosítás: nem a „...” token, hanem a vele jelölt kihagyás rontja az egyeztetést.
- **Kulcs-grep, CI-eszköz:** E2–E16, E19, E20, E26: 0; E25: 3 és E27: 33, repószintű; E12–E15: 0.

## ELTÉRÉS

1. **(alacsony), nyitott:** a Zec.13.9 „...” kezelésére javasolt „külön tétel” nincs nyilvántartva (sem N-F helyőrző, sem `NYITOTT_FELADATOK` sor). Új tétel felvétele a felhasználó jóváhagyásával és a `/befogad` paranccsal történik, ezért nem vettem fel.
2. **(kozmetikai), javítva:** a `SEMA.md` 2.20 felsorolásából hiányzott egy vessző a „)” után.

## Nem ellenőrizhető a szerepkörből

A chatben adott jóváhagyás („mehet a Zakariás”), a K7 újraépítés és a teljes K1/K2 gépi ellenőrzés (`egyesit.py`), a `prompt_sha256_12` és a `prompt_v3.sha256` megfeleltetése, a gépi E17-futás, a külső CI-jelentéssel való összevetés, hogy a távoli main az `origin/main` helyi ref frissítése óta mozdult-e.
