ELTÉRÉS: 7 tétel

# ELLENOR_F85_16 — F85_TAHOT_VERSKULCS_BRIEF.md · `origin/main..1b3cd8ea` (fókusz: `c0408ef7..1b3cd8ea` = F85.16 22320905, F85.17 5209bb24, F85.18 f3c8be74, F85.19 1b3cd8ea)

*A `fuggetlen-ellenor` jelentése (Write-eszköz nélkül futott, csak olvasott); az orkesztrátor mentette le, rövidítve, érdemben változatlanul. A 7. tétel (zárás) nem esedékes. Nem futtatható volt: `feladatok.py ellenoriz`, `tahot_karoli_kulcs_generalas.py --szimulacio`, `versbeosztas.py --onteszt`, `tahot_verskulcs_kivezetes.py --archivum`; ezeknél kódolvasás vagy NEM ELLENŐRIZHETŐ áll. Eljárási jelzés az ellenőrtől: egy Bash-hívása a `futtat.py` kimenetét `grep`-pel szűrte (cső, csak olvasott).*

| pont | eredmény | indok |
|---|---|---|
| ELLENOR_F85_12 (a) `ir` | OK | az `ir` tartalmazza a `versbeosztas.py`-t; a fókusz minden változott fájlja szerepel az `ir`-ben; a `feladatok.py ellenoriz` futása NEM ELLENŐRIZHETŐ |
| (a) hamis állítás | **ELTÉRÉS (alacsony)** | a 244. sor javítva; a `F85_jelentes.md:235` („nem volt az `ir`-ben az F85.12-ig”) még azt sugallja, hogy az F85.12-től benne volt |
| (b) archívum | OK (kódolvasás) | csak az 1. (`#`) sor változott; 97 `kivezetve`, 7 `visszakerult`, 2 `uj_felvett`; a fejléc egyezik a generátor kódjával; az újrafuttatás NEM ELLENŐRIZHETŐ |
| (c) DT-F85a mondat | OK | „`parok_*` és `szavak_*` (mindkét tábla)”; nincs dupla szóköz |
| (d) 462 971, (e) 12. szakasz, (f) 183. sor | OK | a diffben mindhárom javítva |
| F85.17 `erintett_e` szűkítés | OK (kódolvasás) | `tokenek.py:212`: `not (t == 'nincs_karoli' and e in beolvasztott_uj)`; a mai adaton nincs hatás (a függvény a 200. sorban visszatér); ütközés esetén `SystemExit`, csendes megkettőzés nincs |
| F85.17 önteszt 5c | OK (kódolvasás) | a régi kódon végigkövetve bukik (`b` 2×, `X 1:2` megmarad), az újon átmegy; a futás NEM ELLENŐRIZHETŐ |
| F85.17 Hós/Préd 13.2 | OK | 34 = 23+11, 39 = 19+20, 47 = 38+9 (TAHOT + `versosszevonas.tsv:12–14`) |
| F85.18 kód, TAHOT nem íródott | OK | `git log --oneline 8ce6e95c..HEAD -- konkordancia/TAHOT_kivonat.tsv` üres; a `szimulacio` csak olvas |
| F85.18 szimuláció (True; HEAD: False, 5933) | NEM ELLENŐRIZHETŐ | a `--szimulacio` futtatása nem megengedett |
| F85.18 nem idempotens / felülírás veszélye | **ELTÉRÉS (alacsony)** | a `main()` bemenete és kimenete ugyanaz a fájl; ma írás előtt leáll (`FileNotFoundError`, a két nyers bemenet hiányzik); ha az N-F85e teendője teljesül (a két bemenet a repóba kerül), egy sima futtatás felülírná a kivonatot; a korlát csak a jelentés 16. szakaszában áll, a kódban és az N-F85e-ben nincs, őr sincs |
| F85.19 `CLAUDE.md` hatókör | OK | `git diff --numstat`: 1 sor, csak a TAHOT-mondat |
| F85.19 új állítások | OK (a brief 45 kulcsára) | a 27 régi árva kulcs 0 TAHOT-sor, 0 Károli-vers; a 18 üres Károli-vers mind kapott sort; Behemót: Jób 40:10; a teljes ÓSZ-re szóló állítás saját futtatással NEM ELLENŐRIZHETŐ (a 7. tétel feladata) |
| **F85.19 forrásmegjelölés** | **ELTÉRÉS (alacsony–közepes)** | `CLAUDE.md:107` a versszintű teljességet a `tahot_lefedettseg_ellenoriz.py`-nak tulajdonítja, de az csak fejezetszinten mér és a `Karoli_1908.tsv`-t nem olvassa; a versszintű alap a detektor (K-/E-hiány = 0); a teljes kulcs-összevetés (7. tétel) még nem futott |
| F85.19 `TAHOT_TAGNT_README.md` lista | **ELTÉRÉS (alacsony)** | a 257. sor érintett-fejezet listájából hiányzik a Préd (1420 sor); a 266–267. sor között nincs üres sor a `##` címsor előtt |
| F85.19 régi állítások | **ELTÉRÉS (alacsony)** | a `NYITOTT_FELADATOK.md:626` önellentmondó a Jób 40:1–5-ről („nem hiányzott”, majd „hiányzott”, „tételes ellenőrzés még nyitva”); a többi dokumentumban nincs élő régi állítás |
| F85.19 SEMA 4, 9 összevonás, helyőrzők | OK | `TAHOT-teljes` marad, az `OT-full` a DT90-re hagyva; N-F85b/e/f helyőrző, nem végleges szám |
| DT-F85a alkalmazás-cella | **ELTÉRÉS (alacsony)** | „az 5–7. tétel külön engedélyre vár” az F85.18/19 után elavult; az 5. és 6. tétel engedélyét csak a jelentés rögzíti |
| Heredoc | OK | a négy commit-üzenet ép; a szövegekben nincs csonka mondat vagy kiesett backtickes név |
| **CI (`futtat.py`)** | **ELTÉRÉS (közepes)** | E27 HIBA ×2 a `NYITOTT_FELADATOK.md:56`-on: az N-F85e backtickes `phaseA_all.tsv` és `step1_decisions.tsv` nem létező fájlként jelenik meg; a `futtat.py` 1-es kóddal lép ki (a teljes és a fókusz-tartományon is) |
| Sértetlenség | OK | `adat/karoli_strong` (38 fájl) változatlan; a TAHOT az F85.6 óta nem módosult (Δ0); az `f22` a fókuszban csak a `versosszevonas.tsv` megjegyzéssora (F85.14); végleges DT/N szám nincs |
| 7. tétel nem indult | OK | `allapot: dontesre_var`; a PR-állapot NEM ELLENŐRIZHETŐ |

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) CI:** E27 HIBA ×2 a `NYITOTT_FELADATOK.md:56`-on (N-F85e backtickes, nem létező `phaseA_all.tsv` és `step1_decisions.tsv`); a `futtat.py` 1-es kóddal lép ki.
2. **(alacsony–közepes) `CLAUDE.md:107`:** a versszintű teljesség a csak fejezetszintű `tahot_lefedettseg_ellenoriz.py`-nak tulajdonítva.
3. **(alacsony) Generátor:** a `main()` a saját kimenetét olvassa bemenetként; a nem idempotens jelleg és a felülírás veszélye nincs a kódban és az N-F85e-ben, őr nincs.
4. **(alacsony) `TAHOT_TAGNT_README.md:257`:** az érintett-fejezet listából hiányzik a Préd.
5. **(alacsony) `NYITOTT_FELADATOK.md:626`:** önellentmondás a Jób 40:1–5-ről.
6. **(alacsony) `F85_jelentes.md:235`:** az `ir`-ről szóló maradék félrevezető állítás.
7. **(alacsony) `DONTESEK.md:167`:** a DT-F85a alkalmazás-cellája elavult.
