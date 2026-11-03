```
ELTÉRÉS: 5 tétel
```

# ELLENŐR, 2. kör — F123_MIGRACIO2_BRIEF.md (ANTROP-001 új cikk, U4 javítókör) · `c332f160..16667248`

*A `fuggetlen-ellenor` jelentése, 2026-11-03 (claude-opus-5-5; modell-ellenőrzés: EGYEZIK). Hatókör: az 1. kör 12 ELTÉRÉS-ének javítása (DT-F123r). Az ellenőr íróeszköz nélkül futott; ez a fő szál által rögzített kivonat az ELTÉRÉS-listából és az összegző táblából, a megfogalmazás az ellenőré. Az ellenőr jelezte: a `futtat.py` kimenetét háromszor a repón kívüli scratchpadbe irányította; a `general.py --ellenoriz` és az olvasói kapu nem volt megengedett parancsa (ezek pontjai NEM ELLENŐRIZHETŐ). A D2 szerint ez az utolsó kör.*

## ELTÉRÉS-ek súlyossági sorrendben

1. **(közepes) A mérce új kizáró jegye ütközik a bent lévő Luk 1:46–47-tel.** A Kivonat kizáró mondatába új jegy került („szinonimaként vagy párhuzamos tagként említi egymás mellett”), az elutasítási ok megjegyzése ugyanígy („például eszközként vagy párhuzamos tagként”); a forrás a bent lévő Luk 1:46–47-et maga írja le párhuzamos tagként (`motivumok/ANTROP-001.md:81`, `:147`; a lap Funkció-oszlopa: „párhuzamos sor, első tag”). A pozitív kritérium „megkülönbözteti vagy szembeállítja”, az 1Pét 1:22, Fil 1:27, 1Pét 3:19–20 új indoklása csak a szembeállítást tagadja (az 1Pét 1:22-é maga ír le szerep-megkülönböztetést). A `motivumok.tsv` kritériuma („egymás szinonimája”) és a Kivonat szétvált. A „két belső összetevő” jegyének kivétele rendben van.
2. **(alacsony)** A K2 lektorsorának proveniencia-mezője a K1-ből másolt (`naplok/LEKTOR_ANTROP-001.tsv:4`); a `HATAR_ANTROP-001.md` K2-jének proveniencia-sora helyes.
3. **(alacsony) DT28: körkörös proveniencia.** A 8 jelöltsor `forras_kereses`-kiegészítése `forras=adat/elofordulasok.tsv (kapcsolodas, funkcio)`, az `elofordulasok.tsv` proveniencia-mezője pedig a jelöltsorra mutat; a jelöltsorok `datum` oszlopa 2026.08.22 maradt.
4. **(alacsony)** A brief `kovetkezo` mezőjének N-F123f-összefoglalója pontatlan: mindkét maradék BUKÁS a BDB H2416 1.a kivonatában áll, a H2416 blokk külön tétel, nem BUKÁS.
5. **(alacsony, rejtett)** Az `_elso_tagmondat` javítása nem teljes: beágyazott zárójelnél az utolsó `(`-nél vág, nem az első nyitva maradónál; `(`-lel kezdődő szövegnél egyetlen „…” marad. Ma egyik lapot sem érinti.

## Összegző tábla (kivonat)

| tétel | eredmény | súlyosság |
|---|---|---|
| 0 modell | EGYEZIK | — |
| 1 kivétel-mondat szó szerint (motivumok.tsv = Kivonat = lap) | EGYEZIK | — |
| 1 csak a 2:14–15 pár (`scan G4152 --szakasz "1Kor 2:15"` n=1, G4151/G5590/G5591 n=0) | EGYEZIK | — |
| 1 K2 határkártya (a)/(b) | EGYEZIK; a lektorsor proveniencia-mezője hibás | alacsony |
| 2 mérce: indoklás, elutasítási ok, Kivonat | ELTÉRÉS (1.) | közepes |
| 3 Drash nem zárja le; nincs jelöletlen történeti állítás; a nevek forrása (archív 78–79. sor) | EGYEZIK | — |
| 4 a 8 sor proveniencia-mezője | EGYEZIK | — |
| 4 jelöltsor-nyom | ELTÉRÉS (3.) | alacsony |
| 4 N-F123j; ALVIL-001-hez nem nyúltak | EGYEZIK | — |
| 5 DT-F123k (b) | EGYEZIK | — |
| 6 G5590 -/2/- címke (2.a–2.c) | EGYEZIK | — |
| 7 Remez, Sod | EGYEZIK | — |
| 8 Jób 7:11 (rúah = lelkem, nefes = szívem; TAHOT-sorrend) | EGYEZIK | — |
| 9 „két hely” | EGYEZIK | — |
| 10 N-F123f számai | EGYEZIK a `nyitott/uj`-ban; ELTÉRÉS (4.) a briefben | alacsony |
| 11 E16 (előtag nélküli címmel 1 HIBA, `[ELLENŐRZŐ]` címmel 0) | EGYEZIK | — |
| 12 G4152 sz7 (jelentés, `kezi`, megjegyzés) | EGYEZIK | — |
| `_elso_tagmondat`, más lap | EGYEZIK statikusan (egy hívó; más lapon nincs érintett sor); rejtett hiba: 5. | alacsony |
| CI a commit-tartományon és az egész PR-on | EGYEZIK: 0 HIBA (a `TÖRLÉS-SZÁNDÉKOS` jelölés a commit-üzenetekben) | — |
| E17 sorszám-Δ; törölt adatsor | EGYEZIK: Δ=0, 0 törölt sor | — |

## Utójavítás (fő szál, F123.ANTROP2.16; harmadik ellenőri kör nélkül, D2)

- **1.** A Kivonat kizáró mondata visszakerült a kritérium szavára („egymás szinonimája”), a Fil 1:27 határesetként jelölve (Mária énekének saját igével álló párhuzamos sorai bent vannak); az elutasítási ok megjegyzéséből kikerült a „párhuzamos tag”. A jelöltsor-indoklások (az orkesztrátor szövege, DT-F123r (2)) és a Fil 1:27 ↔ Luk 1:46–47 kérdés: N-F123k, illetve a K1 határkártya.
- **3.** A 8 jelöltsor forrás-nyoma a próza szerzőjére és a régi szöveg archívumára mutat, nem a céltáblára; a `datum` oszlop: N-F123k.
- **4.** A brief `kovetkezo` mezője javítva.
- **2., 5.:** generátor-korlátok, N-F123k.
