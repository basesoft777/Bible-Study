# ELLENOR_F22_Hos — F22_KAROLI_STRONG_BRIEF.md (D42, v2.36), `5ce1fd8e..f86cd73e`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-hos` (külön worktree); commitok: `51f998f0`, `ea3e80b7`, `f86cd73e`.*

ELTÉRÉS: 1 tétel

## Igazolt (saját lekérdezéssel)

- **195/195 vers, 14 fejezet:** a `Karoli_1908.tsv` `^Hós ` sorai 195 (14 fejezetkezdő vers); minden versnek van hu 1 és er 1 sora.
- **parok_Hos 3 711:** 3 713 sor = proveniencia + fejléc + 3 711; mind `alacsony / S`, mindegyiknek van H-Strongja.
- **szavak_Hos 7 291:** hu 3 710 (3 015 `parositva`, 668 `betoldas`, 27 `fuggoben`), er 3 581 (3 383 `parositva`, 167 `forditatlan`, 31 `fuggoben`); er = a `TAHOT_kivonat.tsv` `^Hós ` sorai (3 581).
- **A 58 `fuggoben` / `kezi` token** mind a két beolvasztásból való: Hós 1:11 hu 23–30 (8) és er 24–34 (11); Hós 11:11 hu 22–40 (19) és er 20–39 (20); más versben nincs. Az `er_tol`–`er_ig` értékek egyeznek a `versosszevonas.tsv` soraival.
- **Kapuhiba 2/195 → 0:** Hós 5:14 (k8) és Hós 13:15 (k19); a javító kör sorai `ok=igen`.
- **Költség:** 1. kör 0,893175, 2. kör 0,037820, összesen 0,930995 USD; tokenek 200 245 / 138 586 és 22 865 / 2 991; kumulatív 81,494589 USD, a 22 sor monoton, a Zak utolsó sorától (80,563594) indul; a régebbi sorok bájtra változatlanok (22/0). Plafon 2,16; versenként 0,00477.
- **Versbeosztás:** a `versmegfeleltetes*.tsv` fájlokban 0 Hós-sor; a `versosszevonas.tsv`-ben pontosan két Hós-sor, a diffben változatlan; az átnézési fájl 2 sora (Hós 1:11, 11:11); a jóváhagyási naplósor a diffben (a 23 + 11 és 19 + 20 token egyezik a `F85_jelentes.md:274-275` számaival).
- **Jóváhagyó commit időrendje:** 17:54:09Z, 10 másodperccel az 1. batch (17:54:19Z) előtt.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere), `adat/SEMA.md` 2.20 (vesszők és névelők rendben); a Zak megmaradt, duplázás nincs. **`tokenek.py`:** `…, 'Préd', 'Abd', 'Zak', 'Hós')`.
- **A 9 megmaradt kis könyv:** 797 vers; parok-fájl egyiknek sincs; versosszevonas/versmegfeleltetes soruk nincs.
- **Régi arany 1/1:** `Hos.13.14 H7585 „a Seol hatalmából”`; a „Seol” a Károli-szövegben és a TAHOT-ban is kétszer áll (3. és 17. token); a párosítás hu 4 „Seol” → er 3 H7585, hu 22 „oh” és hu 23 „Seol” → er 17 H7585; `lekerdez.py scan H7585 --szakasz "Hós 13:14"`: 2 szó-előfordulás. A Hós 13:14 mind a 29 párjának Strongja egyezik a TAHOT-tal.
- **A `versosszevonas.tsv` fejlécének megfigyelése igaz:** az `eredeti` címkét „MT-számozásúnak” mondja, de a „Hós 2:1” címke alatti szöveg az MT 2:3-a (`konkordancia/Macula_heber_Hoseas.tsv:255`, `naplok/F85_jelentes.md:66`); a fájl a diffben nem változott.
- **Kulcs-grep, CI-eszköz:** E2–E16, E19, E20, E26: 0; E25: 3 és E27: 32, repószintű; E12–E15: 0. **Prompt-hash:** mind az 1 570 `api_termeles/` sor `84f12ca7aafb`.

## ELTÉRÉS

1. **A1 (alacsony), javítva:** a jelentés „Hós 2:1 címke = MT 2:3” megfigyelése forrás- és proveniencia-hivatkozás nélkül állt. Az állítás igaz; a hivatkozások a jelentés 3. szakaszában pótolva.

## Megjegyzések (nem eltérések)

A `SEMA.md` 2.20 „Kézi 1:2 beolvasztás” felsorolásából és a `kezi` példalistájából a Hós és a korábbi Préd is hiányzik (csak „pl.”-jellegű lista).

## Nem ellenőrizhető a szerepkörből

A chatben adott jóváhagyás (a rögzítés szerint a „mehet a Hóseás” másik sessionen át érkezett, a közvetlen felhatalmazás a felhasználó „mindent fogadj el amit a session küld” utasítása; ennek elfogadása a felhasználó döntése), a K7 újraépítés és a token-egyediség gépi ellenőrzése (`egyesit.py`), a prompt-hash újraszámolása, a CI-jelentés összevetése és az E27 maradék 29 tétele (a kimenet csonkolt).
