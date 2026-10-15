# OLVASO_INDITO — zárójelentés (#100)

*2026-10-15 · végrehajtó: claude-sonnet-5-5 · ág: `claude/olvaso-indito`*

- **Kész:** M0 (felmérés, `OLVASO_INDITO_M0_felmeres.md`), M1 (`indit.sh`, `allapot.py`, `--ujratolt`, élő lábléc, `teszt_indito.py` 39 teszt, `teszt_futtat.py`, CLAUDE.md-sor, README), M2.1 gépi próba (36 ellenőrzés, 0 hiba, `OLVASO_INDITO_M2_gepi_proba.md`).
- **Döntések:** DT-F100a (c); DT-F100b igen, csak a belső 8765, az ütemezett feladat az M2 után, a felhasználó külön jóváhagyásával.
- **Mérés** (`OLVASO_INDITO_M1_merés.md`): a hat tesztfájl együtt 274,6 mp (5 percen belül); `teszt_olvaso_szerver.py` 122,4 mp, `teszt_szintek.py` 77,5 mp egyedül futtatva.
- **Ellenőr:** `ELLENOR_F100.md`, 5 eltérés (E1–E5), mind javítva.
- **Egyeztetett eltérések a briefhez:** élő lábléc (`LablecFigyelo`); `.gitattributes` `*.sh eol=lf`; a `.bat` fájlokban a `timeout /t 7` helyett `/statusz`-ra váró hurok; tartalék ág a `.bat`-okban (törölhető a merge után).
- **Ismert korlát:** szintaxishibás szerverfájl mentése után a szerver leáll, és a javítás nem indítja újra; a parancsikon újraindítja (felügyelő a hatókörön kívül).

## Az M2 ⛔ feltétele (nyitott)

- **Az M2.2 (a három parancsikon kipróbálása) csak a merge után, és csak akkor értelmes, ha a fő checkout a `main`-en áll.** Most a (mergelt) `claude/tervezo-mod` ágon áll, ezért a `.bat`-ok tartalék-ága (régi indítás) futna. Az átállást a merge után egy másik session végzi.
- Utána, a felhasználó külön jóváhagyásával: a 8765-ös példány ütemezett feladata (DT-F100b); a `.bat` tartalék-ág törlése.
