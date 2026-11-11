---
feladat: 193
cim: A szabályhelyek igazítása a HAMART-001 új arany szerkezetéhez és a követelménylista döntéseihez
kod: SZABALYHELYEK
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ag: claude/szabalyhelyek-97e545
pr: 687
ad: a sablon 6, 9, 10 és a MUNKAMENET a HAMART új szerkezetét (9. Hatástörténet, 10–12. átszámozva) és a KESZ_LAP_KOVETELMENY (b) és J döntéseit írja elő; az ISTENTISZT-001 prózaírója nem ismétli a „10. Alkalmazás”-hibát
kovetkezo: "Te: a draft PR áttekintése és merge-e; az ISTENTISZT-001 prózája ezután és a visszhang 2 adata (#183) után indulhat (sablon 10 előfeltétel 3.)"
munka: folyamat
olvas: [sablonok/KESZ_LAP_KOVETELMENY.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, MUNKAMENET.md, DONTESEK.md]
ir: [sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, MUNKAMENET.md, .claude/commands/kiadas.md, DONTESEK.md, naplok/ELLENOR_F193.md, dontesek/uj/szabalyhelyek-97e545.md, nyitott/uj/szabalyhelyek-97e545.md, F193_SZABALYHELYEK_BRIEF.md]
fugg: []
---

# F193_SZABALYHELYEK_BRIEF.md — A szabályhelyek igazítása a HAMART új aranyához

*FELADATOK #193 · Modell: opus · v1 · 2026.11.11*

**Indok.** A HAMART-001 lapjára 2026-11-11-én kötelező „10. Alkalmazás” került, mert a sablonok még előírták, pedig a felhasználó kivette („nincs is alkalmazás”). Ha a szabályhelyek nem igazodnak, az ISTENTISZT-001 új cikkének prózaírója ugyanezt a hibát ismétli. Ez a feladat az ISTENTISZT-001 prózájának előfeltétele: a próza csak e PR merge-e után indul.

**Bemenet.**

- `sablonok/KESZ_LAP_KOVETELMENY.md` (main): a (b) lista B01–B19 és a J1–J4, a DT738 szerint lezárva (a felhasználó, 2026-11-11: „Igen, mind”);
- a #182 már igazított egy részt (F182.37; DT755–DT761): B04 (Alkalmazás), B08, B09, B10, B13, és a DT760 (az 1.1–1.2 névszói alcíme);
- a felhasználó további döntései (2026-11-11, az orkesztrátor továbbításában; a közös jegyzetmappa `F183_bemenet_visszhang_foszakasz_2026-11-11.md`):
  1. a visszhang saját főszakasz. Kérdés: „A visszhang 2-vel együtt (ókori fordítások, tanúk, recepció) már túlnő a szótári pont szerepén, és megérdemli a saját főszakaszt, például a 9. Értelmezés előtt. Így legyen?” — „igen”. A cím: **„9. Hatástörténet: ókori fordítások és értelmezők”**, számozatlan alcímekkel („mehet”); utána 10. Értelmezés, 11. Módszertan és nyitott kérdések, 12. Irodalom és idézés. A visszhang 1 és 2 is benne van, és mindkettő az 1. kiadás feltétele: „a visszhang 1-2 kötelező”;
  2. a tanúréteg forrásai: `konkordancia/Tanu_atyak_index.tsv` (HCF), `konkordancia/Tanu_rabbinikus_index.tsv` (Sefaria links, CC BY), és a Chain Lineage Browser tényadatként („mehet”), kettős forrásmegjelöléssel: a böngésző, valamint a BiblIndex (Institut des Sources Chrétiennes, CNRS – HiSoMA, Lyon);
  3. Glossa Ordinaria. Kérdés: „Glossa Ordinaria: szabad forrás nincs. Javaslatom, hogy a követelménylistában a Glossa-sor »nincs szabad forrás, a lap kimondja« alakot kapjon, és ne legyen az 1. kiadás feltétele. Rendben?” — „mehet”;
  4. az alcímek névszói alakúak („1.1 A keresés tárgya · 1.2 A keresés forrásai”), és a lap harmadik személyben szól (B07, DT760).

**Hatókör — ne nyúlj:** `lexikon/`, `eszkozok/lexikon_general.py`, `eszkozok/visszhang/`, `adat/` (a `adat/SEMA.md` is). Ezeken párhuzamosan a #183 dolgozik. A generátor igazítása N-tétel (N-F193a). A `sablonok/KESZ_LAP_KOVETELMENY.md` K-sorait a #183 PR-ja frissíti (K65, K67, K67a–f), ezért ez a feladat nem írja.

