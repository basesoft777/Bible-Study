# Olvasói szint — tervezési napló

Rögzítve: 2026.09.08. Státusz: KONCEPCIONÁLIS FÁZIS, pilot előtt — nincs jóváhagyott implementáció, nincs script, nincs kiválasztott pilot-dokumentum.

## 1. Előzmény és probléma

A studyk és a lexikon-cikkek jelenleg munkapéldányok: a nekem (Basesoftnak) szóló napló-/folyamat-üzenetek (dátumok, "TSK-eredetű", audit-eredmények, döntési indoklások) keverednek az olvasói prózával — van, hogy egy mondaton belül is. Ez a lexikon-cikkeknél is fennáll, ott ráadásul több technikai infó (Strong-számok, táblázatok) is terheli a szöveget.

Konkrét példa a `Segitsegul_hivni_az_Urat_tematikus.md`-ből — három, egymástól eltérő, inkonzisztens napló-jelölési minta ugyanabban a fájlban:
- `*(új, 2026.09.06, TSK-eredetű)*` (dőlt zárójeles címke táblázat-cellában)
- `**2026.09.05-i teljes v12-compliance frissítés:**` (félkövér dátumos bekezdés-nyitó)
- `*(Módszertani megjegyzés, 2026.09.05: ...)*` (dőlt zárójeles bekezdés)

Ez a három forma egy script számára megbízhatóan nem különíthető el egymástól és a sima prózai dőlt/félkövér szövegtől.

## 2. Cél

Olyan olvasóbarát változatot előállítani a munkapéldányokból, ami:
- nyomon követhető, reprodukálható folyamat eredménye — nem persona/skill szabad improvizációja,
- skálázható (bármelyik studyra/lexikon-cikkre alkalmazható),
- tudományos irányból közérthetőbb irány felé mozdít,
- megőrzi a "konfigurációt" — a munkapéldány marad az egyetlen forrás, minden infó megmarad benne, az olvasói változat mindig ebből generálódik.

## 3. Első javaslat (chat, 2026.09.08) — elvetve

Három diszkrét szint: TUDOMÁNYOS (munkapéldány) / KÖZÉRTHETŐ (a meglévő `ISTENTISZT-001_OLVASHATO.md` mintája) / EGYSZERŰSÍTETT (rövidebb mondatok, minimalizált idegen szó). Basesoft elvetette: a TUDOMÁNYOS→KÖZÉRTHETŐ ugrás túl nagy, "szélső tengely" — finomabb, kisebb lépésközű hangolhatóság kell.

## 4. Módosított javaslat — többtengelyes, finomhangolható konfiguráció

Egy szó/név helyett 4, egymástól független paraméter, mindegyik 1-5 fokozattal, mindegyik fokozathoz írott, rögzített rubrikával:

| Paraméter | Mit szabályoz | 1. fokozat | 5. fokozat |
|---|---|---|---|
| Terminológia-szint | eredeti nyelvi szavak/Strong-számok jelenléte | teljes (héber/görög írásjel + Strong + transzliteráció mindenhol) | csak magyar körülírás, idegen szó minimális |
| Apparátus-szint | táblázatok/napló-jelölés megtartása | teljes táblázat + napló-jelölések láthatók | táblázat nélkül, folyamatos próza |
| Mondatszerkezet-szint | mondathossz, alárendelések száma | technikai, több tagmondatos | rövid, egyszerű mondatok |
| Indoklás-sűrűség | mennyi "miért így és nem másképp" marad | teljes érvelési lánc látszik | csak a végkövetkeztetés, indoklás nélkül |

Példa konfiguráció: `terminologia=3, apparatus=1, mondat=2, indoklas=4` — táblázatok eltűnnek, héber szavak félig megmaradnak, mondatok kicsit egyszerűsödnek, indoklás majdnem teljesen megmarad.

Tervezett hívási forma (még nem implementálva): `olvasoi_valtozat_generalo.py --terminologia N --apparatus N --mondat N --indoklas N`

## 5. Kapcsolódó, megoldandó gyökér-probléma

A fenti négy paraméter csak akkor működtethető megbízhatóan, ha előbb:
- a napló-/folyamat-jelölés egységesítve van egyetlen, sosem máshol előforduló jelölőre (javaslat, még nem elfogadva: `【NAPLO: ...】`),
- új írási szabály tiltja a mondaton belüli keveredést (próza és napló-infó soha ne legyen ugyanabban a mondatban) — enélkül semmilyen script nem tud kockázat nélkül szétválasztani.

A meglévő, lezárt studykban a napló-infó jelenleg vegyes formátumú (l. 1. pont) — ezeket egy egyszeri, retrospektív átalakítással kellene egységesíteni, mielőtt bármelyik script rajtuk futtatható lenne.

## 6. Döntés

Basesoft: "pilotozni kellene" — a 4 paraméter fokozatainak konkrét rubrikáját, az egységes napló-jelölést és a script-koncepciót **egy kiválasztott dokumentumon kell először kipróbálni**, mielőtt bármi bekerülne a `study-rules.md`-be vagy a `method-learnings.md`-be mint kötelező szabály.

## 7. Következő lépés

Nincs kiválasztott pilot-dokumentum. Amikor Basesoft kijelöli, a pilot lépései: (a) az egységes napló-jelölés bevezetése abban az egy dokumentumban, (b) a 4 paraméter fokozatainak első, konkrét, írott rubrikája, (c) kézi (nem script-alapú) próba-generálás legalább 2-3 eltérő konfigurációval, (d) Basesoft értékelése, mielőtt a script vagy a sablon-fájl (`7_PaRDeS_olvasoi_szint_sablon.md`) elkészülne.

Forrás: chat-alapú beszélgetés, 2026.09.08.
