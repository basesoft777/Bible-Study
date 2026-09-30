# F21P_arany_v2_diff.md — az Opus-arany v1 -> v2 változásai

<!-- GENERÁLT: eszkozok/karoli_strong/c_diff.py (az arany_v2.JAVITASOK és a két arany alapján) | scope=f21p/arany_opus.jsonl -> f21p/arany_opus_v2.jsonl (60 vers) | forras=f21p/arany_opus.jsonl, f21p/arany_opus_v2.jsonl, f21p/arany_opus_v2.sha256, eszkozok/karoli_strong/arany_v2.py (JAVITASOK), f21p/valaszok/F3.jsonl, f21p/c_diff_besorolas.tsv | ts=2026-09-30T13:12:52+00:00 (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos -->

A v2 a v1 másolata, csak a f21p/arany_opus_jegyzetek.md 2. szakaszának konvencióival ütköző versek javultak (felhasználói döntés, F21.12). A v1 érintetlen. **A v2 jóváhagyásig nem fagy be.** A konvenció-azonosítás és az indok kézi ítélet (Opus).

| vers | régi link (v1) | új link (v2) | sértett konvenció | indok | hatás a C diffre |
|---|---|---|---|---|---|
| 2Móz 25:8 | —; betoldas: [7] -> [] | 7 ő -> 10 ם H9028 [them] | K4 (2. szakasz 4.: birtokos és névmási ragok — ha a magyar külön névmást is kitesz, a névmáshoz is) | az ő közöttök archaikus birtokos szerkezet (vö. az ő ura): az ő a -ām („őket, köztük”) rag külön kitett névmása, nem az 1. személyű ige alanya; a v1 tévesen K6-ként (betoldas) kezelte | (b) tobblet 7->10 -> egyező |
| 2Móz 26:13 | 24 másfelől -> 26 וּ H9002 [and]; forditatlan: [2, 7, 16, 22] -> [2, 7, 16, 22, 26] | — | K9 (2. szakasz 9.: le nem fordított ve-/kai forditatlan) | a וּ (26) a magyarban nem a másfelől része; a v1 a másfelől-höz kötötte, ami a K9-cel ütközik. Nyitott: a K9 szerint az is-hez is köthető volna (egyfelől is másfelől is), de az is betoldas-a a 6. táblázat dokumentált döntése, ezért a v2 a minimális javítást (forditatlan) alkalmazza | (a) hianyzo 24->26 -> egyező |

Összesen: 2 vers változott; a C diffjében 2 eltérés szűnt meg ((a)->egyező: 1, (b)->egyező: 1), 0 új keletkezett.

## Nem javított esetek (kérdések, felhasználói döntésre)

- **Tárgyragok (a döntés K3-at nevezett meg).** A K3 csak a tárgyjelölő *'et* + névmási rag esetét szabályozza (az *'et* forditatlan, a magyar névmás a ragra megy). A kérdéses eset más: tárgyi rag az igén, külön magyar névmás nélkül (a határozott ragozás jelöli). Az aranyban 4 ilyen van: 2Móz 21:6 #11 (*állítsa*) forditatlan; 2Móz 21:26 #16 (*elpusztul*), Péld 30:17 #11 (*kivágják*) és #16 (*megeszik*) az igéhez kötve. Egyik konvenció sem mondja ki ezt az esetet (a K4 a birtokos személyragról szól), ezért nincs megnevezhető konvenciósértés; nem javítottam. Opció: (a) az igéhez kötni mind a négyet (a 2Móz 21:6 #11 -> *állítsa*); (b) forditatlan mind a négy; mindkettőhöz új konvenció kell a jegyzetbe.
- **„való” (2Pét 1:7 kötve, Péld 30:17 *iránt való* betoldas).** Nincs rá konvenció a 2. szakaszban (a K2 a kettéírt kötőszókról és a vonatkozó névmásokról szól); nem javítottam. Opció: új konvenció a „való” melléknévi szerkezetre (kötve a főnévhez, vagy betoldas).
- **Ez 39:13 *megdicsőítem*.** A -י (H9040) rag a *magamat*-hoz kötött; a K4 a „birtokos személyragot viselő magyar szóhoz” köt, a *megdicsőítem* igei személyrag, nem birtokos. Nem megnevezett K4-sértés; nem javítottam. Kérdés: kiterjed-e a K4 az igei személyragra.
- **2Móz 26:13 *is* (23, 25).** A K9 szerint a *ve-* az *is*-hez is köthető volna, de az *is* betoldas a 6. táblázat dokumentált döntése; a v2 a minimális javítást alkalmazta (forditatlan). Kérdés: az *is*-hez kerüljön-e.

**Befagyasztva 2026.09.30, felhasználói jóváhagyással** (F21.14). sha256 (LF-normalizált tartalom): `06a00738f7fd044920ffa79e023b71840d4ba4d04c91ab64d2eb655f1f4a8bb2` — f21p/arany_opus_v2.sha256; az arany_ellenoriz.py, a meres.py és a c_diff.py eltérésnél hibával megáll.

