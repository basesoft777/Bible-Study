---
feladat: 35
cim: Régi „Sir” hivatkozások migrálása JSir-re és a „Szentlélek” / „Isten Lelke” helyek egységesítése „Szent Szellem”-re
kod: SIR_SZENTSZELLEM
tipus: feladat
fazis: 1
modell: sonnet
allapot: dontesre_var
ag: claude/f35-sir-szentszellem
ad: a Siralmak régi „Sir” alakú hivatkozásai (jeloltek.tsv, genezis-tanulmány, auditok.tsv scope-ok) JSir-re cserélve vagy dokumentáltan meghagyva; a 9 „Szentlélek”/„Isten Lelke” hely a forrásrétegben „Szent Szellem”/„Isten Szelleme”-re egységesítve; egy szövegcsere-csomag
kovetkezo: "Te: DT-F35a (M1) eldöntése, utána M2 szövegcsere, M3 ellenőrzés, M4 SEMA E9"
olvas: [adat/jeloltek.tsv, adat/auditok.tsv, naplok/EMELES_szentlelek_lista.tsv, adat/terminologia.tsv, eszkozok/lekerdez.py, adat/SEMA.md]
ir: [adat/jeloltek.tsv, adat/auditok.tsv, genezis/, tematikus_lezart/, eszkozok/teszt_lekerdez_sir.py, adat/SEMA.md]
fugg: [28, 34]
---

# „Sir” → JSir és Szentlélek → Szent Szellem (egy csomag)

## Háttér
Az F28 a Lam → JSir átnevezést vezette be (konkordancia/Konyv_normalizalo_tabla.tsv). Régi „Sir” hivatkozás maradt: `adat/jeloltek.tsv` 329. sor, `adat/auditok.tsv` 169–171. sor (proveniencia-`scope`), és a genezis-tanulmány („Sir 3:52”). A `lekerdez.py` a régi alakot scope-olvasásban elfogadja (F28.32), tehát a rögzített proveniencia ma újrafuttatható.
„Szentlélek” / „Isten Lelke” (DT25 (a)): 9 hely 5 fájlban (`naplok/EMELES_szentlelek_lista.tsv`), a tanulmányokban és a lexikonoldalak kézi szövegében; további 3 találat GENERÁLT-blokkban (`lexikon/ANTROP-001_TUDOMANYOS.md:71,108`, `TEREMT-001_TUDOMANYOS.md:159`) — ezeket a forrás javítása után a generálás igazítja, kézzel nem írható.

## Lépések
1. **M0 — felmérés (csak olvas):** minden „Sir” (Siralmak) hivatkozás a repóban, megkülönböztetve a Sirák fia (Sir) előfordulásaitól (a Sirák fia „Sir” alakja MARAD). A 9+3 Szentlélek-hely listája kontextussal.
2. **⛔ M1 — döntés az `auditok.tsv` 169–171 scope-jairól:** a proveniencia-sor a lekérdezés saját rögzített adata (CLAUDE.md 1. szabály); átírása érinti az újrafuttathatóságot. Javaslat: a scope maradjon, a régi alak elfogadása (F28.32) marad — de ez tartalmi döntés, a felhasználóé. A jeloltek.tsv 329. és a genezis-tanulmány átírható.
3. **M2 — szövegcsere** a jóváhagyott helyeken (a tsv-ket split('\t')-bel; a tanulmányokban csak az egyértelmű „Szentlélek” → „Szent Szellem”, „Isten Lelke” → „Isten Szelleme”; a ruach-magyarázatot idéző mondatok, ahol a Károli-alakot IDÉZIK, MARADNAK — ezeket külön listázd). 
4. **M3 — ellenőrzés:** `python eszkozok/lekerdez.py` rögzített parancsok n-je változatlan; ellenoriz.py SÉRTÉS 0; a terminológia-kapu jelzése a kézi szövegben 0 (kivéve az idézett Károli-alak).

5. **M4 — SEMA E9-javítás (a felhasználó kérésére csatolva):** az `adat/SEMA.md` két sorát a CI E9 szabálya JELENTÉS-ként jelzi (tartalom szerint: „| numerikus | a BDB számozott sense-ekre tagolja…” és „| binyan-címke | **a BDB az igegyököket binyan szerint tagolja, nem számozott sense-ekkel** …”; a sorszámok az F24-merge óta eltolódhattak). Futtasd `python eszkozok/ellenorzes/futtat.py --teljes`-t, azonosítsd, pontosan mit jelez az E9 (az angol „sense” szó a táblázatcellában), és javítsd magyar szóval úgy, hogy a jelentés ne változzon (pl. „jelentés”). A javítás a SEMA.md egyetlen, külön commitja; ⛔ a szövegváltozat jóváhagyása a felhasználóé, ha az E9 többféle javítást enged. Az `ellenoriz.py` ne változzon.

## Nem cél
Az éles `lexikon/` újragenerálása; a tanulmányok tartalmi átírása; más SEMA-módosítás.
