# ELLENOR_F196 — F196_GYOKEROK_KAPUK_BRIEF.md · `7095bc63..4305c992`

*A `fuggetlen-ellenor` jelentése (2026-11-11, modell: claude-opus-5-5). Az ellenőrnek ebben a futásban nem volt fájlíró eszköze; a szöveget a végrehajtó session mentette ide, tartalmi változtatás nélkül, rövidítve a táblázat OK-soraiban. A javítókör: F196.5.*

**ELTÉRÉS: 4 tétel.**

## OK-pontok (összefoglalva)

- **Modell, G1, G2, G4, D1, D2, ⛔, tiltott helyek, helyőrzők:** OK. A diff 8 fájl, mind a brief `ir` listájában; `sablonok/ lexikon/ adat/ konkordancia/ eszkozok/lexikon_general.py eszkozok/visszhang/ DONTESEK.md NYITOTT_FELADATOK.md` diffje üres; végleges DT/N szám nincs. A CI-lépés neve E-szám nélküli, E37-bukás nem várható.
- **Állítás–adat kapu, saját lekérdezéssel igazolva:** kapcsolatok (56 sor, 43/7/6, 26 magas, 42 csomópont), LXX-mondat (`egyeb` = függőben + számozás, 46/6/28/12), 3. szakasz (`vizsgalt_versek` `csoport_n`-nel; 47 / 1 742 / 236 / 1 506), 4.13 régi és új alakja, 4.14 kulcs-szűrése (15 / 2 / 1 / 2312), a melléklet tagonkénti összevetése (29 okcímsor), az 1.3 lenyitható okok alcím szerinti besorolása. Hamis egyezést nem talált; a nem mérhető érték nem egyezés.
- **Követelménylista-kapu:** a 109 K-sor kézi besorolása (55 gépi, 47 ember, 7 nem gyűjthető) egyezik a jelentéssel; az `ellenoriz.py` szabályfüggvényei mind meghívhatók; a gátló/figyelmeztető szint helyes.
- **Régi lapok (szúrópróba):** HODIT 17 ↔ 18 jelöltsor igazolva; a négy régi lap LXX-összesítője a jelentés lapon álló oldalával egyezik.
- **Nem ellenőrizhető az ellenőr körében:** a tesztfuttatás és a két kapu futtatása (a Bash-kör csak git/lekerdez/futtat); a `futtat.py` egy másik session zárára várt.

## Az ELTÉRÉS-ek súlyossági sorrendben

1. **CI E19/E34 mérés nélküli teljesülés** (`kovetelmeny_kapu.py:251`). Az E19 a lapfájlra üres listát ad (`E19_FAJLOK` csak `adat/…`), az E34 a találatát az adattáblára teszi (`E34_TABLA`), ezért a `fajl == lap_rel` szűrő mindig 0-t hagy; a K59 és a K44 mérés nélkül „teljesül”. Ennek „nem gyűjthető”-nek kellene lennie.
2. **Az LXX-összesítő új címkéi** (`allitas_adat.py:374`). Az új szerkezetű lapon az olvasói utófeldolgozás a címkéket átírja („a megfelelő nincs megállapítva=11, versszámozás miatt nem párosítva=1”); az `LXX_OSSZESITES` minta csak a régi alakot ismeri, a HAMART-001 5. táblájának összesítője mérés nélkül marad.
3. **Felismerési hiány a követelménylistán.** A K03 „olvasói kapu (Feed 9)” szabálya nincs felismerve; a vegyes cellák (K17 „grep a markerre”, K09/K29/K44 lektori része, K57 „a mért számra: nincs”) nem gépi része némán elmarad, ezért az „N/M teljesül (gépi)” többet állít, mint amit a kapu mér.
4. **`allitas_eredmeny`** (`kovetelmeny_kapu.py:270`): csupa nem mérhető állításnál is teljesül. Ma nem hat (egyik K-cella sem hivatkozik rá), az N-F196d után igen.

Mellékes megjegyzések: az N-F196d szövege szerint a kapu „utána felismerje” az `allitas_adat` hivatkozást, holott már felismeri; az 1.3 okainak `rfind`-je a teljes megelőző szövegben keres (ma helyes).

## A javítókör (F196.5) — a végrehajtó session

| # | Javítás |
|---|---|
| 1 | `CI_LAPRA_NEM_FUT` (E19, E34): a lapra nem futó CI-szabály „nem gyűjthető”, okkal; teszt. |
| 2 | Az `LXX_OSSZESITES` minta mindkét címkekészletet ismeri; a HAMART-001-en 5 új mért állítás (158 → 163, mind egyezik); teszt. |
| 3 | „olvasói kapu” a cellában → `olvasoi_egesz` szabály (0 BUKÁS a lapon); a vegyes cella „részben gépi” jelölést kap, a jelentés megszámolja; teszt. |
| 4 | Csupa nem mérhető állításnál az állítás–adat szabály nem gyűjthető; teszt. |
| + | Az E32 JELENTÉS-e (a `DT771` helyőrző string-literálban): a négy literál számfüggetlen lett. Az N-F196c/d szövege pontosítva. |
