# HATAR_ANTROP-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ANTROP-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ANTROP-001 | ts=2026-11-03T09:25Z | bemenet=adat/elofordulasok.tsv@b120d694f9,adat/motivumok.tsv@8b8bf2c709,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ANTROP-001 — Pneuma/pszükhé megkülönböztetés · hordozó: `lexikai` · fölérendelt fogalom: az ember belső élete, lelke és szelleme általában, a két szó megkülönböztető együttállása nélkül · beépített sor: 11 (11 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), ANTROP-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (11 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | ANTROP-001 versei | másik versei | közös | közös/ANTROP-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 11 | 75 | 0 | 0% | 0% | nincs |
| HAMART-001 | 11 | 77 | 0 | 0% | 0% | nincs |
| HODIT-001 | 11 | 33 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 11 | 22 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 11 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 11 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 11 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 11 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

**a hordozó lexikai: a gépi negatív-kritérium próba nem fut.** A hordozó (`azonossag_tipusa`) = `lexikai` (`adat/motivumok.tsv:8`). A #150 szókapcsolat-próbája csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.

## Modelles rész

<!-- MODELLES-KEZDET -->
*A `hatar-ellenor` modelles része nem futott (DT443 után). Az alábbi K1 nem a `hatar-ellenor` kimenete: a #123 ANTROP-001 új cikkének U2-jében az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket és hozza is meg« (2026-11-03) — a Fil 1:27 egyelőre elutasítva, de a hely határkérdés, ezért a felhasználóé (`naplok/F123_ANTROP2_naplo.md` U2). A K2 ugyanígy kézi: az U4 javítókörében (DT-F123r (1)) az 1Kor 2:15 név szerinti kivétellel bent marad, a kérdés a 2. kiadás bemenete. A válaszok következménye az `eszkozok/lektor_felulet/osszefoglalo_ANTROP-001.tsv`-ben.*

**2 kérdés.**

**K1 — Bekerüljön-e a Fil 1:27 („egy lélekben, egy érzéssel”) a motívumba?**
Érintett igehelyek: Fil 1:27, Luk 1:46, Luk 1:47.
**A jelenlegi határ** (az adatból):
- Negatív kritérium (`adat/motivumok.tsv`): a πνεῦμα és a ψυχή (vagy melléknévi alakjuk) egy mondatban áll, és a mondat a kettőt megkülönbözteti vagy szembeállítja; nem tartozik ide, ahol a kettő egymás szinonimája.
- A Fil 1:27-ben a két szó egy mondatban, két mellérendelt tagként áll: „megállotok egy lélekben (πνεῦμα), egy érzéssel (ψυχή)”. A Thayer a πνεῦμα 2. jelentésénél megjegyzi, hogy itt a μία ψυχή helyett „μία καρδία” (egy szív) is állhatna, a ψυχή-nál pedig az ApCsel 4:32 („szíve-lelke egy vala”) mellé, az érzelmek székhelye jelentés alá sorolja: a mondat a két szót nem szembeállítja, hanem párhuzamos tagként említi egymás mellett, együtt a közösség egységét fejezik ki.
- Mégis: a Luk 1:46–47 (Mária éneke) szintén két mellérendelt, párhuzamos tag („Magasztalja az én lelkem … És örvendez az én lelkem”), és bent van, mert mindkét szónak saját igéje van. A „megkülönböztető szerepben” mérce a két helyen nem ad egyértelmű választ.
Válaszok: (a) a Fil 1:27 bekerül, a Luk 1:46–47 mintájára (11 → 12 igehely); (b) kint marad, a Thayer-indokkal (javasolt; a lap határesetként említi).

(proveniencia: scope=adat/jeloltek.tsv (ANTROP-001 Fil 1:27), adat/elofordulasok.tsv (11 sor), adat/thayer_szakaszok.tsv (G4151 -/2/-, G5590 -/2/-) | forras=split('\t') | ts=2026-11-03)

**K2 — Bent maradjon-e az 1Kor 2:15 („A lelki ember azonban mindent megítél”) a név szerinti kivétellel?**
Érintett igehelyek: 1Kor 2:14, 1Kor 2:15.
**A jelenlegi határ** (az adatból):
- Negatív kritérium (`adat/motivumok.tsv`): nem tartozik ide a vers, amelyben csak az egyik szó áll, vagy amelyben a két szó két külön mondatban áll; név szerinti kivétel az 1Kor 2:14–15 ellentétpárja (ψυχικὸς ἄνθρωπος ↔ ὁ πνευματικός), amely egy érvelés két versben.
- Az 1Kor 2:15-ben csak a πνευματικός áll (`scan G4152 --szakasz "1Kor 2:15"`: 1 találat; a G4151, G5590, G5591 nincs a versben). A 2:14 és a 2:15 két mondat, de a 2:15 („A lelki ember azonban …”) a 2:14 kifejezett szembeállítását közvetlenül folytatja.
- Mégis: az ApCsel 4:31–32, 20:23–24, 2Kor 1:22–23 és Luk 9:55–56 helyeken a két szó szintén szomszédos versekben áll, és kint van; ezekben a két szó csak közel áll egymáshoz, szembeállítás nélkül. A csak a πνευματικός szót hordozó többi vers (16 vers, blokk-sor) kint marad.
Válaszok: (a) bent marad, a név szerinti kivétellel (javasolt; 11 igehely); (b) kizárva, az 1Kor 2:14 marad (11 → 10 igehely).

(proveniencia: scope=adat/motivumok.tsv (ANTROP-001 negativ_kriterium), adat/jeloltek.tsv (ANTROP-001 1Kor 2:15, ApCsel 4:31-32, ApCsel 20:23-24, 2Kor 1:22-23, Luk 9:55-56, 1Kor 3:1 blokk), naplok/ELLENOR_F123_ANTROP-001.md 1. tétel | forras=split('\t') | ts=2026-11-03 · scope=range:1Kor 2:15 | forras=TAGNT_kivonat.tsv | strong=G4152 | n=1 | ts=2026-11-03T10:41Z; ugyanígy G4151, G5590, G5591: n=0)

**Felhasználói besorolás** (2026-11-03, a Kiadón; szó szerint: „LEKTOR-VALASZ | hatar:ANTROP-001:mK1 | elfogadom | LEKTOR-VALASZ | hatar:ANTROP-001:mK2 | elfogadom |”, majd: „maradnak”; az orkesztrátor közvetítésével)
- K1: Elfogadom (Javasolt) — a felhasználó döntése, 2026-11-03: a Fil 1:27 kint marad („elfogadom”, „maradnak”); a motívum 11 igehelyes, adat és lapszöveg nem változik. LEZÁRVA.
- K2: Elfogadom (Javasolt) — a felhasználó döntése, 2026-11-03: az 1Kor 2:15 bent marad, a név szerinti kivétellel („elfogadom”, „maradnak”); a motívum 11 igehelyes, adat és lapszöveg nem változik. LEZÁRVA.
<!-- MODELLES-VEGE -->
