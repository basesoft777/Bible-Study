# Frázis-keresési módszertan — README

*Rögzítve: 2026.09.05, a "Segítségül hívni az Urat" tematikus study
friss auditja során kifejlesztett módszer alapján.*

## Mikor használd

Ha egy motívum egy **több szavas, rögzült formula** (pl. "קָרָא בְשֵׁם
יְהוָה" — "segítségül hívni az Úr nevét"), NEM pedig egyetlen ritka
szótő — a puszta Strong-szám grep ilyenkor használhatatlan, mert az
egyes szavak önmagukban túl gyakoriak (l. `frazis_kereses_pozicio_
alapon.py` docstringje a konkrét példával: 153 nyers találat vs. 11-13
valódi).

## A 3 lépés

1. **Kalibráció** — mérd meg a tényleges szó-távolságot a már ismert,
   biztos találatokban. Ne találgass ablakméretet.
2. **Szűk ablak, explicit ellenőrzés** — keress a kalibrált távolságon
   belül, a releváns "harmadik szereplő" (pl. isteni név) közvetlen
   szomszédságában.
3. **Bővített ablak + anafora-teszt** — nézz körül a szűk ablakon
   kívül is (hamis-negatív teszt), és fogadd el a névmásos
   hivatkozásokat IS, ha az előzmény korábban a versben szerepel.

## KRITIKUS SZABÁLY

**A 3. lépés kimenete SOHA nem építhető be automatikusan.** Minden
"anaforikus" jelöltet egyenként, tartalmilag kell ellenőrizni — a
2026.09.05-i futtatásnál 7 jelöltből csak 3 volt valódi, 4 hamis
pozitív volt (homonim szerkezet, más jelentésű "név"-használat).

## Kiegészítő ellenőrzési rétegek (ajánlott, nem kötelező)

- **LXX-keresztellenőrzés**: ha a görög fordítás következetesen
  ugyanazt a kifejezést használja a biztos találatoknál, ez megerősítés
  — de ne várj tökéletes egyezést (a 2026.09.05-i esetben 3 különböző
  görög ige fordult elő ugyanarra a héber szerkezetre: ἐπικαλέομαι,
  καλέω, βοάω — a fordítói hagyomány nem mereven egységes).
- **TSK-kereszthivatkozás**: ha a hagyományos kereszthivatkozási
  adatbázis (`TSK_kereszthivatkozasok.tsv`) is összeköti a jelölt
  igehelyet egy már ismert találattal, ez további megerősítés — de
  hiánya NEM zárja ki a valódiságot (a projekt saját lexikai
  megfigyelése lehet erősebb, mint a hagyományos kereszthivatkozás).

## Alkalmazási precedens

Első alkalmazás: "Segítségül hívni az Urat" tematikus study, 2026.09.05.
Eredmény: a korábbi 11 ismert igehely mellé 2 új valódi találat került
(Zsolt 105:1 / 1Krón 16:8, párhuzamos szöveg; Ézs 12:4), miközben 5
hamis jelölt (Ézs 43:1, 44:5, 45:3, Ruth 4:11, 4:14) helyesen
kiszűrésre került.
