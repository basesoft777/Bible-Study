# ELLENŐR — F17 (Macula-import), merge-előkészítő kör (F17.9–F17.13), tömörítve

Ág: `claude/macula-import` (#87). Ellenőr: `fuggetlen-ellenor`; a jelentés az orkesztrátor által mentett tömörítés (az ellenőrnek nincs írási eszköze). A `naplok/ELLENOR_F17.md` az F17.1–F17.8 három körét rögzíti; ez a fájl az utána következő kört.

**1. menet (F17.9–F17.12) — ELTÉRÉS 9.** Rendben: a 39 könyvfájl adatsorainak összege 475 911; minden fájl adatsora és a hat közös fejlécsor soronként azonos a régi fájllal (`f15fc91:konkordancia/Macula_heber.tsv`, blob-numstat mind a 39 fájlra); minden fájlban megvan a licenc-attribúció; szerepmátrix és SEMA változatlan; nincs main-beli sorcsökkenés; E2–E16 0 találat.
Eltérések: (1) **a DT6 azonosító már foglalt más ágakon** (`claude/f21-pilot` DT6 és DT5, `claude/nave-import` DT5) — az azonosító-kiosztás a felhasználó szabálya szerint történt (main utolsó DT4, DT-F16 = DT5, DT-F17 = DT6); az ütközés a merge-nél oldandó fel, a felhasználónak jelezve; (2) a DT6 (f) datasetszáma hiányos (a #18 is bővíti); (3) a DT6 (e) opciói a bontás után elavultak; (4) alacsony: egy maradék `DT-F17` szó, a `macula_bont.py` alapértelmezett bemenete a törölt fájl, „58,7 MB” vs. 65 051 446 bájt, a fejlécek „sorrendben” szövege, hiányzó rebase.
**Javítás (F17.13):** mind a négy alacsony és a (2)–(3) pont.

**2. menet (F17.13 után) — ELTÉRÉS 1 (alacsony):** az `ELLENOR_F17.md` 14. sora utólag módosult (58,7 → 65 051 446 bájt); ez a fájl (ELLENOR_F17_2) rögzíti a kört. Az orkesztrátor a saját `feladatok.py ellenoriz` futtatásával kiegészítette: 47 brief, 0 hiba.
Nem ellenőrizhető: a 39 blokk kánonsorrendű összefűzése és a bájt-egyezés (a régi blob mérete) — ezt a `macula_bont.py --ellenoriz` futtatása igazolta a bontáskor (F17.9); a brief ⛔ pontjai a szűkített körben.

**Eredmény:** TISZTA az azonosító-ütközés kivételével (DT6, l. fent), amely felhasználói döntés.
