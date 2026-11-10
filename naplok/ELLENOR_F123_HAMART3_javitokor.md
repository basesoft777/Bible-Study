# ELLENŐR — F123.HAMART3 javítókör (HAMART-001, 2026-11-08)

*A `fuggetlen-ellenor` jelentése (claude-opus-5-5, friss kontextus). A subagentnek nincs fájlíró eszköze, ezért a jelentést a menet sessionje mentette, tömörítve: a tételek, az eredmény és a bizonyíték lényege. A teljes szöveg a menet átiratában van. A második rész a javítókört rögzíti tételenként.*

- **Tartomány:** `b70bc688..ef3a81fc` és `e888431d^..e888431d`
- **Modell-ellenőrzés:** a session `claude-opus-5-5`, a kért modell `opus`, egyezik.
- **Első sor:** ELTÉRÉS: 11 tétel.
- **Futtatott kapuk:** az ellenőr csak a megengedett parancsokat futtathatta (`lekerdez.py`, `futtat.py`). Az `ellenoriz.py`-t, az `olvasoi_kapu.py`-t, a `proza_1a.py`-t és a `nyilt_mag_kapu.py`-t nem futtatta: NEM ELLENŐRIZHETŐ. Ezeket a menet sessionje futtatta a javítókör után (lent).

## RENDBEN pontok

- **G1, a határdöntések:**
  - a 11 kivett hely nincs az `elofordulasok.tsv`-ben;
  - a szűkítés és a kimaradt versek elutasított sora megvan;
  - a `lekerdez.py kollokacio H0779 H0127` öt helyet ad: 1Móz 3:17, 4:11, 5:29, 12:3 és 5Móz 28:18, ez egyezik az indoklással;
  - a Jel 19:2 sorában nincs Jer 51:25;
  - a Gal 3:10 és a Gal 3:13 adatsorai nem változtak;
  - DT28: minden törölt előfordulásnak van elutasított jelöltsora, DT685 hivatkozással;
  - egyik ok sem „egyéb”;
  - az indoklásban nincs belső jel.
- **G2, próza:** a hibás Kivonat-mondat kikerült, a számok egyeznek (49 sor, 56 vers, 1Móz 24, többi ÓSZ 18, ÚSZ 7, tematikus 4; az 577 = 255 + 174 + 36 + 112). A Károli-idézetek szó szerintiek.
- **G3, Nave:** a `title`-ös alak, a karakterkód-javítás és a ragos útvonal nélküli mondat a lapon. A NAVE_ANGOL kapu tesztje bekerült.
- **G4, a 37. és 38. őr:** van kód és teszt. A valódi adaton nem futtatta.
- **G6, generált lapok:** az E28 a kör után 0 hibát ad.
- **A3, A4, A5:** a tematikus címke, a Remez/Sod hivatkozások rétege és a nevesített tanító pontja rendben.
- **L1–L3, L5:** a sorszám-változások bontása, a kulcstartomány, a „nulla-diff” hatóköre és a ⛔ pontok rendben.

## ELTÉRÉS-ek (súlyossági sorrendben)

1. **CI E5 HIBA:** a `lexikon/HAMART-001_TUDOMANYOS.md` görög szavas címsorából kiesett a G1261 (Mt 15:19, Mk 7:21-23) és a G2626 (2Pét 3:6-7), de egyik commit-üzenetben sincs „TÖRLÉS-SZÁNDÉKOS:” jelölés.
2. **Hamis, beégetett mondat a generátorban** (`olvasoi_kovetkeztetes.kizart`): „és a kereszthivatkozások ajánlásait is megnéztük”. Az ALVIL-001 és az ANTROP-001 lapján ez akkor is áll, ha a jelöltek közt nincs TSK-forrás.
3. **N-F123hb felülírva:** négy másik lap is tartalmilag újragenerálódott, pedig az N-F123hb halasztó döntést rögzít. Új döntés nincs mellette.
4. **Az új határmondat ütközik az 1Móz 3:14-gyel:** az 1Móz 12:3 „árar + adámá” határa szó szerint az 1Móz 3:14-re is vonatkozna, abban pedig nincs adámá.
5. **A Gal 3:10/3:13 függő döntése** nincs nyitott tételként rögzítve.
6. **A 38. őr gyenge:** kis-nagybetű-érzékeny, és a szerkezeti szavak listája túl tág. Az „idéz” miatt a Gal 3:10 átmegy.
7. **A `nyilt_angol` +177 sora** kategóriás bontás nélkül, 4 elavult sorral, amelyek forrásszövege már nem létezik.
8. **A Kivonat 8:21-mondata** („A föld megátkozása itt lezárul”) feltételes jelölés nélkül az egyik olvasat felé hajlik.
9. **Jel 19:2:** az „ugyanaz az ige és tárgy” pontatlan, mert a görög 1Móz 6:11-ben a föld alany.
10. **1Krón 20:1:** az összesítő sor szerint a Jer 51:25 „ugyanezzel az okkal” áll kint, pedig az oka más (fizikai pusztítás).
11. **Elavult proveniencia** a „Melyik görög szöveg a mérce” bekezdés alatt: 10 sor áll, a szöveg hét helyet mond.

