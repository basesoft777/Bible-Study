ELTÉRÉS: 4 tétel

# Független ellenőrzés: F179 · origin/main..HEAD (a5977a96..1a5cf583)

*(A `fuggetlen-ellenor` jelentése, az orkesztrátor mentette el, mert az ellenőrnek nincs fájlíró eszköze. Modell: claude-opus-5-5.)*

## Rendben
- A lista a `Konyv_normalizalo_tabla.tsv` Mat..Rev soraiból épül, 27 könyv, őrrel (`eszkozok/general.py:261-271`); más fogyasztó mind a `konyv_teszamentum`-on át megy.
- A teszt tartalmilag lefedi a 27 rövidítést és a Gal 3:13-at (nem futtatta az ellenőr).
- Mérés a main adatán: HAMART-001 = 52 sor, 43 ÓSZ / 9 ÚSZ. A brief 42/6-a a #639 ágának 48 soros állapota. Csak a HAMART-001 érintett.
- A diff nem módosít lapot, adatot, TSV-t (Δ = 0). E12–E15: 0. Saját `futtat.py --valtozott`: exit 0.
- N-F09f kódszinten jogosan lezárva.

## Eltérések
1. A brief `allapot: lezarva`, de a „Kész” feltétel nem teljesült: a main-beli HAMART-001 TUDOMANYOS (789–793. sor) és TORZSCIKK (955–959. sor) lapon a Gal és az Mk továbbra is a LXX-táblában áll; az `ad` mező „újragenerálva”-t állít.
2. A döntésigény (HAMART-lap újragenerálása A/B/C) és az `n14_hamart_betoltes.py:389` nyitott listája nincs `dontesek/uj/` (DT-F179a) és `nyitott/uj/` (N-F179a) helyőrzőben rögzítve.
3. Kitalált adat a `naplok/F179_jelentes.md` 34. és 43. sorában: „Ján 3, Mt 3” és „3 Ján-sor”; valójában 0 Ján-sor van, a HAMART-001-ben Mt = 1. A 43/9 végösszeg helyes. A kapcsolódó n14-hatásindoklás téves.
4. A `naplok/F179_zaras.md` nincs a brief `ir` mezőjében (kicsi).

## Nem ellenőrizhető
Teszt-futás, olvasói kapu, a „62 sor / 43/9 a lapon” generált érték, CI-jelentés.
