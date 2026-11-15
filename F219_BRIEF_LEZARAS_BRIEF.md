---
feladat: 219
cim: Gépi lezárás a merge-kor — a mergelt PR briefje `lezarva`, a `lezar:` N-tételek lezárva
kod: BRIEF_LEZARAS
tipus: feladat
fazis: folyamat
sav: SYSTEMS
modell: sonnet
allapot: fut
ad: a main-re futó `feladatok.yml` a mergelt PR briefjét `lezarva`-ra állítja (ha csak a merge volt hátra), és a `lezar:` N-tételeit lezárja; a kapu jelent, ha egy mergelt brief nincs lezárva, vagy egy lezárt brief N-tétele nyitva maradt
kovetkezo: "Te: a draft PR áttekintése és merge-e"
munka: folyamat
olvas: [CLAUDE.md, .github/workflows/feladatok.yml, eszkozok/gepi_commit_uzenet.py, F201_SZAMKIOSZTAS_BRIEF.md, F217_GENERALAS_MAINEN_BRIEF.md, NYITOTT_FELADATOK.md]
ir: [eszkozok/brief_lezaras.py, eszkozok/teszt_brief_lezaras.py, eszkozok/gepi_commit_uzenet.py, eszkozok/feladatok.py, BRIEF_SABLON.md, .github/workflows/feladatok.yml, .github/workflows/ellenorzes.yml, dontesek/uj/dreamy-hugle-c875f6.md, dontesek/uj/f219b-lezar-kapu.md, F219_BRIEF_LEZARAS_BRIEF.md, F220_HETI_ATTEKINTO_BRIEF.md, F221_VEDOSZABALYOK_BRIEF.md, naplok/F219_jelentes.md]
fugg: []
nem_fugg: [201, 212, 216, 217]
ag: claude/f219b-lezar-kapu
---

# F219_BRIEF_LEZARAS_BRIEF.md — Gépi lezárás a merge-kor

*FELADATOK #219 · Modell: sonnet · v1 · 2026.11.15*

**Jóváhagyás (a felhasználó, 2026-11-15, az orkesztrátor közvetítésében), szó szerint:** „Igen, indítsd”.

## Gyökérok (M-GAZDÁTLAN)
A session a draft PR-nál zárja a menetét, a fejlécébe „megállt / Te: merge” kerül; a merge később, a session nélkül történik, és utána semmi nem állítja `lezarva`-ra. Így lett 35+ mergelt, de nyitottnak látszó brief; az N-tételek lezárása ugyanígy kézi, és elmarad (265 nyitott sor).

## A. Lezárás a merge-kor (Action)
- `eszkozok/brief_lezaras.py` (`--szaraz` / `--ir` / `--kapu`): a `feladatok.yml`-be épített lépés (a szamkiosztas után, az `ellenoriz` és a FELADATOK.md-generálás előtt; egy futás, egy commit, F201). Állapotalapú és idempotens.
- A lezárás feltétele (a mai fejlécmezőkből; részletesen a szkript docstringjében): `fut`/`megallt` feladat vagy naplózás; a `kovetkezo` `Te:`-vel kezdődik, megnevezi a merge-et, és mást nem nevez meg; az `ag:` (vagy `pr:`) szerinti PR-merge a main first-parent történetében van; és az `allapot`/`kovetkezo`/`lezar` a PR ágán ugyanaz, mint ma (a merge óta nem folytatódott a menet).
- `lezar: [N…]` fejlécmező: az N-tételek a `NYITOTT_FELADATOK.md`-ben a meglévő formában zárulnak (`**N<n> — LEZÁRVA (dátum, a #PR merge-ével, F<nn>) — …`).

## B. Kapu (a #734 `sav` PR mergelése után; kész: F219 B. rész PR)
`feladatok.py ellenoriz`: JELENTÉS (nem HIBA), ha (1) a brief PR-ja mergelve, de a fejléc nem `lezarva`; (2) a lezárt brief `lezar:` tétele nyitva maradt. A logika kész (`brief_lezaras.kapu_jelentesek`); a bekötés, a `lezar` kulcs a `KULCSOK`/`LISTA_KULCSOK`-ban, a brief-sablon és a séma csak a másik session (local_b39fa535) PR-ja után, az ütközés elkerülésére.

## Megkötések
Brief-fejlécet és a `NYITOTT_FELADATOK.md`-t ebben a menetben kézzel nem szerkesztünk; a régi esetek takarítása a #sav PR-é. ⛔ A merge nem ennek a sessionnek a dolga.

## B. rész (kész)
- `feladatok.py`: `lezar` a `KULCSOK`/`LISTA_KULCSOK`-ban, az azonosító alakja ellenőrzött (`N12`, `N-F219a`; HIBA); az `ellenoriz` `JELENTÉS` sorokat ad (nem HIBA) a mergelt, de nem lezárt briefekről és a nyitva maradt `lezar:` tételekről.
- `BRIEF_SABLON.md`: a `lezar` mező és a kanonikus `Te: … merge` alak; a hatókör-szűkítés szabálya (DT-F221a, a #733 kész szövege, ugyanaz a fájl).
- A `sav` mező hiányát pótoltam a három, a #734-gyel párhuzamosan mergelt briefben (F219, F220, F221: SYSTEMS), mert a main `ellenoriz`-e emiatt piros volt.
