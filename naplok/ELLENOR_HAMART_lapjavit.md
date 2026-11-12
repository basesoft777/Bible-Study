ELTÉRÉS: 17 tétel

# Független ellenőrzés: /lap-javit HAMART-001

*Tartomány: `9926ae54..aa775d31` (F125.LJ1–LJ3). Ellenőr: `fuggetlen-ellenor`, claude-opus-5-5 (a kért modell: opus). A jelentést a fő szál írta ki az ellenőr válaszából, mert az ellenőrnek nincs fájlíró eszköze. Az ellenőrzés közben az ágra került az LJ4 (a döntésfájl áthelyezése) és az LJ5 (az értelmező rések egybeírása); ezeket az ellenőr nem vizsgálta, csak jelezte, ha egy tételt érintenek.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A modell `claude-opus-5-5`, a kért `opus`; a `javasolta` mező és a Co-Authored-By sor egyezik vele. |
| 0 Modell (nyílt angol) | ELTÉRÉS | `adat/nyilt_angol.tsv` | A `modell` mező `claude-sonnet-5-5`, holott a végrehajtó belejavított. A minta ilyenkor: `…; javítás: claude-opus-5-5`. |
| 3. Határ: előfordulások, jelöltek, kapcsolatok, motívumtábla | OK | `adat/*.tsv` | `git diff` mezőnként: csak a kapcsolódás-szöveg, a funkció, az indoklás, a `dontes_ref` és a negatív kritérium változott. A döntések és az igehely-halmaz változatlan. |
| 3. A hallás + erőszak kiterjesztése | OK | — | `lekerdez.py kollokacio H2555 H8085`: 4 vers, mind a listán. A Hab 2:8 és a 2:17 H8085 nélkül áll. |
| E17/DT3 sorszám-változás | OK | — | Az adattáblák sorszáma nem változott; a `lap_javitasok` +48 sor (23/9/16). |
| 1. A 46 tétel lefedése | OK | `adat/lap_javitasok.tsv` | Mind a 46 tételnek van sora. |
| 2/41. 2Kir 17:23 „a »szín« szava nélkül” | ELTÉRÉS | `motivumok/HAMART-001.md` (Nyitott kérdések 1.) | `scan H6440 --szakasz "2Kir 17:23"` → 1; Károli: „az ő színe elől”. |
| 2/5, 6, 21, 22, 25, 31, 32, 41, 42 | OK | — | TAHOT- és Károli-lekérdezésekkel igazolva. |
| 2/13. Ez 28:16 megszólítottja | ELTÉRÉS | `adat/jeloltek.tsv` (Ez 28:16, 28:17), nyílt mag | A 2.1 blokk javult, a jelöltsor, a kizárt Ez 28:17 és a nyílt mag nem: „Tírusz fejedelme”. |
| 2/15. KH-blokk számai | OK | — | A Sof 1:9 listája a Mt 12:22 listájának része; 26 hely, 112 utalás, 55%. |
| 2/39. Az 577 vers | NEM ELLENŐRIZHETŐ | — | A csoportos kizárás lexémái megengedett paranccsal nem bonthatók szét. |
| 2/19. „nem köti össze” | OK | — | `lekerdez.py tsk` egyezik. |
| 4. `nevelo_le` | ELTÉRÉS | `eszkozok/lexikon_general.py` | A kódblokk belseje nem védett; a „`” előtag miatt az inline kód is változhat; a teljes mondatos cellák nyelvtanilag hibásak lettek („Szótár a héber … idézi”, „Lánc szava áll …”). |
| 4. LISTA_NEVELO, KH_MASOLT | NEM ELLENŐRIZHETŐ | — | A KH_MASOLT kapura nincs rontott bemenetes teszt. |
| 4. Hatás a régi lapokra | ELTÉRÉS | `eszkozok/olvasoi_kovetkeztetes.py` | A „többsége közepes” feltétel hibás (`kozepes >= (n-magas)/2`). A `kozepes` átadását az LJ5 lezárta. |
| 5. Nyitott tételek | OK | — | A végrehajtó döntései megfelelnek a lektor feltételeinek. |
| 5/11. Hab 1:2 | ELTÉRÉS | 2.1, Hab 1:2 | „A Jeremiás-helyek … fordulata itt … tér vissza”: függést sugall. |
| 6/24, 26. Maradék | ELTÉRÉS | 9. szakasz | A cellában „az alapvonal nem mérhető”, „előképversében”. |
| 6. Ismétlés | ELTÉRÉS | lap eleje / Kivonat | Az „A motívum.” és a Kivonat szinte szó szerint egyezik. A chámász-kizárás a lap elején hiányzik. |
| 6. Kiejtés | OK | — | TBESH szerint. |
| 7. Proveniencia | ELTÉRÉS | Nyitott kérdések 1–3., Kivonat, Jer 51:46 | Az új TAHOT-állítások mellől hiányzik a proveniencia-sor. |
| 7. SEMA 2.49 | ELTÉRÉS | `adat/lap_javitasok.tsv` | A `generátor` sorok `uj` mezője nem `N-F…`. Az „Emberi lektorálás” címke modell-lektort is takar. „14.. tétele” elírás. Az Ézs 60:18 jelöltsora „visszavonás”. |
| ⛔ Döntéshely | ELTÉRÉS | `dontes/uj/` | A helyes hely `dontesek/uj/` (az LJ4 javította). |
| Sablon | ELTÉRÉS | `sablonok/6_…:406, 558` | A kapu neve „NEVELO” a LISTA_NEVELO helyett; „(a teljes cím)” ellentmond. |
| 8. Nyílt mag kapu | NEM ELLENŐRIZHETŐ | — | A parancs nem engedett. |
| 8. Angol hűség | OK | — | A 6 sor hű. |
| CI | ELTÉRÉS | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1390` | E28 HIBA 2 a tartományban (a régi lap Kapcsolatok-mondata); az LJ5 kapuzta. E30: „indoklas” ékezet nélkül egy commitüzenetben. |

