ELTÉRÉS: 2 tétel

# ELLENOR_F145_2 — F145_THAYER_KAPU_JAVITAS_BRIEF.md · 84ac013d..761a3675 (2. javítókör újraellenőrzése, ág ccr-4d66ac1d-v5f9un)

Ellenőr modellje: `claude-opus-5-5`, a kért `opus`, egyezik. (Az ellenőr nem tudott fájlt írni; az orkesztrátor mentette, a táblázatot tömörítve, a tételeket tartalmilag változatlanul.)

**ELTÉRÉSEK, súlyossági sorrendben:**

1. **Zárónapló és brief-fejléc elavult (A2):** a `naplok/F145_zaras.md` 3. sora még az általános „nagybetűs-folytatású műcím” szabályt írja le; a 8. sor nyitottként sorolja a már megszűnt „átvétel-szabály ismert határát”; a 6. sor `teszt_lanc.py 32` tesztet ír, a napló szerint most 34 van. A brief `ad` és `lezarva_osszegzes` mezője az általános műcím-kivételt állítja, holott az F145.14 óta csak a G0012-re szól. A 2. körben a zárónapló nem módosult (`git diff --stat 84ac013d..HEAD -- naplok/F145_zaras.md`: üres).
2. **Nem diszkriminatív bizonyíték az F145.14 naplósorban (`naplok/F145_naplo.md:142`):** az 5 Strongra („bájtra azonos”, `F145_meres.py --gyoker .`) vonatkozó mérés olyan fán futott, ahol a `thayer_sigla.tsv` minden sigla-sora `javaslat` állapotú (besorolt: 0, javaslat: 91), így a 16_sigla semmit nem ellenőrzött, és az előtte/utána egyezés semmit nem bizonyít. Az eredmény a #142 fájának adataiból levezetve helyes (a 19 `sz<n>` fordítássorban egyik sigla sem áll fordítatlanul), a naplóbeli bizonyíték viszont nem.

**Rendben (kódolvasás):** az `_atvett` csak az `ATVETEL_KIVETEL` (sigla, ablak) párra ad True-t (`thayer_kapuk.py:108-116, 135`); a `ROVIDITES` és a nagybetűs-követő-szó feltétel kikerült; a `cf.`/szerző-típusú fordítatlan sigla SERTES (`teszt_lanc.py:193-219`); a G0012 ablak egyedi a forrásban; a Strong csak dokumentáció (a hívó nem adja át); SEMA 2.37 egyezik a kóddal; hatókörön kívüli fájlok (`forditas_kapuk.py`, `normalizal.py`, adat/*.tsv) érintetlenek; E12–E15 0; CI-futtatás E2–E32 0 HIBA a változott fájlokon.

**Nem ellenőrizhető:** a tesztek zöld állapota (az ellenőr nem futtathatja), a #142 fáján a kapu tényleges viselkedése (csak levezetve).

**Megjegyzés (ellenőr):** a DT „Strong + sigla + ablak” kulcsot ír, a megvalósítás csak a (sigla, ablak) párt egyezteti; ha más Strong forrásába bekerül ugyanaz a cím, a kivétel arra is kiterjed. Az indok dokumentált.
