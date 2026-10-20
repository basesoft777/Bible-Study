# F130 — M4 forrás-ellenőrzés és összevetés (ISTENTISZT-001, nevesített tanítói keresés)

*FELADATOK #130 · `F130_TANITOI_KERESES_ISTENTISZT_BRIEF.md` M4 · 2026.10.20 · ítélet: `claude-opus-5-5`*

## Módszer

- **Munkamegosztás:** a forrásokat friss Sonnet subagent nyitotta meg és kivonatolta (nem a `tanito-kereso` példány); az ítéletet a session hozta, a `sablonok/4_PaRDeS_tematikus_sablon.md` 5. pontjának 4. lépése szerint: a forrás ténylegesen az adott igehelyre vagy a „segítségül hívni az Úr nevét” témára hivatkozik-e, vagy csak asszociatív/tematikus rokonság. A megosztás alapja az orkesztrátor 2026-10-20-i feladatkiadása, amely a DT273 1. opcióját a felhasználó döntéseként közölte. **A `DONTESEK.md`-ben a DT273 rögzítése (🟡 → 🟢) megtörtént az F130.2a-ban (02f4d302);** a döntés ott a Javaslat-oszlopba került, a Döntés-oszlopba az F130.7 tette át (ELLENOR_F130 4. tétel).
- **A kivonat:** a session scratchpadjában (`F130_M4_kivonat.md`, a repón kívül), 7 URL, mind olvasható, lekérés 2026-10-20. Fenntartás: a kivonat a WebFetch mellékmodelljének kimenetén alapul, nem a teljes átirat közvetlen olvasásán; a sermons/426 átirata a végén csonkának tűnik.
- **Saját megnyitás:** ahol az ítélet a forrás pontos szövegén múlt (sermons/138, sermons/347, awmi.net Receive Jesus), a session is megnyitotta a forrást (WebFetch, 2026-10-20); ez is mellékmodell-kimenet, nem teljes szövegolvasás.

## Ítéletek találatonként

