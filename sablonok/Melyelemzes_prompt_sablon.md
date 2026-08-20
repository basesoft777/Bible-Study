# Mélyelemzés prompt sablon

Ez a sablon egy AI-asszisztensnek (pl. Claude) szánt prompt-váz, amivel egy adott szentírási szakasz vagy több párhuzamos szakasz mélyelemzését lehet kérni.

## Cél
[Rövid leírás: mit kell elemezni, és milyen mélységben]

## Bemeneti szakaszok
- [könyv fejezet:vers(ek)]
- [párhuzamos hely 1]
- [párhuzamos hely 2]

## Elvárt módszertan
1. Minden szakaszt elemezz PaRDeS szerint (Pshat, Remez, Drash, Sod) — ld. [2_PaRDeS_bovitett_sablon.md](2_PaRDeS_bovitett_sablon.md)
2. Vesd össze a szakaszokat: közös motívumok, terminológia, teológiai ív
3. Emeld ki az eredeti nyelvi (héber/görög) kulcsfogalmakat és ezek kapcsolatát
4. Azonosítsd a releváns motívumokat a [[motivumlog]] naplóhoz
5. Zárd szintézissel: mit tanulunk a szakaszok együttolvasásából

## Kimeneti formátum
- Fájlnév-konvenció: `[Könyv1_fej_vers-Könyv2_fej_vers]_melyelemzes.md`
- Célmappa: `melyelemzesek/`
- Struktúra: ld. [3_PaRDeS_research_sablon.md](3_PaRDeS_research_sablon.md) mint kiindulópont, kiegészítve az összevető résszel

## Minőségi elvárások
- Eredeti nyelvi hivatkozások pontossága (Strong-szám vagy gyök megadása ajánlott)
- Fordítási variánsok feltüntetése, ha eltérés releváns
- Nyitott kérdések explicit jelölése, nem a végkövetkeztetésbe csempészve

## Példa prompt
"Végezz mélyelemzést az 1Móz 14:18-20, Zsolt 110:4 és Zsid 5-7 szakaszokon a fenti módszertan szerint, különös tekintettel a Melkisédek-motívumra."