## Javítókör (F123.HAMART3.30, egy kör)

1. Az F123.HAMART3.30 commit-üzenete tartalmazza a „TÖRLÉS-SZÁNDÉKOS:” sort a görög szavas címsorra. Ok: a G1261 és a G2626 csak a kikerült sorokon állt.
2. A generátorban javítva (`olvasoi_kovetkeztetes.kizart`, teszttel): a mondat csak TSK- vagy Károli-kereszthivatkozás forrás esetén szól a kereszthivatkozásokról. Az ALVIL-001 és az ANTROP-001 lap újragenerálva.
3. Az N-F123hb kiegészítve. Megmondja, miért és mely lapok generálódtak újra (CI E28, NAVE_ANGOL, az orkesztrátor felhatalmazása), és hogy a négy régi lap (HODIT, KIRALY, MENNY, TEREMT-001) továbbra is halasztva van.
4. Az 1Móz 12:3 indoklása pontosítva: „Az átok-formula ismétléseinél a határ…”. Az 1Móz 3:14 a lánc első kimondása, nem ismétlés (`naplok/F123_HAMART3_javitokor2.py`).
5. Új nyitott tétel: **N116** (Gal 3:10 / 3:13, ⛔, javaslattal).
6. A 38. őr szóegyezés-mintája kis-nagybetű-független, új teszttel. Az „idéz” szűkítése az N116 döntésével együtt jár, mert ma csak a Gal 3:10 akadna fenn rajta.
7. **Nem javítva, csak bontás:** a +177 sor táblánként és mezőnként a következő:
   - kizarasok/indoklas 120;
   - elofordulasok/funkcio 49;
   - beepitesi_dontesek/indoklas 10;
   - motivumok 2.

   A 4 forrás nélküli elavult sort a `nyilt_mag_angol.py betolt` nem törli, mert kulcsvesztés-őr védi őket. Az export nem veszi be őket.
8. A Kivonat mondata semleges lett: „Új átok a földre ezután nem hangzik el …”, utalással a vitatott pontokra. A vitatott pontok első olvasata melletti mondat proveniencia-sort kapott (`lekerdez.py scan H0779 --szakasz "1Móz 9:1-50:26"`: 9:25, 12:3, 27:29, 49:7).
9. A Jel 19:2 javítva az adatban és a prózában is: „ugyanaz az ige, ugyanarra a földre”.
10. Az 1Krón 20:1 összesítő sora javítva: „fizikai pusztításként elutasítva áll”.
11. A proveniencia-sor kiegészítve: a mérés a határkör előtti állapoton futott, a mai 7 hely ennek része.

**Kapuk a javítókör után** (a menet sessionje futtatta):

| Kapu | Eredmény |
|---|---|
| `ellenoriz.py` | 0 SÉRTÉS (RENDBEN 27) |
| `olvasoi_kapu.py` | 0 BUKÁS: HAMART-001, ALVIL-001, ANTROP-001 |
| `proza_1a.py HAMART-001` | 49/49 |
| `teszt_ellenoriz_37_38.py` | OK |
| `nyilt_mag_kapu.py`, CI `futtat.py` | a nyílt mag újragenerálása után, lásd a commit-üzenetet |