| # | Forrás | URL | Lekérés | Megnyitás | Mit mond (saját szavakkal) | Ítélet | Erősség |
|---|---|---|---|---|---|---|---|
| 1 | Derek Prince: *War on Earth* | https://www.derekprince.com/sermons/426 | 2026-10-20 | Sonnet-kivonat | A Jóel 2:32-t névvel és idézve hozza; saját szabadulása a levertség lelkétől, amikor segítségül hívta az Urat. ApCsel 2:21 és Róm 10 nincs. Az átirat vége csonkának tűnik. | igehelyre hivatkozik (Jóel 2:32), a szabadulás-tanítás része | ⚠️ marad |
| 2 | Derek Prince: *How I Came To Grips With Demons* | https://www.derekprince.com/sermons/82 | 2026-10-20 | Sonnet-kivonat | A Jóel 2:32-t névvel és idézve a Lélek-kitöltés csúcspontjaként: aki segítségül hívja az Úr nevét, szabadulást kap; a zárásban újra, versszám nélkül. | igehelyre hivatkozik (Jóel 2:32), a démonológiai sorozat része | ⚠️ marad |
| 3 | Derek Prince: *Deliverance From The Fleshly Nature* | https://www.derekprince.com/sermons/138 | 2026-10-20 | Sonnet-kivonat + session | Az átirat igehely nélkül, „egy másik Írás”-ként idézi: „whosoever shall call on the name of the Lord shall be delivered”, és azt mondja, ezt cselekedte. A „delivered” a KJV Jóel 2:32 szövege (a Róm 10:13 és az ApCsel 2:21 KJV-szövege „saved”); a Jóel-azonosítás a szövegegyezésből tett következtetés (`manual`), nem a forrás állítása. | a témára hivatkozik (maga a formula, szó szerint idézve); ugyanaz a személyes beszámoló, mint az 1. és az 5. sorban | ⚠️ marad, „a hely azonosítása `manual`” megjegyzéssel |
| 4 | Derek Prince: *The Prayer of Release* (Legacy Radio) | https://www.derekprince.com/radio/210 | 2026-10-20 | Sonnet-kivonat | A Jóel 2:32-t névvel és idézve (NKJ) átfogó ígéretként, az átok alóli szabadulás hetedik feltételeként. | igehelyre hivatkozik (Jóel 2:32), az átok-tanítás része | ⚠️ marad |
| 5 | Derek Prince: *You've Got to Have Hope* (Teaching Letter) | https://www.derekprince.com/teaching/05-2 | 2026-10-20 | Sonnet-kivonat | A Jóel 2:32-t (KJV) névvel és idézve, az Ézs 61:3-mal párosítva; az 1. sor beszámolója írásban. | igehelyre hivatkozik (Jóel 2:32), a remény-tanítás része | ⚠️ marad |
| 6 | Derek Prince: *The Roman Pilgrimage (Part 15)* | https://www.derekprince.com/sermons/347 | 2026-10-20 | Sonnet-kivonat + session | A Róm 10:13-at névvel felolvassa, a 10:12-t versszám nélkül idézi; a segítségül hívást a szívbeli hit és a szájjal való megvallás mellé harmadik lépésként állítja, és azt mondja, „mindenkinek” működik; a segítségül hívás tartalmát nem fejti ki. Róm 10:14 és Jóel 2:32 nincs. | igehelyre hivatkozik (Róm 10:12–13), a Róma-levél-sorozat része | ⚠️ marad |
| 7 | Andrew Wommack Ministries: *Receive Jesus* | https://www.awmi.net/resources/receive-jesus/ | 2026-10-20 | Sonnet-kivonat + session | A Róm 10:13-at mottóként, „Romans 10:9-10,13” jelöléssel idézi, utána megvallási ima; a segítségül hívásról magyarázat nincs; szerző nincs megnevezve (a szolgálat oldala). | nem nevesíthető tanítói forrás (szerző nincs), és nem tanítás, csak igeidézet | gap marad |

**Összesen:** 0 ✅, 6 ⚠️ (mind Derek Prince), 0 törlés; az erősségek nem változtak. Megjegyzés: az 1., a 3. és az 5. sor ugyanazt a személyes beszámolót hordozza (három előadás/írás); a ⚠️ számot ez nem növeli tartalmilag.

## Összevetés a régi, manual változattal

*(`archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md`)*

| Tanító | Régi (manual) | Új (F130) | Változás |
|---|---|---|---|
| Kenneth Hagin | ✅ (*Understanding Confession*; *Confession: Key to Unlocking Faith*; Róm 10:9–10 vonal) | gap | **eltűnt.** Nincs URL-lel igazolt, megnyitott forrás (rhema.org: 403; e-book PDF olvashatatlan). Ráadásul a régi indoklás maga a Róm 10:9–10-re épült, amely nem a motívum előfordulása (1. pont, 2. csomópont); a 4. lépés szerint ez önmagában tematikus rokonság. A gap részben hozzáférési korlát, nem bizonyított hiány. |
| Derek Prince | ⚠️ (*Deliverance and Demonology* vázlat; *The Helmet of Hope*; Jóel 2:32, szabadulás) | ⚠️ (6 forrás URL-lel) | **maradt.** A régi két hivatkozás tartalmilag megerősödött: a *How I Came To Grips With Demons* a Deliverance and Demonology sorozat része, a *You've Got to Have Hope* a The Helmet of Hope tanításból adaptált. Új: Róm 10:12–13 (*The Roman Pilgrimage*). |
| Charles Capps | gap | gap (csoportos keresés) | maradt |
| Copeland, Roberts, Osborn, Wigglesworth, a lista többi tagja | gap | gap; Osborn, Kuhlman, Lindsay, Savelle, Price nem keresett (indokolva) | maradt; új, önállóan keresett gap: Wommack, Bosworth, Lake |

