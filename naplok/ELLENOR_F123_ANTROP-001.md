```
ELTÉRÉS: 12 tétel
```

# ELLENŐR — F123_MIGRACIO2_BRIEF.md (v2, ANTROP-001 új cikk, U1–U4) · `origin/main..4d489527`

*A `fuggetlen-ellenor` jelentése, 2026-11-03 (claude-opus-5-5). Az ellenőr íróeszköz nélkül futott; ez a fő szál által rögzített kivonat a jelentés ELTÉRÉS-listájából és összegző táblájából, a megfogalmazás az ellenőré. Az ellenőr jelezte, hogy néhány Bash-hívásban `head`/`tail`/`grep`/`python -c` szűrőt használt (csak olvasás).*

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) 1Kor 2:15** bent marad a saját negatív kritériuma ellenére: a versben csak a πνευματικός áll (`scan G4152 --szakasz "1Kor 2:15"` → 1, a többi 0), a forrás a 2:14–15-öt „két mondat”-nak nevezi, és ugyanezzel az okkal zárta ki a menet az ApCsel 4:31–32, 20:23–24, 2Kor 1:22–23, Luk 9:55–56 helyeket és a „csak πνευματικός” blokk 16 versét. Határkártya erről nincs. (`adat/elofordulasok.tsv:160`; `adat/motivumok.tsv:8`; `motivumok/ANTROP-001.md:29`)
2. **(közepes) A mérce következetessége:** az elutasítás oka („nem az ember két belső összetevőjét különbözteti meg”, 1Pét 1:22, Fil 1:27) szigorúbb, mint amit a bent lévő 1Kor 2:14, Júd 1:19 (a πνεῦμα ott is Isten Lelke, Thayer G4151 4.a) és 1Kor 15:44/46 teljesít; a próza maga írja: „nem az ember két részét, hanem két embert nevez meg”. A `motivumok.tsv` kritériuma ezt a jegyet nem kéri.
3. **(közepes) Drash ↔ vitatott pont (A1):** a Drash („az ember nem egynemű …”) forrás nélkül egy oldalra zárja a vitát, amelyről a vitatott pont azt írja, hogy a lap nem dönti el; a vitatott pont („A teológiában régi vita”) megnevezett képviselő nélküli, jelöletlen memóriaállítás. (`motivumok/ANTROP-001.md:89` ↔ `:95`)
4. **(közepes–alacsony) DT28 proveniencia:** a 8 régi 1/a sor `kapcsolodas`/`funkcio` mezője 2026-11-03-án nulláról újraíródott, a proveniencia mégis `forras=Pneuma_pszukhe_megkulonboztetes_tematikus.md | ts=2026-08-22` maradt, jelöltsor nincs hozzá (brief U3: a jeloltek.tsv-n át, manual provenienciával). Az ALVIL-001 ugyanígy járt el.
5. (alacsony) **DT586 jelölése:** az opciólistában a „(b)” = „a Fil 1:27 is beépítve”, a végén „(b) javasolt” áll, a HATAR K1-ben a (b) = „kint marad”.
6. (alacsony) **G5590 -/2/- címke** csak a 2.a-t mondja; a 2.b–2.c (a testtől különböző lélek) is alá tartozik.
7. (alacsony) **Remez:** „Az összecsengés kétirányú …” értelmező következtetés a Remez-rétegben; a Sod „az ember útja … a megelevenítő szellem felé” — a megelevenítő szellem Krisztusé.
8. (alacsony) **Héber háttér, Jób 7:11:** a Károli „lelkemnek” a rúahot, a „szívemnek” a nefest fordítja; a mondat fordított megfeleltetést sugall.
9. (alacsony) **A forrás 1. szakasza:** „Három helyen …” — csak két pár van (a lapra nem renderelődik).
10. (alacsony) **N92:** az „Utolsó frissítés” sor és a brief `kovetkezo` mezője 3 BUKÁS-t ír, a tétel és a napló 4-et; a „(4)” kétszer szerepel.
11. (alacsony) **E16:** a napló „PR-mód: 0 HIBA” állítása csak `[ELLENŐRZŐ]` előtagú PR-címmel igaz (a PR címe ilyen).
12. (alacsony) **G4152 sz7 fordítás:** „and we find it opposed to σωματικον in Plutarch” → „és ezzel szemben találjuk: σωματικον Plutarkhosznál” — a jelentés megfordul (helyesen: Plutarkhosznál a σωματικόν ellentéteként áll).

## Összegző tábla

| tétel | eredmény | súlyosság |
|---|---|---|
| 0 modell | EGYEZIK | — |
| CI (futtat.py) | EGYEZIK (`[ELLENŐRZŐ]` címmel 0 HIBA) / ELTÉRÉS (E16 más címmel) | alacsony |
| 1 teljesség (71; 10 görög; ±1 vers) | EGYEZIK; a Károli- és a szótár-háló újramérése nem ellenőrizhető | — |
| 2 12 jelölt / 3 új előfordulás | EGYEZIK | — |
| 2 1Kor 2:15 a negatív kritérium ellen | ELTÉRÉS | közepes |
| 2 a mérce következetessége | ELTÉRÉS | közepes |
| 2 Fil 1:27 ↔ Luk 1:46–47 határkártya | EGYEZIK (jelölve) | — |
| 3 DT502, szótári gerinc | EGYEZIK; G5590 2. címke szűk | alacsony |
| 4 1/a 11 sor (forma, idézet, tény) | EGYEZIK | — |
| 4 1/a proveniencia (DT28) | ELTÉRÉS | közepes–alacsony |
| 5 számok, Thayer, πνοή | EGYEZIK | — |
| 5 Drash ↔ vitatott pont, A1 | ELTÉRÉS | közepes |
| 5 Remez, Jób 7:11, „három helyen” | ELTÉRÉS | alacsony |
| 6 archív, E27, E28, res_forras | EGYEZIK | — |
| 7 lexikon_general nulladiff | EGYEZIK (statikus); újragenerálással nem ellenőrizhető | — |
| 8 fordítás formája / hűsége | EGYEZIK / 1 ELTÉRÉS (G4152 sz7) | alacsony |
| 9 `9_` v1, MUNKAMENET, `dontesek/uj`, `nyitott/uj` | EGYEZIK; DT586 „(b)”, N92 3/4 | alacsony |
| E17 Δ-bontás | EGYEZIK | — |
| 0.1 előfeltétel a naplóban | nem ellenőrizhető | — |

Megjegyzések az ellenőrtől: a B5 jelöltminősítést az orkesztrátor hozta meg felhatalmazással (a brief 2c szerint ez a felhasználóé; a megbízó jóváhagyottnak adta meg); a végrehajtó a briefben `vegrehajto-sonnet`, ténylegesen `general-purpose` subagent (a napló indokolja); Fable-kör nem futott, `kiadasok.tsv`/`lap_atnezesek.tsv` nem változott.
