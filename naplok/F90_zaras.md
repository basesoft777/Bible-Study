# F90 zárójelentés — a TAGNT-kivonat zárójeles sorainak pótlása

*2026.10.12 · ág: `claude/f90-tagnt-zarojeles` · modell: opus · ellenőr: `naplok/ELLENOR_F90.md` (TISZTA)*

- **Eredmény:** a `konkordancia/TAGNT_kivonat.tsv` 141 746 → 142 096 sor: +350 szó-sor (48 csoport, `[..]` 235, `{..}` 115), 0 törölt vagy módosított sor (K1, K2). Az újrafuttatás nem ír.
- **Új vers (9):** Ján 7:53, Róm 16:25–27, 2Kor 13:13, Fil 1:16–17, 3Ján 1:15, Jel 12:18; 49 kulcs érintett.
- **Szkript:** `eszkozok/tagnt_zarojeles_potlas.py` (szárazon fut, `--ir` ír; sha256-, döntés- és vetület-őrökkel).
- **Döntések:** DT-F90a (letöltés: blob nélküli klón, 4 fájl; a 08.24-i commit `manual`, a két blob azonos), DT-F90b (a Károli-döntési tábla jóváhagyva; az 1Thessz 2:12[2:11] #01–#04 → 2:11, #05–#06 → 2:12; Zsid 12:23; TR-utóiratok a vers kulcsán; Fil 1:16–17 kulcs-sorrend). Végleges számot a `szamkiosztas` ad.
- **Igazolás:** `tokenek.py` sorszám-hiba 0; `sorrend_ellenoriz.py` TAGNT-ág hibaszám 0 (a TAHOT-ágat az F90 nem érintette); `eredeti_nelkuli_lista.py`: Károli-vers eredeti nélkül 0, megmaradt 3 versösszevonás.
- **Frissítve:** `TAHOT_TAGNT_README.md` zárójeles szakasza, `sorrend_ellenoriz.py` (`SOR_GOROG`), `NYITOTT_FELADATOK.md` (N-F22c, N-F22d).
- **Egyeztetett eltérés:** nincs a briefhez képest; a `naplok/F22_nincs_parja_versek.tsv` bekerült az `ir`-be (a 4. lépés előírja az újragenerálást).
- **Nyitva:** az érintett versek újrapárosítása és a 2Kor futtatása az F22 dolga (N-F22c). A nyers TAGNT a repón kívül van.
- **Merge:** a felhasználótól.
