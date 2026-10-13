# ELLENOR_F94_3 — szűkített harmadik ellenőrzés

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`; kért: `opus`, egyezik). Tartomány: f736257a..b285a3b8 (71eb0a4e, f250bd05, b285a3b8, a 05aecde9 és 8cf83310 fejléc). A jelentés szövegét az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze); tömörített másolat, érdemi változtatás nélkül.*

**Eredmény: ELTÉRÉS, 1 tétel (A3). A többi pont rendben.**

## Az eltérés (A3, alacsony–közepes: adat és dokumentáció)

A *megevék* `mult.E3` jegye a Károli mind a 4 előfordulásában hibás: T/3 tárgyas, többes alannyal (2Krón 30:18, Ezsd 6:21, Mk 4:4, Luk 8:5). Az *evék* 2 helyen szintén T/3 tárgyas (2Móz 16:35, Ján 6:58); a többi *evék* és mind a 9 *ivék* E/3, ott a javítás helyes. A napló 18.2, az N-F94e „LEZÁRVA” szövege és a zárójelentés 5. sora a *megevék*-et helyes E/3-ként tünteti fel; az N-F94h csak általánosan írja le a kétértelműséget, ezt az esetet nem nevesíti. A DT140 a felhasználó döntéseként kifejezetten felsorolja a *megevék*-et, ezért ez döntést igényel. Lehetőségek: (a) az N-F94h nevesíti a *megevék* és az *evék* T/3 esetét, a 18.2 pontosul, a jegy marad; (b) a felhasználó más jegyről dönt.

## Rendben (saját lekérdezéssel)

- **A1:** a `karoli_szotari_alak.tsv` 71eb0a4e-ben csak a `regies_jegy`-ben változott: 4 adatsor (*Evék, evék, ivék, megevék*, `mult.E1` → `mult.E3`) + a `# GENERÁLT` sor hibrid-sha256-ja; sorszám (Δ0), sorrend, fejléc, minden más bájt azonos.
- **A2:** a `hibrid.py` diffje: csak az `evék`/`ivék` került át a `_j('mult.E1', …)` listából új `_j('mult.E3', …)` sorba; alakra szabott egyéb változás nincs; a vevék/tevék/vivék és összetételeik maradnak `mult.E1`.
- **B1:** 3 232 jegyes sor. **B2:** `random.Random(20261013).sample(jegyes, 100)`, determinisztikus (a futtatás nem ellenőrizhető; kódolvasással OK); 16 mintasor egyezik a táblával. **B3:** mind a 100 sor `ellenorzes=modell_ellenorizetlen`, proveniencia-sor és SEMA 2.27 leírás rendben. **B4:** 26 sor szúrópróba, 26/26 egyezik a végrehajtó besorolásával (19 helyes jegy, 6 hibás, mind *-ék* ige). **B5:** a Wilson-intervallumok kézzel számolva: 6/100 → 2,8–12,5%; 0/100 → 0–3,7%; táblaszinten 194 (90–403) sor.
- **C1–C6:** brief v1.2 K6-szöveg, DT140 🟢, N-F94h, a zárójelentés (11 sor), a 16.5 és 17.3 pontosítása, az *érte* határeset — következetes. Megjegyzés: a K6 „jegyes alak” halmazába a K tábla és a kivételtábla jegyes sorai is beletartoznak (267 sor, mind ige).
- **D1–D2:** CI exit 0 (E25: 3, E27: 33 régi, az ág fájljain kívül); nincs abszolút útvonal, `csv` modul, Bible Discovery- vagy emMorph-tartalom a hozzáadott sorokban.
- Ellenőrzési lista 1–5 rendben (törölt sor 0; sorszám-Δ; a nulla-diff hatóköre: a `GENERÁLT` sor és a jegyhelyesség kivételével; ⛔ pontok).

## Megfigyelés (nem eltérés)

A `karoli_szotari_alak.tsv` `# GENERÁLT` sorának `ts=2026-10-13T17:00Z` értéke az újragenerálás után változatlan maradt (valószínűleg explicit `--ts`); a hibrid hash-e frissült, így a változat azonosítható, de a `ts` nem a tényleges futás ideje.

## Nem ellenőrizhető az ellenőr szerepéből

K2/K3 saját futtatása; a minta-szkript tényleges futtatása; a tábla `565e1f573ef8` hash-ének újraszámolása (a `git log` szerint a tábla 71eb0a4e után nem változott).

## Lezárás

Nem zár eltérés nélkül: az A3 a felhasználó döntésére vár.
