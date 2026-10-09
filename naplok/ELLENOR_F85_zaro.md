ELTÉRÉS: 3 tétel

# ELLENOR_F85_zaro — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main..HEAD` (b8c8f317; fókusz: F85.20 `5b3a8a00`, F85.21 `c484f38c`, F85.22 `67fff6ad`, F85.23 `b8c8f317`)

*A záró `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott, csak olvasott); az orkesztrátor mentette le, rövidítve, érdemben változatlanul. Nem futtatható volt: `tahot_verskulcs_igazolas.py`, `tahot_karoli_kulcs_generalas.py --onteszt/--szimulacio`, `tahot_verskulcs_kulcsosszevetes.py`, `feladatok.py ellenoriz`, `gh`; ezeknél kódolvasás vagy NEM ELLENŐRIZHETŐ áll. Eljárási jelzés az ellenőrtől: néhány Bash-hívása csövet/`echo`-t/`;` láncolást tartalmazott, mind csak olvasott.*

| pont | eredmény | indok |
|---|---|---|
| EP1 kulcs-összevetés kódja | OK (kódolvasás) | csak olvas, `split('\t')`; halmazkülönbség, kilépési kód 1 eltérésnél; gyenge pont (nem eltérés): a 3. vizsgálat „napló ⊆ versosszevonas” üres halmazon igaz, a 9 közös kulcsot az `F85_igazolas.md` e) pontja igazolja |
| EP1 27 árva kulcs | OK | a TAHOT-ban 0, a Károliban 0 találat |
| EP1 18 üres Károli-vers | OK | mind megvan (Károli 18 vers, TAHOT 279 sor); a tartalom egyezik (Jób 40:1, 2Móz 35:36, Hós 14:10) |
| EP1 ÓSZ-Károli-versszám | OK | 23 204 (= a napló értéke) |
| EP1 különböző TAHOT-kulcsok (23 204) | NEM ELLENŐRIZHETŐ | különböző értékek számlálása a megengedett eszközökkel nem végezhető; a fenti ellenőrzések részben alátámasztják |
| EP1 `lekerdez.py` szúrópróba, 9 összevonás | OK | `scan`/`karoli` szúrópróbák egyeznek; 9 adatsor az `f22/versosszevonas.tsv`-ben = a kulcs-összevetés listája |
| EP2 sorszám, csak az Igehely mező | OK | 5885/5885; 469 301 sor; 6330 napló-sor; szúrópróbák és kódolvasás egyeznek |
| EP3 parok/szavak | OK | `git diff --raw origin/main HEAD -- adat/karoli_strong/` üres (38 fájl); bemenet-azonosság: 17 747 vers, 0 eltérés (napló); 5 könyvnél csak a proveniencia-sor eltér (a felhasználó elfogadta) |
| **EP4 hivatkozás minden sornál** | **ELTÉRÉS (alacsony)** | `naplok/F85_kivezetett_sorok.tsv:7`: az Ézs 64:1 `torol` (Károli-oldali) sornál az `atkulcsolt_eset` és a `megjegyzes` üres, mert a generátor (`tahot_verskulcs_kivezetes.py:92`) üres `eredeti`-nél üres szöveget ír; az indok csak a jelentés 10. szakaszában áll |
| EP5 `CLAUDE.md`, SEMA 4, README-k | OK | `CLAUDE.md`: 1/1 sor, csak a TAHOT-mondat; számok egyeznek (23 204, 337/6330, 9 hely) |
| **EP5 élő régi állítás (repószintű)** | **ELTÉRÉS (alacsony)** | `ADATVAGYON_TERV.md:766`, `ATALAKITASI_TERV.md.md:845` („maradó korlát: a Jób 40 kulcsai MT-számozásúak”), `NYITOTT_FELADATOK.md:590` („nincs a 41. fejezet”) és `:592` („TAHOT-megfeleltetésük … 40:6”); az `ir` listán kívül esnek (kivéve a NYITOTT-ot), részben F84 előttiek |
| **(7) DT90** | **ELTÉRÉS (közepes)** | `DONTESEK.md:165`: a nyitott 🟡 DT90 kérdése és javaslat-indoka élő hamis premisszát hordoz („a Károli-kulcs szerinti lekérdezés a Jób 40-nél ma eltolt tartalmat adna”); `lekerdez.py scan H5591 --szakasz "Jób 40"` → Jób 40:1 ennek ellentmond; az ellenőr nem zárta le és nem írta át; a DT90-döntés a felhasználóé |
| (6) E27 javítás | OK | az E27 listán a `NYITOTT_FELADATOK.md:56` nincs; exit 0 |
| (6) generátor-őr | OK (kódolvasás) | a `main()` első sora az őr; átkulcsolt/vegyes bemeneten `SystemExit` az írás előtt; a TAHOT-ot az F85.22 nem írta; az N-F85e rögzíti a korlátot |
| (6) ELLENOR_F85_16 eltérései | OK | mind javítva |
| (7) CI teljes | OK | `futtat.py --teljes`: exit 0, csak JELENTES/FIGYELMEZTETES; a változott 36 fájlra is exit 0; HIBA nincs; végleges DT/N szám nincs (DT92, N-F85a/b/c/e/f helyőrző) |
| (8) commit-üzenetek, szövegépség | OK | mind a 26 üzenet ép, ékezetes, tétel-azonosítóval kezdődik (megjegyzés: az `F85.4:` és az `F85.12:` kétszer szerepel); csonka mondat/kiesett backtick nincs |
| (9) indokolatlan fájl / `ir` | OK | 36 fájl; a brief és az 5 `ELLENOR_F85*.md` kivételével mind az `ir`-ben; az ELLENOR-naplók konvenció szerinti kivételek |
| (10) a 7. tétel nem zárt | OK / NEM ELLENŐRIZHETŐ (PR) | `allapot: dontesre_var`; zárójelentés és PR nincs (ekkor) |
| Ell.1–5, A1–A6 | OK | törölt TAHOT-sor nincs; adattábla-Δ 0; `adat/karoli_strong` blob-azonos; E12–E15: 0 találat |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) `DONTESEK.md:165` (DT90):** a nyitott döntés premisszája és javaslat-indoka a #85 mért adata szerint már hamis; a felhasználó DT90-döntése előtt a mért adattal frissítendő (nem az ellenőr, nem a végrehajtó zárja le).
2. **(alacsony) Élő elavult állítások az `ir` listán kívül:** `ADATVAGYON_TERV.md:766`, `ATALAKITASI_TERV.md.md:845`, `NYITOTT_FELADATOK.md:590` és `:592`.
3. **(alacsony) `naplok/F85_kivezetett_sorok.tsv:7`:** az Ézs 64:1 `torol` sornál nincs hivatkozás/indok (a generátor üres eredetinél üres szöveget ír).