## Szövegjavaslat — `motivumok/ISTENTISZT-001.md` 5. pont (376–380. sor)

*Csak javaslat; a forrás a ⛔ M4 jóváhagyásáig nem változik (F130.3).* A mai szöveg Hagin ✅ forrására és két igazolatlan tanítói állításra épül: Hagin „szóbeli hitbeli cselekvése”, illetve Prince „szégyen/kudarc” ellenállás-tanítása. Ezek közül az M4 egyiket sem igazolta.

- **376. sor**, a zárójeles rész: „kiegészítve a saját fájlban nevesített tanítói forrásokkal: Hagin ✅ erős/közvetlen, Derek Prince ⚠️ részleges/beágyazott” →
  „kiegészítve a saját fájlban nevesített tanítói forrással: Derek Prince ⚠️ részleges/beágyazott; a többi jóváhagyott tanítónál, Kenneth Hagint is beleértve, nincs igazolt forrás (gap)”
- **378. sor (1. kérdés)**: „A segítségül hívás — Hagin tanítása szerint — nem passzív érzés, hanem tudatos, szóbeli hitbeli cselekvés;” →
  „A segítségül hívás nem passzív érzés, hanem hitbeli cselekvés: az Úr nevét az hívja segítségül, aki hisz benne (Róm 10:14, l. 3. pont);”
- **380. sor (3. kérdés)**: „Derek Prince szabadulás-tanítása szerint pedig gyakori ellenállás a szégyen/kudarc érzése, amely visszatartja az embert a segítségül hívástól —” →
  „Derek Prince a levertségből való saját szabadulásáról szóló beszámolóiban a Jóel 2:32 ígéretére támaszkodva hívta segítségül az Úr nevét (a tanítói fájl 3.1) —”
  és a mondat vége: „a szöveg ezzel szemben azt mutatja” → „a szöveg is azt mutatja”; a többi része változatlan („…, hogy pontosan ez (a függőség beismerése) a helyes válasz.”)

## Javítókör 1 (`/elteres 130`, ELLENOR_F130)

- **Szándékos címsor-törlés (ELLENOR_F130 1. tétel, E5).** A `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md` felülírása a régi, manual törzset és három címsorát (`## Eredet`; `## Az átvett eredmény (bájtra, a motivumok/ISTENTISZT-001.md 5. pontjából)`; `### A nevesített tanítói egyezés-keresés eredménye (öt lépéses módszertan szerint)`) szándékosan törölte: a régi változat bájtra archiválva van (`archivum/ISTENTISZT-001/ISTENTISZT-001_tanitoi_kereses_manual.md`, F130.1, DT-F130b), az új szerkezet a `sablonok/7_PaRDeS_tanitoi_kereses_sablon.md` négy pontját követi. A jelölés a F130.5 commit-üzenetében áll (`TÖRLÉS-SZÁNDÉKOS:`).
- **Modell-dokumentáció (ELLENOR_F130 5. tétel, DT275 (a)).** Az F130.2a (02f4d302) commit `Co-Authored-By` sora `Claude Sonnet 5.5`, az `opus`-briefen; ezt a felhasználó a DT-F130e-vel (2026-10-20, chat, (a)) elfogadta, a history nem íródik át. Az M4-ben a forrásokat megnyitó friss Sonnet subagent **tényleges modellneve nincs rögzítve, és utólag nem állapítható meg: explicit hiány** (nem „ellenőrizve”, és nem kitöltött érték; a „Sonnet” csak a kiadott szerep, nem a futás saját környezetéből vett név). A tanítói fájl `Modell` mezője (`claude-sonnet-5-5`, 2–4. pont) a `tanito-kereso` M3-keresésére vonatkozik, nem az M4-subagentre, ezért ennek nem mond ellent, és nem változott.
