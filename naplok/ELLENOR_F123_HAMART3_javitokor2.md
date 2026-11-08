# ELLENŐR — F123.HAMART3 javítókör, 2. ellenőrzés (HAMART-001, .20 → .31, 2026-11-08)

*A `fuggetlen-ellenor` jelentése (claude-opus-5-5, friss kontextus). A subagentnek nincs fájlíró eszköze, ezért a menet
sessionje mentette, tömörítve; a teljes szöveg a menet átiratában van. Tartomány: `e888431d^..e888431d` és
`b70bc688..643562ce`; a d758d040 (main-merge) kívül esik. Kapukat (`ellenoriz.py`, `olvasoi_kapu.py`, `proza_1a.py`,
`nyilt_mag_kapu.py`) a parancskorlát miatt nem futtatott: NEM ELLENŐRIZHETŐ. ELTÉRÉS: 9 tétel.*

**RENDBEN:**
- G1 határ: a kivett 11 hely, a szűkítés és az 1Móz 12:3 „ismétléseinél” megszorítása; DT28, nincs „egyéb” ok;
- G2 Gal 3:10 (az indoklás betűre egyezik), a Gal 3:13-14 1/a prózája (betűre egyezik), a hangnem;
- a Károli-idézetek (14 vers);
- G4 Nave;
- a korábbi 1., 2., 3., 5., 10. és 11. ELTÉRÉS megoldva;
- A2, A3, A5, A6, L1–L5.

## ELTÉRÉS-ek (súlyossági sorrendben)

1. **Testamentum-szám a lapon:** a `lexikon/HAMART-001_TUDOMANYOS.md:105` 43 ószövetségi és 5 újszövetségi helyet mond, az adat szerint 42 és 6 van; a Gal-sorok az ószövetségi LXX-táblában állnak. Generátor-hiba: a `general.py` `UJSZOVETSEGI_TOKENEK` halmazából hiányzik a `Gal` és az `Mk` (N-F09f).
2. **Jel 19:2:** a beépítési indoklás (`jeloltek.tsv`) és a közölt nyílt mag még „ige+tárgy szerkezetet” mond; a görög 1Móz 6:11-ben a föld alany.
3. **Kivonat, 8:21:** az „Új átok a földre ezután nem hangzik el” túl tág, mert a lap maga hozza az Ézs 24:6-ot és az 5Móz 28:18-at; a proveniencia-sor csak az 1Móz 9–50-et fedi.
4. **Motívumnapló:** a kézi szakaszok (`motivumlog/PaRDeS_motivumok.md:476–581`) még a régi határt viszik. HAMART-leletként áll bennük a Gal 3:10, a Jer 17:5, a Jón 3:8, a Hab 2:8 és 2:17 és az 5Móz 27, a „magára veszi” kiemeléssel együtt.
5. **nyilt_angol.tsv:** 8 forrás nélküli elavult sor maradt; az export nem érintett.
6. **38. őr:** az „idéz” kivételére nincs regressziós teszt; a „lánc” és az „együtt” puszta előfordulással is átenged.
7. **A4 és A1:**
   - az 5Móz 28:18 csak a Sod-ban áll, a Peshat, a Remez és a Drash nem hordozza;
   - a 4. nyitott kérdésben a „címzettjei nem zsidók” `manual` jelölés nélkül áll;
   - a „bálványok alatti élet” olvasat a Gal 4:8-9-re épül, a lap viszont csak a 4:3-at idézi.
8. **A Gal 3:13-14 sor-mezői:** a sor határeset, mégis `magas` bizonyosságú, „új lexikai lelet” jelölésű és `Drash/Sod` rétegű, a Sod pedig már nem hivatkozik rá.
9. **E16:** a saját futás szerint HIBA, ha a PR címe nem „[ELLENŐRZŐ]” kezdetű. A cím nem volt ismert.
