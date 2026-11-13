"""lapgen — a rétegzett lapgenerátor (F218a).

Rétegek, egyirányú függéssel: `szoveg` ← `bemenet` ← `szamitas` ← `megjelenites`.
A `konfig` mindenkié. Az alapszabály (DT823): a lap látható szövege csak kézi prózából,
strukturált értékű sablonmondatból vagy szó szerinti idézetből jöhet; a szabály szövege a
`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`-ben áll, a típus a `szoveg` modulban.

Belépési pont: `python eszkozok/general.py --cel lexikon2 --id <ID> --kimenet <könyvtár>`.
"""