## Teendő

| # | Tétel | Hely |
|---|---|---|
| F193.0 | brief, helyőrzős DT és N | ez a fájl; `dontesek/uj/szabalyhelyek-97e545.md`; `nyitott/uj/szabalyhelyek-97e545.md` |
| F193.1 | a lapszabály: v4 szakaszrend (9. Hatástörténet, 10–12.), a Hatástörténet szabályai (visszhang 1 és 2, tanúréteg, Glossa), alcím és hang; az A) rész és a Minőségi kapu elavult pontjai (B01, B02, B03, B05, B11, B12); J1 | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` |
| F193.2 | a forrás- és cikkszabály: a 4. pont szakasztáblája (a lap új számai), J2–J4, a kerek 1/a mintája a HAMART-001-ből | `sablonok/9_PaRDeS_motivum_forras_sablon.md` |
| F193.3 | a próza promptja: a szakaszszámok, a Hatástörténet a próza előtt, J2–J4 hivatkozással, harmadik személy | `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md` |
| F193.4 | a munkamenet: C-vh (a visszhang 1 és 2 a 9.-ben), a lezárás új menete (B06), C-g, C-o, C-v, C5, C-k | `MUNKAMENET.md` |
| F193.5 | a felülírás-jelölések, meglévő sorok szerkesztésével (B17, B19, B04, DT756 számozása) | `DONTESEK.md` |
| F193.6 | egy független ellenőrzés (csak a szabályszöveg), legfeljebb egy javítókör; draft PR | `naplok/ELLENOR_F193.md` |

## Eltérések a bemenettől (a végrehajtó döntése, indokkal)

1. **Részleges felülírás (DT-F193d).** A DT752 jelölése (⛔ + `**FELÜLÍRVA → DT<n>**`) az egész sort érvényteleníti. A DT547-ből csak a lezárás sorrendje avult el (a DT566 tette a Fable-kört az 1. kiadás utánra); a Feed 9. kapuja (olvasói kapu) és a lap megnyitása a kiadás előtt ma is a DT547-ből érvényes (C-o, C-v, K03, K98). Ezért a B17 „felülírta: DT566” jelölése részleges alakot kap: `**RÉSZBEN FELÜLÍRVA → DT566**`, ⛔ nélkül. Ugyanígy a DT276 (Alkalmazás: DT756; tanítói rés: DT643), a DT566 (a lektor helye: DT738, B06), a DT730 (a mért szám a lapon: DT738, B19) és a DT756 (a számozás: DT-F193a).
2. **DT733 (B19).** A B19 szerint a DT733 is „felülírta: a felhasználó 2026-11-10” jelölést kapna. A DT733 viszont maga a felhasználó „semmi helye ott” szavának alkalmazása (a mért pontosság kikerül az olvasóból), tehát nem felülírt, hanem a felülíró. A sor nem kap felülírás-jelölést, csak egy utalást: a DT738 (B19) a lapra is kiterjeszti. Az F35 a leletlista tétele, nem `DONTESEK.md`-sor; jelölése nem e fájl dolga.
3. **A 4.11 helye.** A felhasználó döntése a 4.11 sorsát nyitva hagyta („mutató marad, vagy a blokk megszűnik”), a #183-ra bízva. A szabály ezért csak azt rögzíti, hogy a blokk tartalma egy helyen, a 9.-ben áll; a 4.11 helyén legfeljebb egysoros mutató.

## Megállás

A DT-F193a–c a felhasználó döntéseinek alkalmazása. A DT-F193d (részleges jelölés, az Eltérések 1–2. pontja) a B17 és a B19 szövegétől eltér, ezért javaslatként ment a felhasználó elé; jóváhagyva (2026-11-11, az orkesztrátor továbbításában: „mehet”), 🟢. A merge a felhasználóé.

## Ellenőrzés és javítókör

`naplok/ELLENOR_F193.md`: 10 eltérés. Az egy javítókör (F193.6) javította: az átnézés és a javítókör viszonyát (a változáslista jóváhagyása új átnézési sor a javított lap commitjával, SEMA 2.48), a C-h helyét a kötött sorrendben, a C-o sort, a `/kiadas` parancsfájl szerepleírását, az alcím-szabályt (a DT760 szerint marad az 1.3–1.5), a „visszhang” szó tilalmát (csak rétegnévként), a C-vh kettőzött forrásszabályát (most hivatkozás), a B9 sor 4.11-utalását, a DT-F193d állapotát (🟡) és ezt a fejlécet (`kovetkezo`). Második kör nincs.
