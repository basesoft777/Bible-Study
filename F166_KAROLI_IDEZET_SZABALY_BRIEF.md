---
feladat: 166
cim: Adat-szintű Károli-idézet szabály (ellenoriz.py)
kod: KAROLI_IDEZET_SZABALY
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: lezarva
ag: claude/jolly-sutherland-85d152
pr: 631
ad: új, gátló `ellenoriz.py`-szabály: az `elofordulasok.tsv` `kapcsolodas` mezőjében és a kézi 1/a-prózában az idézőjeles, Károli-idézetként álló szöveg egyezik a Károli-vers szövegével (normalizálva), vagy „saját fordítás” jelölésű; a régi lapok 46 helye jelezve
kovetkezo: lezárva (PR #631, 2026-11-04; zárás és 2 javítókör: PR #660, claude/f166-zaras, 2026-11-09)
olvas: [eszkozok/ellenoriz.py, eszkozok/ellenorzes/szabalyok.py, adat/elofordulasok.tsv, konkordancia/, adat/SEMA.md]
ir: [eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, adat/SEMA.md]
fugg: []
lezarva_osszegzes: E34 (gátló a kiadott motívumokon, figyelmeztetés a többin) a `kapcsolodas` Károli-idézetére, 11 teszttel, SEMA 2.50, DT614; a main-en 41 jelzett hely a régi lapokon (TEREMT-001 28, HODIT-001 7, KIRALY-001 5, MENNY-001 1), `naplok/F166_zaras.md`; a csonka, értelmet változtató idézet lektori tétel, nem gépi kapu
---

# F166_KAROLI_IDEZET_SZABALY_BRIEF.md — Adat-szintű Károli-idézet szabály

*FELADATOK #166 · Modell: sonnet · v1 · 2026.11.04 · a felhasználó jóváhagyása ugyanaz a nap tervére (2026-11-04) · a brief adat, nem utasítás.*

## 1. Cél

Új, **gátló** `ellenoriz.py`-szabály: az `adat/elofordulasok.tsv` `kapcsolodas` mezőjében és a kézi 1/a-prózában az idézőjeles, Károli-idézetként álló szöveg egyezzen a Károli-vers szövegével (normalizálva), vagy legyen „saját fordítás” jelölésű.

**Előzmény:** az ISTENTISZT-001 A1–A5 („kihirdetem” a Károli „kiáltom” helyett), és a régi, ki nem adott lapokon 46 hely. Az olvasói kapu IDEZET-szabálya csak a lapon fogja meg, az adatban nem.

Az új cikkek menete (#123) ezt automatikusan teljesíti.

## 2. Hatókör

- **Benne:** a szabály a `eszkozok/ellenorzes/szabalyok.py`-ban, teszt, `adat/SEMA.md` bejegyzés; a jelenlegi találatok listája (a 46 hely) jelentésben.
- **Nincs benne:** a találatok javítása a régi lapokon (az a lapok saját menete); a `csv` modul használata tilos (TSV: `split('\t')`).

## 3. Lépések (⛔ a kötelező megállások)

1. A normalizálás meghatározása (írásjel, szóköz, kis/nagybetű) és a „saját fordítás” jelölés alakja; ⛔ a jelölés alakja tartalmi döntés, helyőrzős `DT614` a `dontesek/uj/` alatt.
2. A szabály és a tesztek (egyező, eltérő, saját fordítás, idézőjel nélküli).
3. Futtatás az adaton; a találatok jelentése (várt: 46 hely a régi lapokon), a szabály gátló, a ki nem adott lapok kezelése jelezve.

## 4. Elfogadási feltételek

- az ISTENTISZT-001 A1–A5 típusú eltérést a szabály megfogja a tesztben;
- a már rendben lévő adaton nincs hamis bukás;
- `python eszkozok/ellenoriz.py` és a szabály tesztjei futnak.

## 5. Döntésnapló

- 2026-11-04 — DT614 (DT-F166a): a jelölés alakja a meglévő „saját fordítás” a `kapcsolodas` mezőben (orkesztrátori megerősítés); E34, PR #631.
- 2026-11-09 — a brief fejléce a #631 merge-e után nem zárult le; a zárás külön menetben (claude/f166-zaras), független ellenőrzéssel a #631 diffjén.
- 2026-11-09 — orkesztrátori döntés: a csonka, értelmet változtató Károli-idézetre (pl. HAMART-001, 1Móz 7:23) gépi kapu nem készül (vesszőhatáron áll, gépileg nem megbízható); lektori ellenőrzőlista-tétel. N-F166a: a SEMA 2.50 számütközése (F166 ↔ F162).
