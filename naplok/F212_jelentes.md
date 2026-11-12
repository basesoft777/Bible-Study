# F212 — CS3 generátor-kör: jelentés

## F212.1 — Sablonmondat-lista (csak olvasó)

`scope=lexikon/HAMART-001_TUDOMANYOS.md (1. kiadás, fd3ed4e7) + 12 modul (main 860b6618) | forras=naplok/F212_sablonmondat_kigyujt.py | ts=2026-11-12`

- **Módszer.** A `naplok/F212_sablonmondat_kigyujt.py` a `lexikon_general.py` és 11 renderelő (`olvasoi_kovetkeztetes`, `olvasoi_utofeldolg`, `tablajegyzet`, `szotari_glossza`, `kiejtes_szoveg`, `bdb_tagolas`, `szerep_karoli`, `szerep_nave`, `szerep_kizart`, `nyilt_mag_export`, `general`) minden szöveges literálját AST-ből gyűjti (f-string, `%`- és `.format`-helyőrző `{…}`-ként), és a HAMART-001 lap látható szövegén soronként illeszti. A jelölteket a lapon és a kódban egyenként ellenőriztem.
- **Szám.** 10 470 literál, ebből 3 291 olvasói alakú; a lapon 611 illeszkedik, **523 különböző szöveggel**.
- **Jelölt: 29 csoport** — M (műhelyszó) 14, I (ismétlődő címke) 5, L (csak linket adó sor) 5, Sz (blokkok közti szám-/mérce-eltérés) 5; ezen kívül E 2, A (adatból) 1, T (tájékoztató, nem jelölt) 3.
- **Blokkok közti számok:** a 4.6 ×2, az 5. összegző és Összesítés és a szavankénti mondatok ma egyeznek (6 + 4 + 1 + 23 + 11 + 1 = 46); a lektor C/1 eltérése az 1. kiadásban nincs meg. Három külön számítás, egyezés-kapu nincs (Sz1); a mérce három helyen eltér (Sz2–Sz5).
- **Korlát.** A gépi függelék egy-egy általános literált adat- vagy prózasorra is illeszthet, és összevetésre használt literált is mutathat; a jelöltek forrását egyenként ellenőriztem. Több darabból összerakott mondatot a gép csak a leghosszabb darabja alapján talál meg.
- A lista: `naplok/F212_sablonmondat_lista.md`.

## Zárás

- **Kész:** az 1. lépés (lista, draft PR). ⛔ Megállás: a felhasználó a listát nézi át.
- **Nem készült:** generátor-kód, lap, adat; a `lexikon/` érintetlen.
- **Folytatási pont:** a felhasználó döntései (tételenként vagy osztályonként) után F212.2; a kódírás csak a #703 (F202) és a #704 (F203) merge-e után, friss main-ről.
