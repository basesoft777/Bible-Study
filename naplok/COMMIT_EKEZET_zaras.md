# COMMIT_EKEZET — zárójelentés (#112, F112)

*2026.10.19 · modell: claude-sonnet-5-5 · ág: claude/f112-commit-ekezet*

- **Eredmény:** az E30 szabály (ékezet nélküli magyar szó a PR `base..head` kézi, nem-merge commitjaiban) bekötve, **FIGYELMEZTETÉS** szinten; a CI nem pirosodik. `push`-eseménynél és `--teljes` módban nem fut (G4).
- **Döntés:** DT253 — 3. változat, szűk kizárólistával (orkesztrátor, a felhasználó felhatalmazásával, 2026-10-19). HIBA-szint 20 PR után, `N-F112a`.
- **Mérés (M0):** a main 3 296 kézi commitjából 659 jelölt (20%); az 50 elemes seedelt minta pontossága 84% (szűk lista), 90% (bővített, mintára tanult lista — nem használt). `naplok/COMMIT_EKEZET_meres.md`.
- **Kizárólista:** `eszkozok/ellenorzes/e30_ascii_alakok.tsv`, 21 sor (mezőnév/értékkészlet/kétértelmű pár), mind `ok` + forrás mezővel (G5, teszttel).
- **Tesztek (G1):** `TestE30`, 10 teszt; a `test_szabalyok.py` 154 teszt zöld. Kézi próba: ékezetlen üzenetre 5 találat; a saját ág commitjain 0.
- **Független ellenőr (`ELLENOR_F112.md`):** ELTÉRÉS 7 tétel, mind mechanikus/dokumentációs, javítva (F112.5): besorolás (`kiegeszitve`) → 84%/90%; újrafuttatás rögzített fejjel; DT-sor szövege; `ir` bővítve a workflow-fájllal; a nagybetűs szó korlátja dokumentálva.
- **Ismert korlát:** nagybetűs (mondat-/üzenetkezdő) ékezetlen szót nem jelez; a `forras`, `cim` stb. mezőnév-szavak közül csak a zárt séma-mezőnevek kizártak.
- **Nyitott:** `N-F112a` (újraértékelés 20 PR után); a PR címének `[ELLENŐRZŐ]` előtaggal kell indulnia (E16). Merge a felhasználóé.