## Javítókör (F125.LJ6)

Az egyetlen javítókör, tételenként:

| ELTÉRÉS | Javítás |
|---|---|
| 2Kir 17:23 „szín” | „a föld színe fordulat nélkül (a 2Kir 17:23 »színe« Istené: »az ő színe elől«)”; proveniencia-sor a Nyitott kérdések után |
| Ez 28:16/17 | jelöltek: „Tírus királyáról (Ez 28:12)”, „Tírus királyának”; nyílt mag újragenerálva, angol újrafordítva |
| `nevelo_le` | a kódblokk belseje védett, az inline kód nem előtag; a legalább 6 szavas (mondat értékű) elem a névelőt megtartja, nagybetűvel; teszt rontott bemenettel |
| KH_MASOLT teszt | `test_kh_masolt_kapu_rontott`: az új szerkezetű lapon BUKÁS |
| „többsége közepes” | csak ha `2·közepes > n`; különben „kevesebb mint fele magas bizonyosságú” |
| Hab 1:2 | „A hallás igéje itt nem az erőszakra, hanem a kiáltásra vonatkozik; …” |
| 24., 26. maradék | „így nem mérhető, szokásos fordítás-e”; „versében / verseiben” (új szerkezet) |
| Ismétlés | a Kivonat: „Mivel a motívumot a szavak láncolata tartja össze …”; a lap elején a chámász-kizárás is áll |
| Proveniencia | Nyitott kérdések: proveniencia-sor; Kivonat: a forrás végi proveniencia-blokkban; Jer 51:46: a jelöltsor `dontes_ref`-jében |
| SEMA 2.49 | „14.. tétele” → „14. tétele”; az Ézs 60:18 jelöltsora: „eszkatológiai megfordítás”. A `generátor` sorok `uj` mezője leírja a generátorban végzett javítást (nem `N-F…`, mert a javítás az ágon megtörtént). Az „Emberi lektorálás” sor: a helyekre a modell-lektor mutatott, a jóváhagyás a felhasználóé, az orkesztrátoron át; a jelentés ezt kimondja. |
| Sablon | LISTA_NEVELO; „a motívum (az azonosság hordozója)” |
| Nyílt angol `modell` | `claude-sonnet-5-5; javítás: claude-opus-5-5` (a Mik 6:12 indoklása) |
| E30 | a korábbi commitüzenet nem írható át (nincs force push); a további üzenetekben ékezetes „indoklás” |
